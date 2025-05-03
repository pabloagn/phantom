# packages/phantom-visuals/phantom_visuals/transformers/author.py

"""Author image transformation for Phantom Visuals.

This module provides specialized transformations for author portraits
to create consistent and distinctive styling across the Phantom ecosystem.
"""

import glob
import math
import random
from pathlib import Path
from typing import Optional, Union, Tuple, List

import cv2
import numpy as np
import noise
from skimage.feature import structure_tensor
# TODO:Import specific feature if needed later, e.g., from skimage import feature

# Assuming these are correctly defined and importable:
from phantom_visuals.core.config import Configuration
from phantom_visuals.core.engine import StyleEngine
from phantom_visuals.core.palette import ColorPalette, RGBColor
from phantom_visuals.effects import (
    EffectChain, add_grain, add_noise, add_vignette, adjust_brightness,
    adjust_contrast, adjust_saturation, apply_symmetry, blur_regions,
    detect_edges, displace, duotone, enhance_edges, ethereal_glow,
    ghost_trails, glitch, lens_distortion, pixel_sort, solarize,
    threshold, wave_distortion
)
from phantom_visuals.effects.artistic import create_glitch_blocks

# Helper functions (can be moved to a utils file if preferred)
def _calculate_rgb_color(base_color_obj: RGBColor, factor: float, mode: str = 'mult') -> Tuple[int, int, int]:
    """Manually calculate darker or lighter RGB color."""
    base_tuple = base_color_obj.as_tuple
    if mode == 'darken': # Treat factor as retention (0.1 = 10% brightness)
        return tuple(max(0, int(c * factor)) for c in base_tuple)
    elif mode == 'lighten': # Treat factor as multiplier (1.5 = 150% brightness)
         return tuple(min(255, int(c * factor)) for c in base_tuple)
    # Default: multiply (can be darken or lighten based on factor)
    return tuple(max(0, min(255, int(c * factor))) for c in base_tuple)

def _create_motion_blur_kernel(kernel_size: int, angle_degrees: float) -> np.ndarray:
    """Creates a motion blur kernel for a given size and angle."""
    if kernel_size <= 1:
        return np.array([[1.0]]) # No blur

    kernel_size = max(3, kernel_size if kernel_size % 2 != 0 else kernel_size + 1) # Ensure odd size >= 3
    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
    center = kernel_size // 2

    # Convert angle: 0 degrees is horizontal right, 90 is vertical up
    # OpenCV filter2D kernel rotation differs from typical math angles
    angle_rad_kernel = math.radians(angle_degrees - 90)
    x_dir, y_dir = math.cos(angle_rad_kernel), math.sin(angle_rad_kernel)

    half_length = kernel_size // 2
    # Create a line on the kernel
    # Use integer coordinates by drawing line from one end to the other
    pt1 = (center - int(round(x_dir * half_length)), center - int(round(y_dir * half_length)))
    pt2 = (center + int(round(x_dir * half_length)), center + int(round(y_dir * half_length)))
    cv2.line(kernel, pt1, pt2, 1.0, 1) # Draw line with thickness 1

    # Normalize the kernel
    sum_kernel = np.sum(kernel)
    if sum_kernel == 0: # Handle potential edge case where line is length 0
        kernel[center, center] = 1.0
    else:
        kernel /= sum_kernel

    return kernel

def _normalized_gradient_magnitude(gray_img: np.ndarray, ksize:int = 3, blur_ksize:int = 5) -> np.ndarray:
    """ Calculates normalized gradient magnitude (0=smooth, 1=edge)."""
    if not isinstance(gray_img, np.ndarray) or gray_img.ndim != 2:
        raise ValueError("Input must be a 2D NumPy array (grayscale image).")

    # Apply Gaussian blur to reduce noise before gradient calculation
    if blur_ksize > 0:
        # Ensure kernel size is odd
        blur_ksize_odd = blur_ksize if blur_ksize % 2 != 0 else blur_ksize + 1
        gray_smooth = cv2.GaussianBlur(gray_img, (blur_ksize_odd, blur_ksize_odd), 0)
    else:
        gray_smooth = gray_img

    # Calculate gradients using Sobel operator (more robust to noise than Scharr with blur)
    # Use 32-bit float for gradients to avoid overflow/loss of precision
    grad_x = cv2.Sobel(gray_smooth, cv2.CV_32F, 1, 0, ksize=ksize)
    grad_y = cv2.Sobel(gray_smooth, cv2.CV_32F, 0, 1, ksize=ksize)

    # Calculate magnitude
    magnitude = cv2.magnitude(grad_x, grad_y)

    # Normalize magnitude robustly: use min-max scaling
    min_val, max_val = np.min(magnitude), np.max(magnitude)
    if max_val > min_val:
        # Standard min-max normalization to [0, 1]
        norm_mag = (magnitude - min_val) / (max_val - min_val)
    else:
        # Handle flat image case (no gradient)
        norm_mag = np.zeros_like(magnitude, dtype=np.float32)

    # Optional: Enhance contrast of magnitude map slightly to sharpen distinction
    # Be careful not to over-saturate edges
    # norm_mag = np.clip(norm_mag**0.8, 0.0, 1.0)

    return norm_mag

def _generate_perlin_flow_field(width: int, height: int, scale: float, octaves: int, persistence: float, lacunarity: float, seed: int) -> Tuple[np.ndarray, np.ndarray]:
    """ Generates a flow field using Perlin noise. Returns (flow_x, flow_y)."""
    flow_x = np.zeros((height, width), dtype=np.float32)
    flow_y = np.zeros((height, width), dtype=np.float32)
    # Use different seeds/offsets for x and y flow for less correlated movement
    seed_x = seed
    seed_y = seed + 1

    for i in range(height):
        for j in range(width):
            # Generate noise values for x and y directions separately
            # Scale coordinates before passing to noise function
            scaled_x = j / width * scale
            scaled_y = i / height * scale
            # noise.pnoise3 adds depth, which we map to angle or use 2 independent 2D noises
            # Option 1: Use 3D noise, z=0 for flow_x, z=1 for flow_y angle components? Less intuitive.
            # Option 2: Two independent 2D noises for x and y magnitudes/angles. Simpler.
            angle_rad = noise.pnoise2(scaled_x, scaled_y,
                                     octaves=octaves, persistence=persistence, lacunarity=lacunarity,
                                     base=seed_x) * math.pi * 2.0 # Noise value maps to angle (-pi to pi roughly)

            magnitude = 0.5 + (noise.pnoise2(scaled_x, scaled_y, # Use different noise seed/instance for magnitude
                                      octaves=octaves, persistence=persistence, lacunarity=lacunarity,
                                      base=seed_y) + 1.0) / 2.0 # Normalize noise approx -1 to 1 -> 0 to 1 for magnitude scale

            flow_x[i, j] = math.cos(angle_rad) * magnitude
            flow_y[i, j] = math.sin(angle_rad) * magnitude # Regular sin, y inversion handled later if needed

    return flow_x, flow_y

# --- End Helper Functions ---


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
        elif style_variant == "topographic_wave":
            self._add_topographic_wave_style()
        elif style_variant == "slit_scan_distort":
            self._add_slit_scan_style()
        elif style_variant == "smudge_flow":
            self._add_smudge_flow_style()
        elif style_variant == "topographic_refined": self._add_topographic_refined_style()
        elif style_variant == "long_exposure_scan": self._add_long_exposure_scan_style()
        elif style_variant == "ghostly_smear": self._add_ghostly_smear_style()
        # --- NEW Refined Styles ---
        elif style_variant == "topographic_depth": self._add_topographic_depth_style()
        elif style_variant == "temporal_flow": self._add_temporal_flow_style()
        elif style_variant == "liquid_ghost": self._add_liquid_ghost_style()
        # --- NEW Methodical Styles (v2) ---
        elif style_variant == "topographic_mesh": self._add_topographic_mesh_style()
        elif style_variant == "temporal_streak": self._add_temporal_streak_style()
        elif style_variant == "ethereal_smudge": self._add_ethereal_smudge_style()
        # --- NEW METHODICAL Styles (v3) ---
        # NOTE: Renamed again slightly to avoid collision and indicate version
        elif style_variant == "plotter_mesh_v3": self._add_plotter_mesh_v3_style()
        elif style_variant == "streak_accumulate_v3": self._add_streak_accumulate_v3_style()
        elif style_variant == "flow_smudge_v3": self._add_flow_smudge_v3_style()
        elif style_variant == "celestial_drift_v4": self._add_celestial_drift_v4_style()


        else:
            # Default to phantom style
            print(
                f"Warning: Style '{style_variant}' not recognized. Defaulting to 'phantom'."
            )
            self._add_phantom_style()

        # Process the image
        return self.engine.transform(input_path, output_path)

    # <<< --- NEW METHODICAL IMPLEMENTATIONS (v3) --- >>>

    def _add_celestial_drift_v4_style(self) -> None:
        """(V4) Advanced particle advection aiming for elegant, celestial streaks."""
        effects = EffectChain()

        # Pre-processing
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.8))
        # Keep color info for now

        def apply_celestial_drift(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 501
                np.random.seed(seed); random.seed(seed)

            if img.ndim == 2:
                gray = img; current_frame_color = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            else:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY); current_frame_color = img.copy()

            current_frame_float = current_frame_color.astype(np.float32)
            gray_float = gray.astype(np.float32)
            height, width = gray.shape
            params = cfg.effect_params

            # --- Parameters ---
            num_steps = 30 + int(params.intensity * 50)
            max_particles = 5000 + int(params.intensity * 15000)
            min_particle_distance = 3
            quality_level = 0.01 + (1.0-params.intensity) * 0.04
            flow_strength = 0.5 + params.intensity * 1.0
            structure_alignment_factor = 0.5 + params.distortion * 0.4
            noise_scale = 25 + params.noise_level * 40
            noise_influence = 0.3 + params.noise_level * 0.7
            # --- V4 Variable Name ---
            initial_brightness_boost = 1.8
            brightness_fade_factor = 0.975  # <<< DEFINED HERE (V4 NAME) <<<
            min_brightness_render = 15
            base_thickness = 1.0
            max_thickness_factor = 2.5
            bloom_strength = 0.1 + params.intensity * 0.25
            bloom_radius = 5 + int(params.blur_radius * 0.5)
            final_gamma = 0.8

            # --- Particle Seeding ---
            corners = cv2.goodFeaturesToTrack(gray, max_particles, quality_level, min_particle_distance, blockSize=5)
            if corners is None or len(corners) == 0: return img
            initial_coords = corners.reshape(-1, 2)
            initial_x, initial_y = initial_coords[:, 0], initial_coords[:, 1]
            initial_x = np.clip(initial_x, 0, width - 1).astype(int)
            initial_y = np.clip(initial_y, 0, height - 1).astype(int)
            initial_gray_brightness = gray[initial_y, initial_x].astype(np.float32)
            valid_start = initial_gray_brightness > 10
            initial_x, initial_y = initial_x[valid_start], initial_y[valid_start]
            initial_gray_brightness = initial_gray_brightness[valid_start]
            if len(initial_x) == 0: return img
            initial_color = current_frame_float[initial_y, initial_x]
            current_brightness = np.mean(initial_color, axis=1) * initial_brightness_boost
            current_color = initial_color.copy()
            current_x, current_y = initial_x.astype(np.float32), initial_y.astype(np.float32)
            active_particles = np.ones(len(initial_x), dtype=bool)

            # --- Flow Field Calculation ---
            sigma_structure= 3 + params.distortion * 3
            Axx, Axy, Ayy = structure_tensor(gray, sigma=sigma_structure, mode='reflect', order='xy')
            structure_angle_rad = np.arctan2(2 * Axy, Ayy - Axx + 1e-6) / 2.0 # Add epsilon
            perlin_flow_x, perlin_flow_y = _generate_perlin_flow_field(width, height, scale=noise_scale, octaves=5, persistence=0.5, lacunarity=2.0, seed=seed+1)

            # --- Accumulation Canvas ---
            accumulator = np.zeros_like(current_frame_float, dtype=np.float64)

            # --- Simulation Loop ---
            for step in range(num_steps):
                if not np.any(active_particles): break
                active_idx = np.where(active_particles)[0]
                x_t, y_t, brightness_t, color_t = current_x[active_idx], current_y[active_idx], current_brightness[active_idx], current_color[active_idx]

                # Calculate Flow
                x_int, y_int = np.clip(np.round(x_t), 0, width-1).astype(int), np.clip(np.round(y_t), 0, height-1).astype(int)
                particle_struct_angle = structure_angle_rad[y_int, x_int]
                particle_noise_x, particle_noise_y = perlin_flow_x[y_int, x_int], perlin_flow_y[y_int, x_int]
                struct_flow_x, struct_flow_y = np.cos(particle_struct_angle), -np.sin(particle_struct_angle)
                step_flow_x = (struct_flow_x * structure_alignment_factor + particle_noise_x * noise_influence)
                step_flow_y = (struct_flow_y * structure_alignment_factor + particle_noise_y * noise_influence)
                flow_mag = np.sqrt(step_flow_x**2 + step_flow_y**2) + 1e-6
                speed = flow_strength * (0.5 + (brightness_t / (initial_brightness_boost*255))**0.5)
                step_vx = (step_flow_x / flow_mag) * speed
                step_vy = (step_flow_y / flow_mag) * speed

                # Update Positions
                x_next, y_next = x_t + step_vx, y_t + step_vy

                # Draw Streaks
                for k in range(len(active_idx)):
                    render_brightness = brightness_t[k]
                    if render_brightness < min_brightness_render: continue
                    x1_rnd, y1_rnd = int(round(x_t[k])), int(round(y_t[k]))
                    x2_rnd, y2_rnd = int(round(x_next[k])), int(round(y_next[k]))
                    if not (0 <= x1_rnd < width and 0 <= y1_rnd < height): continue
                    norm_brightness = render_brightness / (initial_brightness_boost * 255)
                    thickness = max(1.0, base_thickness + norm_brightness * (max_thickness_factor - base_thickness))
                    line_value = np.array([render_brightness]*3, dtype=np.float32)
                    cv2.line(accumulator, (x1_rnd, y1_rnd), (x2_rnd, y2_rnd), line_value.tolist(), thickness=max(1, int(round(thickness))), lineType=cv2.LINE_AA)

                # Update Particle State
                current_x[active_idx] = x_next
                current_y[active_idx] = y_next
                 # --- V4 Variable Name Used ---
                current_brightness[active_idx] *= brightness_fade_factor # <<< USED HERE (V4 NAME) <<<
                off_screen = (x_next < 0) | (x_next >= width) | (y_next < 0) | (y_next >= height)
                too_faint = current_brightness[active_idx] < (min_brightness_render * 0.5)
                active_particles[active_idx[off_screen | too_faint]] = False

            # --- Post-Process Accumulator ---
            min_acc, max_acc = np.min(accumulator), np.max(accumulator)
            if max_acc > min_acc + 1e-6:
                norm_acc = (accumulator - min_acc) / (max_acc - min_acc)
            else: norm_acc = np.zeros_like(accumulator)

            # Bloom
            if bloom_strength > 0 and bloom_radius > 0:
                 bright_pixels = (norm_acc > (1.0 - bloom_strength * 0.8)).astype(np.float32); highlights = norm_acc * bright_pixels
                 bloom_ksize = int(bloom_radius) * 2 + 1; blurred_highlights = cv2.GaussianBlur(highlights, (bloom_ksize, bloom_ksize), 0)
                 bloom_layer = blurred_highlights * bloom_strength * 3.0
                 norm_acc = 1.0 - (1.0 - norm_acc) * (1.0 - bloom_layer); norm_acc = np.clip(norm_acc, 0.0, 1.0)

            # Gamma & Convert
            final_result_float = np.power(norm_acc, final_gamma) * 255.0
            final_result = np.clip(final_result_float, 0, 255).astype(np.uint8)
            if final_result.ndim == 3: final_result = cv2.cvtColor(final_result, cv2.COLOR_RGB2GRAY)

            return final_result
        # --- End apply_celestial_drift ---

        effects.add(apply_celestial_drift)
        if self.config.effect_params.grain > 0: effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.25, monochrome=True))
        if self.config.effect_params.vignette > 0: effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.35))
        self.engine.add_transformation(effects)

    def _add_plotter_mesh_v3_style(self) -> None:
        """(V3) Plotter/Topographic style aiming for weighted mesh look."""
        effects = EffectChain()
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 2.5))

        def apply_plotter_mesh(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            # (Implementation is exactly as provided in my previous full message)
            # Starts with seed setting, parameter definition, blurring...
            # ... includes the back-to-front loop with occlusion check ...
            # ... ends with returning the 'canvas' np.ndarray ...
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 203
                np.random.seed(seed); random.seed(seed)

            if img.ndim == 3: gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else: gray = img.copy()
            height, width = gray.shape
            params = cfg.effect_params

            # Parameters
            line_count = int(65 + params.intensity * 60)
            amplitude_factor = 18 + params.distortion * 65
            base_thickness = 1
            thickness_multiplier_low = 0.8
            thickness_multiplier_high = 2.8
            noise_pos_scale = params.noise_level * 1.8
            noise_amp_scale = params.noise_level * 0.1
            vertical_focus_start = 0.05
            vertical_focus_end = 0.90

            # Blurring
            blur_k_shape = int(5 + params.blur_radius * 1.0) * 2 + 1
            blur_k_detail = 7
            gray_shape = cv2.GaussianBlur(gray, (blur_k_shape, blur_k_shape), 0)
            gray_detail = cv2.GaussianBlur(gray, (blur_k_detail, blur_k_detail), 0)

            # Colors
            bg_color_tuple = _calculate_rgb_color(pal.primary, 0.02, 'darken')
            line_color_tuple = _calculate_rgb_color(pal.accent, 1.9, 'lighten')

            # Canvas & Occlusion
            canvas = np.full((height, width, 3), bg_color_tuple, dtype=np.uint8)
            start_y = int(height * vertical_focus_start)
            end_y_for_spacing = int(height * vertical_focus_end)
            total_draw_height = end_y_for_spacing - start_y
            line_count = max(1, line_count)
            line_spacing = max(1.0, total_draw_height / float(line_count))
            horizon_line = np.full(width, height + 100, dtype=np.int32)

            # Wave Generation
            for i in range(line_count - 1, -1, -1):
                y_base = start_y + int(round(i * line_spacing))
                if y_base >= height: continue
                sample_y = min(y_base, height - 1)
                brightness_wave_row = gray_shape[sample_y, :]
                brightness_detail_row = gray_detail[sample_y, :]
                segment_points: List[Tuple[int, int]] = []
                segment_weights: List[float] = []
                for x in range(width):
                    brightness_s = brightness_wave_row[x] / 255.0
                    brightness_d = brightness_detail_row[x] / 255.0
                    amp_noise = 1.0 + (random.random() - 0.5) * noise_amp_scale
                    displacement = ((1.0 - brightness_s) ** 1.6) * amplitude_factor * amp_noise
                    y_disp_f = y_base - displacement
                    thickness_norm = np.clip(displacement / amplitude_factor if amplitude_factor > 0 else 0, 0, 1)
                    thickness = base_thickness * (thickness_multiplier_low + thickness_norm * (thickness_multiplier_high - thickness_multiplier_low))
                    x_noise, y_noise = (np.random.randn(2) * noise_pos_scale)
                    x_rnd, y_rnd = int(round(x + x_noise)), int(round(y_disp_f + y_noise))
                    x_check = min(max(0, x_rnd), width-1)
                    is_visible = 0 <= y_rnd < horizon_line[x_check]
                    if is_visible:
                        segment_points.append((x_rnd, y_rnd))
                        segment_weights.append(thickness)
                        horizon_line[x_check] = min(horizon_line[x_check], y_rnd)
                    else:
                        if len(segment_points) > 1:
                            avg_thick = max(1, int(round(np.mean(segment_weights))))
                            cv2.polylines(canvas, [np.array(segment_points, dtype=np.int32)], False, line_color_tuple, avg_thick, cv2.LINE_AA)
                        segment_points, segment_weights = [], []
                if len(segment_points) > 1:
                     avg_thick = max(1, int(round(np.mean(segment_weights))))
                     cv2.polylines(canvas, [np.array(segment_points, dtype=np.int32)], False, line_color_tuple, avg_thick, cv2.LINE_AA)
            return canvas
        # --- End apply_plotter_mesh ---

        effects.add(apply_plotter_mesh)
        if self.config.effect_params.grain > 0: effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.08))
        if self.config.effect_params.vignette > 0: effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.15))
        self.engine.add_transformation(effects)


    def _add_streak_accumulate_v3_style(self) -> None:
        """(V3) Simulates long exposure streaks via particle advection/accumulation."""
        effects = EffectChain()
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 3.0))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.0))

        def apply_temporal_streak(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            # (Implementation is exactly as provided in my previous full message)
            # Starts with seed setting, parameter definition, particle selection...
            # ... includes the iterative simulation loop with flow calculation and drawing...
            # ... ends with post-processing the accumulator and returning final_result ...
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 303
                np.random.seed(seed); random.seed(seed)

            if img.ndim == 3: gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else: gray = img.copy()
            height, width = gray.shape
            params = cfg.effect_params

            # Parameters
            num_steps = 25 + int(params.intensity * 40)
            flow_strength = 0.8 + params.intensity * 1.5
            base_angle = 90
            angle_variation = params.distortion * 60
            flow_noise_scale = 30 + params.noise_level * 50
            flow_noise_strength = params.noise_level * 1.0
            brightness_threshold = int(150 + (1.0-params.intensity) * 80)
            streak_fade_factor = 0.98
            min_brightness = 20
            initial_brightness_scale = 1.5

            # Particle Selection
            _, thresh_img = cv2.threshold(gray, brightness_threshold, 255, cv2.THRESH_BINARY)
            particle_coords = np.argwhere(thresh_img > 0)
            if len(particle_coords) == 0: return img
            initial_y, initial_x = particle_coords[:, 0], particle_coords[:, 1]
            initial_brightness = gray[initial_y, initial_x].astype(np.float32) * initial_brightness_scale
            current_x = initial_x.astype(np.float32)
            current_y = initial_y.astype(np.float32)
            current_brightness = initial_brightness.copy()
            active_particles = np.ones(len(initial_x), dtype=bool)

            # Flow Field
            gray_smooth = cv2.GaussianBlur(gray, (7,7), 0)
            grad_x = cv2.Sobel(gray_smooth, cv2.CV_32F, 1, 0, ksize=5)
            grad_y = cv2.Sobel(gray_smooth, cv2.CV_32F, 0, 1, ksize=5)
            base_angle_rad = math.radians(base_angle)
            grad_angle_rad = np.arctan2(-grad_x, grad_y)
            # Ensure _generate_perlin_flow_field is available in the scope
            flow_noise_x, flow_noise_y = _generate_perlin_flow_field(width, height, scale=flow_noise_scale, octaves=4, persistence=0.5, lacunarity=2.0, seed=seed+1)

            # Accumulation Canvas
            accumulator = np.zeros((height, width), dtype=np.float64)

            # Simulation Loop
            for step in range(num_steps):
                if not np.any(active_particles): break
                active_idx = np.where(active_particles)[0]
                x_t, y_t = current_x[active_idx], current_y[active_idx]
                brightness_t = current_brightness[active_idx]

                # Calculate Flow
                x_int, y_int = np.clip(np.round(x_t), 0, width-1).astype(int), np.clip(np.round(y_t), 0, height-1).astype(int)
                particle_grad_angle = grad_angle_rad[y_int, x_int]
                particle_noise_x = flow_noise_x[y_int, x_int]
                particle_noise_y = flow_noise_y[y_int, x_int]
                step_random_angle = np.random.uniform(-angle_variation, angle_variation, size=len(active_idx)) * (math.pi / 180.0)
                step_angle_rad = base_angle_rad + particle_grad_angle * params.distortion + particle_noise_y * flow_noise_strength * 2.0 + step_random_angle

                step_flow_mag = flow_strength * random.uniform(0.8, 1.2)
                step_vx = np.cos(step_angle_rad) * step_flow_mag
                step_vy = -np.sin(step_angle_rad) * step_flow_mag

                # Update Positions
                x_next = x_t + step_vx
                y_next = y_t + step_vy

                # Draw Streaks
                for k in range(len(active_idx)):
                    x1, y1 = int(round(x_t[k])), int(round(y_t[k]))
                    x2, y2 = int(round(x_next[k])), int(round(y_next[k]))
                    color_val = brightness_t[k]
                    if 0 <= x1 < width and 0 <= y1 < height:
                         cv2.line(accumulator, (x1, y1), (x2, y2), float(color_val), thickness=1, lineType=cv2.LINE_AA)

                # Update Particle State
                current_x[active_idx] = x_next
                current_y[active_idx] = y_next
                current_brightness[active_idx] *= streak_fade_factor
                off_screen = (x_next < 0) | (x_next >= width) | (y_next < 0) | (y_next >= height)
                too_faint = current_brightness[active_idx] < min_brightness
                active_particles[active_idx[off_screen | too_faint]] = False

            # Post-Process Accumulator
            final_blur_ksize = int(1 + params.blur_radius * 0.3) * 2 + 1
            if final_blur_ksize > 1:
                accumulator = cv2.GaussianBlur(accumulator, (final_blur_ksize, final_blur_ksize), 0)

            min_acc, max_acc = np.min(accumulator), np.max(accumulator)
            if max_acc > min_acc:
                gamma = 0.7 + params.intensity * 0.5
                norm_acc = np.power(accumulator / max_acc, gamma) * 255.0
            else:
                norm_acc = accumulator

            final_result = np.clip(norm_acc, 0, 255).astype(np.uint8)

            if final_result.ndim == 3: final_result = cv2.cvtColor(final_result, cv2.COLOR_RGB2GRAY)
            return final_result
        # --- End apply_temporal_streak ---

        effects.add(apply_temporal_streak)
        if self.config.effect_params.grain > 0: effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.3))
        if self.config.effect_params.vignette > 0: effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.4))
        self.engine.add_transformation(effects)


    def _add_flow_smudge_v3_style(self) -> None:
        """(V3) Fluid smudge using iterative warping based on Perlin noise flow fields."""
        effects = EffectChain()
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.2))
        effects.add(lambda img, cfg, pal: adjust_brightness(img, cfg, pal, 1.1))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.1))

        def apply_flow_smudge(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
             # (Implementation is exactly as provided in my previous full message)
             # Starts with seed setting, parameter definition, structure mask calc...
             # ... includes Perlin flow field generation using _generate_perlin_flow_field...
             # ... includes iterative warp/blur/blend loop...
             # ... ends with returning final_result ...
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 403
                np.random.seed(seed); random.seed(seed)

            current_result = img.astype(np.float32)
            height, width = current_result.shape[:2]
            is_color = current_result.ndim == 3
            params = cfg.effect_params

            # Parameters
            num_steps = 5 + int(params.intensity * 15)
            noise_scale = 15 + params.distortion * 35
            noise_octaves = 4 + int(params.distortion * 3)
            noise_persistence = 0.4 + params.intensity * 0.25
            noise_lacunarity = 2.0
            flow_strength = 1.5 + params.intensity * 4.0
            structure_preservation = 0.3 + (1.0-params.intensity) * 0.6
            blur_ksize = 3 + int(params.blur_radius * 0.4)
            step_opacity = 0.1 + params.intensity * 0.2

            # Structure Mask
            if is_color: gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else: gray = img.copy()
            structure_map = _normalized_gradient_magnitude(gray, ksize=3, blur_ksize=1) # Uses helper
            effect_mask = (1.0 - structure_map**(0.8 + structure_preservation*1.0))**1.2
            effect_mask = cv2.GaussianBlur(effect_mask,(9,9),0)
            if is_color: effect_mask = cv2.cvtColor(effect_mask, cv2.COLOR_GRAY2RGB)

            # Generate Base Flow Field
            # Ensure _generate_perlin_flow_field is available
            flow_x, flow_y = _generate_perlin_flow_field(width, height, scale=noise_scale, octaves=noise_octaves, persistence=noise_persistence, lacunarity=noise_lacunarity, seed=seed)
            magnitude = np.sqrt(flow_x**2 + flow_y**2) + 1e-6
            max_mag = np.max(magnitude)
            if max_mag > 0: norm_flow_x, norm_flow_y = (flow_x / max_mag) * flow_strength, (flow_y / max_mag) * flow_strength
            else: norm_flow_x, norm_flow_y = flow_x, flow_y

            # Base Meshgrid
            map_base_x, map_base_y = np.meshgrid(np.arange(width, dtype=np.float32), np.arange(height, dtype=np.float32))

            # Iterative Smudging
            for step in range(num_steps):
                 # Warp
                 map_x = np.clip(map_base_x + norm_flow_x, 0, width - 1) # Use same flow field? Or evolve it? Let's keep simple for now.
                 map_y = np.clip(map_base_y + norm_flow_y, 0, height - 1)
                 warped_img = cv2.remap(current_result, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

                 # Blur
                 if blur_ksize > 1:
                      blur_k_odd = blur_ksize if blur_ksize % 2 != 0 else blur_ksize + 1
                      blurred_img = cv2.GaussianBlur(warped_img, (blur_k_odd, blur_k_odd), 0)
                 else: blurred_img = warped_img

                 # Blend
                 alpha = step_opacity * effect_mask
                 current_result = current_result * (1.0 - alpha) + blurred_img * alpha

                 # Optional: Evolve flow field slightly?
                 # angle_rad = math.radians(1.0)
                 # cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
                 # old_fx, old_fy = norm_flow_x.copy(), norm_flow_y.copy()
                 # norm_flow_x = old_fx * cos_a - old_fy * sin_a
                 # norm_flow_y = old_fx * sin_a + old_fy * cos_a

            # Final Output
            final_result = np.clip(current_result, 0, 255).astype(np.uint8)
            if is_color: final_result = cv2.cvtColor(final_result, cv2.COLOR_RGB2GRAY)
            return final_result
        # --- End apply_flow_smudge ---

        effects.add(apply_flow_smudge)
        if self.config.effect_params.grain > 0: effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.5, monochrome=True, grain_size=0.9))
        if self.config.effect_params.vignette > 0: effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.5))
        self.engine.add_transformation(effects)

    # V2
    def _add_topographic_mesh_style(self) -> None:
        """(V2) Topographic style with focus on depth, weight, and mesh-like quality."""
        effects = EffectChain()

        def apply_topographic_mesh(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 202 # Distinct seed
                np.random.seed(seed)
                random.seed(seed)

            if img.ndim == 3: gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else: gray = img.copy()
            height, width = gray.shape
            params = cfg.effect_params

            # --- Parameters ---
            line_count = int(65 + params.intensity * 60) # Density control
            amplitude_factor = 18 + params.distortion * 65 # Wave height
            base_thickness = 1
            thickness_multiplier_low = 0.8 # Thinner in troughs
            thickness_multiplier_high = 2.8 # Thicker on peaks/brightness
            noise_pos_scale = params.noise_level * 1.8 # Noise added to vertex positions
            noise_amp_scale = params.noise_level * 0.1 # Noise added to amplitude
            vertical_focus_start = 0.05
            vertical_focus_end = 0.90

            # --- Blurring ---
            blur_k_shape = int(5 + params.blur_radius * 1.0) * 2 + 1 # Blur for wave shape
            blur_k_detail = 5 # Constant small blur for thickness modulation
            gray_shape = cv2.GaussianBlur(gray, (blur_k_shape, blur_k_shape), 0)
            gray_detail = cv2.GaussianBlur(gray, (blur_k_detail, blur_k_detail), 0)

            # --- Colors ---
            bg_color_tuple = _calculate_rgb_color(pal.primary, 0.02, 'darken') # Almost black BG
            line_color_tuple = _calculate_rgb_color(pal.accent, 1.9, 'lighten') # Bright lines

            # --- Canvas & Occlusion ---
            canvas = np.full((height, width, 3), bg_color_tuple, dtype=np.uint8)
            start_y = int(height * vertical_focus_start)
            end_y_for_spacing = int(height * vertical_focus_end)
            total_draw_height = end_y_for_spacing - start_y
            # Ensure line_count > 0 to avoid division error
            line_count = max(1, line_count)
            line_spacing = max(1, total_draw_height / line_count) # Allow float spacing for base calc
            horizon_line = np.full(width, height + 100, dtype=np.int32) # Horizon starts well below screen

            # --- Wave Generation (Back to Front) ---
            for i in range(line_count - 1, -1, -1):
                y_base = start_y + int(i * line_spacing) # Use int for base pixel row
                if y_base >= height: continue

                sample_y = min(y_base, height - 1)
                brightness_wave_row = gray_shape[sample_y, :]
                brightness_detail_row = gray_detail[sample_y, :]

                current_segment_points: List[Tuple[int, int]] = []
                current_segment_weights: List[float] = [] # Store displacement or brightness for thickness avg

                for x in range(width):
                    # Displacement based on smooth shape
                    brightness_shape = brightness_wave_row[x] / 255.0
                    amp_noise = 1.0 + (random.random() - 0.5) * noise_amp_scale
                    displacement = ((1.0 - brightness_shape) ** 1.6) * amplitude_factor * amp_noise
                    y_displaced_float = y_base - displacement

                    # Thickness modulation based on detail brightness & displacement
                    brightness_detail = brightness_detail_row[x] / 255.0
                    # Higher brightness (lighter) OR higher displacement (peak) -> thicker line
                    thickness_mod = (brightness_detail**0.7 + (displacement / amplitude_factor if amplitude_factor > 0 else 0)**0.5) / 2.0
                    thickness = base_thickness * (thickness_multiplier_low + thickness_mod * (thickness_multiplier_high - thickness_multiplier_low))

                    # Positional noise
                    x_noise = (random.random() - 0.5) * noise_pos_scale
                    y_noise = (random.random() - 0.5) * noise_pos_scale
                    x_perturbed_rnd = int(round(x + x_noise))
                    y_displaced_rnd = int(round(y_displaced_float + y_noise))

                    # Visibility & Occlusion Check (more robust index check)
                    x_check = min(max(0, x_perturbed_rnd), width-1)
                    is_visible = y_displaced_rnd >= 0 and y_displaced_rnd < horizon_line[x_check]

                    # Segment Handling
                    if is_visible:
                        current_segment_points.append((x_perturbed_rnd, y_displaced_rnd))
                        current_segment_weights.append(thickness)
                        # Update horizon smoothly
                        horizon_line[x_check] = min(horizon_line[x_check], y_displaced_rnd)
                        # Optional wider horizon update:
                        # hw=1; update_slice = slice(max(0, x_check - hw), min(width, x_check + hw + 1))
                        # horizon_line[update_slice] = np.minimum(horizon_line[update_slice], y_displaced_rnd)
                    else: # Point occluded or off screen
                        if len(current_segment_points) > 1:
                            avg_thickness = max(1, int(round(np.mean(current_segment_weights))))
                            pts_np = np.array(current_segment_points, dtype=np.int32)
                            cv2.polylines(canvas, [pts_np], isClosed=False, color=line_color_tuple, thickness=avg_thickness, lineType=cv2.LINE_AA)
                        current_segment_points = []
                        current_segment_weights = []

                # Draw final segment for this line
                if len(current_segment_points) > 1:
                     avg_thickness = max(1, int(round(np.mean(current_segment_weights))))
                     pts_np = np.array(current_segment_points, dtype=np.int32)
                     cv2.polylines(canvas, [pts_np], isClosed=False, color=line_color_tuple, thickness=avg_thickness, lineType=cv2.LINE_AA)

            return canvas
        # --- End apply_topographic_mesh ---

        effects.add(apply_topographic_mesh)
        if self.config.effect_params.grain > 0:
            effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.1, monochrome=True))
        if self.config.effect_params.vignette > 0:
            effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.2))

        self.engine.add_transformation(effects)


    def _add_temporal_streak_style(self) -> None:
        """(V2) Simulates temporal effects with motion flow and weighted accumulation."""
        effects = EffectChain()

        # Pre-processing: High contrast, B&W is common for the reference look
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 2.0 + cfg.effect_params.intensity * 0.5))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.0)) # Force B&W

        def apply_temporal_streak(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 302
                np.random.seed(seed)
                random.seed(seed)

            # Ensure input is grayscale float32 for accumulation
            if img.ndim == 3: gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else: gray = img.copy()
            current_frame = gray.astype(np.float32)
            height, width = current_frame.shape
            params = cfg.effect_params

            # --- Parameters ---
            num_steps = 10 + int(params.intensity * 20)
            # Flow control: distortion affects angle/randomness, intensity affects strength/length
            flow_strength = 1.0 + params.intensity * 4.0 # Pixels per step potential
            base_angle = 90 # Vertical default
            angle_variation = params.distortion * 45 # Degrees variation
            noise_flow_influence = params.noise_level * 0.8 # How much noise affects flow direction
            # Blur controls streak softness
            blur_kernel_size = 3 + int(params.blur_radius * 0.7) # Base kernel size
            blur_increase_factor = 1.1 # Kernel size increases slightly each step
            # Accumulation control
            persistence = 0.05 + (1.0 - params.intensity) * 0.2 # Alpha for weighted average (lower alpha = longer trails)


            # --- Initialize Accumulator & Flow ---
            accumulator = current_frame.copy() * persistence # Start with dimmed original
            total_weight = persistence
            map_base_x, map_base_y = np.meshgrid(np.arange(width, dtype=np.float32), np.arange(height, dtype=np.float32))
            current_map_x = map_base_x.copy()
            current_map_y = map_base_y.copy()

            # --- Iterative Process ---
            for step in range(num_steps):
                # --- Calculate Flow for this step ---
                step_angle_deg = base_angle + random.uniform(-angle_variation, angle_variation)
                # Add noise influence, scaled by step
                step_noise_angle_rad = (np.random.randn(height, width) * noise_flow_influence * math.pi * ((step+1)/num_steps)).astype(np.float32)
                current_angle_rad = math.radians(step_angle_deg) + step_noise_angle_rad

                # Base flow vector for this step (magnitude based on intensity)
                step_flow_mag = flow_strength * random.uniform(0.7, 1.3) / num_steps
                step_flow_x = np.cos(current_angle_rad) * step_flow_mag
                step_flow_y = -np.sin(current_angle_rad) * step_flow_mag # Y is inverted

                # --- Update Total Displacement Map ---
                current_map_x += step_flow_x
                current_map_y += step_flow_y
                # Clip map coordinates
                map_x = np.clip(current_map_x, 0, width - 1)
                map_y = np.clip(current_map_y, 0, height - 1)

                # --- Warp Original Image ---
                # Warp the *original* grayscale image to avoid accumulating blur artefacts
                warped_original = cv2.remap(gray, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

                # --- Apply Directional Blur ---
                current_blur_ksize = int(blur_kernel_size * (blur_increase_factor**step))
                motion_kernel = _create_motion_blur_kernel(current_blur_ksize, step_angle_deg)
                if motion_kernel is not None:
                     processed_frame = cv2.filter2D(warped_original, cv2.CV_32F, motion_kernel)
                else:
                     processed_frame = warped_original.astype(np.float32)

                # --- Accumulate using weighted average ---
                alpha = (1.0 - persistence) / num_steps # Distribute remaining weight
                accumulator += processed_frame * alpha
                # total_weight += alpha # Optional: track actual total weight if alpha varies more

            # Final normalization/clipping not strictly needed if weights sum ~1.0
            final_result = np.clip(accumulator, 0, 255).astype(np.uint8)

            # --- Post-Processing ---
            # Optional: Enhance contrast of streaks
            # clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
            # final_result = clahe.apply(final_result)

            # Convert back to color if original was color? For B&W effect, keep gray.
            # if img.ndim == 3: final_result = cv2.cvtColor(final_result, cv2.COLOR_GRAY2RGB)
            # Let's force output to be grayscale for this style
            if final_result.ndim == 3: # If accumulation made it color somehow
                final_result = cv2.cvtColor(final_result, cv2.COLOR_RGB2GRAY)

            return final_result
        # --- End apply_temporal_streak ---

        effects.add(apply_temporal_streak)
        if self.config.effect_params.grain > 0:
             effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.35, monochrome=True))
        if self.config.effect_params.vignette > 0:
             effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.45))

        self.engine.add_transformation(effects)


    def _add_ethereal_smudge_style(self) -> None:
        """(V2) Ghostly/Liquid smudge effect using masked iterative warp/blur."""
        effects = EffectChain()

        # Pre-processing: Generally less contrast initially, allow smudge to create it
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.1 + cfg.effect_params.intensity * 0.2))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.1)) # Near B&W

        def apply_ethereal_smudge(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 402
                np.random.seed(seed)
                random.seed(seed)

            # Work in float32
            current_result = img.astype(np.float32)
            height, width = current_result.shape[:2]
            is_color = current_result.ndim == 3
            params = cfg.effect_params

            # --- Parameters ---
            num_steps = 5 + int(params.intensity * 15) # Iterations
            # Smudge Flow: distortion controls randomness/swirl
            flow_noise_scale = params.distortion * 0.8 # Spatial scale of noise
            flow_noise_strength = params.distortion * 3.0 # Magnitude of noise vectors
            flow_base_strength = 0.5 + params.intensity * 1.0 # Base movement speed
            # Smear Blur: blur_radius controls kernel size
            smear_ksize = 3 + int(params.blur_radius * 0.6) # Smaller kernels applied iteratively
            # Structure Preservation: Intensity affects how much detail is kept
            structure_preservation = 0.1 + (1.0 - params.intensity) * 0.6
            # Blend Opacity: Controls ghosting strength per step
            step_opacity = 0.1 + params.intensity * 0.2

            # --- Calculate Structure Mask ---
            if is_color: gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else: gray = img.copy()
            # Higher value = edge/detail = LESS smudging
            structure_map = _normalized_gradient_magnitude(gray, ksize=3, blur_ksize=3)
            # Invert and scale to create the mask where smudging occurs
            # Power sharpens transition: higher power = preserve edges more strictly
            smear_mask = (1.0 - structure_map**(0.5 + structure_preservation*1.5) ) ** 1.5
            smear_mask = cv2.GaussianBlur(smear_mask, (7,7), 0) # Blur mask for smooth transition
            if is_color: smear_mask = cv2.cvtColor(smear_mask, cv2.COLOR_GRAY2RGB)

            # --- Base Meshgrid for Remapping ---
            map_base_x, map_base_y = np.meshgrid(np.arange(width, dtype=np.float32),
                                                 np.arange(height, dtype=np.float32))

            # --- Iterative Smudging ---
            for step in range(num_steps):
                # --- Generate Flow Field for this Step ---
                # Create noise field (approximate Perlin/Simplex with blurred random)
                noise_x = cv2.GaussianBlur((np.random.randn(height, width) * flow_noise_strength).astype(np.float32), (21, 21), flow_noise_scale * 10)
                noise_y = cv2.GaussianBlur((np.random.randn(height, width) * flow_noise_strength).astype(np.float32), (21, 21), flow_noise_scale * 10)
                # Combine with simple base flow (e.g., slight directional drift)
                base_angle = math.radians(random.uniform(0, 360)) # Or parameter controlled
                flow_x = noise_x + math.cos(base_angle) * flow_base_strength
                flow_y = noise_y - math.sin(base_angle) * flow_base_strength # Y inverted

                # --- Apply Small Warp ---
                step_dist = 1.0 # Small distance per step
                map_x = map_base_x + flow_x * step_dist
                map_y = map_base_y + flow_y * step_dist
                # Warp the *current result*
                warped_img = cv2.remap(current_result, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

                # --- Apply Small Blur ---
                if smear_ksize > 1:
                     # Could potentially use directional blur along flow here too (slower)
                     # avg_angle = math.degrees(np.arctan2(np.mean(-flow_y), np.mean(flow_x))) # Average direction
                     # blur_kernel = _create_motion_blur_kernel(smear_ksize, avg_angle)
                     # if blur_kernel is not None:
                     #      blurred_img = cv2.filter2D(warped_img, -1, blur_kernel)
                     # else: blurred_img = warped_img
                     # Simpler: Gaussian blur
                     blurred_img = cv2.GaussianBlur(warped_img, (smear_ksize, smear_ksize), 0)
                else:
                     blurred_img = warped_img

                # --- Blend using Structure Mask & Opacity ---
                # Alpha blend based on mask: result = prev * (1-alpha) + current * alpha
                # Where alpha = step_opacity * smear_mask (high alpha in smooth areas)
                alpha = step_opacity * smear_mask
                current_result = current_result * (1.0 - alpha) + blurred_img * alpha
                # Could also explore Screen blending for brighter ghosting:
                # screen = 1.0 - (1.0 - current_result/255.0) * (1.0 - blurred_img/255.0)
                # current_result = current_result * (1.0 - alpha) + (screen*255.0) * alpha

            # --- Final Output ---
            final_result = np.clip(current_result, 0, 255).astype(np.uint8)

            # Optional final subtle blur
            # ...

            # Force grayscale output? Consistent with references.
            if is_color: final_result = cv2.cvtColor(final_result, cv2.COLOR_RGB2GRAY)


            return final_result
        # --- End apply_ethereal_smudge ---

        effects.add(apply_ethereal_smudge)
        if self.config.effect_params.grain > 0:
            effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.4, monochrome=True))
        if self.config.effect_params.vignette > 0:
            effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.5))

        self.engine.add_transformation(effects)

    # New style methods

    def _add_topographic_depth_style(self) -> None:
        """Add refined Topographic Wave style (v2) with better depth."""
        effects = EffectChain()

        def apply_topographic_depth(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            """Applies the v2 topographic wave effect with depth cues."""
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 201 # Distinct seed offset
                np.random.seed(seed)
                random.seed(seed)

            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img.copy()

            height, width = gray.shape
            params = cfg.effect_params

            # --- Parameters ---
            line_count = int(60 + params.intensity * 50) # Control density
            amplitude_factor = 15 + params.distortion * 60 # Control height/prominence
            base_line_thickness = 1
            max_thickness_multiplier = 2.5 # Max thickness = base * multiplier
            # Vertical distribution focus (0 = top, 1 = full height)
            vertical_focus_end = 0.85
            vertical_focus_start = 0.1

            # More significant blur for very smooth, flowing lines
            blur_radius_px = int(3 + params.blur_radius * 1.0)
            ksize = blur_radius_px * 2 + 1
            gray_smooth = cv2.GaussianBlur(gray, (ksize, ksize), 0)
            # Also keep less blurred version for brightness modulation if needed
            gray_detail = cv2.GaussianBlur(gray, (5,5), 0) if ksize > 5 else gray_smooth


            # --- Colors (Using helper) ---
            bg_color_tuple = _calculate_rgb_color(pal.primary, 0.05, 'darken') # Very dark BG
            line_color_tuple = _calculate_rgb_color(pal.accent, 1.7, 'lighten') # Bright lines

            # --- Canvas & Occlusion Setup ---
            canvas = np.full((height, width, 3), bg_color_tuple, dtype=np.uint8)
            start_y = int(height * vertical_focus_start)
            end_y_for_spacing = int(height * vertical_focus_end)
            line_spacing = max(1, (end_y_for_spacing - start_y) // line_count)
            # Horizon line: keeps track of highest *visible* point per column
            horizon_line = np.full(width, height, dtype=np.int32) # Start horizon at bottom

            # --- Wave Generation (Back to Front) ---
            for i in range(line_count - 1, -1, -1):
                y_base = start_y + i * line_spacing
                if y_base >= height: continue

                sample_y = min(y_base, height - 1)
                # Use heavily blurred image for wave shape
                brightness_wave = gray_smooth[sample_y, :]
                # Use less blurred image for line thickness/intensity modulation
                brightness_detail = gray_detail[sample_y, :]

                current_segment_points: List[Tuple[int, int]] = []
                current_segment_thicknesses: List[float] = []

                for x in range(width):
                    # --- Displacement ---
                    brightness = brightness_wave[x] / 255.0
                    displacement = ((1.0 - brightness) ** 1.7) * amplitude_factor # Use power for contrast
                    y_displaced_float = y_base - displacement

                    # --- Line Thickness ---
                    # Thicker for brighter areas (closer peaks in Joy Division) or higher displacement
                    brightness_mod_detail = brightness_detail[x] / 255.0
                    thickness_mod = (brightness_mod_detail**0.5 + (displacement / amplitude_factor if amplitude_factor > 0 else 0)) / 2.0
                    thickness = base_line_thickness + thickness_mod * (max_thickness_multiplier - base_line_thickness)

                    # --- Noise Perturbation ---
                    if params.noise_level > 0:
                         noise_scale = params.noise_level * 1.5 # Control noise strength
                         x_perturbed = x + (random.random() - 0.5) * noise_scale
                         y_displaced_float += (random.random() - 0.5) * noise_scale
                    else:
                         x_perturbed = float(x)

                    y_displaced = int(round(y_displaced_float))
                    x_rounded = int(round(x_perturbed))


                    # --- Occlusion & Segment Drawing ---
                    # Check if point is visible (above horizon and on screen)
                    is_visible = y_displaced >= 0 and y_displaced < horizon_line[min(max(0, x_rounded), width-1)]

                    if is_visible:
                        # Add point if segment is empty or continues visibility
                        if not current_segment_points or horizon_line[min(max(0, x_rounded-1), width-1)] > y_displaced :
                            current_segment_points.append((x_rounded, y_displaced))
                            current_segment_thicknesses.append(thickness)
                        else: # Point visible but previous was occluded - start new segment
                             if len(current_segment_points) > 1:
                                # Draw previous segment first
                                avg_thickness = int(round(np.mean(current_segment_thicknesses)))
                                pts_np = np.array(current_segment_points, dtype=np.int32)
                                cv2.polylines(canvas, [pts_np], isClosed=False, color=line_color_tuple, thickness=max(1, avg_thickness), lineType=cv2.LINE_AA)
                             # Start new segment
                             current_segment_points = [(x_rounded, y_displaced)]
                             current_segment_thicknesses = [thickness]

                        # Update horizon line smoothly
                        update_y = y_displaced
                        hw = 1 # Horizon smoothing width
                        update_slice = slice(max(0, x_rounded - hw), min(width, x_rounded + hw + 1))
                        horizon_line[update_slice] = np.minimum(horizon_line[update_slice], update_y)

                    else: # Point is occluded or off screen
                        if len(current_segment_points) > 1:
                            # Draw the finished segment
                            avg_thickness = int(round(np.mean(current_segment_thicknesses)))
                            pts_np = np.array(current_segment_points, dtype=np.int32)
                            cv2.polylines(canvas, [pts_np], isClosed=False, color=line_color_tuple, thickness=max(1, avg_thickness), lineType=cv2.LINE_AA)
                        # Reset segment
                        current_segment_points = []
                        current_segment_thicknesses = []


                # Draw final segment for the line if any points remain
                if len(current_segment_points) > 1:
                     avg_thickness = int(round(np.mean(current_segment_thicknesses)))
                     pts_np = np.array(current_segment_points, dtype=np.int32)
                     cv2.polylines(canvas, [pts_np], isClosed=False, color=line_color_tuple, thickness=max(1, avg_thickness), lineType=cv2.LINE_AA)

            return canvas
        # --- End apply_topographic_depth ---

        effects.add(apply_topographic_depth)
        # Add final subtle grain/vignette if desired
        if self.config.effect_params.grain > 0:
            effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.1, monochrome=True))
        if self.config.effect_params.vignette > 0:
            effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.2))

        self.engine.add_transformation(effects)


    def _add_temporal_flow_style(self) -> None:
        """Add Temporal Flow style (v2) using flow fields and iteration."""
        effects = EffectChain()

        # Start with contrast and desaturation
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.6 + cfg.effect_params.intensity * 0.4))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.05)) # Near B&W


        def apply_temporal_flow_remap(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            """Applies iterative flow, blur, and sampling."""
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 301
                np.random.seed(seed)
                random.seed(seed)

            height, width = img.shape[:2]
            params = cfg.effect_params
            result = img.astype(np.float32) # Work in float

            # --- Parameters ---
            num_steps = 8 + int(params.intensity * 12) # Iterations simulating time
            flow_strength = 0.5 + params.distortion * 2.5 # Overall flow speed/distance
            blur_strength = 1 + params.blur_radius * 0.8 # Base blur kernel radius per step
            noise_strength = params.noise_level * 0.5 # Add turbulence to flow
            # Let's bias flow vertically, responding to intensity
            base_flow_angle_deg = 90 # Vertical
            persistence = 0.6 + (1.0 - params.intensity) * 0.3 # How much original shows through

            # --- Calculate Base Flow Field (Gradient-based) ---
            if img.ndim == 3: gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else: gray = img.copy()
            # Smooth before gradient calculation
            gray_smooth = cv2.GaussianBlur(gray, (5,5), 0)
            grad_x = cv2.Sobel(gray_smooth, cv2.CV_32F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray_smooth, cv2.CV_32F, 0, 1, ksize=3)
            # Calculate magnitude and angle of gradient
            magnitude = cv2.magnitude(grad_x, grad_y)
            # Normalize magnitude (0 to 1)
            mag_norm = cv2.normalize(magnitude, None, 0.0, 1.0, cv2.NORM_MINMAX)
            # Angle perpendicular to gradient (for flow along edges) + base vertical bias
            angle_rad = np.arctan2(grad_y, grad_x) + math.pi / 2.0 + math.radians(base_flow_angle_deg - 90)

            # Define base flow vector field (normalized direction * flow strength * magnitude bias)
            # Stronger flow in areas of higher contrast/detail
            flow_scale = flow_strength * (0.5 + mag_norm * 1.5)
            flow_x = np.cos(angle_rad) * flow_scale
            flow_y = np.sin(angle_rad) * flow_scale


            # --- Iterative Process (Simulating Time) ---
            # Store intermediate frames if needed for slit-scan sampling later (optional)
            frames = [result.copy()]
            # Create base maps for remapping
            map_base_x, map_base_y = np.meshgrid(np.arange(width, dtype=np.float32),
                                                 np.arange(height, dtype=np.float32))
            # Accumulate flow map over steps
            acc_flow_x = np.zeros_like(flow_x)
            acc_flow_y = np.zeros_like(flow_y)

            # Initialize accumulator image
            accumulator = np.zeros_like(result, dtype=np.float32)
            weight_sum = 0.0

            # Add initial frame with persistence weight
            accumulator += result * persistence
            weight_sum += persistence


            for step in range(num_steps):
                progress = (step + 1) / num_steps

                # --- Update Accumulated Flow ---
                # Add noise/turbulence that increases over time?
                step_noise_x = (np.random.randn(height, width) * noise_strength * progress).astype(np.float32)
                step_noise_y = (np.random.randn(height, width) * noise_strength * progress).astype(np.float32)
                acc_flow_x += (flow_x + step_noise_x) / num_steps # Average flow increment per step
                acc_flow_y += (flow_y + step_noise_y) / num_steps

                # --- Remap Image based on Accumulated Flow ---
                map_x = map_base_x + acc_flow_x
                map_y = map_base_y + acc_flow_y
                # Clip maps to stay within image bounds
                map_x = np.clip(map_x, 0, width - 1)
                map_y = np.clip(map_y, 0, height - 1)
                remapped_img = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

                # --- Apply Motion Blur along Current Flow ---
                current_blur_strength = int(blur_strength * progress * random.uniform(0.8, 1.2)) # Variable blur
                if current_blur_strength > 0:
                     # Estimate average angle for blur kernel for this step (using accumulated flow)
                     avg_angle = np.arctan2(np.mean(acc_flow_y), np.mean(acc_flow_x))
                     blur_kernel = _create_motion_blur_kernel(current_blur_strength, math.degrees(avg_angle))
                     blurred_img = cv2.filter2D(remapped_img, -1, blur_kernel)
                else:
                     blurred_img = remapped_img

                # --- Accumulate Result ---
                # Weight decreases for later steps (older frames contribute less)
                step_weight = (1.0 - progress) * (1.0 - persistence) # Total weight sums to (1-persistence)
                accumulator += blurred_img.astype(np.float32) * step_weight
                weight_sum += step_weight

                # Store frame if implementing slit-scan variant later
                # frames.append(blurred_img.copy())

            # Normalize accumulated result by total weight
            # Avoid division by zero if weight_sum is somehow zero
            if weight_sum > 1e-6:
                 final_result = accumulator / weight_sum
            else:
                 final_result = accumulator # Should be the original * persistence


            # --- Post-Processing within Effect ---
            final_result = np.clip(final_result, 0, 255).astype(np.uint8)

            # Example: Add subtle sharpening to retain some structure
            # sharp_kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]], dtype=np.float32)
            # final_result = cv2.filter2D(final_result, -1, sharp_kernel)

            return final_result
        # --- End apply_temporal_flow_remap ---

        effects.add(apply_temporal_flow_remap)
        # Add grain/vignette after the main effect
        if self.config.effect_params.grain > 0:
            effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.3, monochrome=True))
        if self.config.effect_params.vignette > 0:
            effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.4))

        self.engine.add_transformation(effects)


    def _add_liquid_ghost_style(self) -> None:
        """Add Liquid Ghost style (v2) using flow, masking, and blending."""
        effects = EffectChain()

        # Initial toning - Desaturated, maybe cool tint
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.4 + cfg.effect_params.intensity * 0.3))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.05))
        # Example cool tint (adjust B channel)
        # effects.add(lambda img, cfg, pal: cool_tint(img, 1.1))


        def apply_liquid_ghost_smear(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            """Applies iterative, masked, flow-driven smearing and blending."""
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 401
                np.random.seed(seed)
                random.seed(seed)

            height, width = img.shape[:2]
            params = cfg.effect_params
            is_color = img.ndim == 3
            current_result = img.astype(np.float32) # Work in float

            # --- Parameters ---
            num_steps = 6 + int(params.intensity * 10)
            # Distortion controls flow complexity/turbulence
            flow_noise_strength = params.distortion * 1.5
            # Blur controls smear length/softness
            max_smear_length = int(15 + params.blur_radius * 25)
            # Intensity affects blend opacity & structure preservation
            blend_opacity = 0.15 + params.intensity * 0.20
            structure_preservation = 0.2 + (1.0 - params.intensity) * 0.5 # Lower intensity = more structure preserved

            # --- Calculate Structure/Gradient Mask ---
            if is_color: gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else: gray = img.copy()
            gray_smooth = cv2.GaussianBlur(gray, (5,5), 0)
            grad_x = cv2.Sobel(gray_smooth, cv2.CV_32F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray_smooth, cv2.CV_32F, 0, 1, ksize=3)
            magnitude = cv2.magnitude(grad_x, grad_y)
            # Normalize magnitude (0=low detail, 1=high detail/edge)
            mag_norm = cv2.normalize(magnitude, None, 0.0, 1.0, cv2.NORM_MINMAX)
            # Create smear mask: high value where smearing should occur (low detail areas)
            # Power function sharpens the transition
            smear_mask = (1.0 - mag_norm**0.8) ** (1.0 + structure_preservation * 2.0)
            # Slightly blur the mask for smoother application
            smear_mask = cv2.GaussianBlur(smear_mask,(5,5),0)
            # Match dimensions if color image
            if is_color: smear_mask = cv2.cvtColor(smear_mask, cv2.COLOR_GRAY2RGB)


            # --- Iterative Smear Application ---
            # Base direction - could be random or parameter controlled
            base_angle_deg = random.uniform(0, 360)

            for step in range(num_steps):
                # --- Define Flow/Smear for this Step ---
                # Calculate smear angle - varies locally and with distortion noise
                # Use gradient angle + base angle + noise
                angle_rad = np.arctan2(grad_y, grad_x) + math.radians(base_angle_deg)
                if flow_noise_strength > 0:
                    noise_angle = (np.random.randn(height, width) * math.pi * flow_noise_strength).astype(np.float32)
                    angle_rad += noise_angle
                angle_deg_map = np.degrees(angle_rad)

                # Calculate smear length for this step - varies with progress
                current_smear_length = int(max_smear_length * random.uniform(0.5, 1.0) * ((step + 1) / num_steps))

                # --- Apply Smear (Blur + Subtle Remap) ---
                smeared_step = current_result.copy()
                if current_smear_length > 1:
                    # Create locally varying motion blur kernels? Too slow. Apply average blur first.
                    avg_angle = np.mean(angle_deg_map)
                    blur_kernel = _create_motion_blur_kernel(current_smear_length, avg_angle)
                    smeared_step = cv2.filter2D(current_result, -1, blur_kernel)

                    # Add subtle displacement along the flow AFTER blur
                    remap_strength = params.distortion * 0.1 * current_smear_length
                    flow_x = np.cos(angle_rad) * remap_strength
                    flow_y = np.sin(angle_rad) * remap_strength
                    map_base_x, map_base_y = np.meshgrid(np.arange(width, dtype=np.float32), np.arange(height, dtype=np.float32))
                    map_x = np.clip(map_base_x + flow_x, 0, width - 1)
                    map_y = np.clip(map_base_y + flow_y, 0, height - 1)
                    smeared_step = cv2.remap(smeared_step, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

                # --- Blend Step Result using Screen and Mask ---
                # Normalize for screen blending
                smeared_norm = smeared_step / 255.0
                base_norm = current_result / 255.0
                # Screen blend
                screen_blended = (1.0 - (1.0 - base_norm) * (1.0 - smeared_norm)) * 255.0

                # Combine using smear mask and blend opacity
                step_alpha = blend_opacity * smear_mask # Apply opacity only where mask allows
                current_result = current_result * (1.0 - step_alpha) + screen_blended * step_alpha

            # --- Final Touches ---
            final_result = np.clip(current_result, 0, 255).astype(np.uint8)
            # Optional: very soft overall blur to blend artefacts
            final_blur_ksize = int(params.blur_radius * 0.1) * 2 + 1
            if final_blur_ksize > 1:
                final_result = cv2.GaussianBlur(final_result, (final_blur_ksize, final_blur_ksize), 0)

            return final_result
        # --- End apply_liquid_ghost_smear ---

        effects.add(apply_liquid_ghost_smear)
        # Add grain/vignette after the main effect
        if self.config.effect_params.grain > 0:
             # Grain adds to the analog/ghostly feel
             effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.45, monochrome=True, grain_size=1.0))
        if self.config.effect_params.vignette > 0:
             effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.5))

        self.engine.add_transformation(effects)

    def _add_topographic_refined_style(self) -> None:
        """Add refined Topographic Wave style transformations."""
        effects = EffectChain()

        def apply_refined_topographic_wave(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            """Applies the core refined topographic wave effect."""
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 200
                np.random.seed(seed)
                random.seed(seed)

            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img.copy()

            height, width = gray.shape
            params = cfg.effect_params

            # --- Parameters ---
            # Fewer lines, potentially thicker, for a bolder look. Intensity controls density.
            line_count = int(50 + params.intensity * 40) # Slightly fewer lines than before
            # Distortion affects amplitude more significantly
            amplitude_factor = 10 + params.distortion * 50
            line_thickness = 2 # Thicker lines
            # Calculate line spacing, prevent division by zero
            line_spacing = max(1, int(height * 0.8 / line_count)) # Space lines out more, use only top 80% height maybe?
            vertical_offset_factor = 0.1 # Start drawing lower down the canvas

            # Blur source image significantly for smoother waves
            blur_radius_px = int(2 + params.blur_radius * 1.5) # More base blur, slightly less scaling
            ksize = blur_radius_px * 2 + 1
            gray = cv2.GaussianBlur(gray, (ksize, ksize), 0)

            # --- Colors ---
            primary_tuple = pal.primary.as_tuple
            # Brighter line color relative to background
            accent_tuple = pal.accent.lighter(0.6).as_tuple if hasattr(pal.accent, 'lighter') else \
                           tuple(min(255, int(c * 1.8)) for c in pal.accent.as_tuple)
            # Darker background
            bg_color_tuple = pal.primary.darker(0.9).as_tuple if hasattr(pal.primary, 'darker') else \
                            tuple(max(0, int(c * 0.1)) for c in primary_tuple)
            # Slightly lighter shadow color for depth if needed (optional)
            # shadow_color = tuple(min(255, int(c*1.1)) for c in bg_color_tuple)


            # --- Canvas Setup ---
            canvas = np.full((height, width, 3), bg_color_tuple, dtype=np.uint8)
            start_y = int(height * vertical_offset_factor)


            # --- Improved Wave Generation & Occlusion ---
            # Keep track of the highest point reached for each column (basic occlusion)
            horizon_line = np.full(width, height, dtype=np.int32) # Start horizon at the bottom

            # Draw lines from back to front (bottom to top) for better occlusion
            for i in range(line_count - 1, -1, -1):
                y_base = start_y + i * line_spacing

                if y_base >= height: continue # Skip lines starting off-canvas

                sample_y = min(y_base, height - 1)
                brightness_values = gray[sample_y, :]

                current_segment_points = []
                for x in range(width):
                    brightness = brightness_values[x] / 255.0
                    # Exponent emphasizes contrast between light/dark peaks
                    displacement = ((1.0 - brightness) ** 1.8) * amplitude_factor
                    if params.noise_level > 0:
                        displacement += (random.random() - 0.5) * params.noise_level * 5.0 # Less noise

                    y_displaced = y_base - int(displacement)

                    # --- Visibility Check ---
                    # Only add point if it's above the current horizon for this column
                    if y_displaced >= 0 and y_displaced < horizon_line[x]:
                         current_segment_points.append((x, y_displaced))
                         # Update the horizon (lower y = higher on screen)
                         # Apply update smoothly across a small width to avoid single pixel spikes
                         hw = 1 # Half-width for horizon smoothing
                         update_y = y_displaced
                         horizon_line[max(0, x-hw) : min(width, x+hw+1)] = \
                             np.minimum(horizon_line[max(0, x-hw) : min(width, x+hw+1)], update_y)
                    else:
                        # Point is hidden or off-canvas, draw previous segment if any
                        if len(current_segment_points) > 1:
                            pts_np = np.array(current_segment_points, dtype=np.int32)
                            # Draw line slightly thicker maybe?
                            cv2.polylines(canvas, [pts_np], isClosed=False, color=accent_tuple, thickness=line_thickness, lineType=cv2.LINE_AA)
                            # Optional: Add a subtle shadow line below for depth
                            # shadow_pts = pts_np + [0, line_thickness]
                            # cv2.polylines(canvas, [shadow_pts], False, shadow_color, 1, cv2.LINE_AA)
                        current_segment_points = [] # Reset segment

                # Draw any final segment for this line
                if len(current_segment_points) > 1:
                     pts_np = np.array(current_segment_points, dtype=np.int32)
                     cv2.polylines(canvas, [pts_np], isClosed=False, color=accent_tuple, thickness=line_thickness, lineType=cv2.LINE_AA)
                     # Optional shadow line
                     # shadow_pts = pts_np + [0, line_thickness]
                     # cv2.polylines(canvas, [shadow_pts], False, shadow_color, 1, cv2.LINE_AA)

            return canvas
        # --- End of apply_refined_topographic_wave ---

        effects.add(apply_refined_topographic_wave)
        if self.config.effect_params.grain > 0:
            effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.05)) # Even more subtle grain
        if self.config.effect_params.vignette > 0:
             effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.15))

        self.engine.add_transformation(effects)


    def _add_long_exposure_scan_style(self) -> None:
        """Add Long Exposure Scan style transformations.

        Simulates temporal smearing and slit-scan effects with a focus
        on motion and ghostly trails, guided by reference images.
        """
        effects = EffectChain()

        # Apply initial high-contrast B&W conversion, similar to reference images
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.8))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.05)) # Near B&W


        def apply_temporal_scan_blur(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            """Applies slit-scan simulation with motion blur layers."""
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 300
                np.random.seed(seed)
                random.seed(seed)

            height, width = img.shape[:2]
            is_color = img.ndim == 3
            params = cfg.effect_params

            # --- Parameters ---
            num_frames = 10 # Number of "virtual" frames to simulate motion
            max_blur_strength = int(5 + params.blur_radius * 1.5) # Kernel size for blur
            max_shift_amount = int(8 + params.distortion * 20) # Pixel shift between frames
            # Intensity affects the opacity/contribution of blurred frames
            effect_intensity = 0.5 + params.intensity * 0.5
            # Vertical smearing bias from references
            base_angle_deg = 90 + random.uniform(-15, 15)


            # --- Generate "Motion" Frames ---
            frames = [img.astype(np.float32)] # Start with original as frame 0
            for i in range(1, num_frames):
                frame_img = img.copy()
                # Calculate progressive shift and blur for this frame
                progress = i / (num_frames - 1) # 0 to 1

                # Shift amount increases progressively
                shift_amount = int(max_shift_amount * progress * random.uniform(0.7, 1.0))
                angle_deg = base_angle_deg + random.uniform(-10, 10) * params.distortion
                angle_rad = math.radians(angle_deg)
                shift_x = int(math.cos(angle_rad) * shift_amount)
                shift_y = int(math.sin(angle_rad) * shift_amount)

                # Apply shift using warpAffine
                M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
                frame_img = cv2.warpAffine(frame_img, M, (width, height), borderMode=cv2.BORDER_REPLICATE)

                # Apply progressive directional motion blur
                blur_strength = int(max_blur_strength * progress * random.uniform(0.7, 1.0))
                if blur_strength > 1:
                    kernel_size = blur_strength * 2 + 1 # Ensure odd kernel size
                    # Create motion blur kernel along the shift direction
                    kernel = np.zeros((kernel_size, kernel_size))
                    center = kernel_size // 2
                    # Correct angle for kernel creation (-90 deg adjustment)
                    angle_rad_kernel = math.radians(angle_deg - 90)
                    x_dir, y_dir = math.cos(angle_rad_kernel), math.sin(angle_rad_kernel)
                    cv2.line(kernel, (center - int(x_dir*(kernel_size//2)), center - int(y_dir*(kernel_size//2))),
                                     (center + int(x_dir*(kernel_size//2)), center + int(y_dir*(kernel_size//2))), 1.0, 1)
                    kernel /= np.sum(kernel) # Normalize
                    frame_img = cv2.filter2D(frame_img, -1, kernel)

                frames.append(frame_img.astype(np.float32))


            # --- Slit-Scan Sampling ---
            result = np.zeros_like(img, dtype=np.float32)
            # Time warp function - determines which frame contributes to which column
            # Use a combination of linear and sinusoidal/noise for organic feel
            time_freq = 0.5 + params.distortion * 2.0
            time_noise_strength = params.noise_level * 0.2

            for x in range(width):
                # Calculate normalized position
                norm_x = x / width
                # Base linear progression through frames
                base_frame_idx = norm_x * (num_frames - 1)
                # Add non-linear warping
                warp_factor = math.sin(norm_x * math.pi * time_freq) * params.distortion * 0.3
                # Add noise
                noise_factor = (random.random() - 0.5) * time_noise_strength
                # Final frame index, clamped
                frame_idx = base_frame_idx + (warp_factor + noise_factor) * (num_frames - 1)
                frame_idx = np.clip(frame_idx, 0, num_frames - 1)

                # Interpolate between the two nearest frames for smoother transition
                frame_floor = int(frame_idx)
                frame_ceil = min(frame_floor + 1, num_frames - 1)
                interp_weight = frame_idx - frame_floor # Weight for the ceiling frame

                # Get columns from the two frames
                col_floor = frames[frame_floor][:, x]
                col_ceil = frames[frame_ceil][:, x]

                # Perform weighted interpolation (lerp)
                interpolated_col = col_floor * (1.0 - interp_weight) + col_ceil * interp_weight

                # Blend into the result using an opacity based on intensity
                # Fade effect slightly towards the edges maybe?
                edge_fade = 1.0 # (1.0 - abs(norm_x - 0.5) * 0.2) # Optional edge fade
                blend_alpha = effect_intensity * edge_fade

                # Combine this column with the original image column for partial effect
                result[:, x] = img[:, x].astype(np.float32) * (1.0 - blend_alpha) + interpolated_col * blend_alpha


            # --- Final Touches ---
            final_result = np.clip(result, 0, 255).astype(np.uint8)

            # Optional: Apply slight overall blur
            final_blur_ksize = int(params.blur_radius * 0.3) * 2 + 1
            if final_blur_ksize > 1:
                final_result = cv2.GaussianBlur(final_result, (final_blur_ksize, final_blur_ksize), 0)

            return final_result
        # --- End of apply_temporal_scan_blur ---

        effects.add(apply_temporal_scan_blur)
        if self.config.effect_params.grain > 0:
             # Grain suits this style well
            effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.4, monochrome=True))
        if self.config.effect_params.vignette > 0:
             effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.5))

        self.engine.add_transformation(effects)


    def _add_ghostly_smear_style(self) -> None:
        """Add Ghostly Smear style transformations.

        Simulates long exposure photography with emphasis on soft,
        directional smearing and transparent layering.
        """
        effects = EffectChain()

        # Initial contrast/toning - often B&W or heavily desaturated
        effects.add(lambda img, cfg, pal: adjust_contrast(img, cfg, pal, 1.5 + cfg.effect_params.intensity * 0.5))
        effects.add(lambda img, cfg, pal: adjust_saturation(img, cfg, pal, 0.1)) # Start near B&W
        # Optional: Apply slight blue/cool toning common in ghostly aesthetics
        # effects.add(lambda img, cfg, pal: cool_tone_effect(img, cfg, pal))

        def apply_directional_smear_blend(img: np.ndarray, cfg: Configuration, pal: ColorPalette) -> np.ndarray:
            """Applies directional blur and blends layers for a ghostly smear."""
            if cfg.effect_params.seed is not None:
                seed = cfg.effect_params.seed + 400
                np.random.seed(seed)
                random.seed(seed)

            height, width = img.shape[:2]
            params = cfg.effect_params
            result = img.astype(np.float32) # Work in float

            # --- Parameters ---
            num_layers = 3 + int(params.intensity * 3) # More layers for stronger effect
            max_blur_strength = int(20 + params.blur_radius * 30) # Kernel size for blur
            max_shift_amount = int(5 + params.distortion * 15) # Less shift, more blur focus
            # Angle variability - allow multiple directions for swirling effect
            angle_mean = random.uniform(0, 360)
            angle_spread = 45 * params.distortion # How much angle varies between layers

            # --- Layer Generation & Blending ---
            # Start with original image slightly faded
            current_image = result * (0.6 + (1.0 - params.intensity) * 0.4)

            for i in range(num_layers):
                layer_img = img.copy() # Start from original each time for cleaner layers
                progress = (i + 1) / num_layers # Use progress for fading/effects

                # --- Apply Layer Effects ---
                # Random angle for this layer's smear
                angle_deg = angle_mean + random.uniform(-angle_spread, angle_spread)
                angle_rad = math.radians(angle_deg)

                # 1. Shift (Subtle)
                shift_amount = int(max_shift_amount * random.uniform(0.5, 1.0))
                shift_x = int(math.cos(angle_rad) * shift_amount)
                shift_y = int(math.sin(angle_rad) * shift_amount)
                M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
                layer_img = cv2.warpAffine(layer_img, M, (width, height), borderMode=cv2.BORDER_REPLICATE)

                # 2. Strong Directional Motion Blur
                blur_strength = int(max_blur_strength * random.uniform(0.4, 1.0))
                if blur_strength > 1:
                    kernel_size = max(5, blur_strength * 2 + 1) # Larger kernels
                    kernel = np.zeros((kernel_size, kernel_size))
                    center = kernel_size // 2
                    angle_rad_kernel = math.radians(angle_deg - 90)
                    x_dir, y_dir = math.cos(angle_rad_kernel), math.sin(angle_rad_kernel)
                    half_length = int((kernel_size // 2) * 0.9) # Make line slightly shorter than kernel
                    pt1 = (center - int(x_dir*half_length), center - int(y_dir*half_length))
                    pt2 = (center + int(x_dir*half_length), center + int(y_dir*half_length))
                    cv2.line(kernel, pt1, pt2, 1.0, 1)
                    kernel /= np.sum(kernel) # Normalize
                    layer_img = cv2.filter2D(layer_img, -1, kernel)


                # 3. Masking (Optional - Feature coherence)
                # Reduce effect on edges/features
                use_masking = params.intensity < 0.8 # Apply masking less at high intensity
                if use_masking:
                    if img.ndim == 3: gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    else: gray = img
                    # Use Canny edges, dilated to create a wider mask
                    edges = cv2.Canny(gray, 50, 150)
                    kernel_dilate = np.ones((5,5),np.uint8)
                    feature_mask = cv2.dilate(edges, kernel_dilate, iterations = 1)
                    feature_mask = feature_mask.astype(np.float32) / 255.0
                    # Invert mask (0 on features, 1 elsewhere)
                    smear_mask = 1.0 - feature_mask
                    if img.ndim == 3: smear_mask = cv2.cvtColor(smear_mask, cv2.COLOR_GRAY2RGB) # Match dimensions
                    # Apply mask: original image * feature_mask + smeared_layer * smear_mask
                    layer_img = img.astype(np.float32) * feature_mask + layer_img.astype(np.float32) * smear_mask

                # --- Blending Layer ---
                # Use 'Screen' or 'Lighten' blend mode for ghostly effect
                # Screen: 1 - (1 - Base) * (1 - Layer)
                # Normalize layer to 0-1
                layer_norm = layer_img.astype(np.float32) / 255.0
                base_norm = current_image / 255.0

                # Calculate screen blend
                screen_blended = 1.0 - (1.0 - base_norm) * (1.0 - layer_norm)

                # Blend using addWeighted with decreasing opacity for later layers
                layer_alpha = 0.4 / (i + 1) # Opacity decreases for subsequent layers
                current_image = cv2.addWeighted(current_image, 1.0, (screen_blended*255), layer_alpha, 0)
                # Alternative: Just use Lighten blending?
                # current_image = np.maximum(current_image, layer_img * (0.7 / (i + 1)))


            # --- Final Touches ---
            final_result = np.clip(current_image, 0, 255).astype(np.uint8)
            # Apply maybe a very soft Gaussian blur overall?
            final_blur_ksize = int(params.blur_radius * 0.2) * 2 + 1
            if final_blur_ksize > 1:
                 final_result = cv2.GaussianBlur(final_result, (final_blur_ksize, final_blur_ksize), 0)

            return final_result
        # --- End of apply_directional_smear_blend ---

        effects.add(apply_directional_smear_blend)
        if self.config.effect_params.grain > 0:
            # Authentic film grain fits well
            effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.5, monochrome=True, grain_size=0.8))
        if self.config.effect_params.vignette > 0:
             # Vignette enhances the mood
             effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.6))

        self.engine.add_transformation(effects)

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
                        displacement_x[y, x] += (
                            intensity * math.sin(y / scale + x / (scale * 1.5)) * 2
                        )
                        displacement_y[y, x] += (
                            intensity * math.cos(x / scale + y / (scale * 1.2)) * 2
                        )

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
        effects.add(
            lambda img, cfg, pal: add_vignette(
                img, cfg, pal, amount=0.5, color=pal.primary.as_tuple
            )
        )

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
                    luminance = (
                        0.299 * blurred[:, :, 0]
                        + 0.587 * blurred[:, :, 1]
                        + 0.114 * blurred[:, :, 2]
                    )

                    # Create a mask for bright areas
                    mask = np.clip((luminance - 100) / 50, 0, 1)

                    # Apply the mask to each channel
                    for c in range(3):
                        # Add the glow component
                        result[:, :, c] += (
                            blurred[:, :, c] * mask * glow_amount * weight
                        )
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
        effects.add(
            lambda img, cfg, pal: duotone(
                img,
                cfg,
                pal,
                pal.additional.get("shadow", pal.primary),
                pal.additional.get("highlight", pal.accent),
            )
        )

        # Add subtle vignette
        effects.add(
            lambda img, cfg, pal: add_vignette(
                img, cfg, pal, amount=0.4, color=pal.primary.as_tuple
            )
        )

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
                result[0:height, 0 : width - shift_x, 0] = img[
                    0:height, shift_x:width, 0
                ]
                # Blue channel shift left
                result[0:height, shift_x:width, 2] = img[
                    0:height, 0 : width - shift_x, 2
                ]

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
                line = img[y_pos : min(y_pos + thickness, height), :].copy()

                # Create shifted version
                if shift > 0:
                    shifted_line = np.zeros_like(line)
                    shifted_line[:, shift:] = line[:, : width - shift]
                else:
                    shift = abs(shift)
                    shifted_line = np.zeros_like(line)
                    shifted_line[:, : width - shift] = line[:, shift:]

                # Blend shifted line with original line for better integration
                blended_line = cv2.addWeighted(
                    line, 1 - line_opacity, shifted_line, line_opacity, 0
                )

                # Place back in image
                result[y_pos : min(y_pos + thickness, height), :] = blended_line

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
                block = img[y : y + block_h, x : x + block_w].copy()

                # Determine offset - smaller offsets for subtlety
                offset_x = random.randint(-10, 10)

                # Ensure destination is within bounds
                dest_x = max(0, min(width - block_w, x + offset_x))

                # Apply with slight transparency for better integration
                if img.ndim == 3:
                    # Blend colors
                    for c in range(3):
                        result[y : y + block_h, dest_x : dest_x + block_w, c] = (
                            result[y : y + block_h, dest_x : dest_x + block_w, c] * 0.2
                            + block[:, :, c] * 0.8
                        )
                else:
                    result[y : y + block_h, dest_x : dest_x + block_w] = (
                        result[y : y + block_h, dest_x : dest_x + block_w] * 0.2
                        + block * 0.8
                    )

            return result

        effects.add(controlled_block_glitches)

        # Add subtle noise for texture
        effects.add(
            lambda img, cfg, pal: add_noise(
                img, cfg, pal, amount=0.03, noise_type="gaussian"
            )
        )

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
                glow_color = (
                    np.array(pal.additional.get("highlight", pal.accent).as_normalized)
                    * 255
                )

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
                        result[y, x] = (
                            result[y, x] * (1 - opacity) + ghost[src_y, src_x] * opacity
                        )

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
        effects.add(
            lambda img, cfg, pal: add_vignette(
                img,
                cfg,
                pal,
                amount=0.4,
                color=(220, 225, 255),  # Light blue vignette
            )
        )

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
                (15, 0),  # Horizontal right
                (-12, 0),  # Horizontal left
                (0, 10),  # Vertical down
                (0, -8),  # Vertical up
                (7, 7),  # Diagonal down-right
                (-7, -7),  # Diagonal up-left
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
                src_region = img[
                    src_y_start : src_y_start + (y_end - y_start),
                    src_x_start : src_x_start + (x_end - x_start),
                ]

                # Apply blur
                blurred = cv2.GaussianBlur(src_region, (0, 0), blur_amount).astype(
                    np.float32
                )

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
            hue_shift = np.where(
                brightness < 0.5,
                (0.5 - brightness) * 20,  # Blue shift for shadows
                (brightness - 0.5) * -10,
            )  # Warm shift for highlights

            # Apply shifts
            h = np.mod(h + hue_shift, 180)

            # Slightly boost saturation in midtones
            midtone_mask = 1 - np.abs(brightness - 0.5) * 4  # Peaks at 0.5 brightness
            midtone_mask = np.clip(midtone_mask, 0, 1)
            s = s * (1 + midtone_mask * 0.2)
            s = np.clip(s, 0, 255)

            # Merge channels
            hsv_result = cv2.merge([h, s, v])

            # Convert back to RGB
            return cv2.cvtColor(hsv_result.astype(np.uint8), cv2.COLOR_HSV2RGB)

        effects.add(subtle_color_shift)

        # Add slight vignette
        effects.add(
            lambda img, cfg, pal: add_vignette(
                img, cfg, pal, amount=0.3, center=None, strength=1.2
            )
        )

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
                        cv2.polylines(
                            result, [np.array(points)], False, (255, 255, 255), 1
                        )
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
                        cv2.polylines(
                            result, [np.array(points)], False, (255, 255, 255), 1
                        )

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
                img,
                cfg,
                pal,
                amount=0.4,
                grain_size=0.5,  # Finer grain for more subtle texture
                monochrome=True,
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
            map_x += spiral_strength * np.cos(angle) * np.exp(-radius / (width * 0.3))
            map_y += spiral_strength * np.sin(angle) * np.exp(-radius / (height * 0.3))

            # Normalize the maps to valid image coordinates
            map_x = np.clip(map_x, 0, width - 1)
            map_y = np.clip(map_y, 0, height - 1)

            # Remap the image
            return cv2.remap(
                img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE
            )

        effects.add(chaotic_displacement)

        # Apply extreme pixel sorting with varied thresholds
        effects.add(
            lambda img, cfg, pal: pixel_sort(
                img,
                cfg,
                pal,
                threshold=random.uniform(0.3, 0.7),
                sort_direction=random.choice(["horizontal", "vertical", "both"]),
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
                dist = np.sqrt((y_grid - center_y) ** 2 + (x_grid - center_x) ** 2)
                mask = np.clip(dist / (h / 2), 0, 1.0)

                # Apply varied hue shift based on mask
                shift_amount = random.uniform(20, 60)
                hsv[:, :, 0] = (hsv[:, :, 0] + shift_amount * mask) % 180

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
                pal.accent.as_tuple,
            ]
            if "highlight" in pal.additional:
                shift_colors.append(pal.additional["highlight"].as_tuple)
            if "mist" in pal.additional:
                shift_colors.append(pal.additional["mist"].as_tuple)

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
                region = img[y : y + region_h, x : x + region_w].copy()

                # Apply subtle color tint from palette
                color = random.choice(shift_colors)
                color_overlay = np.ones_like(region) * np.array(color, dtype=np.uint8)
                tinted_region = cv2.addWeighted(region, 0.85, color_overlay, 0.15, 0)

                # Apply to result with slight transparency
                result[
                    target_y : target_y + region_h, target_x : target_x + region_w
                ] = tinted_region

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
            line_color = pal.additional.get("shadow", (10, 10, 15))
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
                        result[y : y + line_width, :, c] = (
                            result[y : y + line_width, :, c] * (1 - line_alpha)
                            + line_color[c] * line_alpha
                        ).astype(np.uint8)

            return result

        effects.add(refined_scan_lines)

        # Add film-like grain instead of digital noise
        grain_amount = 0.25
        effects.add(
            lambda img, cfg, pal: add_grain(
                img,
                cfg,
                pal,
                amount=grain_amount,
                grain_size=0.7,  # More film-like
                monochrome=True,
            )
        )

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
                freq_x = (
                    0.001 + random.random() * 0.005
                )  # Lower frequencies for smoother flows
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
            return cv2.remap(
                img, map_x, map_y, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
            )

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
                shifted = cv2.warpAffine(
                    blurred, M, (width, height), borderMode=cv2.BORDER_REPLICATE
                )

                # Blend with decreasing opacity
                alpha = 0.3 / (i + 1)
                result = cv2.addWeighted(
                    result, 1.0, shifted.astype(np.float32), alpha, 0
                )

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
                highlight_boost=1.7,
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
                hsv[:, :, 1] = np.clip(hsv[:, :, 1] * s_factor, 0, 255)

                # Convert back to RGB
                return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

            return glowing

        effects.add(natural_glow)

        # Add organic texture with film grain
        grain_amount = 0.2
        effects.add(
            lambda img, cfg, pal: add_grain(
                img,
                cfg,
                pal,
                amount=grain_amount,
                grain_size=0.8,  # Larger grain for more natural look
            )
        )

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
            seed = (
                cfg.effect_params.seed
                if cfg.effect_params.seed is not None
                else random.randint(0, 10000)
            )
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
                    grid_c = grid[:, :, c].astype(np.float32) / 255.0
                    img_c = result[:, :, c].astype(np.float32) / 255.0
                    mask_f = mask.astype(np.float32) / 255.0

                    # Apply grid with mask
                    result[:, :, c] = (
                        (1 - alpha) * img_c + alpha * grid_c * mask_f
                    ) * 255

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
                    shadows = gradient * 1.5
                    result[:, :, c] = result[:, :, c] * (1.0 - shadows * 0.9)

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
            c1 = np.array([color1[0] / 255.0, color1[1] / 255.0, color1[2] / 255.0])
            c2 = np.array([color2[0] / 255.0, color2[1] / 255.0, color2[2] / 255.0])

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
                        displacement_x[y, x] += (
                            intensity * math.sin(y / scale + x / (scale * 1.5)) * 2
                        )
                        displacement_y[y, x] += (
                            intensity * math.cos(x / scale + y / (scale * 1.2)) * 2
                        )

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
        effects.add(
            lambda img, cfg, pal: add_vignette(
                img, cfg, pal, amount=0.5, color=pal.primary.as_tuple
            )
        )

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
            lines = cv2.HoughLinesP(
                edges, 1, np.pi / 180, threshold=80, minLineLength=40, maxLineGap=10
            )

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
            edge_strength = cv2.GaussianBlur(
                edges.astype(np.float32) / 255.0, (0, 0), 3
            )

            # Create variable strength flow based on image content
            for y in range(height):
                for x in range(width):
                    # Scale flow by local edge strength and intensity
                    local_strength = (
                        edge_strength[y, x]
                        * (1.0 + gray[y, x] / 255.0)
                        * cfg.effect_params.intensity
                        * 35
                    )
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
                    value += amplitude * math.sin(
                        (x * frequency / width * 6.28)
                        + (y * frequency / height * 6.28 * 0.7)
                    )
                    value += amplitude * math.cos(
                        (y * frequency / height * 6.28)
                        + (x * frequency / width * 6.28 * 0.5)
                    )

                    # Adjust parameters for next octave
                    amplitude *= 0.5
                    frequency *= 2.0

                return value * scale

            # Generate the displacement map with organic flow
            intensity = cfg.effect_params.intensity * 12.0

            for y in range(height):
                for x in range(width):
                    # Create varied flow patterns
                    displacement_x[y, x] = organic_flow(
                        x, y, scale=intensity, octaves=4
                    )
                    displacement_y[y, x] = organic_flow(
                        y, x, scale=intensity, octaves=4
                    )

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
                luminance_diff = (
                    enhanced_gray.astype(np.float32) - gray.astype(np.float32)
                ) * 0.7

                # Add luminance enhancement to each channel while preserving color
                for c in range(3):
                    result[:, :, c] = np.clip(
                        result[:, :, c] + luminance_diff, 0, 255
                    ).astype(np.uint8)
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
                    result[:, :, c] = np.clip(
                        result[:, :, c] + edges * edge_strength * 30, 0, 255
                    ).astype(np.uint8)
            else:
                result = np.clip(result + edges * edge_strength * 30, 0, 255).astype(
                    np.uint8
                )

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
                luminance = lab[:, :, 0] / 255.0

                for c in range(3):
                    # Apply stronger grain in shadows, less in highlights
                    grain_mask = grain * (1.0 - luminance * 0.5) * grain_amount * 30
                    result[:, :, c] = np.clip(result[:, :, c] + grain_mask, 0, 255)
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
                luminance = (
                    0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
                )
            else:
                luminance = img.copy()

            # Create highlight mask
            highlight_threshold = 180
            highlight_mask = np.clip(
                (luminance - highlight_threshold) / (255 - highlight_threshold), 0, 1
            )

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
                    result[:, :, c] = np.clip(
                        result[:, :, c] + combined_bloom * halation_strength * 60,
                        0,
                        255,
                    )
            else:
                result = np.clip(
                    result + combined_bloom * halation_strength * 60, 0, 255
                )

            return result.astype(np.uint8)

        effects.add(apply_light_halation)

        # Final vignette effect to complete the analog look
        def apply_subtle_vignette(img, cfg, pal):
            height, width = img.shape[:2]
            result = img.copy()

            # Create natural-looking vignette mask
            center_x, center_y = width / 2, height / 2
            max_dist = np.sqrt(center_x**2 + center_y**2)

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
                    result[:, :, c] = np.clip(
                        result[:, :, c] * vignette, 0, 255
                    ).astype(np.uint8)
            else:
                result = np.clip(result * vignette, 0, 255).astype(np.uint8)

            return result

        effects.add(apply_subtle_vignette)

        self.engine.add_transformation(effects)

    def _add_topographic_wave_style(self) -> None:
        """Add Topographic Wave style transformations.

        Inspired by the Joy Division "Unknown Pleasures" cover, this style
        converts image brightness into stacked wave patterns.
        """
        effects = EffectChain()

        # --- Complete apply_topographic_wave function definition ---
        def apply_topographic_wave(img: np.ndarray, cfg: Configuration, pal) -> np.ndarray:
            """Applies the core topographic wave effect."""
            # Ensure reproducibility for this specific effect step
            if cfg.effect_params.seed is not None:
                # Use a distinct seed for this step if global seed is set
                current_seed = cfg.effect_params.seed + 100
                np.random.seed(current_seed)
                random.seed(current_seed)

            # Convert to grayscale for brightness mapping
            if img.ndim == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            else:
                gray = img.copy()

            height, width = gray.shape
            params = cfg.effect_params

            # Determine parameters based on config
            # Intensity controls density, distortion controls height
            line_count = int(60 + params.intensity * 60)
            amplitude_factor = 15 + params.distortion * 40
            line_thickness = 1 # Keep lines thin
            line_spacing = max(1, height // line_count) # Ensure spacing is at least 1

            # --- Color Calculation Correction ---
            # Get base colors as tuples
            primary_tuple = pal.primary.as_tuple
            accent_tuple = pal.accent.as_tuple

            # Calculate darker background color manually
            # Factor < 1 darkens, clamp values at 0
            darken_factor = 0.15 # Make it very dark
            bg_color = tuple(max(0, int(c * darken_factor)) for c in primary_tuple)

            # Calculate lighter line color manually
            # Factor > 1 lightens, clamp values at 255
            lighten_factor = 1.6 # Make it brighter
            line_color = tuple(min(255, int(c * lighten_factor)) for c in accent_tuple)
            # --- End Color Calculation Correction ---

            # Create blank canvas (using calculated background color) - ONCE before loop
            canvas = np.full((height, width, 3), bg_color, dtype=np.uint8)

            # Optional: Gaussian blur for smoother waves based on blur param
            blur_radius_px = int(params.blur_radius * 0.5) # Convert param (0-50) to reasonable pixel value
            if blur_radius_px >= 1:
                # Gaussian kernel size must be odd
                ksize = blur_radius_px * 2 + 1
                gray = cv2.GaussianBlur(gray, (ksize, ksize), 0)
                # print(f"Applying Gaussian blur with ksize={ksize}") # Debug print

            # --- Wave Generation Logic ---
            # Process horizontal lines with vertical displacement based on brightness
            for i in range(line_count):
                y_base = i * line_spacing # Base y-position for this line

                # Ensure y_base is within valid image bounds for sampling brightness
                sample_y = min(y_base, height - 1)
                if sample_y < 0: continue # Should not happen with line_spacing >= 1

                # Extract brightness values along the sampled horizontal line
                brightness_values = gray[sample_y, :]

                # --- Build points for the current line segment ---
                current_line_segment_points = []
                for x in range(width):
                    brightness = brightness_values[x] / 255.0 # Normalize brightness to 0-1
                    # Invert brightness for displacement (darker areas have higher peaks)
                    # Apply exponent for sharper peaks if desired (e.g., ** 1.5 or ** 2.0)
                    displacement = ((1.0 - brightness) ** 1.5) * amplitude_factor

                    # Optional: Add minor random perturbation based on noise parameter
                    if params.noise_level > 0:
                         displacement += (random.random() - 0.5) * params.noise_level * 8.0 # Scaled noise

                    # Calculate final y-coordinate (displace upwards from base)
                    y_displaced = y_base - int(displacement)

                    # --- Simple Occlusion & Line Segment Handling ---
                    # If the point is above the canvas top, break the current line segment
                    if y_displaced < 0:
                        if len(current_line_segment_points) > 1:
                            # Draw the completed segment before breaking
                            pts_np = np.array(current_line_segment_points, dtype=np.int32)
                            cv2.polylines(canvas, [pts_np], isClosed=False, color=line_color, thickness=line_thickness, lineType=cv2.LINE_AA)
                        current_line_segment_points = [] # Start a new empty segment
                    else:
                         # If the point is visible, add it to the current segment
                        current_line_segment_points.append((x, y_displaced))

                # --- Draw any remaining points after the inner loop finishes ---
                if len(current_line_segment_points) > 1:
                    pts_np = np.array(current_line_segment_points, dtype=np.int32)
                    cv2.polylines(canvas, [pts_np], isClosed=False, color=line_color, thickness=line_thickness, lineType=cv2.LINE_AA)
            # --- End Wave Generation Loop ---

            return canvas
        # --- End of apply_topographic_wave function definition ---


        # Add the core effect function to the processing chain
        effects.add(apply_topographic_wave)

        # Optional: Add subtle overall grain AFTER the main effect if configured
        if self.config.effect_params.grain > 0:
             # Keep grain very subtle for this style
            effects.add(lambda img, cfg, pal: add_grain(img, cfg, pal, amount=cfg.effect_params.grain * 0.1))

        # Optional: Add a very faint vignette AFTER the main effect if configured
        if self.config.effect_params.vignette > 0:
            effects.add(lambda img, cfg, pal: add_vignette(img, cfg, pal, amount=cfg.effect_params.vignette * 0.2))

        # Add the configured effects chain to the engine for processing
        self.engine.add_transformation(effects)

    def _add_slit_scan_style(self) -> None:
        """Add Slit-Scan distortion style transformations.

        Simulates the effect of slit-scan photography by taking slices
        from differently distorted versions of the input image and stitching them.
        """
        effects = EffectChain()

        # Define the core slit-scan simulation function
        def apply_slit_scan_simulation(
            img: np.ndarray, cfg: Configuration, pal
        ) -> np.ndarray:
            # Ensure reproducibility
            if cfg.effect_params.seed is not None:
                np.random.seed(cfg.effect_params.seed + 2)
                random.seed(cfg.effect_params.seed + 2)

            height, width = img.shape[:2]
            params = cfg.effect_params

            # Number of "time slices" corresponds to the width (for horizontal scan)
            num_slices = width
            # Create an empty canvas for the result
            result = np.zeros_like(img)

            # Base distortion amount - scales with intensity
            base_distortion = params.distortion * 0.5
            intensity_scale = params.intensity * 1.5

            # Use a non-linear progression for distortion (e.g., sinusoidal)
            # for more interesting visual flow than simple linear increase
            max_displacement = (
                30 * intensity_scale
            )  # Max pixel displacement for distortion

            # Prepare parameters for wave distortion or remap
            map_x_base, map_y_base = np.meshgrid(
                np.arange(width, dtype=np.float32), np.arange(height, dtype=np.float32)
            )

            # --- Slice Generation and Stitching ---
            # Simulate temporal evolution by varying distortion across slices
            for i in range(num_slices):
                # Calculate the distortion strength for this slice (non-linear)
                # Example: Use a sine wave based on slice position 'i'
                current_phase = (
                    (i / num_slices) * math.pi * 2
                )  # Full cycle across the width
                distortion_factor = (
                    base_distortion
                    + (math.sin(current_phase) + 1) / 2 * intensity_scale * 0.8
                )

                # Create a distorted version of the image for this "time slice"
                # Using cv2.remap for controlled distortion is efficient here
                map_x = map_x_base.copy()
                map_y = map_y_base.copy()

                # Apply a wave distortion that changes with 'i'
                wave_amplitude = max_displacement * distortion_factor
                wave_freq = (
                    0.01 + distortion_factor * 0.02
                )  # Frequency changes slightly too

                # Modify map_x and map_y based on distortion parameters
                # Simple example: Add wave offset to map_x
                map_x += wave_amplitude * np.sin(map_y * wave_freq + current_phase)
                # Could add more complex distortion here (e.g., pinching, swirling)

                # Apply the displacement map using remap
                distorted_img = cv2.remap(
                    img,
                    map_x,
                    map_y,
                    interpolation=cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_REPLICATE,
                )

                # Optionally apply other subtle per-slice effects (e.g., slight blur, color shift)
                if params.blur_radius > 0.1:
                    blur_ksize = (
                        int(params.blur_radius * distortion_factor * 0.5) * 2 + 1
                    )
                    if blur_ksize > 1:
                        distorted_img = cv2.GaussianBlur(
                            distorted_img, (blur_ksize, blur_ksize), 0
                        )

                # Optionally add a subtle color shift per slice
                if img.ndim == 3 and params.noise_level > 0.1:
                    shift_amount = (
                        (np.random.rand(3) - 0.5)
                        * params.noise_level
                        * 20
                        * distortion_factor
                    )
                    distorted_img = np.clip(
                        distorted_img.astype(np.float32) + shift_amount, 0, 255
                    ).astype(np.uint8)

                # Take the i-th column (the "slit") from the distorted image
                if i < width:  # Ensure index is within bounds
                    result[:, i] = distorted_img[:, i]

            return result

        # Add initial contrast/brightness adjustments
        effects.add(
            lambda img, cfg, pal: adjust_contrast(
                img, cfg, pal, 1.0 + cfg.effect_params.intensity * 0.3
            )
        )
        effects.add(
            lambda img, cfg, pal: adjust_saturation(
                img, cfg, pal, 1.0 - cfg.effect_params.intensity * 0.2
            )
        )

        # Add the core slit-scan effect
        effects.add(apply_slit_scan_simulation)

        # Optional: Add a slight motion blur effect *after* slit-scan
        def apply_post_motion_blur(
            img: np.ndarray, cfg: Configuration, pal
        ) -> np.ndarray:
            params = cfg.effect_params
            blur_strength = int(params.blur_radius * 0.8)  # Control blur amount
            if blur_strength <= 1:
                return img

            kernel_size = blur_strength
            # Create horizontal motion blur kernel
            kernel = np.zeros((kernel_size, kernel_size))
            kernel[kernel_size // 2, :] = 1.0 / kernel_size

            # Apply kernel
            blurred = cv2.filter2D(img, -1, kernel)
            return blurred

        effects.add(apply_post_motion_blur)

        # Optional: Add grain for texture
        effects.add(
            lambda img, cfg, pal: add_grain(
                img, cfg, pal, amount=cfg.effect_params.grain * 0.3
            )
        )

        # Optional: Add vignette
        effects.add(
            lambda img, cfg, pal: add_vignette(
                img, cfg, pal, amount=cfg.effect_params.vignette * 0.4
            )
        )

        self.engine.add_transformation(effects)

    def _add_smudge_flow_style(self) -> None:
        """Add Smear/Smudge style transformations.

        Creates effects resembling digital smudging or smearing, often
        involving directional blur and pixel displacement.
        """
        effects = EffectChain()

        # Define the core smudging/smearing function
        def apply_smudge_flow(img: np.ndarray, cfg: Configuration, pal) -> np.ndarray:
            # Ensure reproducibility
            if cfg.effect_params.seed is not None:
                np.random.seed(cfg.effect_params.seed + 3)
                random.seed(cfg.effect_params.seed + 3)

            height, width = img.shape[:2]
            params = cfg.effect_params
            result = img.copy()  # Start with original

            # Smudge parameters
            smudge_intensity = params.intensity  # Use intensity directly
            smudge_strength = (
                15 + smudge_intensity * 40
            )  # Max pixel displacement/blur size
            smudge_angle_deg = random.uniform(
                0, 360
            )  # Base direction, add randomness later
            smudge_iterations = int(2 + smudge_intensity * 5)  # Number of smear passes

            # --- Smearing Logic ---
            # Combine directional blur and displacement for a robust smudge
            for iteration in range(smudge_iterations):
                # Vary angle slightly per iteration for more organic flow
                current_angle_deg = (
                    smudge_angle_deg + random.uniform(-20, 20) * params.distortion
                )
                current_strength = smudge_strength * (
                    1.0 - iteration * 0.1
                )  # Decrease strength slightly

                # 1. Directional Motion Blur component
                kernel_size = max(3, int(current_strength * 0.6))  # Blur kernel size
                kernel = np.zeros((kernel_size, kernel_size))
                center = kernel_size // 2

                # Convert angle for kernel generation
                angle_rad_kernel = np.deg2rad(
                    current_angle_deg - 90
                )  # Adjust for kernel orientation
                x_dir_k, y_dir_k = np.cos(angle_rad_kernel), np.sin(angle_rad_kernel)

                # Create line on kernel
                for i in range(kernel_size):
                    offset = i - center
                    x_k = center + offset * x_dir_k
                    y_k = center + offset * y_dir_k
                    if 0 <= int(y_k) < kernel_size and 0 <= int(x_k) < kernel_size:
                        kernel[int(y_k), int(x_k)] = 1

                # Normalize kernel
                if np.sum(kernel) > 0:
                    kernel = kernel / np.sum(kernel)
                else:  # Avoid division by zero if kernel is empty
                    kernel[center, center] = 1.0

                # Apply the directional blur
                motion_blurred = cv2.filter2D(result, -1, kernel)

                # 2. Pixel Displacement (Remap) component
                map_x, map_y = np.meshgrid(
                    np.arange(width, dtype=np.float32),
                    np.arange(height, dtype=np.float32),
                )

                # Calculate displacement vector based on angle
                angle_rad_disp = np.deg2rad(current_angle_deg)
                disp_x = (
                    np.cos(angle_rad_disp) * current_strength * 0.4
                )  # Displacement scale
                disp_y = np.sin(angle_rad_disp) * current_strength * 0.4

                # Modulate displacement by image brightness (smear more in darker areas?)
                if result.ndim == 3:
                    gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
                else:
                    gray = result.copy()

                # Normalize brightness 0-1, potentially invert (darker = more smear)
                brightness_mod = (1.0 - (gray.astype(np.float32) / 255.0)) ** 1.2

                # Apply displacement modulated by brightness
                map_x += disp_x * brightness_mod
                map_y += disp_y * brightness_mod

                # Ensure maps are within bounds
                map_x = np.clip(map_x, 0, width - 1)
                map_y = np.clip(map_y, 0, height - 1)

                # Apply displacement using remap
                displaced_img = cv2.remap(
                    result,
                    map_x,
                    map_y,
                    interpolation=cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_REPLICATE,
                )

                # 3. Blend the components
                # Blend motion blur, displacement, and previous result
                blend_factor_blur = (
                    0.4 + params.distortion * 0.2
                )  # How much blur contributes
                blend_factor_disp = (
                    0.4 + smudge_intensity * 0.2
                )  # How much displacement contributes

                # Weighted blend for this iteration
                alpha = 0.6 + smudge_intensity * 0.3  # Weight towards the new smear
                result = cv2.addWeighted(
                    result, 1.0 - alpha, motion_blurred, alpha * blend_factor_blur, 0
                )
                result = cv2.addWeighted(
                    result, 1.0 - alpha, displaced_img, alpha * blend_factor_disp, 0
                )

            return result

        # Initial adjustments
        effects.add(
            lambda img, cfg, pal: adjust_contrast(
                img, cfg, pal, 1.0 + cfg.effect_params.intensity * 0.2
            )
        )
        effects.add(
            lambda img, cfg, pal: adjust_saturation(
                img, cfg, pal, 1.0 - cfg.effect_params.distortion * 0.1
            )
        )

        # Add the core smudging effect
        effects.add(apply_smudge_flow)

        # Optional: Enhance edges slightly after smudging to regain some definition
        effects.add(
            lambda img, cfg, pal: enhance_edges(
                img, cfg, pal, amount=cfg.effect_params.intensity * 0.3
            )
        )

        # Optional: Add grain
        effects.add(
            lambda img, cfg, pal: add_grain(
                img, cfg, pal, amount=cfg.effect_params.grain * 0.35
            )
        )

        # Optional: Add vignette
        effects.add(
            lambda img, cfg, pal: add_vignette(
                img, cfg, pal, amount=cfg.effect_params.vignette * 0.4
            )
        )

        self.engine.add_transformation(effects)
