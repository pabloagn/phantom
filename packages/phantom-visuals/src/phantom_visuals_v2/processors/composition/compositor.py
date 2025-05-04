# apts/composition/compositor.py

"""Compositor module for blending multiple effect layers into a coherent result."""

import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import torch


class Compositor:
    """Intelligent composition system for blending multiple effect layers
    and creating coherent artistic transformations.
    """

    def __init__(self, config, device=None):
        """
        Initialize the compositor.

        Args:
            config: Configuration dictionary
            device: Computation device (CPU or CUDA)
        """
        self.config = config
        self.device = (
            device
            if device is not None
            else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )

        # Initialize blend modes
        self.blend_mode = config.get("blend_mode", "normal")
        self.blend_strength = config.get("blend_strength", 1.0)

        # Initialize masking options
        self.use_face_mask = config.get("use_face_mask", True)
        self.mask_feather = config.get(
            "mask_feather", 0.1
        )  # As proportion of image width

        # Initialize region-aware composition
        self.region_aware = config.get("region_aware", True)

    def compose(self, image: np.ndarray, state: Dict) -> Dict[str, Any]:
        """Compose multiple effect layers into a coherent result.

        Args:
            image: Original input image
            state: Current transformation state

        Returns:
            Dictionary with composition results
        """
        result = {}
        h, w = image.shape[:2]

        # Initialize composition
        composed_image = image.astype(np.float32) / 255.0

        # Get face mask if needed and available
        face_mask = None
        if self.use_face_mask and "landmarks" in state:
            face_mask = self._create_face_mask(image, state)
            result["face_mask"] = face_mask

        # Check if we have material results
        if "material_diffuse" in state:
            material_diffuse = state["material_diffuse"]

            # Apply material effect
            composed_image = self._blend_layers(
                composed_image,
                material_diffuse,
                self.blend_mode,
                self.blend_strength,
                mask=face_mask,
            )

        # Apply additional effects based on flow field
        if "flow_field" in state:
            flow_effect = self._generate_flow_effect(image, state)

            if flow_effect is not None:
                # Blend flow effect
                flow_mode = self.config.get("flow_blend_mode", "screen")
                flow_strength = self.config.get("flow_blend_strength", 0.5)

                composed_image = self._blend_layers(
                    composed_image,
                    flow_effect,
                    flow_mode,
                    flow_strength,
                    mask=face_mask,
                )

        # Apply region-aware composition if enabled
        if self.region_aware and "landmarks" in state:
            region_effects = self._generate_region_effects(image, state)

            for region, effect in region_effects.items():
                if effect is None:
                    continue

                # Get region mask
                region_mask = effect.get("mask")

                if region_mask is not None and "image" in effect:
                    # Blend region effect
                    region_mode = effect.get("blend_mode", "normal")
                    region_strength = effect.get("blend_strength", 1.0)

                    composed_image = self._blend_layers(
                        composed_image,
                        effect["image"],
                        region_mode,
                        region_strength,
                        mask=region_mask,
                    )

        # Ensure composition is in valid range
        composed_image = np.clip(composed_image, 0, 1)

        # Save result
        result["composed_image"] = composed_image

        return result

    def _create_face_mask(self, image: np.ndarray, state: Dict) -> np.ndarray:
        """Create a mask for the face region."""
        h, w = image.shape[:2]
        mask = np.zeros((h, w), dtype=np.float32)

        # Use face bounding box or landmarks
        if "face_bbox" in state:
            x1, y1, x2, y2 = state["face_bbox"]

            # Create elliptical mask centered on face
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            radius_x = (x2 - x1) // 2
            radius_y = (y2 - y1) // 2

            # Add padding
            radius_x = int(radius_x * 1.2)
            radius_y = int(radius_y * 1.2)

            # Create mask
            y_indices, x_indices = np.ogrid[:h, :w]
            dist = ((x_indices - center_x) / radius_x) ** 2 + (
                (y_indices - center_y) / radius_y
            ) ** 2
            mask = (dist <= 1).astype(np.float32)
        elif "landmarks" in state:
            # Create mask from landmarks
            landmarks = state["landmarks"]

            # Use convex hull of landmarks
            points = np.array(landmarks[:, :2], dtype=np.int32)
            hull = cv2.convexHull(points)

            # Fill the hull
            cv2.fillConvexPoly(mask, hull, 1.0)

        # Feather mask edges
        feather_radius = int(w * self.mask_feather)
        if feather_radius > 0:
            mask = cv2.GaussianBlur(mask, (0, 0), feather_radius)

        return mask

    def _blend_layers(
        self,
        base: np.ndarray,
        blend: np.ndarray,
        mode: str = "normal",
        strength: float = 1.0,
        mask: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Blend two layers using specified blend mode and mask.

        Args:
            base: Base image as float32 [0,1]
            blend: Blend layer as float32 [0,1]
            mode: Blend mode ('normal', 'multiply', 'screen', etc.)
            strength: Blend strength factor [0,1]
            mask: Optional mask for blend (float32 [0,1])

        Returns:
            Blended image
        """
        # Ensure inputs are in the right shape
        if base.shape != blend.shape:
            # Resize blend layer to match base
            blend = cv2.resize(blend, (base.shape[1], base.shape[0]))

        # Apply blend mode with proper numerical stability
        if mode == "normal":
            result = blend
        elif mode == "multiply":
            result = base * blend
        elif mode == "screen":
            result = 1.0 - (1.0 - base) * (1.0 - blend)
        elif mode == "overlay":
            mask_dark = base <= 0.5
            result = np.zeros_like(base)
            result[mask_dark] = np.clip(2 * base[mask_dark] * blend[mask_dark], 0, 1)
            result[~mask_dark] = np.clip(
                1.0 - 2 * (1.0 - base[~mask_dark]) * (1.0 - blend[~mask_dark]), 0, 1
            )
        elif mode == "soft_light":
            mask_dark = blend <= 0.5
            result = np.zeros_like(base)
            result[mask_dark] = base[mask_dark] - (1.0 - 2 * blend[mask_dark]) * base[
                mask_dark
            ] * (1.0 - base[mask_dark])
            # Calculate sqrt safely
            safe_base = np.maximum(0, base[~mask_dark])
            sqrt_base = np.sqrt(safe_base)
            result[~mask_dark] = base[~mask_dark] + (2 * blend[~mask_dark] - 1.0) * (
                sqrt_base - base[~mask_dark]
            )
        elif mode == "hard_light":
            mask_dark = blend <= 0.5
            result = np.zeros_like(base)
            result[mask_dark] = np.clip(2 * base[mask_dark] * blend[mask_dark], 0, 1)
            result[~mask_dark] = np.clip(
                1.0 - 2 * (1.0 - base[~mask_dark]) * (1.0 - blend[~mask_dark]), 0, 1
            )
        elif mode == "difference":
            result = np.abs(base - blend)
        elif mode == "exclusion":
            result = base + blend - 2 * base * blend
        elif mode == "color_dodge":
            result = np.zeros_like(base)
            # Avoid division by zero
            mask_div = blend < 1.0 - 1e-6
            result[mask_div] = np.minimum(1.0, base[mask_div] / (1.0 - blend[mask_div]))
            result[~mask_div] = 1.0
        elif mode == "color_burn":
            result = np.ones_like(base)
            # Avoid division by zero
            mask_div = blend > 1e-6
            result[mask_div] = 1.0 - np.minimum(
                1.0, (1.0 - base[mask_div]) / blend[mask_div]
            )
            result[~mask_div] = 0.0
        elif mode == "linear_dodge":
            result = np.clip(base + blend, 0, 1)
        elif mode == "linear_burn":
            result = np.clip(base + blend - 1.0, 0, 1)
        elif mode == "vivid_light":
            mask_dark = blend <= 0.5
            result = np.zeros_like(base)
            # Protect against division by zero with safe denominators
            safe_blend_dark = 2 * blend[mask_dark] + 1e-6
            safe_blend_light = 2 * (1.0 - blend[~mask_dark]) + 1e-6
            result[mask_dark] = np.clip(
                1.0 - (1.0 - base[mask_dark]) / safe_blend_dark, 0, 1
            )
            result[~mask_dark] = np.clip(base[~mask_dark] / safe_blend_light, 0, 1)
        else:
            # Default to normal blend
            result = blend

        # Apply strength
        result = base * (1.0 - strength) + result * strength

        # Apply mask if provided
        if mask is not None:
            # Ensure mask has right shape for broadcasting
            if len(mask.shape) == 2 and len(base.shape) == 3:
                mask = mask[:, :, np.newaxis]

            # Apply mask
            result = base * (1.0 - mask) + result * mask

        # Final validation to ensure no NaN or Inf values
        if np.any(np.isnan(result)) or np.any(np.isinf(result)):
            print("Warning: NaN or Inf values detected in blend result, fixing...")
            result = np.nan_to_num(result, nan=0.0, posinf=1.0, neginf=0.0)

        return np.clip(result, 0, 1)

    def _generate_flow_effect(
        self, image: np.ndarray, state: Dict
    ) -> Optional[np.ndarray]:
        """Generate visual effect based on flow field."""
        if "flow_field" not in state:
            return None

        h, w = image.shape[:2]
        flow = state["flow_field"]

        # Get flow effect type
        effect_type = self.config.get("flow_effect_type", "streak")

        if effect_type == "streak":
            # Create streak effect
            return self._generate_streak_effect(image, flow, state)
        elif effect_type == "particle":
            # Create particle effect
            return self._generate_particle_effect(image, flow, state)
        elif effect_type == "distort":
            # Create distortion effect
            return self._generate_distort_effect(image, flow, state)
        else:
            # No effect
            return None

    def _generate_streak_effect(
        self, image: np.ndarray, flow: np.ndarray, state: Dict
    ) -> np.ndarray:
        """Generate streak effect based on flow field."""
        h, w = image.shape[:2]

        # Create empty streak image
        streak_img = np.zeros((h, w, 3), dtype=np.float32)

        # Number of streak lines
        num_streaks = self.config.get("streak_count", 1000)

        # Streak parameters
        streak_length = self.config.get("streak_length", 30)
        streak_width = self.config.get("streak_width", 1.0)
        streak_opacity = self.config.get("streak_opacity", 0.5)
        bright_streaks = self.config.get("bright_streaks", True)

        # Sample streak starting points
        # Focus on areas with interesting flow
        flow_mag = np.sqrt(flow[:, :, 0] ** 2 + flow[:, :, 1] ** 2)
        flow_mag_norm = flow_mag / (np.max(flow_mag) + 1e-6)

        # Create sampling probability map
        prob_map = flow_mag_norm.flatten()
        prob_map = prob_map / (np.sum(prob_map) + 1e-6)

        # Sample indices
        indices = np.random.choice(h * w, size=num_streaks, p=prob_map)
        y_indices = indices // w
        x_indices = indices % w

        # Generate streaks
        for i in range(num_streaks):
            x, y = x_indices[i], y_indices[i]

            # Get color from image (with optional brightening)
            color = image[y, x] / 255.0
            if bright_streaks:
                color = np.minimum(1.0, color * 1.5)

            # Create points along streak
            points = []
            curr_x, curr_y = x, y

            for _ in range(streak_length):
                points.append((curr_x, curr_y))

                # Get flow direction
                if 0 <= curr_y < h and 0 <= curr_x < w:
                    fx, fy = flow[int(curr_y), int(curr_x)]
                else:
                    break

                # Move in flow direction
                curr_x += fx * 2.0  # Scaled step size
                curr_y += fy * 2.0

                # Check bounds
                if curr_x < 0 or curr_x >= w or curr_y < 0 or curr_y >= h:
                    break

            # Convert points to array
            if len(points) < 2:
                continue

            points = np.array(points, dtype=np.int32)

            # Draw streak with varying opacity
            for j in range(len(points) - 1):
                p1 = points[j]
                p2 = points[j + 1]

                # Opacity decreases along streak
                local_opacity = streak_opacity * (1.0 - j / len(points))

                # Draw anti-aliased line
                cv2.line(
                    streak_img,
                    tuple(p1),
                    tuple(p2),
                    color * local_opacity,
                    int(streak_width),
                )

        return streak_img

    def _generate_particle_effect(
        self, image: np.ndarray, flow: np.ndarray, state: Dict
    ) -> np.ndarray:
        """Generate particle effect based on flow field."""
        h, w = image.shape[:2]

        # Create empty particle image
        particle_img = np.zeros((h, w, 3), dtype=np.float32)

        # Particle parameters
        num_particles = self.config.get("particle_count", 5000)
        particle_size_range = self.config.get("particle_size_range", (0.5, 2.0))
        particle_opacity = self.config.get("particle_opacity", 0.7)
        particle_brightness = self.config.get("particle_brightness", 1.2)

        # Generate particles
        particle_pos_x = np.random.uniform(0, w, num_particles)
        particle_pos_y = np.random.uniform(0, h, num_particles)
        particle_sizes = np.random.uniform(
            particle_size_range[0], particle_size_range[1], num_particles
        )

        # Get colors from image
        particle_colors = np.zeros((num_particles, 3), dtype=np.float32)
        for i in range(num_particles):
            x, y = (
                int(min(w - 1, max(0, particle_pos_x[i]))),
                int(min(h - 1, max(0, particle_pos_y[i]))),
            )
            particle_colors[i] = image[y, x] / 255.0 * particle_brightness

        # Sort particles by size for better rendering
        sort_indices = np.argsort(particle_sizes)
        particle_pos_x = particle_pos_x[sort_indices]
        particle_pos_y = particle_pos_y[sort_indices]
        particle_sizes = particle_sizes[sort_indices]
        particle_colors = particle_colors[sort_indices]

        # Move particles along flow
        motion_strength = self.config.get("particle_motion_strength", 10.0)

        for i in range(num_particles):
            x, y = particle_pos_x[i], particle_pos_y[i]

            # Skip particles outside image
            if x < 0 or x >= w or y < 0 or y >= h:
                continue

            # Get flow at particle position
            fx, fy = flow[int(y), int(x)]

            # Move particle
            new_x = x + fx * motion_strength
            new_y = y + fy * motion_strength

            # Draw particle trail
            color = particle_colors[i] * particle_opacity
            size = particle_sizes[i]

            # Draw line for trail
            cv2.line(
                particle_img,
                (int(x), int(y)),
                (int(new_x), int(new_y)),
                color,
                int(size),
            )

            # Draw circle for particle
            cv2.circle(particle_img, (int(new_x), int(new_y)), int(size), color, -1)

        return particle_img

    def _generate_distort_effect(
        self, image: np.ndarray, flow: np.ndarray, state: Dict
    ) -> np.ndarray:
        """Generate distortion effect based on flow field."""
        h, w = image.shape[:2]

        # Create displacement map
        displacement_scale = self.config.get("displacement_scale", 10.0)
        displacement_map = flow * displacement_scale

        # Create distorted image
        distorted = np.zeros_like(image, dtype=np.float32)

        # Apply displacement
        for y in range(h):
            for x in range(w):
                # Get displacement
                dx, dy = displacement_map[y, x]

                # Sample position
                sample_x = int(max(0, min(w - 1, x + dx)))
                sample_y = int(max(0, min(h - 1, y + dy)))

                # Sample color
                distorted[y, x] = image[sample_y, sample_x] / 255.0

        return distorted

    def _generate_region_effects(
        self, image: np.ndarray, state: Dict
    ) -> Dict[str, Dict]:
        """Generate effects for specific facial regions."""
        region_effects = {}

        # Check if we have facial landmarks
        if "landmarks" not in state or len(state["landmarks"]) < 468:
            return region_effects

        h, w = image.shape[:2]
        landmarks = state["landmarks"]

        # Define facial regions
        regions = {
            "eyes": [33, 133, 160, 158, 153, 145, 263, 362, 385, 380, 373, 374],
            "nose": [4, 5, 6, 7, 8, 9, 10],
            "mouth": [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291],
            "forehead": [
                10,
                338,
                337,
                336,
                296,
                297,
                332,
                333,
                334,
                293,
                296,
                67,
                109,
                10,
            ],
        }

        # Create masks for each region
        for region_name, indices in regions.items():
            # Get landmarks for this region
            region_points = np.array(
                [landmarks[i, :2] for i in indices], dtype=np.int32
            )

            # Create mask
            mask = np.zeros((h, w), dtype=np.float32)
            cv2.fillConvexPoly(mask, region_points, 1.0)

            # Feather mask
            mask_feather = int(w * 0.02)  # 2% of image width
            mask = cv2.GaussianBlur(mask, (0, 0), mask_feather)

            # Different effects for different regions
            if region_name == "eyes":
                effect = self._generate_eye_effect(image, mask, state)
            elif region_name == "nose":
                effect = self._generate_nose_effect(image, mask, state)
            elif region_name == "mouth":
                effect = self._generate_mouth_effect(image, mask, state)
            elif region_name == "forehead":
                effect = self._generate_forehead_effect(image, mask, state)
            else:
                effect = None

            if effect is not None:
                effect["mask"] = mask
                region_effects[region_name] = effect

        return region_effects

    def _generate_eye_effect(
        self, image: np.ndarray, mask: np.ndarray, state: Dict
    ) -> Optional[Dict]:
        """Generate special effect for eye region."""
        # Check if eye effect is enabled
        if not self.config.get("eye_effect_enabled", True):
            return None

        h, w = image.shape[:2]
        effect_type = self.config.get("eye_effect_type", "glow")

        if effect_type == "glow":
            # Create glowing eyes effect
            eye_img = np.zeros((h, w, 3), dtype=np.float32)

            # Extract eye region
            eye_region = (image * mask[:, :, np.newaxis]) / 255.0

            # Blur for glow
            glow_intensity = self.config.get("eye_glow_intensity", 1.5)
            glow_radius = self.config.get("eye_glow_radius", w * 0.01)

            # Create glow
            blurred = cv2.GaussianBlur(eye_region, (0, 0), glow_radius)
            eye_img = blurred * glow_intensity

            return {"image": eye_img, "blend_mode": "screen", "blend_strength": 0.8}
        else:
            return None

    def _generate_nose_effect(
        self, image: np.ndarray, mask: np.ndarray, state: Dict
    ) -> Optional[Dict]:
        """Generate special effect for nose region."""
        # Simple implementation - can be expanded
        return None

    def _generate_mouth_effect(
        self, image: np.ndarray, mask: np.ndarray, state: Dict
    ) -> Optional[Dict]:
        """Generate special effect for mouth region."""
        # Check if mouth effect is enabled
        if not self.config.get("mouth_effect_enabled", True):
            return None

        h, w = image.shape[:2]
        effect_type = self.config.get("mouth_effect_type", "blur")

        if effect_type == "blur":
            # Create motion blur effect for mouth
            mouth_img = image.astype(np.float32) / 255.0

            # Extract mouth region
            mouth_region = mouth_img * mask[:, :, np.newaxis]

            # Apply motion blur
            blur_radius = self.config.get("mouth_blur_radius", w * 0.02)
            blur_angle = self.config.get("mouth_blur_angle", 0)  # horizontal

            # Create motion blur kernel
            kernel_size = int(blur_radius * 2 + 1)
            kernel = np.zeros((kernel_size, kernel_size))

            # Draw line in kernel
            center = kernel_size // 2
            x1 = center
            y1 = center
            x2 = int(center + blur_radius * np.cos(np.radians(blur_angle)))
            y2 = int(center + blur_radius * np.sin(np.radians(blur_angle)))

            cv2.line(kernel, (x1, y1), (x2, y2), 1.0, 1)

            # Normalize kernel
            kernel = kernel / np.sum(kernel)

            # Apply blur
            blurred = cv2.filter2D(mouth_region, -1, kernel)

            return {"image": blurred, "blend_mode": "normal", "blend_strength": 0.7}
        else:
            return None

    def _generate_forehead_effect(
        self, image: np.ndarray, mask: np.ndarray, state: Dict
    ) -> Optional[Dict]:
        """Generate special effect for forehead region."""
        # Simple implementation - can be expanded
        return None
