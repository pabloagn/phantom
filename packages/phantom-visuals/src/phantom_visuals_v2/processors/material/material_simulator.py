# apts/material/material_simulator.py

"""Material simulation module for creating realistic material effects."""

import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import torch


class MaterialSimulator:
    """
    Simulates advanced material properties and transformations for artistic effects.
    This module handles liquid, crystalline, fabric, and other material simulations.
    """

    def __init__(self, config, device=None):
        """
        Initialize the material simulator.

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
        self.material_type = config.get("material_type", "default")

        # Load any additional resources needed for specific material types
        if self.material_type == "liquid":
            self._init_liquid_simulator()
        elif self.material_type == "crystalline":
            self._init_crystalline_simulator()
        elif self.material_type == "fabric":
            self._init_fabric_simulator()
        elif self.material_type == "particle":
            self._init_particle_simulator()

    def _init_liquid_simulator(self):
        """Initialize resources for liquid simulation."""
        self.liquid_viscosity = self.config.get("viscosity", 0.8)
        self.liquid_surface_tension = self.config.get("surface_tension", 0.6)
        self.liquid_iterations = self.config.get("iterations", 5)

    def _init_crystalline_simulator(self):
        """Initialize resources for crystalline material simulation."""
        self.crystal_facets = self.config.get("facets", 12)
        self.crystal_reflectivity = self.config.get("reflectivity", 0.7)
        self.crystal_sharpness = self.config.get("sharpness", 0.8)

    def _init_fabric_simulator(self):
        """Initialize resources for fabric simulation."""
        self.fabric_weave_density = self.config.get("weave_density", 100)
        self.fabric_elasticity = self.config.get("elasticity", 0.5)
        self.fabric_drape = self.config.get("drape", 0.7)

    def _init_particle_simulator(self):
        """Initialize resources for particle simulation."""
        self.particle_count = self.config.get("particle_count", 10000)
        self.particle_size_range = self.config.get("size_range", (0.5, 2.0))
        self.particle_velocity_damping = self.config.get("velocity_damping", 0.95)

    def simulate(self, image: np.ndarray, state: Dict) -> Dict[str, Any]:
        """
        Simulate material properties and transformations.

        Args:
            image: Input RGB image
            state: Current transformation state

        Returns:
            Dictionary with material maps and parameters
        """
        result = {}
        h, w = image.shape[:2]

        # Create basic material map (default)
        material_map = np.zeros((h, w, 4), dtype=np.float32)  # RGBA
        material_map[:, :, 3] = 1.0  # Default alpha

        # Initialize material properties based on image and face analysis
        result.update(self._initialize_material_properties(image, state))

        # Apply material-specific simulations
        if self.material_type == "liquid":
            result.update(self._simulate_liquid(image, state))
        elif self.material_type == "crystalline":
            result.update(self._simulate_crystalline(image, state))
        elif self.material_type == "fabric":
            result.update(self._simulate_fabric(image, state))
        elif self.material_type == "particle":
            result.update(self._simulate_particles(image, state))
        elif self.material_type == "custom":
            # Use custom material definition from config
            custom_type = self.config.get("custom_material", "mixed")
            if custom_type == "mixed":
                result.update(self._simulate_mixed_materials(image, state))
            else:
                # Default to base material properties
                pass

        # Generate material transition map if needed
        if "flow_field" in state and self.config.get("generate_transition_map", True):
            transition_map = self._generate_transition_map(image, state)
            result["transition_map"] = transition_map

        # Return material simulation results
        return result

    def _initialize_material_properties(
        self, image: np.ndarray, state: Dict
    ) -> Dict[str, Any]:
        """Initialize basic material properties from image and face analysis."""
        result = {}
        h, w = image.shape[:2]

        # Create base material property maps
        diffuse_map = image.astype(np.float32) / 255.0
        specular_map = np.zeros((h, w), dtype=np.float32)
        roughness_map = np.ones((h, w), dtype=np.float32) * 0.5
        normal_map = np.zeros((h, w, 3), dtype=np.float32)
        normal_map[:, :, 2] = 1.0  # Default surface normal (facing camera)

        # If we have face analysis, refine material properties
        if "landmarks" in state:
            face_mask = np.zeros((h, w), dtype=np.float32)

            # Create face mask from landmarks or bbox
            if "face_bbox" in state:
                x1, y1, x2, y2 = state["face_bbox"]
                face_mask[y1:y2, x1:x2] = 1.0
            else:
                # Fallback to convex hull of landmarks
                landmarks = state["landmarks"]
                points = np.array([landmarks[:, :2]], dtype=np.int32)
                cv2.fillConvexPoly(face_mask, points, 1.0)

            # Smooth face mask
            face_mask = cv2.GaussianBlur(face_mask, (0, 0), w * 0.02)

            # Different material properties for face vs background
            # For example, skin is more diffuse, less specular, and smoother
            face_spec = self.config.get("face_specularity", 0.3)
            face_rough = self.config.get("face_roughness", 0.7)
            bg_spec = self.config.get("background_specularity", 0.1)
            bg_rough = self.config.get("background_roughness", 0.9)

            # Blend material properties
            specular_map = face_mask * face_spec + (1 - face_mask) * bg_spec
            roughness_map = face_mask * face_rough + (1 - face_mask) * bg_rough

            # Use depth map for normals if available
            if "depth_map" in state and "normal_map" in state:
                depth_scaled = cv2.resize(
                    state["depth_map"], (w, h), interpolation=cv2.INTER_LINEAR
                )
                normal_scaled = cv2.resize(
                    state["normal_map"], (w, h), interpolation=cv2.INTER_LINEAR
                )

                # Use provided normal map
                normal_map = normal_scaled.copy()
            else:
                # Estimate normal map from grayscale image
                gray = (
                    cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
                )

                # Simple normal estimation from image gradients
                dx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
                dy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)

                # Create normal map
                normal_strength = self.config.get("normal_strength", 0.5)
                normal_map[:, :, 0] = -dx * normal_strength
                normal_map[:, :, 1] = -dy * normal_strength

                # Renormalize
                norm = np.sqrt(np.sum(normal_map**2, axis=2, keepdims=True))
                norm = np.maximum(norm, 1e-6)
                normal_map /= norm

        # Store material property maps
        result["diffuse_map"] = diffuse_map
        result["specular_map"] = specular_map
        result["roughness_map"] = roughness_map
        result["normal_map"] = normal_map

        return result

    def _simulate_liquid(self, image: np.ndarray, state: Dict) -> Dict[str, Any]:
        """Simulate liquid material properties."""
        result = {}
        h, w = image.shape[:2]

        # Get base material maps
        diffuse_map = state.get("diffuse_map", image.astype(np.float32) / 255.0)

        # Check if we should downsample for simulation
        max_sim_size = self.config.get("max_simulation_size", 512)
        do_downsample = max(h, w) > max_sim_size

        if do_downsample:
            # Calculate downsample ratio
            scale = max_sim_size / max(h, w)
            sim_h, sim_w = int(h * scale), int(w * scale)

            # Downsample image and maps
            diffuse_small = cv2.resize(diffuse_map, (sim_w, sim_h))
        else:
            # Use original size
            sim_h, sim_w = h, w
            diffuse_small = diffuse_map

        # Create liquid state maps at simulation resolution
        viscosity_map = (
            np.ones((sim_h, sim_w), dtype=np.float32) * self.liquid_viscosity
        )
        displacement_map = np.zeros((sim_h, sim_w, 2), dtype=np.float32)

        # If we have flow field, use it to guide liquid simulation
        if "flow_field" in state:
            flow = state["flow_field"]

            # Downsample flow if needed
            flow_small = cv2.resize(flow, (sim_w, sim_h)) if do_downsample else flow

            # Define simulation parameters
            iterations = self.liquid_iterations
            dt = self.config.get("time_step", 0.1)

            # Initialize displacement map
            init_displace_scale = self.config.get("init_displacement_scale", 0.0)
            if init_displace_scale > 0:
                noise = np.random.normal(0, init_displace_scale, (sim_h, sim_w, 2))
                displacement_map += noise

            # Run fluid simulation iterations
            for i in range(iterations):
                # Advection: move displacement by flow
                # Create buffer to avoid read/write conflicts
                new_displacement = np.zeros_like(displacement_map)

                for y in range(sim_h):
                    for x in range(sim_w):
                        # Get flow at this point
                        fx, fy = flow_small[y, x]

                        # Sample displacement at upstream position
                        sample_x = int(max(0, min(sim_w - 1, x - fx * dt)))
                        sample_y = int(max(0, min(sim_h - 1, y - fy * dt)))

                        # Add displacement from current and upstream positions
                        new_displacement[y, x] = (
                            displacement_map[y, x]
                            + displacement_map[sample_y, sample_x] * dt * 0.1
                        )

                # Update displacement map
                displacement_map = new_displacement.copy()

                # Viscosity step: smooth displacement
                displacement_map[:, :, 0] = cv2.GaussianBlur(
                    displacement_map[:, :, 0], (0, 0), self.liquid_viscosity * 5
                )
                displacement_map[:, :, 1] = cv2.GaussianBlur(
                    displacement_map[:, :, 1], (0, 0), self.liquid_viscosity * 5
                )

                # Constraint step: limit displacement magnitude
                mag = np.sqrt(
                    displacement_map[:, :, 0] ** 2 + displacement_map[:, :, 1] ** 2
                )
                max_mag = self.config.get("max_displacement", 20.0)
                scale = np.minimum(1.0, max_mag / (mag + 1e-6))
                displacement_map[:, :, 0] *= scale
                displacement_map[:, :, 1] *= scale

            # Upsample results if we downsampled
            if do_downsample:
                # Upsample displacement map
                displacement_map = cv2.resize(displacement_map, (w, h))

        # Create liquid-specific material maps
        refraction_map = np.ones((h, w), dtype=np.float32) * self.config.get(
            "refraction_index", 1.33
        )
        absorption_map = np.zeros((h, w, 3), dtype=np.float32)
        caustics_map = np.zeros((h, w), dtype=np.float32)

        # Adjust based on displacement
        mag = np.sqrt(displacement_map[:, :, 0] ** 2 + displacement_map[:, :, 1] ** 2)
        mag_norm = np.minimum(1.0, mag / self.config.get("max_displacement", 20.0))

        # More refraction and less absorption where displacement is high
        refraction_map += mag_norm * 0.5
        absorption_map = np.stack([mag_norm * 0.2] * 3, axis=-1)

        # Generate caustics (simplified)
        caustics_strength = self.config.get("caustics_strength", 0.5)
        if caustics_strength > 0:
            # Use second derivatives of displacement as caustics
            dx_dx = cv2.Sobel(displacement_map[:, :, 0], cv2.CV_32F, 1, 0, ksize=3)
            dy_dy = cv2.Sobel(displacement_map[:, :, 1], cv2.CV_32F, 0, 1, ksize=3)

            # Caustics intensity proportional to displacement concentration
            caustics_map = np.abs(dx_dx + dy_dy) * caustics_strength
            caustics_map = cv2.GaussianBlur(caustics_map, (0, 0), 1.0)

        # Create distorted diffuse map for liquid effect
        liquid_diffuse = np.zeros_like(diffuse_map)

        # Apply displacement to diffuse map
        for y in range(h):
            for x in range(w):
                dx, dy = displacement_map[y, x]

                # Sample position with displacement
                sample_x = int(max(0, min(w - 1, x + dx)))
                sample_y = int(max(0, min(h - 1, y + dy)))

                # Sample color
                liquid_diffuse[y, x] = diffuse_map[sample_y, sample_x]

        # Apply lighting effects (simplified)
        specular_power = self.config.get("specular_power", 50.0)
        specular_color = np.array([1.0, 1.0, 1.0])

        # Light direction (simplified to one directional light)
        light_dir = np.array([0.5, 0.5, 0.7])
        light_dir = light_dir / np.linalg.norm(light_dir)

        # Calculate lighting
        if "normal_map" in state:
            normals = state["normal_map"]

            # Apply displacement to normals
            perturbed_normals = normals.copy()
            perturbed_normals[:, :, 0] += displacement_map[:, :, 0] * 0.05
            perturbed_normals[:, :, 1] += displacement_map[:, :, 1] * 0.05

            # Renormalize
            norm = np.sqrt(np.sum(perturbed_normals**2, axis=2, keepdims=True))
            perturbed_normals /= np.maximum(norm, 1e-6)

            # Calculate diffuse lighting (N dot L)
            n_dot_l = np.maximum(0, np.sum(perturbed_normals * light_dir, axis=2))

            # Apply diffuse lighting
            liquid_diffuse *= n_dot_l[:, :, np.newaxis] * 0.8 + 0.2

            # Calculate specular lighting (simplified Blinn-Phong)
            view_dir = np.array([0, 0, 1])  # Viewing from front
            half_dir = (light_dir + view_dir) / 2
            half_dir = half_dir / np.linalg.norm(half_dir)

            # N dot H for specular
            n_dot_h = np.maximum(0, np.sum(perturbed_normals * half_dir, axis=2))
            specular = (
                np.power(n_dot_h, specular_power)[:, :, np.newaxis] * specular_color
            )

            # Add specular highlight
            liquid_diffuse += specular * 0.3

        # Add caustics
        liquid_diffuse += caustics_map[:, :, np.newaxis] * np.array([0.5, 0.7, 1.0])

        # Clip to valid range
        liquid_diffuse = np.clip(liquid_diffuse, 0, 1)

        # Store liquid simulation results
        result["liquid_diffuse"] = liquid_diffuse
        result["displacement_map"] = displacement_map
        result["refraction_map"] = refraction_map
        result["caustics_map"] = caustics_map

        # Set main material output for later stages
        result["material_diffuse"] = liquid_diffuse
        result["material_type"] = "liquid"

        return result

    def _simulate_crystalline(self, image: np.ndarray, state: Dict) -> Dict[str, Any]:
        """Simulate crystalline material properties."""
        result = {}
        h, w = image.shape[:2]

        # Get base material maps
        diffuse_map = state.get("diffuse_map", image.astype(np.float32) / 255.0)

        # Create crystalline property maps
        facet_map = np.zeros((h, w), dtype=np.int32)
        reflection_map = np.ones((h, w), dtype=np.float32) * self.crystal_reflectivity

        # Generate Voronoi-like facets
        num_seeds = self.crystal_facets
        seeds = np.random.rand(num_seeds, 2)
        seeds[:, 0] *= w
        seeds[:, 1] *= h

        # Add face landmarks as seeds if available
        if "landmarks" in state:
            landmarks = state["landmarks"]
            # Add key facial landmarks as seeds
            if len(landmarks) >= 468:
                key_indices = [33, 133, 362, 263, 4, 61, 291, 199]  # Eyes, nose, mouth
                for idx in key_indices:
                    if idx < len(landmarks):
                        seeds = np.vstack([seeds, landmarks[idx, :2]])

        # Create facet map
        for y in range(h):
            for x in range(w):
                # Find closest seed
                closest_idx = np.argmin(np.sum((seeds - [x, y]) ** 2, axis=1))
                facet_map[y, x] = closest_idx

        # Generate normals for each facet
        facet_normals = np.zeros(
            (num_seeds + len(key_indices) if "landmarks" in state else num_seeds, 3)
        )
        for i in range(len(facet_normals)):
            # Random orientation for each facet
            theta = np.random.uniform(0, np.pi / 4)  # Tilt angle
            phi = np.random.uniform(0, 2 * np.pi)  # Rotation angle

            # Convert to normal
            facet_normals[i, 0] = np.sin(theta) * np.cos(phi)
            facet_normals[i, 1] = np.sin(theta) * np.sin(phi)
            facet_normals[i, 2] = np.cos(theta)

        # Create normal map from facets
        crystal_normal = np.zeros((h, w, 3), dtype=np.float32)
        for y in range(h):
            for x in range(w):
                idx = facet_map[y, x]
                if idx < len(facet_normals):
                    crystal_normal[y, x] = facet_normals[idx]

        # Add edge details to emphasize crystal facets
        edge_mask = np.zeros((h, w), dtype=np.float32)
        facet_edges = cv2.Laplacian(facet_map.astype(np.float32), cv2.CV_32F)
        edge_mask = np.abs(facet_edges) > 0

        # Smooth edges
        edge_mask = edge_mask.astype(np.float32)
        edge_mask = cv2.GaussianBlur(edge_mask, (0, 0), 0.5)

        # Create crystal diffuse map
        crystal_diffuse = diffuse_map.copy()

        # Apply edge darkening
        crystal_diffuse *= 1.0 - edge_mask[:, :, np.newaxis] * 0.5

        # Apply facet lighting
        light_dir = np.array([0.5, 0.5, 0.7])
        light_dir = light_dir / np.linalg.norm(light_dir)

        # N dot L for diffuse
        n_dot_l = np.maximum(0, np.sum(crystal_normal * light_dir, axis=2))
        crystal_diffuse *= n_dot_l[:, :, np.newaxis] * 0.7 + 0.3

        # Add specular highlights
        view_dir = np.array([0, 0, 1])
        half_dir = (light_dir + view_dir) / 2
        half_dir = half_dir / np.linalg.norm(half_dir)

        # N dot H for specular
        n_dot_h = np.maximum(0, np.sum(crystal_normal * half_dir, axis=2))
        specular_power = 100.0  # Higher for more concentrated highlights
        specular = np.power(n_dot_h, specular_power)[:, :, np.newaxis]

        # Add colored specular
        if self.config.get("colored_specular", True):
            # Use input image colors for specular tint
            specular_tint = diffuse_map * 0.5 + 0.5
            specular = specular * specular_tint
        else:
            specular = specular * np.array([1.0, 1.0, 1.0])

        # Add specular to diffuse
        crystal_diffuse += specular * self.crystal_reflectivity

        # Clip to valid range
        crystal_diffuse = np.clip(crystal_diffuse, 0, 1)

        # Store crystalline simulation results
        result["crystal_diffuse"] = crystal_diffuse
        result["facet_map"] = facet_map
        result["crystal_normal"] = crystal_normal
        result["edge_mask"] = edge_mask

        # Set main material output for later stages
        result["material_diffuse"] = crystal_diffuse
        result["material_type"] = "crystalline"

        return result

    def _simulate_fabric(self, image: np.ndarray, state: Dict) -> Dict[str, Any]:
        """Simulate fabric material properties."""
        result = {}
        h, w = image.shape[:2]

        # Get base material maps
        diffuse_map = state.get("diffuse_map", image.astype(np.float32) / 255.0)

        # Create fabric property maps
        weave_map = np.zeros((h, w), dtype=np.float32)
        stretch_map = np.zeros((h, w, 2), dtype=np.float32)

        # Generate fabric weave pattern
        density = self.fabric_weave_density
        scale_x = self.config.get("weave_scale_x", 1.0)
        scale_y = self.config.get("weave_scale_y", 1.0)

        # Create simple interlaced weave pattern
        for y in range(h):
            for x in range(w):
                wx = int(x * scale_x * density / w)
                wy = int(y * scale_y * density / h)

                # Alternating pattern
                if (wx % 2 == 0 and wy % 2 == 0) or (wx % 2 == 1 and wy % 2 == 1):
                    weave_map[y, x] = 1.0
                else:
                    weave_map[y, x] = 0.5

        # Apply fabric draping effect
        if "flow_field" in state:
            flow = state["flow_field"]

            # Use flow field for fabric stretching
            stretch_map = flow * self.fabric_elasticity * 10.0

            # Simulate fabric stretch along flow directions
            fabric_diffuse = np.zeros_like(diffuse_map)

            # Apply stretching/draping
            for y in range(h):
                for x in range(w):
                    # Get stretch at this point
                    sx, sy = stretch_map[y, x]

                    # Sample position with stretch
                    sample_x = int(max(0, min(w - 1, x + sx)))
                    sample_y = int(max(0, min(h - 1, y + sy)))

                    # Sample color and weave
                    fabric_diffuse[y, x] = diffuse_map[sample_y, sample_x]

                    # Adjust weave pattern based on stretch
                    stretch_amount = np.sqrt(sx**2 + sy**2)
                    weave_map[y, x] *= max(0.5, 1.0 - stretch_amount * 0.05)
        else:
            fabric_diffuse = diffuse_map.copy()

        # Apply weave pattern to diffuse
        fabric_diffuse *= weave_map[:, :, np.newaxis] * 0.5 + 0.5

        # Add fabric texture
        if self.config.get("add_fabric_texture", True):
            # Generate noise for fabric texture
            texture_scale = self.config.get("texture_scale", 50.0)
            octaves = self.config.get("texture_octaves", 3)
            from noise import pnoise2

            texture = np.zeros((h, w), dtype=np.float32)
            for y in range(h):
                for x in range(w):
                    nx = x / texture_scale
                    ny = y / texture_scale
                    texture[y, x] = pnoise2(nx, ny, octaves=octaves)

            # Normalize texture
            texture = (texture - texture.min()) / (texture.max() - texture.min() + 1e-6)

            # Apply texture
            texture_strength = self.config.get("texture_strength", 0.3)
            fabric_diffuse *= (
                1.0 - texture_strength + texture[:, :, np.newaxis] * texture_strength
            )

        # Apply lighting
        light_dir = np.array([0.5, 0.5, 0.7])
        light_dir = light_dir / np.linalg.norm(light_dir)

        # Create fabric normals
        fabric_normal = np.zeros((h, w, 3), dtype=np.float32)
        fabric_normal[:, :, 2] = 1.0  # Base normal facing camera

        # Modulate normals with weave pattern for micro-surface variations
        weave_grad_x = cv2.Sobel(weave_map, cv2.CV_32F, 1, 0, ksize=3)
        weave_grad_y = cv2.Sobel(weave_map, cv2.CV_32F, 0, 1, ksize=3)

        normal_strength = self.config.get("fabric_normal_strength", 0.2)
        fabric_normal[:, :, 0] = -weave_grad_x * normal_strength
        fabric_normal[:, :, 1] = -weave_grad_y * normal_strength

        # Normalize
        norm = np.sqrt(np.sum(fabric_normal**2, axis=2, keepdims=True))
        fabric_normal /= np.maximum(norm, 1e-6)

        # Apply lighting
        n_dot_l = np.maximum(0, np.sum(fabric_normal * light_dir, axis=2))
        fabric_diffuse *= n_dot_l[:, :, np.newaxis] * 0.6 + 0.4

        # Add subtle specular (fabric has low specular)
        view_dir = np.array([0, 0, 1])
        half_dir = (light_dir + view_dir) / 2
        half_dir = half_dir / np.linalg.norm(half_dir)

        n_dot_h = np.maximum(0, np.sum(fabric_normal * half_dir, axis=2))
        specular_power = 10.0  # Lower for fabric (more diffuse highlight)
        specular = np.power(n_dot_h, specular_power)[:, :, np.newaxis] * 0.1

        fabric_diffuse += specular

        # Clip to valid range
        fabric_diffuse = np.clip(fabric_diffuse, 0, 1)

        # Store fabric simulation results
        result["fabric_diffuse"] = fabric_diffuse
        result["weave_map"] = weave_map
        result["stretch_map"] = stretch_map
        result["fabric_normal"] = fabric_normal

        # Set main material output
        result["material_diffuse"] = fabric_diffuse
        result["material_type"] = "fabric"

        return result

    def _simulate_particles(self, image: np.ndarray, state: Dict) -> Dict[str, Any]:
        """Simulate particle-based material properties."""
        result = {}
        h, w = image.shape[:2]

        # Get base material maps
        diffuse_map = state.get("diffuse_map", image.astype(np.float32) / 255.0)

        # Create particle system
        num_particles = self.particle_count

        # Initialize particle positions, sizes, colors
        if "face_bbox" in state:
            # Concentrate particles around face
            x1, y1, x2, y2 = state["face_bbox"]

            # Generate particles with higher density in face area
            face_ratio = self.config.get("face_particle_ratio", 0.7)
            face_count = int(num_particles * face_ratio)
            bg_count = num_particles - face_count

            # Face area particles
            face_pos_x = np.random.uniform(x1, x2, face_count)
            face_pos_y = np.random.uniform(y1, y2, face_count)

            # Background particles
            bg_pos_x = np.random.uniform(0, w, bg_count)
            bg_pos_y = np.random.uniform(0, h, bg_count)

            # Combine
            pos_x = np.concatenate([face_pos_x, bg_pos_x])
            pos_y = np.concatenate([face_pos_y, bg_pos_y])
        else:
            # Uniform distribution
            pos_x = np.random.uniform(0, w, num_particles)
            pos_y = np.random.uniform(0, h, num_particles)

        # Get colors from diffuse map at particle positions
        colors = np.zeros((num_particles, 3), dtype=np.float32)
        for i in range(num_particles):
            x, y = int(min(w - 1, max(0, pos_x[i]))), int(min(h - 1, max(0, pos_y[i])))
            colors[i] = diffuse_map[y, x]

        # Generate particle sizes
        min_size, max_size = self.particle_size_range
        sizes = np.random.uniform(min_size, max_size, num_particles)

        # If we have flow field, use it to move particles
        if "flow_field" in state:
            flow = state["flow_field"]

            # Apply flow to particle positions
            motion_strength = self.config.get("particle_motion_strength", 5.0)

            # Initialize velocities
            vel_x = np.zeros(num_particles, dtype=np.float32)
            vel_y = np.zeros(num_particles, dtype=np.float32)

            # Simulation steps
            steps = self.config.get("particle_sim_steps", 10)
            dt = self.config.get("particle_time_step", 0.1)
            damping = self.particle_velocity_damping

            # Store particle paths for trails
            paths = []
            store_paths = self.config.get("particle_trails", False)
            if store_paths:
                for i in range(num_particles):
                    paths.append([(pos_x[i], pos_y[i])])

            # Run simulation
            for step in range(steps):
                for i in range(num_particles):
                    x, y = (
                        int(min(w - 1, max(0, pos_x[i]))),
                        int(min(h - 1, max(0, pos_y[i]))),
                    )

                    # Get flow at particle position
                    fx, fy = flow[y, x]

                    # Update velocity (simplified physics)
                    vel_x[i] = vel_x[i] * damping + fx * motion_strength * dt
                    vel_y[i] = vel_y[i] * damping + fy * motion_strength * dt

                    # Update position
                    pos_x[i] += vel_x[i] * dt
                    pos_y[i] += vel_y[i] * dt

                    # Boundary conditions
                    if pos_x[i] < 0 or pos_x[i] >= w or pos_y[i] < 0 or pos_y[i] >= h:
                        # Reset to random position in image
                        pos_x[i] = np.random.uniform(0, w)
                        pos_y[i] = np.random.uniform(0, h)
                        vel_x[i] = 0
                        vel_y[i] = 0

                    # Store path
                    if store_paths:
                        paths[i].append((pos_x[i], pos_y[i]))

        # Render particles to image
        particle_img = np.zeros((h, w, 4), dtype=np.float32)  # RGBA

        # Sort particles by Y for back-to-front rendering
        indices = np.argsort(pos_y)

        # Render each particle
        for idx in indices:
            x, y = pos_x[idx], pos_y[idx]
            size = sizes[idx]
            color = colors[idx]

            # Skip particles outside image
            if x < 0 or x >= w or y < 0 or y >= h:
                continue

            # Draw particle
            x_min = max(0, int(x - size))
            x_max = min(w, int(x + size + 1))
            y_min = max(0, int(y - size))
            y_max = min(h, int(y + size + 1))

            for py in range(y_min, y_max):
                for px in range(x_min, x_max):
                    # Calculate distance from particle center
                    dist = np.sqrt((px - x) ** 2 + (py - y) ** 2)

                    # If within particle radius
                    if dist <= size:
                        # Calculate alpha based on distance from center
                        alpha = max(0, 1.0 - dist / size)

                        # Composite over existing particle image
                        existing_alpha = particle_img[py, px, 3]
                        new_alpha = alpha + existing_alpha * (1 - alpha)

                        if new_alpha > 0:
                            # Blend colors
                            for c in range(3):
                                particle_img[py, px, c] = (
                                    color[c] * alpha
                                    + particle_img[py, px, c]
                                    * existing_alpha
                                    * (1 - alpha)
                                ) / new_alpha

                            # Update alpha
                            particle_img[py, px, 3] = new_alpha

        # Create final particle diffuse map
        particle_diffuse = np.zeros_like(diffuse_map)

        # Composite particles over original image
        alpha = particle_img[:, :, 3:4]
        particle_diffuse = particle_img[:, :, :3] * alpha + diffuse_map * (1 - alpha)

        # Store particle simulation results
        result["particle_diffuse"] = particle_diffuse
        result["particle_positions"] = np.stack([pos_x, pos_y], axis=1)
        result["particle_sizes"] = sizes
        result["particle_colors"] = colors

        if "paths" in locals() and len(paths) > 0:
            result["particle_paths"] = paths

        # Store particle simulation results
        result["particle_diffuse"] = particle_diffuse
        result["particle_positions"] = np.stack([pos_x, pos_y], axis=1)
        result["particle_sizes"] = sizes
        result["particle_colors"] = colors

        if "paths" in locals() and store_paths:
            result["particle_paths"] = paths

        # Set main material output
        result["material_diffuse"] = particle_diffuse
        result["material_type"] = "particle"

        return result

    def _simulate_mixed_materials(
        self, image: np.ndarray, state: Dict
    ) -> Dict[str, Any]:
        """Simulate mixed material properties (combines multiple material types)."""
        result = {}
        h, w = image.shape[:2]

        # Define material mix
        # This can be modified based on the specific artistic effect desired
        material_mix = self.config.get(
            "material_mix", {"liquid": 0.4, "crystalline": 0.3, "particle": 0.3}
        )

        # Generate individual material results
        material_results = {}

        # Only simulate materials with non-zero weight
        if material_mix.get("liquid", 0) > 0:
            # Save original material type and temporarily set to liquid
            orig_type = self.material_type
            self.material_type = "liquid"
            material_results["liquid"] = self._simulate_liquid(image, state)
            self.material_type = orig_type

        if material_mix.get("crystalline", 0) > 0:
            orig_type = self.material_type
            self.material_type = "crystalline"
            material_results["crystalline"] = self._simulate_crystalline(image, state)
            self.material_type = orig_type

        if material_mix.get("fabric", 0) > 0:
            orig_type = self.material_type
            self.material_type = "fabric"
            material_results["fabric"] = self._simulate_fabric(image, state)
            self.material_type = orig_type

        if material_mix.get("particle", 0) > 0:
            orig_type = self.material_type
            self.material_type = "particle"
            material_results["particle"] = self._simulate_particles(image, state)
            self.material_type = orig_type

        # Create spatial mix maps if using spatial mixing
        spatial_mix = self.config.get("spatial_mixing", False)
        if spatial_mix:
            mix_maps = self._generate_spatial_mix_maps(image, state, material_mix)
        else:
            # Use global weights
            mix_maps = {
                k: np.ones((h, w), dtype=np.float32) * v
                for k, v in material_mix.items()
                if v > 0
            }

        # Blend material results
        mixed_diffuse = np.zeros((h, w, 3), dtype=np.float32)
        total_weight = np.zeros((h, w), dtype=np.float32)

        for material, weight_map in mix_maps.items():
            if (
                material in material_results
                and "material_diffuse" in material_results[material]
            ):
                diffuse = material_results[material]["material_diffuse"]
                mixed_diffuse += diffuse * weight_map[:, :, np.newaxis]
                total_weight += weight_map

        # Normalize by total weight
        total_weight = np.maximum(total_weight, 1e-6)[:, :, np.newaxis]
        mixed_diffuse /= total_weight

        # Store mixed simulation results
        result["mixed_diffuse"] = mixed_diffuse
        result["material_mix_maps"] = mix_maps

        # Copy individual material results for reference
        for material, mat_result in material_results.items():
            for key, value in mat_result.items():
                result[f"{material}_{key}"] = value

        # Set main material output
        result["material_diffuse"] = mixed_diffuse
        result["material_type"] = "mixed"

        return result

    def _generate_spatial_mix_maps(
        self, image: np.ndarray, state: Dict, material_mix: Dict
    ) -> Dict[str, np.ndarray]:
        """Generate spatially-varying material mix maps."""
        h, w = image.shape[:2]
        mix_maps = {}

        # Create base mix maps based on image properties
        # For more sophisticated effects, this could use face analysis

        if "face_bbox" in state:
            # Create map that separates face from background
            face_mask = np.zeros((h, w), dtype=np.float32)
            x1, y1, x2, y2 = state["face_bbox"]
            face_mask[y1:y2, x1:x2] = 1.0

            # Smooth mask edges
            face_mask = cv2.GaussianBlur(face_mask, (0, 0), w * 0.02)

            # Create material maps based on face mask
            if "liquid" in material_mix:
                # More liquid effect in face area
                liquid_map = face_mask.copy()
                mix_maps["liquid"] = liquid_map

            if "crystalline" in material_mix:
                # More crystalline in background
                crystal_map = 1.0 - face_mask
                mix_maps["crystalline"] = crystal_map

            if "fabric" in material_mix:
                # Equal fabric everywhere
                mix_maps["fabric"] = (
                    np.ones((h, w), dtype=np.float32) * material_mix["fabric"]
                )

            if "particle" in material_mix:
                # Particle density varies with image contrast
                gray = (
                    cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
                )
                contrast = cv2.Laplacian(gray, cv2.CV_32F)
                contrast = np.abs(contrast)
                contrast = cv2.GaussianBlur(contrast, (0, 0), 3.0)
                contrast = (contrast - contrast.min()) / (
                    contrast.max() - contrast.min() + 1e-6
                )

                mix_maps["particle"] = contrast
        else:
            # No face detected, use simpler approach
            # Divide image into regions based on brightness
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0

            # Smooth brightness
            gray_smooth = cv2.GaussianBlur(gray, (0, 0), w * 0.05)

            # Create maps
            if "liquid" in material_mix:
                # More liquid in darker areas
                liquid_map = 1.0 - gray_smooth
                mix_maps["liquid"] = liquid_map * material_mix["liquid"]

            if "crystalline" in material_mix:
                # More crystalline in brighter areas
                crystal_map = gray_smooth
                mix_maps["crystalline"] = crystal_map * material_mix["crystalline"]

            if "fabric" in material_mix:
                # Fabric in mid-tones
                fabric_map = 1.0 - np.abs(gray_smooth - 0.5) * 2.0
                mix_maps["fabric"] = fabric_map * material_mix["fabric"]

            if "particle" in material_mix:
                # Particles based on texture
                texture = cv2.Laplacian(gray, cv2.CV_32F)
                texture = np.abs(texture)
                texture = cv2.GaussianBlur(texture, (0, 0), 3.0)
                texture = (texture - texture.min()) / (
                    texture.max() - texture.min() + 1e-6
                )

                mix_maps["particle"] = texture * material_mix["particle"]

        # Normalize maps
        total = sum(np.sum(m) for m in mix_maps.values())

        if total > 0:
            for material in mix_maps:
                mix_maps[material] /= total / np.sum(mix_maps[material])

        return mix_maps

    def _generate_transition_map(self, image: np.ndarray, state: Dict) -> np.ndarray:
        """Generate material transition map for blending effects."""
        h, w = image.shape[:2]

        # Create transition map based on flow field magnitude
        if "flow_field" in state:
            flow = state["flow_field"]

            # Calculate flow magnitude
            flow_mag = np.sqrt(flow[:, :, 0] ** 2 + flow[:, :, 1] ** 2)

            # Normalize
            flow_mag = flow_mag / np.max(flow_mag + 1e-6)

            # Apply non-linear transformation for better contrast
            transition_map = np.power(flow_mag, 0.5)

            # Blur for smoother transitions
            transition_map = cv2.GaussianBlur(transition_map, (0, 0), w * 0.01)
        else:
            # Fallback to gradient-based transition
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0

            # Calculate gradient magnitude
            grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
            grad_mag = np.sqrt(grad_x**2 + grad_y**2)

            # Normalize
            transition_map = grad_mag / np.max(grad_mag + 1e-6)

            # Smooth
            transition_map = cv2.GaussianBlur(transition_map, (0, 0), w * 0.01)

        return transition_map

    def visualize_materials(self, state: Dict) -> np.ndarray:
        """Create a visualization of the material properties for debugging."""
        if "material_diffuse" not in state:
            # Return empty visualization
            return np.zeros((300, 300, 3), dtype=np.uint8)

        # Use the material diffuse map as visualization
        material_diffuse = state["material_diffuse"]

        # Convert to 8-bit for display
        vis = (material_diffuse * 255).astype(np.uint8)

        return vis
