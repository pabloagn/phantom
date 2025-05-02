# packages/phantom-visuals/phantom_visuals/transformers/author.py

"""Author image transformation for Phantom Visuals.

This module provides specialized transformations for author portraits
to create consistent and distinctive styling across the Phantom ecosystem.
"""

import glob
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
    add_noise,
    add_vignette,
    adjust_brightness,
    adjust_contrast,
    adjust_saturation,
    apply_symmetry,
    blur_regions,
    detect_edges,
    displace,
    duotone,
    enhance_edges,
    ethereal_glow,
    ghost_trails,
    glitch,
    lens_distortion,
    pixel_sort,
    solarize,
    threshold,
    wave_distortion,
)
from phantom_visuals.effects.artistic import create_glitch_blocks


class AuthorTransformer:
    """Specialized transformer for author portraits.

    This class provides a high-level interface for applying specific
    transformations to author images to create various signature styles.
    """

    def __init__(self, config: Optional[Configuration] = None):
        """Initialize the author transformer.

        Args:
            config: Configuration settings to use
        """
        self.engine = StyleEngine(config)
        self.config = self.engine.config

    def transform(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        style: Optional[str] = None,
    ) -> Path:
        """Apply author image transformation and save the result.

        Args:
            input_path: Path to the input author image
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
        if style_variant == "minimal":
            self._add_minimal_style()
        elif style_variant == "minimal_organic":
            self._add_minimal_organic_style()
        elif style_variant == "duotone":
            self._add_duotone_style()
        elif style_variant == "abstract":
            self._add_abstract_style()
        elif style_variant == "abstract_wild":
            self._add_abstract_wild_style()
        elif style_variant == "glitch":
            self._add_glitch_style()
        elif style_variant == "glitch_refined":
            self._add_glitch_refined_style()
        elif style_variant == "ethereal":
            self._add_ethereal_style()
        elif style_variant == "ethereal_organic":
            self._add_ethereal_organic_style()
        elif style_variant == "modernist":
            self._add_modernist_style()
        elif style_variant == "modernist_organic":
            self._add_modernist_organic_style()
        elif style_variant == "phantom":
            self._add_phantom_style()
        elif style_variant == "phantom_enhanced":
            self._add_phantom_enhanced_style()
        elif style_variant == "gothic":
            self._add_gothic_style()
        elif style_variant == "gothic_distorted":
            self._add_gothic_distorted_style()
        elif style_variant == "symmetrical":
            self._add_symmetrical_style()
        elif style_variant == "contour":
            self._add_contour_style()
        elif style_variant == "wave":
            self._add_wave_style()
        # Mathematical styles
        elif style_variant == "fractal":
            self._add_fractal_style()
        elif style_variant == "fourier":
            self._add_fourier_style()
        elif style_variant == "wave_function":
            self._add_wave_function_style()
        elif style_variant == "statistical":
            self._add_statistical_style()
        # New style variations
        elif style_variant == "gothic_subtle":
            self._add_gothic_subtle_style()
        elif style_variant == "phantom_spectral":
            self._add_phantom_spectral_style()
        elif style_variant == "glitch_balanced":
            self._add_glitch_balanced_style()
        elif style_variant == "spectral_veil":
            self._add_spectral_veil_style()
        elif style_variant == "ghost_trails":
            self._add_ghost_trails_style()
        elif style_variant == "phantom_flow":
            self._add_phantom_flow_style()
        else:
            # Default to phantom style
            self._add_phantom_style()

        # Process the image
        return self.engine.transform(input_path, output_path)

    # New style methods

    def _add_gothic_subtle_style(self) -> None:
        """Add gothic style with subtle but pervasive distortion effects."""
        effects = EffectChain()

        # Base adjustment with high contrast
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.3))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 0.85))

        # Apply subtle pervasive distortion
        def subtle_wave_distortion(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Create displacement map
            displacement_x = np.zeros((height, width), dtype=np.float32)
            displacement_y = np.zeros((height, width), dtype=np.float32)

            # Create distortion with multiple frequencies
            intensity = cfg.effect_params.intensity * 0.4  # More subtle than standard

            # Add several subtle wave patterns
            for scale in [6, 12, 24]:
                for y in range(height):
                    for x in range(width):
                        # Apply subtle wave patterns with varying frequencies
                        displacement_x[y, x] += intensity * math.sin(y / scale + x / (scale * 1.5)) * 2
                        displacement_y[y, x] += intensity * math.cos(x / scale + y / (scale * 1.2)) * 2

            # Apply displacement map
            for y in range(height):
                for x in range(width):
                    # Calculate source coordinates with displacement
                    src_x = x + int(displacement_x[y, x])
                    src_y = y + int(displacement_y[y, x])

                    # Ensure we stay within bounds
                    src_x = max(0, min(width - 1, src_x))
                    src_y = max(0, min(height - 1, src_y))

                    # Copy pixel
                    result[y, x] = img[src_y, src_x]

            return result

        effects.add(subtle_wave_distortion)

        # Apply gothic color scheme with deep shadows
        def gothic_tone_mapping(img, cfg, pal):
            # Transform to darker, cooler tones
            result = img.copy().astype(np.float32)

            # Apply tone mapping
            if img.ndim == 3:
                # Apply color toning - enhance blues/purples in shadows, keep highlights
                result[:, :, 0] *= 0.8  # Reduce red
                result[:, :, 2] *= 1.2  # Enhance blue

            # Enhance darks
            result = np.power(result / 255.0, 1.2) * 255.0
            return np.clip(result, 0, 255).astype(np.uint8)

        effects.add(gothic_tone_mapping)

        # Add soft vignette
        effects.add(lambda img, cfg, pal: add_vignette(
            img, cfg, pal,
            amount=0.5,
            color=pal.primary.as_tuple
        ))

        # Add subtle grain for texture
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, 0.15))

        self.engine.add_transformation(effects)

    def _add_phantom_spectral_style(self) -> None:
        """Add enhanced phantasmagoric style with spectral qualities."""
        effects = EffectChain()

        # Base adjustments
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.1))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.7))

        # Spectral glow effect
        def enhanced_spectral_glow(img, cfg, pal):
            # Create multiple phantom layers with different blur amounts
            height, width = img.shape[:2]
            result = img.copy().astype(np.float32)

            # Start with a slightly darkened base
            result = result * 0.85

            # Calculate the glow amount based on intensity
            glow_amount = 0.3 + cfg.effect_params.intensity * 0.4

            # Create multiple spectral layers
            layers = []
            blur_amounts = [5, 15, 30]
            weights = [0.6, 0.3, 0.1]

            for blur, weight in zip(blur_amounts, weights):
                # Create a blurred, brightened layer
                blurred = cv2.GaussianBlur(img, (0, 0), blur).astype(np.float32)

                # Brighten it
                blurred = blurred * 1.5

                # Convert to glowing version by threshold
                if img.ndim == 3:
                    # Calculate luminance
                    luminance = 0.299 * blurred[:, :, 0] + 0.587 * blurred[:, :, 1] + 0.114 * blurred[:, :, 2]

                    # Create a mask for bright areas
                    mask = np.clip((luminance - 100) / 50, 0, 1)

                    # Apply the mask to each channel
                    for c in range(3):
                        # Add the glow component
                        result[:, :, c] += blurred[:, :, c] * mask * glow_amount * weight
                else:
                    # Grayscale version
                    mask = np.clip((blurred - 100) / 50, 0, 1)
                    result += blurred * mask * glow_amount * weight

            # Add a subtle color shift to blues in the shadows
            if img.ndim == 3:
                # Darker areas get a blue tint
                darkness = 1.0 - (result / 255.0)
                result[:, :, 2] += darkness[:, :, 2] * 20  # Add blue to shadows

            # Ensure valid range
            return np.clip(result, 0, 255).astype(np.uint8)

        effects.add(enhanced_spectral_glow)

        # Add spectral trails
        def spectral_trails(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Create a version with directed blur
            angle = 110  # Degree angle for the motion
            kernel_size = int(10 + cfg.effect_params.intensity * 10)

            # Create motion blur kernel
            kernel = np.zeros((kernel_size, kernel_size))

            # Add line to kernel based on angle
            center = kernel_size // 2
            radian_angle = np.deg2rad(angle)
            x_dir, y_dir = np.cos(radian_angle), np.sin(radian_angle)

            for i in range(kernel_size):
                # Calculate position along the line
                offset = i - center
                x = center + offset * x_dir
                y = center + offset * y_dir

                # Ensure we're within bounds
                if 0 <= int(y) < kernel_size and 0 <= int(x) < kernel_size:
                    kernel[int(y), int(x)] = 1

            # Normalize kernel
            kernel = kernel / np.sum(kernel)

            # Apply the motion blur
            if img.ndim == 3:
                motion_blur = np.zeros_like(img)
                for c in range(3):
                    motion_blur[:, :, c] = cv2.filter2D(img[:, :, c], -1, kernel)
            else:
                motion_blur = cv2.filter2D(img, -1, kernel)

            # Blend with original
            result = cv2.addWeighted(result, 0.7, motion_blur, 0.3, 0)

            return result

        effects.add(spectral_trails)

        # Add dual-tone effect
        effects.add(lambda img, cfg, pal: duotone(
            img, cfg, pal,
            pal.additional.get("shadow", pal.primary),
            pal.additional.get("highlight", pal.accent)
        ))

        # Add subtle vignette
        effects.add(lambda img, cfg, pal: add_vignette(
            img, cfg, pal,
            amount=0.4,
            color=pal.primary.as_tuple
        ))

        self.engine.add_transformation(effects)

    def _add_glitch_balanced_style(self) -> None:
        """Add balanced glitch effects that preserve image integrity."""
        effects = EffectChain()

        # Base adjustments
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.1))

        # Add controlled RGB shift
        def controlled_rgb_shift(img, cfg, pal):
            # Create RGB shift with more control to maintain image visibility
            height, width = img.shape[:2]
            result = img.copy()

            if img.ndim != 3:
                return result  # Only apply to color images

            # Determine shift amount based on intensity
            shift_x = int(cfg.effect_params.intensity * 7)

            # Create controllable channel shift
            # Shift red right, blue left
            if shift_x > 0:
                # Red channel shift right
                result[0:height, 0:width-shift_x, 0] = img[0:height, shift_x:width, 0]
                # Blue channel shift left
                result[0:height, shift_x:width, 2] = img[0:height, 0:width-shift_x, 2]

            return result

        effects.add(controlled_rgb_shift)

        # Add scan lines with better integration
        def integrated_scan_lines(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Number of scan lines scaled by intensity
            num_lines = int(7 + cfg.effect_params.intensity * 15)
            line_opacity = 0.7  # More subtle for better integration

            for i in range(num_lines):
                # Random position
                y_pos = random.randint(0, height - 1)

                # Random thickness and shift
                thickness = random.randint(1, 2)  # Thinner lines
                shift = random.randint(-8, 8)  # More moderate shift

                # Get line segment
                line = img[y_pos:min(y_pos+thickness, height), :].copy()

                # Create shifted version
                if shift > 0:
                    shifted_line = np.zeros_like(line)
                    shifted_line[:, shift:] = line[:, :width-shift]
                else:
                    shift = abs(shift)
                    shifted_line = np.zeros_like(line)
                    shifted_line[:, :width-shift] = line[:, shift:]

                # Blend shifted line with original line for better integration
                blended_line = cv2.addWeighted(line, 1-line_opacity, shifted_line, line_opacity, 0)

                # Place back in image
                result[y_pos:min(y_pos+thickness, height), :] = blended_line

            return result

        effects.add(integrated_scan_lines)

        # Add block glitches with more control
        def controlled_block_glitches(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Fewer, more controlled blocks
            num_blocks = int(cfg.effect_params.intensity * 10) + 3

            for _ in range(num_blocks):
                # Make smaller blocks for better image integrity
                block_w = random.randint(10, width // 10)
                block_h = random.randint(5, min(10, height // 20))

                # Random position
                x = random.randint(0, width - block_w - 1)
                y = random.randint(0, height - block_h - 1)

                # Extract block
                block = img[y:y+block_h, x:x+block_w].copy()

                # Determine offset - smaller offsets for subtlety
                offset_x = random.randint(-10, 10)

                # Ensure destination is within bounds
                dest_x = max(0, min(width - block_w, x + offset_x))

                # Apply with slight transparency for better integration
                if img.ndim == 3:
                    # Blend colors
                    for c in range(3):
                        result[y:y+block_h, dest_x:dest_x+block_w, c] = \
                            result[y:y+block_h, dest_x:dest_x+block_w, c] * 0.2 + \
                            block[:, :, c] * 0.8
                else:
                    result[y:y+block_h, dest_x:dest_x+block_w] = \
                        result[y:y+block_h, dest_x:dest_x+block_w] * 0.2 + \
                        block * 0.8

            return result

        effects.add(controlled_block_glitches)

        # Add subtle noise for texture
        effects.add(lambda img, cfg, pal: add_noise(
            img, cfg, pal,
            amount=0.03,
            noise_type="gaussian"
        ))

        self.engine.add_transformation(effects)

    def _add_spectral_veil_style(self) -> None:
        """Add ghostly veil overlaying the image with transparency."""
        effects = EffectChain()

        # Base adjustments
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.15))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.8))

        # Create spectral veil effect
        def spectral_veil_overlay(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy().astype(np.float32)

            # Create base veil layer
            veil = np.zeros_like(result)

            # Create gradient for veil
            for y in range(height):
                # Calculate gradient based on position
                v = (1 + math.sin(y / height * math.pi * 3)) / 2

                # Create undulating pattern across width
                for x in range(width):
                    h = (1 + math.sin(x / width * math.pi * 2 + y / 50)) / 2

                    # Combine for final opacity
                    opacity = v * h * (0.3 + cfg.effect_params.intensity * 0.3)

                    # Fill with color from palette
                    if img.ndim == 3:
                        veil[y, x] = np.array(pal.accent.as_normalized) * 255 * opacity
                    else:
                        veil[y, x] = 220 * opacity

            # Apply Gaussian blur to the veil for softness
            veil = cv2.GaussianBlur(veil, (0, 0), 15)

            # Blend with original image
            result = result * 0.85 + veil * 0.7

            # Add highlights in bright areas
            if img.ndim == 3:
                # Calculate brightness
                brightness = (result[:, :, 0] + result[:, :, 1] + result[:, :, 2]) / 3

                # Create a mask for brightest areas
                highlight_mask = np.clip((brightness - 180) / 40, 0, 1)

                # Add extra glow in highlight areas
                glow = np.zeros_like(result)
                glow_color = np.array(pal.additional.get("highlight", pal.accent).as_normalized) * 255

                for c in range(3):
                    glow[:, :, c] = glow_color[c]

                # Apply the glow with the highlight mask
                for c in range(3):
                    result[:, :, c] += glow[:, :, c] * highlight_mask * 0.6

            # Ensure valid range
            return np.clip(result, 0, 255).astype(np.uint8)

        effects.add(spectral_veil_overlay)

        # Add subtle double exposure effect
        def subtle_double_exposure(img, cfg, pal):
            # Create a shifted, blurred copy
            height, width = img.shape[:2]

            # Create multiple subtle shifted copies
            result = img.copy().astype(np.float32)

            # Make 2-3 ghost copies
            num_ghosts = 2 + (cfg.effect_params.intensity > 0.6)

            for i in range(num_ghosts):
                # Create a copy with progressively more blur and displacement
                blur_amount = 3 + i * 5
                shift_x = int((i + 1) * 7)
                shift_y = int((i + 1) * 4)

                # Alternate shift directions
                if i % 2 == 1:
                    shift_x = -shift_x

                # Create blurred version
                ghost = cv2.GaussianBlur(img, (0, 0), blur_amount).astype(np.float32)

                # Calculate opacity - fade out for further ghosts
                opacity = 0.3 * (1 - i / num_ghosts)

                # Apply the ghost with displacement
                for y in range(height):
                    for x in range(width):
                        # Calculate source coordinates
                        src_x = x + shift_x
                        src_y = y + shift_y

                        # Skip if out of bounds
                        if src_x < 0 or src_x >= width or src_y < 0 or src_y >= height:
                            continue

                        # Blend ghost pixel
                        result[y, x] = result[y, x] * (1 - opacity) + ghost[src_y, src_x] * opacity

            return np.clip(result, 0, 255).astype(np.uint8)

        effects.add(subtle_double_exposure)

        # Add dreamy glow
        def dreamy_glow(img, cfg, pal):
            # Create soft glow effect
            glow = cv2.GaussianBlur(img, (0, 0), 20)

            # Blend with original
            return cv2.addWeighted(img, 0.8, glow, 0.4, 0)

        effects.add(dreamy_glow)

        # Add vignette
        effects.add(lambda img, cfg, pal: add_vignette(
            img, cfg, pal,
            amount=0.4,
            color=(220, 225, 255)  # Light blue vignette
        ))

        self.engine.add_transformation(effects)

    def _add_ghost_trails_style(self) -> None:
        """Add subtle ghosting and trailing effects throughout the image."""
        effects = EffectChain()

        # Base adjustments
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.1))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 0.95))

        # Create multi-directional ghost trails
        def multi_directional_trails(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy().astype(np.float32)

            # Create trails in multiple directions
            directions = [
                (15, 0),    # Horizontal right
                (-12, 0),   # Horizontal left
                (0, 10),    # Vertical down
                (0, -8),    # Vertical up
                (7, 7),     # Diagonal down-right
                (-7, -7)    # Diagonal up-left
            ]

            # Create weighted trail layers
            weights = [0.15, 0.12, 0.1, 0.08, 0.06, 0.05]
            weights = [w * (0.7 + cfg.effect_params.intensity * 0.6) for w in weights]

            # Apply trails with increasing blur
            for i, ((dx, dy), weight) in enumerate(zip(directions, weights)):
                # Create shifted copy with blur
                blur_amount = 2 + i * 2
                shifted = np.zeros_like(result)

                # Create valid regions
                x_start = max(0, dx) if dx > 0 else 0
                y_start = max(0, dy) if dy > 0 else 0
                x_end = width if dx <= 0 else width - dx
                y_end = height if dy <= 0 else height - dy

                src_x_start = 0 if dx >= 0 else -dx
                src_y_start = 0 if dy >= 0 else -dy

                # Copy shifted region
                src_region = img[src_y_start:src_y_start+(y_end-y_start),
                               src_x_start:src_x_start+(x_end-x_start)]

                # Apply blur
                blurred = cv2.GaussianBlur(src_region, (0, 0), blur_amount).astype(np.float32)

                # Place in shifted position
                shifted[y_start:y_end, x_start:x_end] = blurred

                # Add to result with weight
                result = result * (1 - weight) + shifted * weight

            return np.clip(result, 0, 255).astype(np.uint8)

        effects.add(multi_directional_trails)

        # Add edge enhancement for definition
        def enhanced_edges(img, cfg, pal):
            # Create edge mask with Canny
            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img.copy()

            # Detect edges
            edges = cv2.Canny(gray, 50, 150)

            # Dilate edges slightly
            kernel = np.ones((2, 2), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)

            # Convert edges to float
            edges = edges.astype(np.float32) / 255.0

            # Apply to image
            result = img.copy().astype(np.float32)
            if img.ndim == 3:
                for c in range(3):
                    result[:, :, c] = result[:, :, c] * (1 + edges * 0.2)
            else:
                result = result * (1 + edges * 0.2)

            return np.clip(result, 0, 255).astype(np.uint8)

        effects.add(enhanced_edges)

        # Add subtle color toning
        def subtle_color_shift(img, cfg, pal):
            if img.ndim != 3:
                return img

            # Convert to HSV for hue adjustment
            hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float32)

            # Split channels
            h, s, v = cv2.split(hsv)

            # Apply subtle color shift to blues in shadows, warmer in highlights
            # Calculate brightness factor
            brightness = v / 255.0

            # Create shift amount that varies with brightness
            # Shadows get blue shift, highlights get warm shift
            hue_shift = np.zeros_like(brightness)
            hue_shift = np.where(brightness < 0.5,
                                 (0.5 - brightness) * 20,   # Blue shift for shadows
                                 (brightness - 0.5) * -10)   # Warm shift for highlights

            # Apply shifts
            h = np.mod(h + hue_shift, 180)

            # Slightly boost saturation in midtones
            midtone_mask = (1 - np.abs(brightness - 0.5) * 4)  # Peaks at 0.5 brightness
            midtone_mask = np.clip(midtone_mask, 0, 1)
            s = s * (1 + midtone_mask * 0.2)
            s = np.clip(s, 0, 255)

            # Merge channels
            hsv_result = cv2.merge([h, s, v])

            # Convert back to RGB
            return cv2.cvtColor(hsv_result.astype(np.uint8), cv2.COLOR_HSV2RGB)

        effects.add(subtle_color_shift)

        # Add slight vignette
        effects.add(lambda img, cfg, pal: add_vignette(
            img, cfg, pal,
            amount=0.3,
            center=None,
            strength=1.2
        ))

        self.engine.add_transformation(effects)

    def batch_transform(
        self,
        input_pattern: Union[str, Path],
        output_dir: Union[str, Path],
        style: Optional[str] = None,
    ) -> list[Path]:
        """Process multiple author images with the same style.

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

    def _create_contour_map(
        self, img: np.ndarray, levels: int = 20, blur_amount: float = 5.0
    ) -> np.ndarray:
        """Create a contour map effect similar to topographic maps.

        Args:
            img: Input image
            levels: Number of contour levels
            blur_amount: Blur amount for smoothing

        Returns:
            Contour map image
        """
        # Convert to grayscale
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img.copy()

        # Apply gaussian blur to smooth
        blurred = cv2.GaussianBlur(gray, (0, 0), blur_amount)

        # Create empty canvas
        height, width = gray.shape[:2]
        contour_map = np.zeros((height, width, 3), dtype=np.uint8)

        # Create contour lines
        step = 255 // levels
        for i in range(0, 255, step):
            # Create binary threshold at this level
            _, thresh = cv2.threshold(blurred, i, 255, cv2.THRESH_BINARY)

            # Find contours
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
            )

            # Draw contours
            cv2.drawContours(contour_map, contours, -1, (255, 255, 255), 1)

        return contour_map

    def _create_wave_lines(
        self,
        img: np.ndarray,
        frequency: float = 0.1,
        amplitude: float = 10.0,
        line_spacing: int = 8,
        direction: str = "horizontal",
    ) -> np.ndarray:
        """Create a wave line pattern over the image.

        Args:
            img: Input image
            frequency: Wave frequency
            amplitude: Wave amplitude
            line_spacing: Spacing between lines
            direction: Direction of lines (horizontal or vertical)

        Returns:
            Image with wave line pattern
        """
        height, width = img.shape[:2]
        result = np.zeros((height, width, 3), dtype=np.uint8)

        # Convert to grayscale for intensity map
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
        else:
            gray = img.astype(np.float32) / 255.0

        # Apply gaussian blur to smooth
        gray = cv2.GaussianBlur(gray, (0, 0), 5.0)

        # Create wave lines
        if direction == "horizontal":
            for y in range(0, height, line_spacing):
                points = []
                for x in range(width):
                    # Modulate amplitude by image intensity
                    local_amp = amplitude * (
                        1.0 - gray[min(y, height - 1), min(x, width - 1)]
                    )
                    wave_y = y + int(local_amp * math.sin(x * frequency))
                    if 0 <= wave_y < height:
                        points.append([x, wave_y])

                if len(points) > 1:
                    cv2.polylines(result, [np.array(points)], False, (255, 255, 255), 1)
        else:  # vertical
            for x in range(0, width, line_spacing):
                points = []
                for y in range(height):
                    # Modulate amplitude by image intensity
                    local_amp = amplitude * (
                        1.0 - gray[min(y, height - 1), min(x, width - 1)]
                    )
                    wave_x = x + int(local_amp * math.sin(y * frequency))
                    if 0 <= wave_x < width:
                        points.append([wave_x, y])

                if len(points) > 1:
                    cv2.polylines(result, [np.array(points)], False, (255, 255, 255), 1)

        return result

    def _create_moire_pattern(
        self, img: np.ndarray, pattern_scale: float = 0.5, angle: float = 30.0
    ) -> np.ndarray:
        """Create a moiré pattern effect.

        Args:
            img: Input image
            pattern_scale: Scale of the pattern
            angle: Angle of the secondary pattern in degrees

        Returns:
            Image with moiré pattern
        """
        height, width = img.shape[:2]

        # Create coordinate grid
        y_coords, x_coords = np.mgrid[0:height, 0:width]

        # Convert to grayscale for intensity map
        if img.ndim == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
        else:
            gray = img.astype(np.float32) / 255.0

        # Apply gaussian blur
        gray = cv2.GaussianBlur(gray, (0, 0), 5.0)

        # Create pattern 1 - horizontal lines
        pattern1 = np.sin(y_coords * pattern_scale * 0.1)

        # Create pattern 2 - rotated lines
        angle_rad = math.radians(angle)
        rot_y = y_coords * math.cos(angle_rad) - x_coords * math.sin(angle_rad)
        pattern2 = np.sin(rot_y * pattern_scale * 0.1)

        # Combine patterns with image intensity
        combined = (pattern1 * pattern2 * 0.5 + 0.5) * (1.0 - gray)

        # Convert to image
        result = (combined * 255).astype(np.uint8)
        if img.ndim == 3:
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)

        return result

    def _add_minimal_style(self) -> None:
        """Add minimal style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add higher contrast and sharp edges
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 2.0))
        effects.add(lambda img, cfg, pal: enhance_edges(img, cfg, pal, 1.5))

        # Add distinct grain texture for a film-like appearance
        grain_amount = 0.6 + self.config.effect_params.intensity * 0.4
        effects.add(
            lambda img, cfg, pal: add_grain(
                img, cfg, pal, amount=grain_amount, grain_size=1.0, monochrome=True
            )
        )

        # Subtle threshold effect
        effects.add(
            lambda img, cfg, pal: threshold(
                img, cfg, pal, threshold_value=0.85, adaptive=True
            )
        )

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_duotone_style(self) -> None:
        """Add duotone style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add strong contrast adjustment
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.7))

        # Convert to true duotone with refined palette
        def refined_duotone(img, cfg, pal):
            # Use more sophisticated color pairs from palette
            color1 = pal.additional.get("shadow", pal.primary)
            color2 = pal.additional.get("ethereal", pal.secondary)
            return duotone(img, cfg, pal, color1, color2)

        effects.add(refined_duotone)

        # Add elegant grain texture
        grain_amount = 0.25 + self.config.effect_params.intensity * 0.15
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_abstract_style(self) -> None:
        """Add abstract style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast and reduce saturation for more refined look
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.5))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.5))

        # Create flowing, warped displacement effect inspired by reference images
        displace_scale = self.config.effect_params.intensity * 30

        def abstract_displacement(img, cfg, pal):
            # Create a custom displacement map with flowing patterns
            height, width = img.shape[:2]
            map_y, map_x = np.mgrid[0:height, 0:width].astype(np.float32)

            # Add wave patterns to the displacement map
            freq = 0.01 + random.random() * 0.01
            map_y += displace_scale * np.sin(map_x * freq)
            map_x += displace_scale * np.cos(map_y * freq * 1.5)

            # Normalize the maps to [0,1] range
            map_y = cv2.normalize(map_y, None, 0, 1, cv2.NORM_MINMAX)
            map_x = cv2.normalize(map_x, None, 0, 1, cv2.NORM_MINMAX)

            # Create a combined displacement map
            displacement_map = np.stack([map_x, map_y], axis=2)

            # Apply displacement
            return displace(img, cfg, pal, displacement_map, displace_scale)

        effects.add(abstract_displacement)

        # Add solarization effect
        threshold_val = random.randint(100, 150)
        effects.add(lambda img, cfg, pal: solarize(img, cfg, pal, threshold_val))

        # Apply pixel sorting for flowing lines
        effects.add(
            lambda img, cfg, pal: pixel_sort(
                img, cfg, pal, threshold=0.6, sort_direction="both"
            )
        )

        # Add subtle grain
        grain_amount = 0.2 + self.config.effect_params.intensity * 0.1
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_glitch_style(self) -> None:
        """Add glitch style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast adjustment
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.4))

        # RGB channel shift with monochromatic palette
        effects.add(
            lambda img, cfg, pal: glitch(
                img,
                cfg,
                pal,
                intensity=cfg.effect_params.intensity * 1.5,
                num_channels=1,  # More refined with single channel shifts
                channel_shift_range=25,
            )
        )

        # Create data-moshing like effect with pixel sorting
        effects.add(
            lambda img, cfg, pal: pixel_sort(
                img, cfg, pal, threshold=0.3, sort_direction="horizontal"
            )
        )

        # Create random scan lines
        def scan_lines(img, cfg, pal):
            result = img.copy()
            height, width = img.shape[:2]

            # Number of lines based on intensity
            num_lines = int(15 + cfg.effect_params.intensity * 15)

            for _ in range(num_lines):
                # Random position and thickness
                y = random.randint(0, height - 1)
                thickness = random.randint(1, 3)

                # Random shift
                shift = random.randint(-30, 30)

                # Apply horizontal shift to the line
                if 0 <= y < height and thickness > 0:
                    line = result[y : min(y + thickness, height), :].copy()

                    # Shift the line
                    if shift > 0:
                        result[y : min(y + thickness, height), shift:] = line[
                            :, : width - shift
                        ]
                        result[y : min(y + thickness, height), :shift] = line[
                            :, -shift:
                        ]
                    elif shift < 0:
                        shift = abs(shift)
                        result[y : min(y + thickness, height), : width - shift] = line[
                            :, shift:
                        ]
                        result[y : min(y + thickness, height), width - shift :] = line[
                            :, :shift
                        ]

            return result

        effects.add(scan_lines)

        # Add block glitches with more refined appearance
        effects.add(
            lambda img, cfg, pal: create_glitch_blocks(
                img,
                cfg,
                pal,
                intensity=cfg.effect_params.intensity,
                block_size=(5, 40),  # More refined rectangular blocks
                offset_range=20,
                num_blocks=int(cfg.effect_params.intensity * 40),
            )
        )

        # Add digital noise instead of grain
        noise_amount = 0.15 + self.config.effect_params.intensity * 0.2
        effects.add(lambda img, cfg, pal: add_noise(img, cfg, pal, noise_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_ethereal_style(self) -> None:
        """Add ethereal style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add dreamlike contrast and brightness
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.2))
        effects.add(
            lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 0.9)
        )  # Slightly darker

        # Create ghostly double exposure effect
        def ghost_double_exposure(img, cfg, pal):
            # Create a blurred copy of the image
            blurred = cv2.GaussianBlur(img, (0, 0), 15.0)

            # Shift the blurred copy
            height, width = img.shape[:2]
            M = np.float32([[1, 0, 20], [0, 1, 10]])
            shifted = cv2.warpAffine(blurred, M, (width, height))

            # Blend the original and shifted image
            alpha = 0.7
            return cv2.addWeighted(img, alpha, shifted, 1 - alpha, 0)

        effects.add(ghost_double_exposure)

        # Apply extreme ghost trails effect
        effects.add(
            lambda img, cfg, pal: ghost_trails(
                img,
                cfg,
                pal,
                intensity=cfg.effect_params.intensity * 2.0,
                direction=random.uniform(20, 160),
                length=50,
            )
        )

        # Add ethereal glow with higher intensity
        effects.add(
            lambda img, cfg, pal: ethereal_glow(
                img,
                cfg,
                pal,
                intensity=cfg.effect_params.intensity * 2.0,
                radius=cfg.effect_params.blur_radius * 4,
                highlight_boost=2.0,
            )
        )

        # Add solarization for surreal effect
        threshold_val = random.randint(50, 150)
        effects.add(lambda img, cfg, pal: solarize(img, cfg, pal, threshold_val))

        # Create soft shadow edges
        def shadow_edges(img, cfg, pal):
            # Create edge mask
            edges = detect_edges(img, cfg, pal, 0.7, "canny")

            # Blur the edges
            blurred_edges = cv2.GaussianBlur(edges, (0, 0), 5.0)

            # Blend with original
            return cv2.addWeighted(img, 0.7, blurred_edges, 0.3, 0)

        effects.add(shadow_edges)

        # Add subtle grain
        grain_amount = 0.2
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_modernist_style(self) -> None:
        """Add modernist style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add high contrast and low saturation for brutalist look
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 2.0))
        effects.add(
            lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.1)
        )  # Almost monochrome

        # Create grid/mesh pattern effect inspired by reference images
        def grid_overlay(img, cfg, pal):
            # Create a copy of the original image
            result = img.copy()
            height, width = img.shape[:2]

            # Create empty canvas for the grid
            grid = np.zeros((height, width, 3), dtype=np.uint8)

            # Determine grid spacing based on image size
            grid_spacing = max(10, int(min(width, height) * 0.02))

            # Draw grid lines
            for x in range(0, width, grid_spacing):
                cv2.line(grid, (x, 0), (x, height), (255, 255, 255), 1)

            for y in range(0, height, grid_spacing):
                cv2.line(grid, (0, y), (width, y), (255, 255, 255), 1)

            # Apply displacement to the grid based on image intensity
            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img.copy()

            # Normalize and invert the grayscale image
            gray = 255 - cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

            # Create displacement maps
            map_x = np.zeros((height, width), dtype=np.float32)
            map_y = np.zeros((height, width), dtype=np.float32)

            # Calculate displacement values
            displacement_scale = cfg.effect_params.intensity * 10.0
            for y in range(height):
                for x in range(width):
                    map_x[y, x] = x + displacement_scale * (gray[y, x] / 255.0 - 0.5)
                    map_y[y, x] = y + displacement_scale * (gray[y, x] / 255.0 - 0.5)

            # Apply displacement to grid
            distorted_grid = cv2.remap(grid, map_x, map_y, cv2.INTER_LINEAR)

            # Blend with original image
            alpha = 0.7
            return cv2.addWeighted(result, alpha, distorted_grid, 1 - alpha, 0)

        effects.add(grid_overlay)

        # Apply threshold effect with high value
        effects.add(
            lambda img, cfg, pal: threshold(
                img, cfg, pal, threshold_value=0.7, adaptive=True
            )
        )

        # Add subtle grain
        grain_amount = 0.15
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_phantom_style(self) -> None:
        """Add phantom style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast and reduce saturation
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.7))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.3))

        # Apply selective blur with increased intensity
        effects.add(
            lambda img, cfg, pal: blur_regions(
                img,
                cfg,
                pal,
                threshold=0.6,
                blur_amount=cfg.effect_params.blur_radius * 4,
                invert=True,
            )
        )

        # Create spectral glow effect
        def spectral_glow(img, cfg, pal):
            # Create a blurred, inverted copy
            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img.copy()

            # Invert and blur
            inverted = 255 - gray
            blurred = cv2.GaussianBlur(inverted, (0, 0), 15.0)

            # Normalize and create a 3-channel version if needed
            glowing = cv2.normalize(blurred, None, 0, 255, cv2.NORM_MINMAX)
            if img.ndim == 3:
                glowing = cv2.cvtColor(glowing, cv2.COLOR_GRAY2RGB)

            # Blend with original using screen blend mode
            img_f = img.astype(np.float32) / 255.0
            glow_f = glowing.astype(np.float32) / 255.0

            # Screen blend formula: 1 - (1-a)*(1-b)
            result = 1.0 - (1.0 - img_f) * (1.0 - glow_f * 0.7)
            result = np.clip(result, 0.0, 1.0)

            return (result * 255.0).astype(np.uint8)

        effects.add(spectral_glow)

        # Apply duotone with a blend
        def duotone_blend(img, cfg, pal):
            duotoned = duotone(img, cfg, pal)
            # Blend original and duotone
            return cv2.addWeighted(img, 0.3, duotoned, 0.7, 0)

        effects.add(duotone_blend)

        # Add ethereal glow
        effects.add(
            lambda img, cfg, pal: ethereal_glow(
                img,
                cfg,
                pal,
                intensity=cfg.effect_params.intensity * 1.5,
                radius=cfg.effect_params.blur_radius * 3,
            )
        )

        # Add grain
        grain_amount = self.config.effect_params.intensity * 0.4
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_gothic_style(self) -> None:
        """Add gothic style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add dramatic contrast and darken the image
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 2.0))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 0.7))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.2))

        # Apply duotone with dark palette
        effects.add(duotone)

        # Apply lens distortion
        effects.add(
            lambda img, cfg, pal: lens_distortion(
                img, cfg, pal, k1=cfg.effect_params.distortion * 0.3, k2=0.1
            )
        )

        # Create dark, dramatic edges
        def gothic_edges(img, cfg, pal):
            # Detect edges
            edges = detect_edges(img, cfg, pal, 0.9, "canny")

            # Ensure edges is grayscale (single channel)
            if len(edges.shape) == 3 and edges.shape[2] == 3:
                edges_gray = cv2.cvtColor(edges, cv2.COLOR_RGB2GRAY)
            else:
                edges_gray = edges

            # Create inverted mask (single channel)
            inverted = 255 - edges_gray

            # Apply to original
            if img.ndim == 3:
                result = img.copy()
                for c in range(3):
                    result[:, :, c] = cv2.multiply(
                        result[:, :, c], inverted, scale=1 / 255.0
                    )
            else:
                result = cv2.multiply(img, inverted, scale=1 / 255.0)

            return result

        effects.add(gothic_edges)

        # Add grain
        grain_amount = self.config.effect_params.intensity * 0.6
        effects.add(
            lambda img, cfg, pal: add_grain(
                img, cfg, pal, grain_amount, monochrome=True
            )
        )

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_symmetrical_style(self) -> None:
        """Add symmetrical style transformations to the engine."""
        # Create an effect chain
        effects = EffectChain()

        # Add refined contrast adjustment
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.5))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.5))

        # Create more refined symmetry by blending with original
        def refined_symmetry(img, cfg, pal):
            # Create symmetrical version
            symmetry_axis = random.choice(["vertical", "horizontal", "both"])
            symmetric = apply_symmetry(img, cfg, pal, symmetry_axis)

            # Blend with original to preserve some natural features
            alpha = 0.7  # More weight on symmetrical version
            result = cv2.addWeighted(img, 1 - alpha, symmetric, alpha, 0)

            return result

        effects.add(refined_symmetry)

        # Apply wave distortion for a more organic look
        effects.add(
            lambda img, cfg, pal: wave_distortion(
                img,
                cfg,
                pal,
                amplitude=cfg.effect_params.distortion * 3,
                frequency=0.01,
                direction="both",
            )
        )

        # Apply moiré pattern effect
        def apply_moire(img, cfg, pal):
            # Create moiré pattern
            moire = self._create_moire_pattern(img, 0.7, 30.0)

            # Blend with original
            alpha = 0.5
            return cv2.addWeighted(img, alpha, moire, 1 - alpha, 0)

        effects.add(apply_moire)

        # Add subtle grain
        grain_amount = 0.2
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_contour_style(self) -> None:
        """Add contour style transformations inspired by topographic maps."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast adjustment for better contour definition
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.5))

        # Create contour map effect
        def apply_contour(img, cfg, pal):
            # Generate contour map
            contour_levels = int(15 + cfg.effect_params.intensity * 20)

            # Convert to grayscale
            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img.copy()

            # Apply gaussian blur to smooth
            blurred = cv2.GaussianBlur(gray, (0, 0), 5.0)

            # Create empty canvas
            height, width = gray.shape[:2]
            contour_map = np.zeros((height, width, 3), dtype=np.uint8)

            # Create contour lines
            step = 255 // contour_levels
            for i in range(0, 255, step):
                # Create binary threshold at this level
                _, thresh = cv2.threshold(blurred, i, 255, cv2.THRESH_BINARY)

                # Find contours
                contours, _ = cv2.findContours(
                    thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
                )

                # Draw contours
                cv2.drawContours(contour_map, contours, -1, (255, 255, 255), 1)

            # Use a solid background color from palette
            if img.ndim == 3:
                background = np.zeros((height, width, 3), dtype=np.uint8)
                background[:, :] = [pal.additional.get("shadow", (20, 30, 50))]
            else:
                background = np.zeros_like(img)

            # Combine background with contour lines
            return cv2.add(background, contour_map)

        effects.add(apply_contour)

        # Add subtle grain
        grain_amount = 0.1
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_wave_style(self) -> None:
        """Add wave line style transformations."""
        # Create an effect chain
        effects = EffectChain()

        # Add contrast adjustment
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.7))
        effects.add(
            lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.1)
        )  # Almost monochrome

        # Create wave line effect
        def apply_wave_lines(img, cfg, pal):
            # Generate wave lines
            frequency = 0.05 + random.random() * 0.05
            amplitude = 10.0 + cfg.effect_params.intensity * 20.0
            line_spacing = max(3, int(8 - cfg.effect_params.intensity * 4))

            # Choose direction randomly
            direction = random.choice(["horizontal", "vertical"])

            # Create wave pattern
            height, width = img.shape[:2]
            result = np.zeros((height, width, 3), dtype=np.uint8)

            # Convert to grayscale for intensity map
            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
            else:
                gray = img.astype(np.float32) / 255.0

            # Apply gaussian blur to smooth
            gray = cv2.GaussianBlur(gray, (0, 0), 5.0)

            # Create wave lines
            if direction == "horizontal":
                for y in range(0, height, line_spacing):
                    points = []
                    for x in range(width):
                        # Modulate amplitude by image intensity
                        local_amp = amplitude * (
                            1.0 - gray[min(y, height - 1), min(x, width - 1)]
                        )
                        wave_y = y + int(local_amp * math.sin(x * frequency))
                        if 0 <= wave_y < height:
                            points.append([x, wave_y])

                    if len(points) > 1:
                        cv2.polylines(result, [np.array(points)], False, (255, 255, 255), 1)
            else:  # vertical
                for x in range(0, width, line_spacing):
                    points = []
                    for y in range(height):
                        # Modulate amplitude by image intensity
                        local_amp = amplitude * (
                            1.0 - gray[min(y, height - 1), min(x, width - 1)]
                        )
                        wave_x = x + int(local_amp * math.sin(y * frequency))
                        if 0 <= wave_x < width:
                            points.append([wave_x, y])

                    if len(points) > 1:
                        cv2.polylines(result, [np.array(points)], False, (255, 255, 255), 1)

            # Use a solid background color from palette
            if img.ndim == 3:
                background = np.zeros((height, width, 3), dtype=np.uint8)
                background[:, :] = [pal.additional.get("shadow", (15, 30, 60))]
            else:
                background = np.zeros_like(img)

            # Combine background with wave lines
            return cv2.add(background, result)

        effects.add(apply_wave_lines)

        # Add subtle grain
        grain_amount = 0.15
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_minimal_organic_style(self) -> None:
        """Add redesigned minimal style with more organic textures."""
        # Create an effect chain
        effects = EffectChain()

        # Add refined contrast for cleaner look
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.8))

        # Add fine-grained texture rather than pixelation
        effects.add(
            lambda img, cfg, pal: add_grain(
                img, cfg, pal,
                amount=0.4,
                grain_size=0.5,  # Finer grain for more subtle texture
                monochrome=True
            )
        )

        # Add subtle edge enhancement for structure
        effects.add(lambda img, cfg, pal: enhance_edges(img, cfg, pal, 0.7))

        # Add slight tonal shift for warmth
        def apply_tonal_shift(img, cfg, pal):
            # Create a very subtle warm overlay
            overlay = np.ones_like(img) * np.array([5, 2, 0], dtype=np.uint8)
            return cv2.addWeighted(img, 0.97, overlay, 0.03, 0)

        effects.add(apply_tonal_shift)

        # Apply subtle solarization for artistic quality
        threshold_val = 220  # High threshold for subtle effect
        effects.add(lambda img, cfg, pal: solarize(img, cfg, pal, threshold_val))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_abstract_wild_style(self) -> None:
        """Add wild abstract style with more dramatic distortions."""
        # Create an effect chain
        effects = EffectChain()

        # Add higher contrast for more defined shapes
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 2.0))

        # Add dramatic solarization
        threshold_val = random.randint(70, 140)
        effects.add(lambda img, cfg, pal: solarize(img, cfg, pal, threshold_val))

        # Create flowing, chaotic displacement effect
        def chaotic_displacement(img, cfg, pal):
            height, width = img.shape[:2]

            # Create multiple displacement layers for complexity
            map_y, map_x = np.mgrid[0:height, 0:width].astype(np.float32)

            # Use multiple overlapping sine waves with varied frequencies
            displace_scale = cfg.effect_params.intensity * 50  # More extreme

            # Add multiple wave patterns
            for i in range(3):
                freq_x = 0.005 + random.random() * 0.02
                freq_y = 0.005 + random.random() * 0.02
                phase_x = random.random() * math.pi * 2
                phase_y = random.random() * math.pi * 2

                map_y += displace_scale * np.sin(map_x * freq_x + phase_x)
                map_x += displace_scale * np.cos(map_y * freq_y + phase_y)

            # Create a spiral distortion in a random location
            center_x = int(width * random.uniform(0.3, 0.7))
            center_y = int(height * random.uniform(0.3, 0.7))

            # Calculate distance from center for each pixel
            y_grid, x_grid = np.mgrid[0:height, 0:width]
            d_x = x_grid - center_x
            d_y = y_grid - center_y
            radius = np.sqrt(d_x**2 + d_y**2)
            angle = np.arctan2(d_y, d_x) + radius * 0.01

            # Apply spiral distortion
            spiral_strength = random.uniform(0.2, 0.5) * displace_scale
            map_x += spiral_strength * np.cos(angle) * np.exp(-radius/(width*0.3))
            map_y += spiral_strength * np.sin(angle) * np.exp(-radius/(height*0.3))

            # Normalize the maps to valid image coordinates
            map_x = np.clip(map_x, 0, width - 1)
            map_y = np.clip(map_y, 0, height - 1)

            # Remap the image
            return cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

        effects.add(chaotic_displacement)

        # Apply extreme pixel sorting with varied thresholds
        effects.add(
            lambda img, cfg, pal: pixel_sort(
                img, cfg, pal,
                threshold=random.uniform(0.3, 0.7),
                sort_direction=random.choice(["horizontal", "vertical", "both"])
            )
        )

        # Add color shift for intensity
        def wild_color_shift(img, cfg, pal):
            # Convert to HSV for hue manipulation
            if img.ndim == 3:
                hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype(np.float32)

                # Create dramatic hue shifts in specific areas
                h, w = hsv.shape[:2]
                center_y, center_x = h // 2, w // 2

                # Create a gradient mask from center
                y_grid, x_grid = np.mgrid[0:h, 0:w]
                dist = np.sqrt((y_grid - center_y)**2 + (x_grid - center_x)**2)
                mask = np.clip(dist / (h/2), 0, 1.0)

                # Apply varied hue shift based on mask
                shift_amount = random.uniform(20, 60)
                hsv[:,:,0] = (hsv[:,:,0] + shift_amount * mask) % 180

                # Convert back to RGB
                return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
            return img

        effects.add(wild_color_shift)

        # Add grain for texture
        grain_amount = 0.3
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_glitch_refined_style(self) -> None:
        """Add refined glitch style with more sophisticated color palette."""
        # Create an effect chain
        effects = EffectChain()

        # Apply contrast adjustment but preserve tonality
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.3))

        # Replace harsh RGB channel shift with more refined monochromatic shift
        def refined_channel_shift(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Get colors from palette for shifts
            shift_colors = [
                pal.primary.as_tuple,
                pal.secondary.as_tuple,
                pal.accent.as_tuple
            ]
            if 'highlight' in pal.additional:
                shift_colors.append(pal.additional['highlight'].as_tuple)
            if 'mist' in pal.additional:
                shift_colors.append(pal.additional['mist'].as_tuple)

            # Number of shifts based on intensity
            num_shifts = int(10 + cfg.effect_params.intensity * 20)

            for _ in range(num_shifts):
                # Select a random rectangular region
                region_w = random.randint(width // 20, width // 5)
                region_h = random.randint(height // 20, height // 5)
                x = random.randint(0, width - region_w)
                y = random.randint(0, height - region_h)

                # Random shift distance (more subtle than before)
                shift_x = random.randint(-10, 10)
                shift_y = random.randint(-10, 10)

                # Calculate target position
                target_x = max(0, min(width - region_w, x + shift_x))
                target_y = max(0, min(height - region_h, y + shift_y))

                # Extract region
                region = img[y:y+region_h, x:x+region_w].copy()

                # Apply subtle color tint from palette
                color = random.choice(shift_colors)
                color_overlay = np.ones_like(region) * np.array(color, dtype=np.uint8)
                tinted_region = cv2.addWeighted(region, 0.85, color_overlay, 0.15, 0)

                # Apply to result with slight transparency
                result[target_y:target_y+region_h, target_x:target_x+region_w] = tinted_region

            return result

        effects.add(refined_channel_shift)

        # Add more refined block glitches with better color handling
        effects.add(
            lambda img, cfg, pal: create_glitch_blocks(
                img,
                cfg,
                pal,
                intensity=cfg.effect_params.intensity * 0.7,  # More subtle
                block_size=(3, 15),  # Smaller blocks
                offset_range=8,
                num_blocks=int(cfg.effect_params.intensity * 20),
            )
        )

        # Add scan lines with sophisticated color handling
        def refined_scan_lines(img, cfg, pal):
            result = img.copy()
            height, width = img.shape[:2]

            # Use elegant color palette
            line_color = pal.additional.get('shadow', (10, 10, 15))
            line_alpha = 0.7  # Transparency

            # Number of lines based on intensity
            num_lines = int(10 + cfg.effect_params.intensity * 15)
            line_width = random.randint(1, 2)

            for _ in range(num_lines):
                # Random position
                y = random.randint(0, height - line_width)

                # Create a colored line with transparency
                if img.ndim == 3:
                    for c in range(3):
                        result[y:y+line_width, :, c] = (
                            result[y:y+line_width, :, c] * (1-line_alpha) +
                            line_color[c] * line_alpha
                        ).astype(np.uint8)

            return result

        effects.add(refined_scan_lines)

        # Add film-like grain instead of digital noise
        grain_amount = 0.25
        effects.add(lambda img, cfg, pal: add_grain(
            img, cfg, pal,
            amount=grain_amount,
            grain_size=0.7,  # More film-like
            monochrome=True
        ))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_ethereal_organic_style(self) -> None:
        """Add organic ethereal style with more natural, wild elements."""
        # Create an effect chain
        effects = EffectChain()

        # Add soft contrast and slightly reduce brightness for dreaminess
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.1))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 0.85))

        # Apply organic displacement using fluid patterns
        def fluid_displacement(img, cfg, pal):
            height, width = img.shape[:2]

            # Create displacement maps with natural flow patterns
            map_y, map_x = np.mgrid[0:height, 0:width].astype(np.float32)

            # Apply perlin-like noise by combining multiple sine waves
            displace_scale = cfg.effect_params.intensity * 20

            # Use multiple overlapping sine waves with varied frequencies
            for i in range(4):  # More layers for complexity
                freq_x = 0.001 + random.random() * 0.005  # Lower frequencies for smoother flows
                freq_y = 0.001 + random.random() * 0.005
                phase_x = random.random() * math.pi * 2
                phase_y = random.random() * math.pi * 2

                # Create flowing, organic patterns
                flow_x = np.sin(map_y * freq_x + phase_x) * np.cos(map_x * freq_y * 0.5)
                flow_y = np.cos(map_x * freq_y + phase_y) * np.sin(map_y * freq_x * 0.5)

                map_x += displace_scale * flow_x
                map_y += displace_scale * flow_y

            # Normalize maps to valid coordinates
            map_x = np.clip(map_x, 0, width - 1)
            map_y = np.clip(map_y, 0, height - 1)

            # Apply with soft border handling
            return cv2.remap(img, map_x, map_y, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        effects.add(fluid_displacement)

        # Add ghostly double exposure with organic movement
        def organic_double_exposure(img, cfg, pal):
            # Create multiple subtle copies with varied blur amounts
            result = img.copy().astype(np.float32)
            overlay_count = 3

            for i in range(overlay_count):
                # Create a blurred copy with varied blur amounts
                blur_amount = 5.0 + i * 10.0
                blurred = cv2.GaussianBlur(img, (0, 0), blur_amount)

                # Apply organic shift
                height, width = img.shape[:2]

                # Calculate natural-looking shift amounts
                angle = random.uniform(0, math.pi * 2)
                distance = random.uniform(5, 20)
                dx = int(math.cos(angle) * distance)
                dy = int(math.sin(angle) * distance)

                # Create transformation matrix
                M = np.float32([[1, 0, dx], [0, 1, dy]])
                shifted = cv2.warpAffine(blurred, M, (width, height), borderMode=cv2.BORDER_REPLICATE)

                # Blend with decreasing opacity
                alpha = 0.3 / (i + 1)
                result = cv2.addWeighted(result, 1.0, shifted.astype(np.float32), alpha, 0)

            # Add subtle color toning
            if img.ndim == 3:
                # Slightly tint shadows with cool colors and highlights with warm colors
                # for a more natural, organic look
                hls = cv2.cvtColor(result.astype(np.uint8), cv2.COLOR_RGB2HLS)
                h, l, s = cv2.split(hls)

                # Adjust hue slightly based on luminance
                h = h.astype(np.float32)
                l = l.astype(np.float32) / 255.0

                # Shift dark areas toward blue, light areas toward amber
                h_shift = (l - 0.5) * 10
                h = np.mod(h + h_shift, 180).astype(np.uint8)

                # Recombine
                hls = cv2.merge([h, l.astype(np.uint8) * 255, s])
                result = cv2.cvtColor(hls, cv2.COLOR_HLS2RGB)

            return result.astype(np.uint8)

        effects.add(organic_double_exposure)

        # Add ethereal glow with natural color modulation
        def natural_glow(img, cfg, pal):
            # Start with standard ethereal glow
            glowing = ethereal_glow(
                img,
                cfg,
                pal,
                intensity=cfg.effect_params.intensity * 1.5,
                radius=cfg.effect_params.blur_radius * 4,
                highlight_boost=1.7
            )

            # Add additional nature-inspired color modulation
            if img.ndim == 3:
                hsv = cv2.cvtColor(glowing, cv2.COLOR_RGB2HSV).astype(np.float32)

                # Create a soft gradient based on image structure
                h, w = hsv.shape[:2]
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                blurred = cv2.GaussianBlur(gray, (0, 0), 30.0)

                # Normalize blurred image to create a smooth mask
                mask = blurred.astype(np.float32) / 255.0

                # Shift saturation based on mask
                s_factor = np.clip(mask * 1.3, 0.7, 1.3)
                hsv[:,:,1] = np.clip(hsv[:,:,1] * s_factor, 0, 255)

                # Convert back to RGB
                return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

            return glowing

        effects.add(natural_glow)

        # Add organic texture with film grain
        grain_amount = 0.2
        effects.add(lambda img, cfg, pal: add_grain(
            img, cfg, pal,
            amount=grain_amount,
            grain_size=0.8  # Larger grain for more natural look
        ))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_modernist_organic_style(self) -> None:
        """Add organic modernist style with more natural grid patterns."""
        # Create an effect chain
        effects = EffectChain()

        # Add strong contrast for graphic look but reduce saturation
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.8))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.2))

        # Create organic grid pattern with natural variations
        def organic_grid(img, cfg, pal):
            # Create a copy of the original image
            result = img.copy()
            height, width = img.shape[:2]

            # Create empty canvas for the grid
            grid = np.zeros((height, width, 3), dtype=np.uint8)

            # Set random seed for reproducibility but with variations
            seed = cfg.effect_params.seed if cfg.effect_params.seed is not None else random.randint(0, 10000)
            random.seed(seed)

            # Create curved, organic grid lines
            # Instead of straight lines, create curved paths
            line_count = int(10 + random.random() * 15)
            line_color = (255, 255, 255)

            # Generate horizontal flowing lines
            for i in range(line_count):
                # Create a flowing curve
                points = []
                y_base = int(height * i / line_count)

                # Amplitude of the curve
                amplitude = random.uniform(5, 15)
                # Frequency of the curve
                frequency = random.uniform(0.005, 0.015)
                # Phase shift
                phase = random.uniform(0, math.pi * 2)

                for x in range(0, width, 2):
                    # Calculate y-position with sine wave
                    y = y_base + int(amplitude * math.sin(x * frequency + phase))
                    if 0 <= y < height:
                        points.append([x, y])

                # Draw the curve
                if len(points) > 1:
                    cv2.polylines(grid, [np.array(points)], False, line_color, 1)

            # Generate vertical flowing lines with different parameters
            for i in range(line_count):
                points = []
                x_base = int(width * i / line_count)

                # Different parameters for variety
                amplitude = random.uniform(5, 15)
                frequency = random.uniform(0.005, 0.015)
                phase = random.uniform(0, math.pi * 2)

                for y in range(0, height, 2):
                    x = x_base + int(amplitude * math.sin(y * frequency + phase))
                    if 0 <= x < width:
                        points.append([x, y])

                if len(points) > 1:
                    cv2.polylines(grid, [np.array(points)], False, line_color, 1)

            # Apply mask to grid based on image intensity
            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img.copy()

            # Normalize and adjust contrast of the mask
            mask = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
            _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

            # Blur the mask for softer transitions
            mask = cv2.GaussianBlur(mask, (0, 0), 3.0)

            # Use mask to apply grid to original
            alpha = 0.7
            if img.ndim == 3:
                for c in range(3):
                    grid_c = grid[:,:,c].astype(np.float32) / 255.0
                    img_c = result[:,:,c].astype(np.float32) / 255.0
                    mask_f = mask.astype(np.float32) / 255.0

                    # Apply grid with mask
                    result[:,:,c] = ((1-alpha) * img_c + alpha * grid_c * mask_f) * 255

            return result.astype(np.uint8)

        effects.add(organic_grid)

        # Apply slight edge enhancement for structure
        effects.add(lambda img, cfg, pal: enhance_edges(img, cfg, pal, 1.2))

        # Add film-like grain for texture
        grain_amount = 0.15
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_phantom_enhanced_style(self) -> None:
        """Add enhanced phantom style with more dramatic effects while remaining elegant."""
        # Create an effect chain
        effects = EffectChain()

        # Add increased contrast and reduced saturation
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 2.0))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.25))

        # Apply selective blur with increased intensity
        effects.add(
            lambda img, cfg, pal: blur_regions(
                img,
                cfg,
                pal,
                threshold=0.65,
                blur_amount=cfg.effect_params.blur_radius * 5,
                invert=True,
            )
        )

        # Create dramatic light and shadow effect
        def dramatic_lighting(img, cfg, pal):
            # Create a radial gradient mask
            height, width = img.shape[:2]

            # Randomize center position
            center_x = int(width * random.uniform(0.3, 0.7))
            center_y = int(height * random.uniform(0.3, 0.7))

            # Calculate distance from center for each pixel
            y_grid, x_grid = np.mgrid[0:height, 0:width]
            d_x = x_grid - center_x
            d_y = y_grid - center_y
            radius = np.sqrt(d_x**2 + d_y**2)

            # Create gradient mask
            max_radius = np.sqrt(width**2 + height**2)
            gradient = np.clip(radius / (max_radius * 0.5), 0.0, 1.0)

            # Apply to image with high contrast
            if img.ndim == 3:
                result = img.copy().astype(np.float32)

                # Different processing for highlights and shadows
                for c in range(3):
                    # Darken shadows dramatically
                    shadows = (gradient * 1.5)
                    result[:,:,c] = result[:,:,c] * (1.0 - shadows * 0.9)

                # Clip and convert back
                result = np.clip(result, 0, 255).astype(np.uint8)
                return result

            return img

        effects.add(dramatic_lighting)

        # Apply enhanced ghost trails effect
        effects.add(
            lambda img, cfg, pal: ghost_trails(
                img,
                cfg,
                pal,
                intensity=cfg.effect_params.intensity * 2.5,
                direction=random.uniform(30, 150),
                length=60,
            )
        )

        # Apply duotone with a stronger blend
        def enhanced_duotone(img, cfg, pal, color1=None, color2=None):
            """Enhanced duotone effect with more sophisticated color handling."""
            if color1 is None:
                color1 = pal.primary.as_tuple
            if color2 is None:
                color2 = pal.accent.as_tuple

            # Convert to float for processing
            img_float = img.astype(np.float32) / 255.0

            # Create an empty RGB image
            height, width = img.shape[:2]
            result = np.zeros((height, width, 3), dtype=np.float32)

            # Convert to grayscale if not already
            if img.ndim == 3:
                grayscale = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                grayscale = img.copy()
            grayscale = grayscale.astype(np.float32) / 255.0

            # Extract colors as normalized RGB
            c1 = np.array([color1[0]/255.0, color1[1]/255.0, color1[2]/255.0])
            c2 = np.array([color2[0]/255.0, color2[1]/255.0, color2[2]/255.0])

        effects.add(enhanced_duotone)

        # Add ethereal glow
        effects.add(
            lambda img, cfg, pal: ethereal_glow(
                img,
                cfg,
                pal,
                intensity=cfg.effect_params.intensity * 1.5,
                radius=cfg.effect_params.blur_radius * 3,
            )
        )

        # Add grain
        grain_amount = self.config.effect_params.intensity * 0.4
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, grain_amount))

        # Add the effect chain to the engine
        self.engine.add_transformation(effects)

    def _add_gothic_distorted_style(self) -> None:
        """Add gothic style with subtle but pervasive distortion effects."""
        effects = EffectChain()

        # Base adjustment with high contrast
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.3))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 0.85))

        # Apply subtle pervasive distortion
        def subtle_wave_distortion(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Create displacement map
            displacement_x = np.zeros((height, width), dtype=np.float32)
            displacement_y = np.zeros((height, width), dtype=np.float32)

            # Create distortion with multiple frequencies
            intensity = cfg.effect_params.intensity * 0.4  # More subtle than standard

            # Add several subtle wave patterns
            for scale in [6, 12, 24]:
                for y in range(height):
                    for x in range(width):
                        # Apply subtle wave patterns with varying frequencies
                        displacement_x[y, x] += intensity * math.sin(y / scale + x / (scale * 1.5)) * 2
                        displacement_y[y, x] += intensity * math.cos(x / scale + y / (scale * 1.2)) * 2

            # Apply displacement map
            for y in range(height):
                for x in range(width):
                    # Calculate source coordinates with displacement
                    src_x = x + int(displacement_x[y, x])
                    src_y = y + int(displacement_y[y, x])

                    # Ensure we stay within bounds
                    src_x = max(0, min(width - 1, src_x))
                    src_y = max(0, min(height - 1, src_y))

                    # Copy pixel
                    result[y, x] = img[src_y, src_x]

            return result

        effects.add(subtle_wave_distortion)

        # Apply gothic color scheme with deep shadows
        def gothic_tone_mapping(img, cfg, pal):
            # Transform to darker, cooler tones
            result = img.copy().astype(np.float32)

            # Apply tone mapping
            if img.ndim == 3:
                # Apply color toning - enhance blues/purples in shadows, keep highlights
                result[:, :, 0] *= 0.8  # Reduce red
                result[:, :, 2] *= 1.2  # Enhance blue

            # Enhance darks
            result = np.power(result / 255.0, 1.2) * 255.0
            return np.clip(result, 0, 255).astype(np.uint8)

        effects.add(gothic_tone_mapping)

        # Add soft vignette
        effects.add(lambda img, cfg, pal: add_vignette(
            img, cfg, pal,
            amount=0.5,
            color=pal.primary.as_tuple
        ))

        # Add subtle grain for texture
        effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, 0.15))

        self.engine.add_transformation(effects)

    def _add_phantom_flow_style(self) -> None:
        """Add organic long-exposure style with flowing phantasmagoric movements and film grain.

        This style recreates the effect of long exposure photography with an emphasis on
        organic flowing movements, high contrast, and analog film qualities.
        """
        effects = EffectChain()

        # Initial high contrast black and white conversion
        def high_contrast_mono(img, cfg, pal):
            # Convert to grayscale with controlled contrast
            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img.copy()

            # Apply strong contrast with careful clipping
            contrast_factor = 2.8
            enhanced = ((gray.astype(np.float32) - 128) * contrast_factor) + 128

            # Apply slight sigmoid curve for more natural highlights/shadows transition
            enhanced = 255 / (1 + np.exp(-(enhanced - 128) / 30))

            result = np.clip(enhanced, 0, 255).astype(np.uint8)

            # Convert back to 3-channel if original was color
            if img.ndim == 3:
                result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)

            return result

        effects.add(high_contrast_mono)

        # Directional flow effect inspired by long exposure photography
        def directional_flow(img, cfg, pal):
            # Create flowing, directional blur based on image content
            height, width = img.shape[:2]
            result = img.copy().astype(np.float32)

            # Convert to single channel for processing if needed
            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img.copy()

            # Create edge detection to find direction of potential movement
            edges = cv2.Canny(gray, 50, 150)

            # Detect dominant angles in the image
            lines = cv2.HoughLinesP(edges, 1, np.pi/180,
                                    threshold=80,
                                    minLineLength=40,
                                    maxLineGap=10)

            # Create a directional flow map
            flow_map = np.zeros((height, width, 2), dtype=np.float32)

            # If lines were detected, use them to determine flow direction
            dominant_angle = None
            if lines is not None:
                angles = []
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    if x2 != x1:  # Avoid division by zero
                        angle = np.arctan2(y2 - y1, x2 - x1)
                        angles.append(angle)

                if angles:
                    # Find dominant angle (most common direction)
                    dominant_angle = np.median(angles)

            # Default to diagonal flow if no clear direction detected
            if dominant_angle is None:
                dominant_angle = np.pi / 4  # 45 degrees

            # Create directional flow vector based on the dominant angle
            flow_x = np.cos(dominant_angle)
            flow_y = np.sin(dominant_angle)

            # Scale flow by intensity - stronger at edges
            edge_strength = cv2.GaussianBlur(edges.astype(np.float32) / 255.0, (0, 0), 3)

            # Create variable strength flow based on image content
            for y in range(height):
                for x in range(width):
                    # Scale flow by local edge strength and intensity
                    local_strength = edge_strength[y, x] * (1.0 + gray[y, x] / 255.0) * cfg.effect_params.intensity * 35
                    flow_map[y, x, 0] = flow_x * local_strength
                    flow_map[y, x, 1] = flow_y * local_strength

            # Apply directional blur following the flow map
            num_steps = 15  # Number of steps for the flow
            step_weight = 1.0 / num_steps

            # Create accumulation buffer
            accumulated = np.zeros_like(result)

            # Apply flow by sampling along flow direction
            for step in range(num_steps):
                # Weight decreases slightly over steps
                weight = step_weight * (1.0 - step / (num_steps * 1.2))

                # Create a sampling map for this step
                map_x = np.zeros((height, width), dtype=np.float32)
                map_y = np.zeros((height, width), dtype=np.float32)

                for y in range(height):
                    for x in range(width):
                        # Sample position, modulated by step
                        sample_x = x + flow_map[y, x, 0] * step / 3.0
                        sample_y = y + flow_map[y, x, 1] * step / 3.0

                        # Store sampling coordinates
                        map_x[y, x] = np.clip(sample_x, 0, width - 1)
                        map_y[y, x] = np.clip(sample_y, 0, height - 1)

                # Remap image using the sampling map
                if img.ndim == 3:
                    remapped = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)
                    accumulated += remapped.astype(np.float32) * weight
                else:
                    remapped = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)
                    accumulated += remapped.astype(np.float32) * weight

            # Final normalization and conversion
            result = np.clip(accumulated, 0, 255).astype(np.uint8)

            # Apply additional light smearing in the dominant direction
            kernel_size = int(30 + cfg.effect_params.intensity * 20)
            angle_degrees = dominant_angle * 180 / np.pi

            # Create motion blur kernel
            kernel = np.zeros((kernel_size, kernel_size))
            center = kernel_size // 2

            # Convert angle to proper orientation for kernel
            angle_rad = np.deg2rad(angle_degrees - 90)
            x_dir, y_dir = np.cos(angle_rad), np.sin(angle_rad)

            # Create line on kernel
            for i in range(kernel_size):
                # Calculate position along line
                offset = i - center
                x = center + offset * x_dir
                y = center + offset * y_dir

                # Add point to kernel if within bounds
                if 0 <= int(y) < kernel_size and 0 <= int(x) < kernel_size:
                    kernel[int(y), int(x)] = 1

            # Normalize kernel
            kernel = kernel / np.sum(kernel)

            # Apply directional blur
            if img.ndim == 3:
                for c in range(3):
                    result[:, :, c] = cv2.filter2D(result[:, :, c], -1, kernel)
            else:
                result = cv2.filter2D(result, -1, kernel)

            return result

        effects.add(directional_flow)

        # Add swirling, flowing effect to emulate the smooth motion in the image
        def flowing_distortion(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Create displacement maps with organic flow
            displacement_x = np.zeros((height, width), dtype=np.float32)
            displacement_y = np.zeros((height, width), dtype=np.float32)

            # Create perlin-like noise functions for organic flow
            def organic_flow(x, y, scale=1.0, octaves=3):
                value = 0
                amplitude = 1.0
                frequency = 1.0

                for _ in range(octaves):
                    # Add sine waves at different frequencies and orientations
                    value += amplitude * math.sin((x * frequency / width * 6.28) +
                                              (y * frequency / height * 6.28 * 0.7))
                    value += amplitude * math.cos((y * frequency / height * 6.28) +
                                              (x * frequency / width * 6.28 * 0.5))

                    # Adjust parameters for next octave
                    amplitude *= 0.5
                    frequency *= 2.0

                return value * scale

            # Generate the displacement map with organic flow
            intensity = cfg.effect_params.intensity * 12.0

            for y in range(height):
                for x in range(width):
                    # Create varied flow patterns
                    displacement_x[y, x] = organic_flow(x, y, scale=intensity, octaves=4)
                    displacement_y[y, x] = organic_flow(y, x, scale=intensity, octaves=4)

            # Apply displacement to create flow effect
            map_x = np.zeros((height, width), dtype=np.float32)
            map_y = np.zeros((height, width), dtype=np.float32)

            for y in range(height):
                for x in range(width):
                    map_x[y, x] = np.clip(x + displacement_x[y, x], 0, width - 1)
                    map_y[y, x] = np.clip(y + displacement_y[y, x], 0, height - 1)

            # Apply the flow displacement
            result = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)

            return result

        effects.add(flowing_distortion)

        # Add local contrast enhancement to bring out the details and create sharp edges
        def enhance_local_contrast(img, cfg, pal):
            # Apply local contrast enhancement
            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                result = img.copy()
            else:
                gray = img.copy()
                result = img.copy()

            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced_gray = clahe.apply(gray)

            # Apply local contrast boost with structural enhancement
            if img.ndim == 3:
                # Calculate luminance difference
                luminance_diff = (enhanced_gray.astype(np.float32) - gray.astype(np.float32)) * 0.7

                # Add luminance enhancement to each channel while preserving color
                for c in range(3):
                    result[:, :, c] = np.clip(result[:, :, c] + luminance_diff, 0, 255).astype(np.uint8)
            else:
                result = enhanced_gray

            # Apply additional edge enhancement
            edges = cv2.Laplacian(gray, cv2.CV_32F, ksize=3)
            edges = np.abs(edges)

            # Normalize edge values for better control
            edges = cv2.normalize(edges, None, 0, 1, cv2.NORM_MINMAX)

            # Apply edge enhancement with adaptive strength
            edge_strength = 0.3 + cfg.effect_params.intensity * 0.3

            if img.ndim == 3:
                for c in range(3):
                    result[:, :, c] = np.clip(result[:, :, c] + edges * edge_strength * 30, 0, 255).astype(np.uint8)
            else:
                result = np.clip(result + edges * edge_strength * 30, 0, 255).astype(np.uint8)

            return result

        effects.add(enhance_local_contrast)

        # Apply tonal contrast with emphasis on deep blacks and bright whites
        def apply_tonal_contrast(img, cfg, pal):
            # Apply S-curve contrast for deep blacks and bright highlights
            result = img.copy().astype(np.float32)

            # Apply sophisticated tonal curve
            # Convert to 0-1 range
            result = result / 255.0

            # Apply S-curve with stronger shoulders (deeper blacks, brighter whites)
            # Using a custom sigmoid-based curve
            result = 1.0 / (1.0 + np.exp(-(result - 0.5) * 5))

            # Strengthen blacks and whites even more with power curve
            result = np.power(result, 0.85)  # Lighten midtones slightly

            # Apply additional shadow contrast
            shadows = np.clip(1.0 - result * 2, 0, 1)  # Shadow mask
            result = result - shadows * shadows * 0.2  # Deepen shadows

            # Convert back to 0-255 range
            result = np.clip(result * 255.0, 0, 255).astype(np.uint8)

            return result

        effects.add(apply_tonal_contrast)

        # Add authentic film grain texture
        def apply_film_grain(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy().astype(np.float32)

            # Create film grain with proper structure
            grain_amount = 0.18 + cfg.effect_params.intensity * 0.12

            # Create structured noise that mimics film grain
            # Film grain has spatial correlation and is not uniform

            # Generate base noise
            np.random.seed(cfg.random_seed)
            noise = np.random.normal(0, 1, (height, width))

            # Apply multiple frequency components for realistic grain structure
            grain = np.zeros((height, width), dtype=np.float32)

            # Add fine grain
            fine_grain = cv2.resize(noise, (width * 2, height * 2))
            fine_grain = cv2.resize(fine_grain, (width, height))
            grain += fine_grain * 0.6

            # Add medium grain
            medium_grain = cv2.GaussianBlur(noise, (0, 0), 0.5)
            grain += medium_grain * 0.3

            # Add coarse grain structures
            coarse_grain = cv2.GaussianBlur(noise, (0, 0), 1.5)
            grain += coarse_grain * 0.1

            # Normalize the grain
            grain = cv2.normalize(grain, None, 0, 1, cv2.NORM_MINMAX)

            # Apply the grain differently to different tonal regions
            if img.ndim == 3:
                # Convert to LAB for better luminance handling
                lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
                luminance = lab[:,:,0] / 255.0

                for c in range(3):
                    # Apply stronger grain in shadows, less in highlights
                    grain_mask = grain * (1.0 - luminance * 0.5) * grain_amount * 30
                    result[:,:,c] = np.clip(result[:,:,c] + grain_mask, 0, 255)
            else:
                # Luminance is the image itself
                luminance = img / 255.0
                grain_mask = grain * (1.0 - luminance * 0.5) * grain_amount * 30
                result = np.clip(result + grain_mask, 0, 255)

            # Apply slight grain-based texture enhancement
            texture_mask = np.abs(grain) * luminance * 20
            result = np.clip(result + texture_mask, 0, 255).astype(np.uint8)

            return result

        effects.add(apply_film_grain)

        # Add subtle halation effect (light bloom around bright areas)
        def apply_light_halation(img, cfg, pal):
            # Create halation effect (light spreading common in analog photography)
            result = img.copy().astype(np.float32)

            # Extract highlights
            if img.ndim == 3:
                # Calculate luminance
                luminance = 0.299 * img[:,:,0] + 0.587 * img[:,:,1] + 0.114 * img[:,:,2]
            else:
                luminance = img.copy()

            # Create highlight mask
            highlight_threshold = 180
            highlight_mask = np.clip((luminance - highlight_threshold) / (255 - highlight_threshold), 0, 1)

            # Create bloom around highlights with variable radius
            bloom_small = cv2.GaussianBlur(highlight_mask, (0, 0), 3)
            bloom_medium = cv2.GaussianBlur(highlight_mask, (0, 0), 10)
            bloom_large = cv2.GaussianBlur(highlight_mask, (0, 0), 30)

            # Combine blooms with different weights
            combined_bloom = bloom_small * 0.5 + bloom_medium * 0.3 + bloom_large * 0.2

            # Apply halation
            halation_strength = 0.3 + cfg.effect_params.intensity * 0.2

            if img.ndim == 3:
                for c in range(3):
                    # Apply with careful weighting
                    result[:,:,c] = np.clip(result[:,:,c] + combined_bloom * halation_strength * 60, 0, 255)
            else:
                result = np.clip(result + combined_bloom * halation_strength * 60, 0, 255)

            return result.astype(np.uint8)

        effects.add(apply_light_halation)

        # Final vignette effect to complete the analog look
        def apply_subtle_vignette(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Create natural-looking vignette mask
            center_x, center_y = width / 2, height / 2
            max_dist = np.sqrt(center_x ** 2 + center_y ** 2)

            vignette = np.zeros((height, width), dtype=np.float32)

            for y in range(height):
                for x in range(width):
                    # Calculate distance from center
                    dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                    # Create smooth falloff
                    vignette[y, x] = 1 - np.power(dist / max_dist, 2)

            # Apply non-uniform vignette for more organic feel
            vignette = np.power(vignette, 1.5)

            # Scale vignette effect by intensity
            vignette_amount = 0.25 + cfg.effect_params.intensity * 0.15
            vignette = 1.0 - (1.0 - vignette) * vignette_amount

            # Apply to image
            if img.ndim == 3:
                for c in range(3):
                    result[:,:,c] = np.clip(result[:,:,c] * vignette, 0, 255).astype(np.uint8)
            else:
                result = np.clip(result * vignette, 0, 255).astype(np.uint8)

            return result

        effects.add(apply_subtle_vignette)

        self.engine.add_transformation(effects)
