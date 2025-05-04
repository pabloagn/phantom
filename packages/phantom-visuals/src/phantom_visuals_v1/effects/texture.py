# packages/phantom-visuals/phantom_visuals/effects/texture.py

"""Texture effects for adding grain, noise, and other organic qualities.

This module provides effects for adding texture and organic qualities
to images for a more tactile, analog feel.
"""

from typing import Optional, Tuple, List, Union, Any
import math
import random
import numpy as np
import cv2
from scipy import ndimage

from phantom_visuals.core.config import Configuration
from phantom_visuals.core.palette import ColorPalette


def add_noise(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    amount: Optional[float] = None,
    noise_type: str = "gaussian",
) -> np.ndarray:
    """Add random noise to an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        amount: Noise intensity (defaults to config.effect_params.noise_level)
        noise_type: Type of noise ("gaussian", "salt_pepper", "poisson", "speckle")

    Returns:
        Noisy image as numpy array
    """
    if amount is None:
        amount = config.effect_params.noise_level

    # If amount is 0, return the original image
    if amount <= 0:
        return image

    # Make a copy of the input image
    result = image.copy().astype(np.float32)

    # Set random seed if specified
    if config.effect_params.seed is not None:
        np.random.seed(config.effect_params.seed)

    # Apply noise based on type
    if noise_type == "gaussian":
        # Apply Gaussian noise
        sigma = amount * 25.0
        noise = np.random.normal(0, sigma, image.shape).astype(np.float32)
        result = result + noise

    elif noise_type == "salt_pepper":
        # Apply salt & pepper noise
        s_vs_p = 0.5  # Ratio of salt to pepper
        amount = min(amount, 0.005 * amount * 20)  # Scale down the amount

        # Generate salt noise (white)
        salt = np.random.random(image.shape[:2]) < amount * s_vs_p

        # Generate pepper noise (black)
        pepper = np.random.random(image.shape[:2]) < amount * (1 - s_vs_p)

        # Apply salt noise
        if image.ndim == 3:
            for c in range(image.shape[2]):
                result[:, :, c][salt] = 255
                result[:, :, c][pepper] = 0
        else:
            result[salt] = 255
            result[pepper] = 0

    elif noise_type == "poisson":
        # Apply Poisson noise (good for simulating sensor noise)
        # First normalize to 0-1
        result = result / 255.0

        # Apply noise and scale
        noise_scale = amount * 40.0
        result = np.random.poisson(result * noise_scale) / noise_scale

        # Scale back to 0-255
        result = result * 255.0

    elif noise_type == "speckle":
        # Apply speckle noise (multiplicative noise)
        sigma = amount * 0.5
        noise = np.random.normal(0, sigma, image.shape).astype(np.float32)
        result = result * (1 + noise)

    # Clip values to valid range
    return np.clip(result, 0, 255).astype(np.uint8)



def add_grain(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    amount: Optional[float] = None,
    grain_size: float = 1.0,
    monochrome: bool = True,
) -> np.ndarray:
    """Add film grain effect to an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        amount: Grain intensity (defaults to config.effect_params.grain)
        grain_size: Size of grain particles (1.0 = normal)
        monochrome: If True, apply the same grain to all channels

    Returns:
        Grainy image as numpy array
    """
    if amount is None:
        amount = config.effect_params.grain

    # If amount is 0, return the original image
    if amount <= 0:
        return image

    # Set random seed if specified
    if config.effect_params.seed is not None:
        np.random.seed(config.effect_params.seed)

    # Get image dimensions
    height, width = image.shape[:2]

    # Create grain noise
    if monochrome or image.ndim < 3:
        # Calculate noise dimensions based on grain size
        noise_h = max(1, int(height / grain_size))
        noise_w = max(1, int(width / grain_size))

        # Generate noise
        noise = np.random.normal(0, 1, (noise_h, noise_w)).astype(np.float32)

        # Apply Gaussian blur to create more organic grain
        sigma = max(0.1, 0.5 / grain_size)
        noise = cv2.GaussianBlur(noise, (0, 0), sigma)

        # Resize noise to match image dimensions
        noise = cv2.resize(noise, (width, height), interpolation=cv2.INTER_LINEAR)

        # Normalize noise to have a specific standard deviation
        noise = noise / np.std(noise) * amount * 25.0

        # Convert to float for calculations
        result = image.astype(np.float32)

        # Apply grain
        if image.ndim == 3:
            # Apply the same noise to all channels
            for c in range(image.shape[2]):
                result[:, :, c] = result[:, :, c] + noise
        else:
            result = result + noise

    else:
        # Apply different grain to each channel
        result = image.astype(np.float32)

        for c in range(image.shape[2]):
            # Calculate noise dimensions based on grain size
            noise_h = max(1, int(height / grain_size))
            noise_w = max(1, int(width / grain_size))

            # Generate noise for this channel
            channel_noise = np.random.normal(0, 1, (noise_h, noise_w)).astype(
                np.float32
            )

            # Apply Gaussian blur
            sigma = max(0.1, 0.5 / grain_size)
            channel_noise = cv2.GaussianBlur(channel_noise, (0, 0), sigma)

            # Resize noise
            channel_noise = cv2.resize(
                channel_noise, (width, height), interpolation=cv2.INTER_LINEAR
            )

            # Normalize noise
            channel_noise = channel_noise / np.std(channel_noise) * amount * 25.0

            # Apply to this channel
            result[:, :, c] = result[:, :, c] + channel_noise

    # Clip values to valid range
    return np.clip(result, 0, 255).astype(np.uint8)



def add_vignette(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    amount: Optional[float] = None,
    center: Optional[tuple[float, float]] = None,
    strength: float = 1.0,
    color=None,
) -> np.ndarray:
    """Add vignette effect (darkened corners) to an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (used for vignette color if not black)
        amount: Vignette size/intensity (defaults to config.effect_params.vignette)
        center: Vignette center as (x, y) in range 0-1 (defaults to image center)
        strength: Opacity of the vignette effect
        color: Color of vignette (defaults to black or palette.primary if dark style)

    Returns:
        Image with vignette effect as numpy array
    """
    if amount is None:
        amount = config.effect_params.vignette

    # If amount is 0, return the original image
    if amount <= 0:
        return image

    # Get image dimensions
    height, width = image.shape[:2]

    # Set default center to middle of image if not specified
    if center is None:
        center = (0.5, 0.5)

    # Calculate center coordinates in pixels
    center_x = int(center[0] * width)
    center_y = int(center[1] * height)

    # Create a radial gradient for the vignette
    y, x = np.mgrid[0:height, 0:width]

    # Calculate distance from center
    dist_x = (x - center_x) / width
    dist_y = (y - center_y) / height

    # Create normalized distance map (0-1)
    dist_map = np.sqrt(dist_x**2 + dist_y**2)

    # Normalize by the maximum distance from center to corner
    max_dist = np.sqrt(
        max(center[0], 1 - center[0]) ** 2 + max(center[1], 1 - center[1]) ** 2
    )
    dist_map = dist_map / max_dist

    # Create vignette mask (1 in center, 0 at edges)
    # Adjust the curve with the amount parameter (higher = smaller vignette)
    vignette_mask = 1 - np.clip(dist_map * amount * 2, 0, 1) ** strength

    # Set vignette color
    if color is None:
        if hasattr(config, "style_variant") and config.style_variant == "dark":
            # Use primary color from palette
            color = palette.primary.as_tuple
        else:
            # Default to black
            color = (0, 0, 0)

    # Apply vignette effect
    result = image.copy().astype(np.float32)

    if image.ndim == 3:
        # For color images
        for c in range(image.shape[2]):
            if isinstance(color, tuple) and len(color) > c:
                # Blend with specified color
                color_value = color[c]
                result[:, :, c] = result[:, :, c] * vignette_mask + color_value * (
                    1 - vignette_mask
                )
            else:
                # Darken only
                result[:, :, c] = result[:, :, c] * vignette_mask
    else:
        # For grayscale
        if isinstance(color, tuple):
            # Convert color to grayscale
            color_value = sum(color) / len(color)
            result = result * vignette_mask + color_value * (1 - vignette_mask)
        else:
            # Darken only
            result = result * vignette_mask

    # Clip values to valid range
    return np.clip(result, 0, 255).astype(np.uint8)



def add_halftone(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    dots_per_inch: int = 15,
    angle: float = 45.0,
    method: str = "circles",
    blend: float = 0.5,
) -> np.ndarray:
    """Apply halftone effect to an image, simulating printed material.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        dots_per_inch: Density of halftone pattern
        angle: Angle of halftone pattern in degrees
        method: Halftone method ("circles", "lines", "diamonds")
        blend: Blend factor with original image (0-1)

    Returns:
        Halftone image as numpy array
    """
    # Get image dimensions
    height, width = image.shape[:2]

    # Convert to grayscale if color image
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image.copy()

    # Calculate dot size in pixels
    dot_size = max(1, int(min(height, width) / (dots_per_inch * 3)))

    # Create a new blank canvas
    halftone = np.ones((height, width), dtype=np.uint8) * 255

    # Calculate the number of dots in each dimension
    num_dots_y = height // dot_size
    num_dots_x = width // dot_size

    # Create the halftone pattern
    if method == "circles":
        for y in range(num_dots_y):
            for x in range(num_dots_x):
                # Calculate coordinates for this cell
                y_start = y * dot_size
                x_start = x * dot_size

                # Get the average brightness in this cell
                y_end = min(y_start + dot_size, height)
                x_end = min(x_start + dot_size, width)
                cell = gray[y_start:y_end, x_start:x_end]
                avg_brightness = np.mean(cell)

                # Calculate circle radius based on brightness
                radius = (255 - avg_brightness) / 255 * dot_size / 2

                if radius > 0:
                    # Calculate circle center
                    cy = y_start + dot_size // 2
                    cx = x_start + dot_size // 2

                    # Draw the circle
                    cv2.circle(
                        halftone,
                        (cx, cy),
                        int(radius),
                        0,  # Black
                        -1,  # Filled
                    )

    elif method == "lines":
        # Convert angle to radians
        angle_rad = np.deg2rad(angle)
        cos_angle = np.cos(angle_rad)
        sin_angle = np.sin(angle_rad)

        for y in range(num_dots_y):
            for x in range(num_dots_x):
                # Calculate coordinates for this cell
                y_start = y * dot_size
                x_start = x * dot_size

                # Get the average brightness in this cell
                y_end = min(y_start + dot_size, height)
                x_end = min(x_start + dot_size, width)
                cell = gray[y_start:y_end, x_start:x_end]
                avg_brightness = np.mean(cell)

                # Calculate line thickness based on brightness
                thickness = int((255 - avg_brightness) / 255 * dot_size)

                if thickness > 0:
                    # Calculate line endpoints
                    cx = x_start + dot_size // 2
                    cy = y_start + dot_size // 2
                    half_len = dot_size // 2

                    x1 = int(cx - half_len * cos_angle)
                    y1 = int(cy - half_len * sin_angle)
                    x2 = int(cx + half_len * cos_angle)
                    y2 = int(cy + half_len * sin_angle)

                    # Draw the line
                    cv2.line(
                        halftone,
                        (x1, y1),
                        (x2, y2),
                        0,  # Black
                        thickness,
                    )

    elif method == "diamonds":
        for y in range(num_dots_y):
            for x in range(num_dots_x):
                # Calculate coordinates for this cell
                y_start = y * dot_size
                x_start = x * dot_size

                # Get the average brightness in this cell
                y_end = min(y_start + dot_size, height)
                x_end = min(x_start + dot_size, width)
                cell = gray[y_start:y_end, x_start:x_end]
                avg_brightness = np.mean(cell)

                # Calculate diamond size based on brightness
                size = (255 - avg_brightness) / 255 * dot_size

                if size > 0:
                    # Calculate diamond center and corners
                    cx = x_start + dot_size // 2
                    cy = y_start + dot_size // 2
                    half_size = int(size / 2)

                    # Draw the diamond
                    points = np.array(
                        [
                            [cx, cy - half_size],  # Top
                            [cx + half_size, cy],  # Right
                            [cx, cy + half_size],  # Bottom
                            [cx - half_size, cy],  # Left
                        ]
                    )

                    cv2.fillPoly(halftone, [points], 0)

    # If blend is 0, return just the halftone pattern
    if blend <= 0:
        # Convert halftone to RGB if the input was RGB
        if image.ndim == 3:
            return cv2.cvtColor(halftone, cv2.COLOR_GRAY2RGB)
        return halftone

    # If blend is 1, return the original image
    if blend >= 1:
        return image

    # Blend the halftone with the original image
    if image.ndim == 3:
        # Convert halftone to RGB
        halftone_rgb = cv2.cvtColor(halftone, cv2.COLOR_GRAY2RGB)

        # Blend
        result = cv2.addWeighted(image, blend, halftone_rgb, 1 - blend, 0)
    else:
        # Blend grayscale images
        result = cv2.addWeighted(image, blend, halftone, 1 - blend, 0)

    return result
