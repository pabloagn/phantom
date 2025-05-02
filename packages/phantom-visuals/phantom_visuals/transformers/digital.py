# packages/phantom-visuals/phantom_visuals/transformers/digital.py

"""
Digital artist module for Phantom Visuals.

This module provides tools for creating and manipulating digital art
with glitch aesthetics and experimental digital techniques.
"""

from typing import Optional, Dict, List, Tuple, Union, Any
from pathlib import Path
import glob
import random
import math
import numpy as np
import cv2

from phantom_visuals.core.config import Configuration
from phantom_visuals.core.engine import StyleEngine
from phantom_visuals.core.palette import ColorPalette
from phantom_visuals.effects import (
    EffectChain,
    duotone,
    adjust_contrast,
    adjust_brightness,
    adjust_saturation,
    pixelate,
    add_grain,
    add_vignette,
    gaussian_blur,
    pixel_sort,
    glitch,
    create_glitch_blocks,
    wave_distortion,
    add_halftone,
    detect_edges,
    add_noise,
    solarize,
    displace,
)


class DigitalArtist:
    """
    Specialized transformer for digital art.

    This class provides methods for creating and manipulating digital art
    with glitch aesthetics, databending techniques, and experimental
    digital approaches.
    """

    def __init__(self, config: Optional[Configuration] = None):
        """
        Initialize the digital artist.

        Args:
            config: Configuration settings to use
        """
        self.engine = StyleEngine(config)
        self.config = self.engine.config

    def transform(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        style: Optional[str] = None
    ) -> Path:
        """
        Apply digital art transformations and save the result.

        Args:
            input_path: Path to the input image
            output_path: Path where the result should be saved
            style: Style variant to apply (defaults to config.style_variant)

        Returns:
            Path where the transformed image was saved
        """
        # Use specified style or default from config
        style_variant = style or str(self.config.style_variant.value)

        # Reset any previously added transformations
        self.engine.reset_transformations()

        # Add transformations based on style variant
        if style_variant == "glitch":
            self._add_glitch_style()
        elif style_variant == "pixel":
            self._add_pixel_style()
        elif style_variant == "databend":
            self._add_databend_style()
        elif style_variant == "scan":
            self._add_scan_style()
        elif style_variant == "vaporwave":
            self._add_vaporwave_style()
        elif style_variant == "cyberpunk":
            self._add_cyberpunk_style()
        elif style_variant == "digital_decay":
            self._add_digital_decay_style()
        elif style_variant == "compression":
            self._add_compression_style()
        else:
            # Default to glitch style
            self._add_glitch_style()

        # Process the image
        return self.engine.transform(input_path, output_path)

    def batch_transform(
        self,
        input_pattern: Union[str, Path],
        output_dir: Union[str, Path],
        style: Optional[str] = None
    ) -> List[Path]:
        """
        Process multiple images with the same style.

        Args:
            input_pattern: Glob pattern for input files
            output_dir: Directory where the results should be saved
            style: Style variant to apply (defaults to config.style_variant)

        Returns:
            List of paths where the transformed images were saved
        """
        # Get list of input files
        input_files = glob.glob(str(input_pattern))

        # Process each file
        results = []
        for input_file in input_files:
            input_path = Path(input_file)
            output_path = Path(output_dir) / input_path.name
            output_path = output_path.with_suffix(f".{self.config.output_format.value}")

            try:
                result_path = self.transform(input_path, output_path, style)
                results.append(result_path)
            except Exception as e:
                print(f"Error processing {input_path}: {e}")

        return results

    def create_glitched_composition(
        self,
        width: int = 1200,
        height: int = 1600,
        output_path: Union[str, Path] = "output/digital.png",
        style: Optional[str] = None
    ) -> Path:
        """
        Create a purely digital glitch art composition without input image.

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
        if style_variant == "glitch":
            self._add_glitch_style()
        elif style_variant == "pixel":
            self._add_pixel_style()
        elif style_variant == "databend":
            self._add_databend_style()
        elif style_variant == "scan":
            self._add_scan_style()
        elif style_variant == "vaporwave":
            self._add_vaporwave_style()
        elif style_variant == "cyberpunk":
            self._add_cyberpunk_style()
        elif style_variant == "digital_decay":
            self._add_digital_decay_style()
        elif style_variant == "compression":
            self._add_compression_style()
        else:
            # Default to glitch style
            self._add_glitch_style()

        # Process the canvas
        result = self.engine.process_image(canvas)

        # Save and return the result
        return self.engine.save_image(result, output_path)

    def _create_base_canvas(self, width: int, height: int, style: str) -> np.ndarray:
        """
        Create the base canvas for the composition.

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

        # Create a base canvas based on style
        if style == "glitch" or style == "databend":
            return self._create_noise_canvas(width, height)
        elif style == "pixel":
            return self._create_pixel_canvas(width, height)
        elif style == "vaporwave":
            return self._create_gradient_canvas(width, height)
        elif style == "cyberpunk" or style == "digital_decay":
            return self._create_circuit_canvas(width, height)
        else:
            # Default to grid pattern
            return self._create_grid_canvas(width, height)

    def _create_noise_canvas(self, width: int, height: int) -> np.ndarray:
        """Create a canvas with random noise."""
        # Generate noise
        noise = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

        # Get palette colors
        palette = self.engine.palette

        # Apply color mapping to some areas
        color_mask = np.random.random((height, width)) > 0.7

        if np.any(color_mask):
            noise[color_mask] = palette.accent.as_tuple

        return noise

    def _create_pixel_canvas(self, width: int, height: int) -> np.ndarray:
        """Create a canvas with a low-resolution pixel pattern."""
        # Create small random image
        block_size = 16
        small_width = width // block_size
        small_height = height // block_size

        # Generate small random image
        small_img = np.random.randint(0, 256, (small_height, small_width, 3), dtype=np.uint8)

        # Get palette colors
        palette = self.engine.palette
        colors = [
            palette.primary.as_tuple,
            palette.secondary.as_tuple,
            palette.accent.as_tuple,
            palette.foreground.as_tuple,
            palette.background.as_tuple
        ]

        # Apply palette colors
        color_indices = np.random.randint(0, len(colors), (small_height, small_width))
        for y in range(small_height):
            for x in range(small_width):
                small_img[y, x] = colors[color_indices[y, x]]

        # Resize with nearest neighbor interpolation to maintain pixelation
        canvas = cv2.resize(small_img, (width, height), interpolation=cv2.INTER_NEAREST)

        return canvas

    def _create_gradient_canvas(self, width: int, height: int) -> np.ndarray:
        """Create a canvas with gradient patterns."""
        # Get colors from palette
        palette = self.engine.palette
        colors = [
            palette.primary.as_tuple,
            palette.secondary.as_tuple,
            palette.accent.as_tuple
        ]

        # Create gradient
        canvas = np.zeros((height, width, 3), dtype=np.uint8)

        # Create horizontal gradient
        for x in range(width):
            color_idx = int(x / width * len(colors))
            color_idx = min(color_idx, len(colors) - 1)

            # Apply gradient color
            canvas[:, x] = colors[color_idx]

        # Add some horizontal lines
        num_lines = random.randint(5, 20)
        line_color = palette.foreground.as_tuple

        for _ in range(num_lines):
            y = random.randint(0, height - 1)
            thickness = random.randint(1, 10)
            start_x = random.randint(0, width // 2)
            end_x = random.randint(width // 2, width - 1)

            canvas[y:y+thickness, start_x:end_x] = line_color

        return canvas

    def _create_circuit_canvas(self, width: int, height: int) -> np.ndarray:
        """Create a canvas with circuit-like patterns."""
        # Create a dark background
        palette = self.engine.palette
        canvas = np.ones((height, width, 3), dtype=np.uint8) * 20  # Dark background

        # Create a grid of points
        grid_size = 50
        points = []

        for y in range(0, height, grid_size):
            for x in range(0, width, grid_size):
                # Add some randomness to grid points
                jitter_x = random.randint(-15, 15)
                jitter_y = random.randint(-15, 15)

                px = x + jitter_x
                py = y + jitter_y

                if 0 <= px < width and 0 <= py < height:
                    points.append((px, py))

        # Draw lines between some random points
        num_lines = len(points) // 2
        line_color = palette.accent.as_tuple

        for _ in range(num_lines):
            p1, p2 = random.sample(points, 2)
            thickness = random.randint(1, 3)

            cv2.line(canvas, p1, p2, line_color, thickness)

        # Add some "nodes" at points
        for point in points:
            radius = random.randint(2, 8)
            node_color = random.choice([
                palette.primary.as_tuple,
                palette.secondary.as_tuple,
                palette.accent.as_tuple
            ])

            cv2.circle(canvas, point, radius, node_color, -1)

        return canvas

    def _create_grid_canvas(self, width: int, height: int) -> np.ndarray:
        """Create a canvas with grid patterns."""
        # Create a background
        palette = self.engine.palette
        canvas = np.ones((height, width, 3), dtype=np.uint8) * np.array(palette.background.as_tuple)

        # Grid parameters
        grid_spacing = random.randint(20, 100)
        line_color = palette.foreground.as_tuple
        line_thickness = random.randint(1, 3)

        # Draw horizontal lines
        for y in range(0, height, grid_spacing):
            cv2.line(canvas, (0, y), (width, y), line_color, line_thickness)

        # Draw vertical lines
        for x in range(0, width, grid_spacing):
            cv2.line(canvas, (x, 0), (x, height), line_color, line_thickness)

        # Add some blocks of color
        num_blocks = random.randint(5, 15)

        for _ in range(num_blocks):
            x = random.randint(0, width - grid_spacing)
            y = random.randint(0, height - grid_spacing)
            w = random.randint(grid_spacing, grid_spacing * 3)
            h = random.randint(grid_spacing, grid_spacing * 3)

            # Ensure block fits on canvas
            if x + w > width:
                w = width - x
            if y + h > height:
                h = height - y

            # Align to grid
            x = (x // grid_spacing) * grid_spacing
            y = (y // grid_spacing) * grid_spacing
            w = min(w, grid_spacing * 3)
            h = min(h, grid_spacing * 3)

            # Draw block
            block_color = random.choice([
                palette.primary.as_tuple,
                palette.secondary.as_tuple,
                palette.accent.as_tuple
            ])

            canvas[y:y+h, x:x+w] = block_color

        return canvas

    def _add_glitch_style(self) -> None:
        """Add digital glitch style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast adjustment
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.2))

        # Apply RGB channel shift
        effects.add(lambda img, cfg, pal: glitch(
            img, cfg, pal,
            intensity=cfg.effect_params.intensity * 1.5,
            num_channels=2,
            channel_shift_range=20
        ))

        # Apply pixel sorting
        effects.add(lambda img, cfg, pal: pixel_sort(
            img, cfg, pal,
            threshold=0.4,
            sort_direction="horizontal"
        ))

        # Add block glitches
        effects.add(lambda img, cfg, pal: create_glitch_blocks(
            img, cfg, pal,
            intensity=cfg.effect_params.intensity * 1.2,
            block_size=(20, 40),
            offset_range=20
        ))

        # Add noise
        effects.add(lambda img, cfg, pal: add_noise(
            img, cfg, pal,
            cfg.effect_params.noise_level * 0.7,
            "salt_pepper"
        ))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_pixel_style(self) -> None:
        """Add pixel art style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast and saturation adjustments
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.4))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 1.2))

        # Apply pixelation
        pixelation_size = int(self.config.effect_params.intensity * 12) + 4
        effects.add(lambda img, cfg, pal: pixelate(img, cfg, pal, pixelation_size))

        # Reduce color palette
        effects.add(lambda img, cfg, pal: posterize(img, cfg, pal, 8))

        # Add subtle noise
        noise_amount = self.config.effect_params.noise_level * 0.3
        effects.add(lambda img, cfg, pal: add_noise(img, cfg, pal, noise_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_databend_style(self) -> None:
        """Add databending style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Apply color channel shifts
        effects.add(lambda img, cfg, pal: glitch(
            img, cfg, pal,
            intensity=cfg.effect_params.intensity,
            num_channels=3,
            channel_shift_range=15
        ))

        # Apply shifting/repeating "corruption" blocks
        def apply_corruption(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Number of corruption blocks
            num_blocks = int(cfg.effect_params.intensity * 10) + 3

            for _ in range(num_blocks):
                # Random block source position
                src_x = random.randint(0, width - 50)
                src_y = random.randint(0, height - 50)

                # Random block size
                block_w = random.randint(50, min(300, width - src_x))
                block_h = random.randint(20, min(100, height - src_y))

                # Extract the block
                block = img[src_y:src_y+block_h, src_x:src_x+block_w].copy()

                # Random destination position
                dst_x = random.randint(0, width - block_w)
                dst_y = random.randint(0, height - block_h)

                # Paste block with minor stretch/compression
                stretch_w = random.randint(-10, 10)
                new_block_w = max(10, block_w + stretch_w)

                if new_block_w + dst_x > width:
                    new_block_w = width - dst_x

                if new_block_w != block_w:
                    block = cv2.resize(block, (new_block_w, block_h))

                # Apply the block
                result[dst_y:dst_y+block_h, dst_x:dst_x+new_block_w] = block

            return result

        effects.add(apply_corruption)

        # Apply pixel sorting in vertical direction
        effects.add(lambda img, cfg, pal: pixel_sort(
            img, cfg, pal,
            threshold=0.3,
            sort_direction="vertical",
            reverse=True
        ))

        # Add subtle noise
        noise_amount = self.config.effect_params.noise_level * 0.4
        effects.add(lambda img, cfg, pal: add_noise(img, cfg, pal, noise_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_scan_style(self) -> None:
        """Add scan/xerox style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Increase contrast dramatically
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.8))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 1.1))

        # Apply halftone effect
        effects.add(lambda img, cfg, pal: add_halftone(
            img, cfg, pal,
            dots_per_inch=15,
            method="circles",
            blend=0.2
        ))

        # Add scan lines
        def add_scan_lines(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            line_spacing = int(10 / cfg.effect_params.intensity)
            line_spacing = max(2, line_spacing)

            for y in range(0, height, line_spacing):
                darkness = random.uniform(0.7, 0.9)
                if img.ndim == 3:
                    result[y, :] = result[y, :] * darkness
                else:
                    result[y, :] = result[y, :] * darkness

            return result

        effects.add(add_scan_lines)

        # Add noise to simulate paper texture
        noise_amount = self.config.effect_params.noise_level * 0.6
        effects.add(lambda img, cfg, pal: add_noise(img, cfg, pal, noise_amount))

        # Add vignette to simulate scanner issues
        vignette_amount = 0.6 + self.config.effect_params.intensity * 0.4
        effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, vignette_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_vaporwave_style(self) -> None:
        """Add vaporwave aesthetic transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Adjust saturation and hue
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 1.5))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 1.1))

        # Apply color shift (pink/blue/purple)
        def vaporwave_color_shift(img, cfg, pal):
            # Convert to float for calculations
            img_float = img.astype(np.float32) / 255.0

            # Adjust color channels
            result = img_float.copy()

            # Boost red channel
            result[:, :, 0] = np.clip(result[:, :, 0] * 1.2, 0, 1)

            # Boost blue channel
            result[:, :, 2] = np.clip(result[:, :, 2] * 1.3, 0, 1)

            # Convert back to uint8
            return (result * 255).astype(np.uint8)

        effects.add(vaporwave_color_shift)

        # Apply wave distortion
        effects.add(lambda img, cfg, pal: wave_distortion(
            img, cfg, pal,
            amplitude=cfg.effect_params.distortion * 10,
            frequency=0.05,
            direction="horizontal"
        ))

        # Apply scanlines
        def add_grid_pattern(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Horizontal scanlines
            scanline_spacing = 4
            scanline_alpha = 0.1 + cfg.effect_params.intensity * 0.1

            for y in range(0, height, scanline_spacing):
                result[y, :] = result[y, :] * (1 - scanline_alpha)

            # Vertical grid lines
            grid_spacing = 20
            grid_alpha = 0.05 + cfg.effect_params.intensity * 0.05

            for x in range(0, width, grid_spacing):
                result[:, x] = result[:, x] * (1 - grid_alpha)

            return result

        effects.add(add_grid_pattern)

        # Add mild grain
        grain_amount = self.config.effect_params.intensity * 0.3
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add glow
        blur_amount = self.config.effect_params.blur_radius + 2

        def add_glow(img, cfg, pal):
            # Create a blurred copy
            blurred = gaussian_blur(img, cfg, pal, blur_amount)

            # Blend with original
            alpha = 0.2 + cfg.effect_params.intensity * 0.2
            result = cv2.addWeighted(img, 1 - alpha, blurred, alpha, 0)

            return result

        effects.add(add_glow)

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_cyberpunk_style(self) -> None:
        """Add cyberpunk style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Enhance contrast and brightness
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.5))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 1.2))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 1.3))

        # Apply edge detection with neon effect
        def neon_edges(img, cfg, pal):
            # Detect edges
            edges = detect_edges(img, cfg, pal, 0.7, "canny")

            # Create neon glow
            blur_amount = cfg.effect_params.blur_radius + 3
            glow = gaussian_blur(edges, cfg, pal, blur_amount)

            # Colorize the glow
            if glow.ndim == 3:
                # Already has channels
                pass
            else:
                # Convert to RGB
                glow = cv2.cvtColor(glow, cv2.COLOR_GRAY2RGB)

                # Apply neon coloring
                glow[:, :, 0] = glow[:, :, 0] * 0.5  # Reduce red
                glow[:, :, 2] = glow[:, :, 2] * 1.5  # Boost blue

            # Blend with original
            alpha = 0.7
            result = cv2.addWeighted(img, 1 - alpha, glow, alpha, 0)

            return result

        effects.add(neon_edges)

        # Apply glitch effects
        effects.add(lambda img, cfg, pal: glitch(
            img, cfg, pal,
            intensity=cfg.effect_params.intensity * 0.7,
            num_channels=2,
            channel_shift_range=10
        ))

        # Add noise
        noise_amount = self.config.effect_params.noise_level * 0.4
        effects.add(lambda img, cfg, pal: add_noise(img, cfg, pal, noise_amount))

        # Add vignette
        vignette_amount = 0.8 + self.config.effect_params.intensity * 0.3
        effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, vignette_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_digital_decay_style(self) -> None:
        """Add digital decay style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Adjust contrast and brightness
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.4))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 0.9))

        # Apply solarization
        effects.add(lambda img, cfg, pal: solarize(img, cfg, pal, 128))

        # Apply displacement with noise
        displace_scale = self.config.effect_params.intensity * 20
        effects.add(lambda img, cfg, pal: displace(img, cfg, pal, None, displace_scale))

        # Apply glitch blocks
        effects.add(lambda img, cfg, pal: create_glitch_blocks(
            img, cfg, pal,
            intensity=cfg.effect_params.intensity,
            block_size=(30, 10),
            offset_range=15
        ))

        # Simulate digital artifacts
        def add_artifacts(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Number of artifact regions
            num_artifacts = int(cfg.effect_params.intensity * 15) + 5

            for _ in range(num_artifacts):
                # Random artifact position
                x = random.randint(0, width - 10)
                y = random.randint(0, height - 10)

                # Random artifact size
                w = random.randint(5, min(50, width - x))
                h = random.randint(3, min(20, height - y))

                # Create artifact (repeating pattern or solid color)
                if random.random() < 0.5:
                    # Solid color
                    color = random.randint(0, 255)
                    if img.ndim == 3:
                        result[y:y+h, x:x+w] = (color, color, color)
                    else:
                        result[y:y+h, x:x+w] = color
                else:
                    # Repeating pattern - take a 1-pixel slice and repeat
                    if img.ndim == 3:
                        pattern = result[y, x:x+1].copy()
                        for i in range(h):
                            result[y+i, x:x+w] = np.tile(pattern, (1, w, 1))
                    else:
                        pattern = result[y, x:x+1].copy()
                        for i in range(h):
                            result[y+i, x:x+w] = np.tile(pattern, w)

            return result

        effects.add(add_artifacts)

        # Add noise
        noise_amount = self.config.effect_params.noise_level * 0.5
        effects.add(lambda img, cfg, pal: add_noise(img, cfg, pal, noise_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_compression_style(self) -> None:
        """Add JPEG compression artifacts style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Adjust contrast
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.2))

        # Simulate JPEG compression artifacts
        def add_compression_artifacts(img, cfg, pal):
            # Convert to BGR for OpenCV encoding
            if img.ndim == 3:
                img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            else:
                img_bgr = img.copy()

            # Calculate quality based on intensity (lower = more compression)
            quality = int(90 - cfg.effect_params.intensity * 80)
            quality = max(5, quality)

            # Encode to JPEG and decode back
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            _, enc = cv2.imencode('.jpg', img_bgr, encode_param)
            compressed = cv2.imdecode(enc, cv2.IMREAD_UNCHANGED)

            # Convert back to RGB
            if img.ndim == 3:
                compressed = cv2.cvtColor(compressed, cv2.COLOR_BGR2RGB)

            return compressed

        effects.add(add_compression_artifacts)

        # Apply more compression for extreme effect
        def add_chroma_subsampling(img, cfg, pal):
            # Only apply to color images
            if img.ndim < 3:
                return img

            # Convert to YCrCb (separates luminance from chrominance)
            ycrcb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb).astype(np.float32)

            # Downsample chrominance channels
            factor = 8
            h, w = ycrcb.shape[:2]

            # Process Cr and Cb channels (1 and 2)
            for i in range(1, 3):
                # Extract channel
                channel = ycrcb[:, :, i]

                # Downsample
                small = cv2.resize(channel, (w // factor, h // factor))

                # Upsample (introduces the blocky artifacts)
                ycrcb[:, :, i] = cv2.resize(small, (w, h))

            # Convert back to RGB
            result = cv2.cvtColor(ycrcb.astype(np.uint8), cv2.COLOR_YCrCb2RGB)

            return result

        effects.add(add_chroma_subsampling)

        # Add block-based artifacts
        def add_block_artifacts(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Block size
            block_size = 8

            # Number of blocks to modify
            num_blocks = int((height // block_size) * (width // block_size) * cfg.effect_params.intensity * 0.2)

            for _ in range(num_blocks):
                # Random block position
                block_x = random.randint(0, (width // block_size) - 1) * block_size
                block_y = random.randint(0, (height // block_size) - 1) * block_size

                # Modify block
                block = result[block_y:block_y+block_size, block_x:block_x+block_size].copy()

                # Adjust block values to create artifacts
                adjustment = random.randint(-20, 20)
                block = np.clip(block.astype(np.int16) + adjustment, 0, 255).astype(np.uint8)

                # Apply modified block
                result[block_y:block_y+block_size, block_x:block_x+block_size] = block

            return result

        effects.add(add_block_artifacts)

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)
