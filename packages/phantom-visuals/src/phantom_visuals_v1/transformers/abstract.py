# packages/phantom-visuals/phantom_visuals/transformers/abstract.py

"""Abstract art composer for Phantom Visuals.

This module provides tools for creating abstract generative art with
the distinctive Phantom visual aesthetic.
"""

import math
import random
from pathlib import Path
from typing import Optional, Union

import cv2
import numpy as np

from phantom_visuals.core.config import Configuration
from phantom_visuals.core.engine import StyleEngine
from phantom_visuals.effects import (
    EffectChain,
    add_grain,
    add_vignette,
    adjust_brightness,
    adjust_contrast,
    apply_symmetry,
    displace,
    duotone,
    gaussian_blur,
    gradient_map,
    lens_distortion,
    pixel_sort,
    radial_blur,
    swirl,
    wave_distortion,
)


class AbstractComposer:
    """Generator for abstract art compositions.

    This class provides methods for creating abstract generative art with
    various techniques and styles inspired by modernist, minimalist, and
    experimental visual aesthetics.
    """

    def __init__(self, config: Optional[Configuration] = None):
        """Initialize the abstract composer.

        Args:
            config: Configuration settings to use
        """
        self.engine = StyleEngine(config)
        self.config = self.engine.config

    def create_composition(
        self,
        width: int = 1200,
        height: int = 1600,
        output_path: Union[str, Path] = "output/abstract.png",
        style: Optional[str] = None,
    ) -> Path:
        """Create an abstract composition with the specified style.

        Args:
            width: Width of the composition in pixels
            height: Height of the composition in pixels
            output_path: Path where the result should be saved
            style: Style variant to apply (defaults to config.style_variant)

        Returns:
            Path where the composition was saved
        """
        # Use specified style or default from config
        style_variant = style or str(self.config.style_variant.value)

        # Create base canvas
        canvas = self._create_base_canvas(width, height, style_variant)

        # Reset any previously added transformations
        self.engine.reset_transformations()

        # Add transformations based on style variant
        if style_variant == "minimal":
            self._add_minimal_style()
        elif style_variant == "duotone":
            self._add_duotone_style()
        elif style_variant == "abstract":
            self._add_abstract_style()
        elif style_variant == "ethereal":
            self._add_ethereal_style()
        elif style_variant == "modernist":
            self._add_modernist_style()
        elif style_variant == "phantom":
            self._add_phantom_style()
        elif style_variant == "gothic":
            self._add_gothic_style()
        elif style_variant == "symmetrical":
            self._add_symmetrical_style()
        else:
            # Default to phantom style
            self._add_phantom_style()

        # Process the canvas
        result = self.engine.process_image(canvas)

        # Save and return the result
        return self.engine.save_image(result, output_path)

    def _create_base_canvas(self, width: int, height: int, style: str) -> np.ndarray:
        """Create the base canvas for the composition.

        Args:
            width: Width of the canvas in pixels
            height: Height of the canvas in pixels
            style: Style variant to use

        Returns:
            Base canvas as numpy array
        """
        # Set random seed for reproducibility
        if self.config.effect_params.seed is not None:
            random.seed(self.config.effect_params.seed)
            np.random.seed(self.config.effect_params.seed)

        # Choose base generation method based on style
        if style in ["minimal", "modernist"]:
            return self._create_geometric_canvas(width, height)
        if style in ["duotone", "gothic"]:
            return self._create_noisy_canvas(width, height)
        if style in ["ethereal", "phantom"]:
            return self._create_gradient_canvas(width, height)
        if style == "symmetrical":
            return self._create_symmetrical_canvas(width, height)
        # Default to combined approach
        return self._create_combined_canvas(width, height)

    def _create_geometric_canvas(self, width: int, height: int) -> np.ndarray:
        """Create a canvas with geometric shapes."""
        # Create blank canvas
        canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

        # Get palette colors
        palette = self.engine.palette
        colors = [
            palette.primary.as_tuple,
            palette.secondary.as_tuple,
            palette.accent.as_tuple,
            palette.foreground.as_tuple,
            palette.background.as_tuple,
        ]

        for c in palette.additional.values():
            colors.append(c.as_tuple)

        # Number of shapes to draw
        num_shapes = random.randint(10, 30)

        # Draw random shapes
        for _ in range(num_shapes):
            shape_type = random.choice(["rectangle", "circle", "line"])
            color = random.choice(colors)

            if shape_type == "rectangle":
                # Draw rectangle
                x = random.randint(0, width)
                y = random.randint(0, height)
                w = random.randint(50, width // 2)
                h = random.randint(50, height // 2)

                # Ensure rectangle fits on canvas
                if x + w > width:
                    w = width - x
                if y + h > height:
                    h = height - y

                cv2.rectangle(canvas, (x, y), (x + w, y + h), color, -1)

            elif shape_type == "circle":
                # Draw circle
                x = random.randint(0, width)
                y = random.randint(0, height)
                radius = random.randint(20, min(width, height) // 4)

                cv2.circle(canvas, (x, y), radius, color, -1)

            elif shape_type == "line":
                # Draw line
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                x2 = random.randint(0, width)
                y2 = random.randint(0, height)
                thickness = random.randint(5, 50)

                cv2.line(canvas, (x1, y1), (x2, y2), color, thickness)

        return canvas

    def _create_noisy_canvas(self, width: int, height: int) -> np.ndarray:
        """Create a canvas with noise patterns."""
        # Create noise canvas
        noise = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

        # Add low frequency variation using simplex noise
        # Simulate simplex noise using blurred random noise
        low_freq = np.random.randint(
            0, 256, (height // 8, width // 8, 3), dtype=np.uint8
        )
        low_freq = cv2.resize(low_freq, (width, height))
        low_freq = cv2.GaussianBlur(low_freq, (0, 0), 50)

        # Blend high and low frequency noise
        canvas = cv2.addWeighted(noise, 0.3, low_freq, 0.7, 0)

        # Apply threshold to create more interesting patterns
        gray = cv2.cvtColor(canvas, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Create colored version using palette
        palette = self.engine.palette
        result = np.zeros((height, width, 3), dtype=np.uint8)

        # Fill with primary color where mask is 0
        result[mask == 0] = palette.primary.as_tuple

        # Fill with secondary color where mask is 255
        result[mask == 255] = palette.secondary.as_tuple

        return result

    def _create_gradient_canvas(self, width: int, height: int) -> np.ndarray:
        """Create a canvas with gradient patterns."""
        # Create gradient type
        gradient_type = random.choice(["linear", "radial", "angular"])

        # Get colors from palette
        palette = self.engine.palette
        colors = [
            palette.primary.as_normalized,
            palette.secondary.as_normalized,
            palette.accent.as_normalized,
        ]

        # Create canvas
        canvas = np.zeros((height, width, 3), dtype=np.float32)

        if gradient_type == "linear":
            # Create linear gradient
            angle = random.uniform(0, 2 * math.pi)
            dx = math.cos(angle)
            dy = math.sin(angle)

            # Create gradient mask
            y, x = np.mgrid[0:height, 0:width]
            gradient_mask = (x * dx / width + y * dy / height) % 1.0

            # Apply colors
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])

            for c in range(3):
                canvas[:, :, c] = (
                    gradient_mask * color2[c] + (1 - gradient_mask) * color1[c]
                )

        elif gradient_type == "radial":
            # Create radial gradient
            center_x = width // 2
            center_y = height // 2

            # Create distance map
            y, x = np.mgrid[0:height, 0:width]
            distances = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

            # Normalize distances
            max_dist = np.sqrt(width**2 + height**2) / 2
            gradient_mask = distances / max_dist
            gradient_mask = np.clip(gradient_mask, 0, 1)

            # Apply colors
            color1 = np.array(colors[0])
            color2 = np.array(colors[1])

            for c in range(3):
                canvas[:, :, c] = (
                    gradient_mask * color2[c] + (1 - gradient_mask) * color1[c]
                )

        elif gradient_type == "angular":
            # Create angular gradient
            center_x = width // 2
            center_y = height // 2

            # Create angle map
            y, x = np.mgrid[0:height, 0:width]
            angles = np.arctan2(y - center_y, x - center_x)

            # Normalize angles to 0-1
            gradient_mask = (angles + math.pi) / (2 * math.pi)

            # Apply colors in a circular pattern
            num_colors = len(colors)
            color_masks = [
                (gradient_mask * num_colors).astype(int) == i for i in range(num_colors)
            ]

            for i, color in enumerate(colors):
                mask = color_masks[i]
                for c in range(3):
                    canvas[:, :, c][mask] = color[c]

        # Convert to uint8
        return (canvas * 255).astype(np.uint8)

    def _create_symmetrical_canvas(self, width: int, height: int) -> np.ndarray:
        """Create a canvas with symmetrical patterns."""
        # Create base noise or gradient
        if random.random() < 0.5:
            base = self._create_noisy_canvas(width // 2, height // 2)
        else:
            base = self._create_gradient_canvas(width // 2, height // 2)

        # Determine symmetry type
        symmetry_type = random.choice(["horizontal", "vertical", "both", "radial"])

        # Create symmetrical image
        if symmetry_type == "horizontal":
            # Horizontal symmetry (top to bottom)
            top = base
            bottom = cv2.flip(top, 0)  # Flip around x-axis
            canvas = np.vstack((top, bottom))

        elif symmetry_type == "vertical":
            # Vertical symmetry (left to right)
            left = base
            right = cv2.flip(left, 1)  # Flip around y-axis
            canvas = np.hstack((left, right))

        elif symmetry_type == "both":
            # Both horizontal and vertical
            top_left = base
            top_right = cv2.flip(top_left, 1)
            top = np.hstack((top_left, top_right))
            bottom = cv2.flip(top, 0)
            canvas = np.vstack((top, bottom))

        elif symmetry_type == "radial":
            # Radial symmetry (4 quadrants)
            top_left = base
            top_right = cv2.flip(top_left, 1)
            top = np.hstack((top_left, top_right))
            bottom = cv2.flip(top, 0)
            canvas = np.vstack((top, bottom))

            # Add rotation for more variation
            center = (width // 2, height // 2)
            angle = random.uniform(0, 90)
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            canvas = cv2.warpAffine(canvas, rotation_matrix, (width, height))

        return canvas

    def _create_combined_canvas(self, width: int, height: int) -> np.ndarray:
        """Create a canvas with a combination of techniques."""
        # Choose two base techniques
        techniques = [
            self._create_geometric_canvas,
            self._create_noisy_canvas,
            self._create_gradient_canvas,
        ]

        # Select two different techniques
        technique1, technique2 = random.sample(techniques, 2)

        # Generate base canvases
        canvas1 = technique1(width, height)
        canvas2 = technique2(width, height)

        # Choose blend mode
        blend_mode = random.choice(["overlay", "screen", "multiply", "difference"])
        blend_opacity = random.uniform(0.3, 0.7)

        # Convert to float for blending
        c1 = canvas1.astype(np.float32) / 255.0
        c2 = canvas2.astype(np.float32) / 255.0

        # Apply blend
        if blend_mode == "overlay":
            mask = c1 < 0.5
            result = np.zeros_like(c1)
            result[mask] = 2 * c1[mask] * c2[mask]
            result[~mask] = 1.0 - 2 * (1.0 - c1[~mask]) * (1.0 - c2[~mask])

        elif blend_mode == "screen":
            result = 1.0 - (1.0 - c1) * (1.0 - c2)

        elif blend_mode == "multiply":
            result = c1 * c2

        elif blend_mode == "difference":
            result = np.abs(c1 - c2)

        # Convert back to uint8
        return (result * 255).astype(np.uint8)

    def _add_minimal_style(self) -> None:
        """Add minimal style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast adjustment
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.2))

        # Add subtle grain
        grain_amount = self.config.effect_params.intensity * 0.2
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add subtle vignette
        vignette_amount = 0.9 + self.config.effect_params.intensity * 0.2
        effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, vignette_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_duotone_style(self) -> None:
        """Add duotone style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast adjustment
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.4))

        # Apply duotone effect
        effects.add(duotone)

        # Add grain
        grain_amount = self.config.effect_params.intensity * 0.4
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add vignette
        vignette_amount = 0.8 + self.config.effect_params.intensity * 0.4
        effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, vignette_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_abstract_style(self) -> None:
        """Add abstract style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Apply displacement with noise
        displace_scale = self.config.effect_params.intensity * 30
        effects.add(lambda img, cfg, pal: displace(img, cfg, pal, None, displace_scale))

        # Apply pixel sorting on bright regions
        effects.add(
            lambda img, cfg, pal: pixel_sort(
                img,
                cfg,
                pal,
                threshold=0.6,
                sort_direction="both",
                reverse=random.choice([True, False]),
            )
        )

        # Apply radial blur
        blur_amount = self.config.effect_params.blur_radius * 3
        effects.add(lambda img, cfg, pal: radial_blur(img, cfg, pal, None, blur_amount))

        # Add grain
        grain_amount = self.config.effect_params.intensity * 0.5
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add vignette
        vignette_amount = 0.7 + self.config.effect_params.intensity * 0.5
        effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, vignette_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_ethereal_style(self) -> None:
        """Add ethereal style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add brightness adjustment
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 1.2))

        # Apply gaussian blur
        blur_amount = self.config.effect_params.blur_radius * 5
        effects.add(lambda img, cfg, pal: gaussian_blur(img, cfg, pal, blur_amount))

        # Apply gradient mapping with ethereal colors
        effects.add(lambda img, cfg, pal: gradient_map(img, cfg, pal))

        # Apply wave distortion
        effects.add(
            lambda img, cfg, pal: wave_distortion(
                img,
                cfg,
                pal,
                amplitude=cfg.effect_params.distortion * 10,
                frequency=0.005,
                direction="both",
            )
        )

        # Add grain
        grain_amount = self.config.effect_params.intensity * 0.3
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_modernist_style(self) -> None:
        """Add modernist style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast adjustment for bold shapes
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.8))

        # Apply threshold for strong shapes
        def modernist_threshold(img, cfg, pal):
            if random.random() < 0.7:  # 70% chance to apply threshold
                return threshold(img, cfg, pal, 0.5, False, False)
            return img

        effects.add(modernist_threshold)

        # Apply subtle grain
        grain_amount = self.config.effect_params.intensity * 0.2
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_phantom_style(self) -> None:
        """Add phantom style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Apply swirl distortion
        effects.add(
            lambda img, cfg, pal: swirl(
                img, cfg, pal, strength=cfg.effect_params.distortion * 5, radius=0.8
            )
        )

        # Apply duotone with phantom colors
        effects.add(duotone)

        # Apply gaussian blur for ethereal look
        blur_amount = self.config.effect_params.blur_radius * 2
        effects.add(lambda img, cfg, pal: gaussian_blur(img, cfg, pal, blur_amount))

        # Add grain
        grain_amount = self.config.effect_params.intensity * 0.5
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add vignette
        vignette_amount = 0.7 + self.config.effect_params.intensity * 0.5
        effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, vignette_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_gothic_style(self) -> None:
        """Add gothic style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast adjustment for dramatic look
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.6))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 0.8))

        # Apply lens distortion
        effects.add(
            lambda img, cfg, pal: lens_distortion(
                img, cfg, pal, k1=cfg.effect_params.distortion * 0.3, k2=0.1
            )
        )

        # Apply duotone with dark palette
        effects.add(duotone)

        # Add grain
        grain_amount = self.config.effect_params.intensity * 0.6
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add heavy vignette
        vignette_amount = 0.5 + self.config.effect_params.intensity * 0.5
        effects.add(
            lambda img, cfg, pal: add_vignette(
                img, cfg, pal, vignette_amount, strength=1.5
            )
        )

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_symmetrical_style(self) -> None:
        """Add symmetrical style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast adjustment
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.3))

        # Ensure symmetry is applied
        symmetry_axis = random.choice(["both", "radial"])
        effects.add(lambda img, cfg, pal: apply_symmetry(img, cfg, pal, symmetry_axis))

        # Apply gaussian blur for smoother look
        blur_amount = self.config.effect_params.blur_radius * 1.5
        effects.add(lambda img, cfg, pal: gaussian_blur(img, cfg, pal, blur_amount))

        # Add grain
        grain_amount = self.config.effect_params.intensity * 0.3
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)
