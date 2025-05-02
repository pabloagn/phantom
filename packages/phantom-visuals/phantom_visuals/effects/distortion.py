# packages/phantom-visuals/phantom_visuals/effects/distortion.py

"""
Distortion effects for creating warped and glitched imagery.

This module provides a collection of effects for distorting and
manipulating the geometry of images to create unique visual styles.
"""

from typing import Optional, Tuple, List, Union, Callable
import math
import random
import numpy as np
import cv2
from scipy import ndimage

from phantom_visuals.core.config import Configuration
from phantom_visuals.core.palette import ColorPalette


def wave_distortion(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    amplitude: Optional[float] = None,
    frequency: float = 0.1,
    direction: str = "both"
) -> np.ndarray:
    """
    Apply a wave distortion effect to an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        amplitude: Wave amplitude in pixels (defaults to config.effect_params.distortion * 20)
        frequency: Wave frequency (higher = more waves)
        direction: Direction of waves ("horizontal", "vertical", "both")

    Returns:
        Wave-distorted image as numpy array
    """
    if amplitude is None:
        amplitude = config.effect_params.distortion * 20.0

    # If amplitude is 0, return the original image
    if amplitude <= 0:
        return image

    # Get image dimensions
    height, width = image.shape[:2]

    # Create meshgrid for coordinate mapping
    y_coords, x_coords = np.mgrid[0:height, 0:width]

    # Apply wave distortion
    if direction == "horizontal" or direction == "both":
        x_coords = x_coords + amplitude * np.sin(y_coords * frequency)

    if direction == "vertical" or direction == "both":
        y_coords = y_coords + amplitude * np.sin(x_coords * frequency)

    # Clip coordinates to valid image bounds
    x_coords = np.clip(x_coords, 0, width - 1).astype(np.float32)
    y_coords = np.clip(y_coords, 0, height - 1).astype(np.float32)

    # Remap the image using the distorted coordinates
    result = cv2.remap(
        image,
        x_coords,
        y_coords,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )

    return result


def pixel_sort(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    threshold: float = 0.5,
    sort_direction: str = "horizontal",
    reverse: bool = False
) -> np.ndarray:
    """
    Apply pixel sorting effect to create glitchy streaks.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        threshold: Brightness threshold for sorting (0-1)
        sort_direction: Direction to sort ("horizontal", "vertical", "both")
        reverse: If True, sort in descending order

    Returns:
        Pixel-sorted image as numpy array
    """
    # Convert to float for intensity calculations
    img_float = image.astype(np.float32) / 255.0

    # Get image dimensions
    height, width = image.shape[:2]

    # Create a grayscale version for thresholding
    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) / 255.0
    else:
        gray = img_float.copy()

    # Create mask of pixels to sort (above threshold)
    mask = gray > threshold

    # Copy the image for the result
    result = image.copy()

    # Horizontal sorting
    if sort_direction in ["horizontal", "both"]:
        for y in range(height):
            # Get row and corresponding mask
            row = result[y, :].copy()
            row_mask = mask[y, :]

            # Skip if all pixels are below threshold
            if not np.any(row_mask):
                continue

            # Find contiguous regions to sort
            regions = []
            start = None

            for x in range(width):
                if row_mask[x] and start is None:
                    start = x
                elif not row_mask[x] and start is not None:
                    regions.append((start, x))
                    start = None

            # Add the last region if it exists
            if start is not None:
                regions.append((start, width))

            # Sort each region
            for start, end in regions:
                if end - start < 2:
                    continue

                if image.ndim == 3:
                    # Sort each color channel separately
                    for c in range(image.shape[2]):
                        sorted_region = np.sort(row[start:end, c])
                        if reverse:
                            sorted_region = sorted_region[::-1]
                        row[start:end, c] = sorted_region
                else:
                    # Sort grayscale image
                    sorted_region = np.sort(row[start:end])
                    if reverse:
                        sorted_region = sorted_region[::-1]
                    row[start:end] = sorted_region

            # Update the result
            result[y, :] = row

    # Vertical sorting
    if sort_direction in ["vertical", "both"]:
        for x in range(width):
            # Get column and corresponding mask
            col = result[:, x].copy()
            col_mask = mask[:, x]

            # Skip if all pixels are below threshold
            if not np.any(col_mask):
                continue

            # Find contiguous regions to sort
            regions = []
            start = None

            for y in range(height):
                if col_mask[y] and start is None:
                    start = y
                elif not col_mask[y] and start is not None:
                    regions.append((start, y))
                    start = None

            # Add the last region if it exists
            if start is not None:
                regions.append((start, height))

            # Sort each region
            for start, end in regions:
                if end - start < 2:
                    continue

                if image.ndim == 3:
                    # Sort each color channel separately
                    for c in range(image.shape[2]):
                        sorted_region = np.sort(col[start:end, c])
                        if reverse:
                            sorted_region = sorted_region[::-1]
                        col[start:end, c] = sorted_region
                else:
                    # Sort grayscale image
                    sorted_region = np.sort(col[start:end])
                    if reverse:
                        sorted_region = sorted_region[::-1]
                    col[start:end] = sorted_region

            # Update the result
            result[:, x] = col

    return result


def glitch(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    intensity: Optional[float] = None,
    num_channels: int = 1,
    channel_shift_range: int = 10
) -> np.ndarray:
    """
    Create digital glitch effect with RGB channel shifting.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        intensity: Effect strength (defaults to config.effect_params.distortion)
        num_channels: Number of color channels to shift
        channel_shift_range: Maximum pixel offset for channels

    Returns:
        Glitched image as numpy array
    """
    if intensity is None:
        intensity = config.effect_params.distortion

    # Set random seed if specified
    if config.effect_params.seed is not None:
        random.seed(config.effect_params.seed)

    # Only apply to color images
    if image.ndim < 3 or image.shape[2] < 3:
        return image

    # Scale the shift range by intensity
    shift_range = int(channel_shift_range * intensity)
    if shift_range <= 0:
        return image

    # Create a copy of the input image
    result = image.copy()

    # Choose random channels to shift (without duplicates)
    channels = list(range(min(3, image.shape[2])))
    if num_channels < len(channels):
        channels = random.sample(channels, num_channels)

    # Apply channel shifts
    for channel in channels:
        # Generate random shift
        dx = random.randint(-shift_range, shift_range)
        dy = random.randint(-shift_range, shift_range)

        if dx == 0 and dy == 0:
            continue

        # Create shifted version of the channel
        shifted = np.zeros_like(result[:, :, channel])

        # Apply the shift (horizontal)
        if dx > 0:
            shifted[:, dx:] = result[:, :-dx, channel]
        elif dx < 0:
            shifted[:, :dx] = result[:, -dx:, channel]
        else:
            shifted = result[:, :, channel].copy()

        # Apply the shift (vertical)
        if dy != 0:
            temp = shifted.copy()
            if dy > 0:
                shifted[dy:, :] = temp[:-dy, :]
            else:
                shifted[:dy, :] = temp[-dy:, :]

        # Update the result
        result[:, :, channel] = shifted

    return result


def displace(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    displacement_map: Optional[np.ndarray] = None,
    scale: Optional[float] = None
) -> np.ndarray:
    """
    Displace pixels based on a displacement map.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        displacement_map: Image to use as displacement map (will be generated if None)
        scale: Maximum displacement in pixels (defaults to config.effect_params.distortion * 20)

    Returns:
        Displaced image as numpy array
    """
    if scale is None:
        scale = config.effect_params.distortion * 20

    # If scale is 0, return the original image
    if scale <= 0:
        return image

    # Get image dimensions
    height, width = image.shape[:2]

    # Generate displacement map if not provided
    if displacement_map is None:
        # Generate noise
        noise = np.random.normal(0, 1, (height, width, 2)).astype(np.float32)

        # Smooth the noise
        disp_map_x = cv2.GaussianBlur(noise[:, :, 0], (0, 0), 15)
        disp_map_y = cv2.GaussianBlur(noise[:, :, 1], (0, 0), 15)

        # Normalize to [-1, 1]
        disp_map_x = disp_map_x / np.max(np.abs(disp_map_x))
        disp_map_y = disp_map_y / np.max(np.abs(disp_map_y))
    else:
        # Convert the provided map to the right size and range
        displacement_map = cv2.resize(displacement_map, (width, height))

        if displacement_map.ndim == 3 and displacement_map.shape[2] >= 2:
            # Use red and green channels for x/y displacement
            disp_map_x = displacement_map[:, :, 0].astype(np.float32) / 127.5 - 1.0
            disp_map_y = displacement_map[:, :, 1].astype(np.float32) / 127.5 - 1.0
        else:
            # For grayscale, use the same map for both axes but with different phases
            if displacement_map.ndim == 3:
                disp_map = displacement_map[:, :, 0]
            else:
                disp_map = displacement_map

            disp_map = disp_map.astype(np.float32) / 127.5 - 1.0
            disp_map_x = disp_map.copy()
            disp_map_y = -disp_map.copy()  # Inverse for variety

    # Create meshgrid for coordinate mapping
    y_coords, x_coords = np.mgrid[0:height, 0:width]

    # Apply displacement
    x_displaced = x_coords + scale * disp_map_x
    y_displaced = y_coords + scale * disp_map_y

    # Clip coordinates to valid image bounds
    x_displaced = np.clip(x_displaced, 0, width - 1).astype(np.float32)
    y_displaced = np.clip(y_displaced, 0, height - 1).astype(np.float32)

    # Remap the image using the displaced coordinates
    result = cv2.remap(
        image,
        x_displaced,
        y_displaced,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )

    return result


def swirl(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    center: Optional[Tuple[int, int]] = None,
    strength: Optional[float] = None,
    radius: float = 0.5
) -> np.ndarray:
    """
    Apply a swirl distortion effect.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        center: (x, y) center of the swirl (defaults to image center)
        strength: Swirl strength (defaults to config.effect_params.distortion * 10)
        radius: Relative radius of the effect (0-1)

    Returns:
        Swirled image as numpy array
    """
    if strength is None:
        strength = config.effect_params.distortion * 10

    # If strength is 0, return the original image
    if strength == 0:
        return image

    # Get image dimensions
    height, width = image.shape[:2]

    # Set default center to image center if not specified
    if center is None:
        center = (width // 2, height // 2)

    # Calculate absolute radius
    abs_radius = radius * min(width, height)

    # Create meshgrid for coordinate mapping
    y_coords, x_coords = np.mgrid[0:height, 0:width]

    # Calculate distances from center and normalize
    x_center, y_center = center
    x_diff = x_coords - x_center
    y_diff = y_coords - y_center
    distances = np.sqrt(x_diff**2 + y_diff**2)

    # Calculate angles for each pixel
    angles = np.arctan2(y_diff, x_diff)

    # Apply the swirl effect based on distance
    swirl_factor = 1.0 - np.clip(distances / abs_radius, 0, 1)
    angles = angles + strength * swirl_factor

    # Convert back to cartesian coordinates
    x_source = x_center + distances * np.cos(angles)
    y_source = y_center + distances * np.sin(angles)

    # Clip to valid image bounds
    x_source = np.clip(x_source, 0, width - 1).astype(np.float32)
    y_source = np.clip(y_source, 0, height - 1).astype(np.float32)

    # Remap the image
    result = cv2.remap(
        image,
        x_source,
        y_source,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT
    )

    return result


def lens_distortion(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    k1: Optional[float] = None,
    k2: float = 0.0
) -> np.ndarray:
    """
    Apply barrel/pincushion lens distortion.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        k1: Primary distortion coefficient (positive for barrel, negative for pincushion)
           (defaults to config.effect_params.distortion)
        k2: Secondary distortion coefficient for more complex distortion

    Returns:
        Lens-distorted image as numpy array
    """
    if k1 is None:
        k1 = config.effect_params.distortion

    # If k1 and k2 are 0, return the original image
    if k1 == 0 and k2 == 0:
        return image

    # Get image dimensions
    height, width = image.shape[:2]

    # Create meshgrid for coordinate mapping
    y_coords, x_coords = np.mgrid[0:height, 0:width]

    # Normalize coordinates to [-1, 1] with center at (0, 0)
    x_center = width / 2
    y_center = height / 2
    x_norm = (x_coords - x_center) / x_center
    y_norm = (y_coords - y_center) / y_center

    # Calculate squared radius from center
    r_squared = x_norm**2 + y_norm**2

    # Apply distortion
    distortion = 1 + k1 * r_squared + k2 * r_squared**2

    # Multiply normalized coordinates by distortion factor
    x_distorted = x_norm * distortion
    y_distorted = y_norm * distortion

    # Convert back to image coordinates
    x_source = x_distorted * x_center + x_center
    y_source = y_distorted * y_center + y_center

    # Clip to valid image bounds
    x_source = np.clip(x_source, 0, width - 1).astype(np.float32)
    y_source = np.clip(y_source, 0, height - 1).astype(np.float32)

    # Remap the image
    result = cv2.remap(
        image,
        x_source,
        y_source,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0) if image.ndim == 3 else 0
    )

    return result
