# packages/phantom-visuals/phantom_visuals/effects/blur.py

"""
Blur effects for image transformations.

This module provides various blur effects to create ethereal, dreamy,
or out-of-focus visual styles.
"""

from typing import Tuple, Optional
import math
import numpy as np
from scipy import ndimage
import cv2

from phantom_visuals.core.config import Configuration
from phantom_visuals.core.palette import ColorPalette


def gaussian_blur(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    radius: Optional[float] = None
) -> np.ndarray:
    """
    Apply Gaussian blur to an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        radius: Blur radius (defaults to config.effect_params.blur_radius)

    Returns:
        Blurred image as numpy array
    """
    if radius is None:
        radius = config.effect_params.blur_radius

    # Scale intensity by the configuration intensity
    radius = radius * config.effect_params.intensity

    if radius <= 0:
        return image

    # Apply gaussian blur
    return cv2.GaussianBlur(
        image,
        (0, 0),
        sigmaX=radius,
        sigmaY=radius,
        borderType=cv2.BORDER_REFLECT
    )


def motion_blur(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    angle: float = 45.0,
    distance: Optional[float] = None
) -> np.ndarray:
    """
    Apply directional motion blur to an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        angle: Direction of motion blur in degrees
        distance: Length of the motion blur (defaults to blur_radius * 2)

    Returns:
        Motion-blurred image as numpy array
    """
    if distance is None:
        distance = config.effect_params.blur_radius * 2

    # Scale by configuration intensity
    distance = distance * config.effect_params.intensity

    if distance <= 0:
        return image

    # Convert angle to radians
    angle_rad = np.deg2rad(angle)

    # Create the motion blur kernel
    kernel_size = int(distance * 2) + 1
    kernel_size = max(3, kernel_size)
    kernel_size = min(kernel_size, min(image.shape[0], image.shape[1]) // 3)

    # Make kernel size odd
    if kernel_size % 2 == 0:
        kernel_size += 1

    kernel = np.zeros((kernel_size, kernel_size))

    # Calculate line endpoints
    center = (kernel_size - 1) / 2
    dx = math.cos(angle_rad)
    dy = math.sin(angle_rad)

    for i in range(kernel_size):
        offset = i - center
        x = center + dx * offset
        y = center + dy * offset

        # Ensure we're within bounds
        if (0 <= x < kernel_size and 0 <= y < kernel_size):
            # Bilinear interpolation for smoother kernel
            x1, y1 = int(x), int(y)
            x2, y2 = min(x1 + 1, kernel_size - 1), min(y1 + 1, kernel_size - 1)

            wx = x - x1
            wy = y - y1

            # Weighted contribution to surrounding pixels
            kernel[y1, x1] += (1 - wx) * (1 - wy)
            kernel[y1, x2] += wx * (1 - wy)
            kernel[y2, x1] += (1 - wx) * wy
            kernel[y2, x2] += wx * wy

    # Normalize the kernel
    kernel = kernel / kernel.sum()

    # Apply the kernel
    result = cv2.filter2D(image, -1, kernel)

    return result


def radial_blur(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    center: Optional[Tuple[float, float]] = None,
    amount: Optional[float] = None
) -> np.ndarray:
    """
    Apply radial blur emanating from a center point.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        center: (x, y) coordinates of blur center (default: image center)
        amount: Strength of the blur (defaults to blur_radius)

    Returns:
        Radially blurred image as numpy array
    """
    if amount is None:
        amount = config.effect_params.blur_radius

    # Scale by configuration intensity
    amount = amount * config.effect_params.intensity

    if amount <= 0:
        return image

    height, width = image.shape[:2]

    if center is None:
        center = (width / 2, height / 2)

    # Create coordinate maps
    y, x = np.mgrid[0:height, 0:width]

    # Calculate distance from center for each pixel
    cx, cy = center
    dist_x = x - cx
    dist_y = y - cy

    # Create a radial gradient
    distances = np.sqrt(dist_x**2 + dist_y**2)
    max_distance = np.sqrt(width**2 + height**2) / 2

    # Normalize distances
    norm_distances = distances / max_distance

    # Create various blurred versions of the image
    num_steps = 5
    blurred_imgs = []

    for i in range(num_steps):
        # Increasing blur for each step
        sigma = amount * (i + 1) / num_steps
        blurred = cv2.GaussianBlur(image, (0, 0), sigma)
        blurred_imgs.append(blurred)

    # Create the output image
    result = np.zeros_like(image)

    # Blend based on distance from center
    for i in range(num_steps):
        # Calculate weight for this blur level
        min_dist = i / num_steps
        max_dist = (i + 1) / num_steps

        # Create mask for this distance range
        mask = np.logical_and(
            norm_distances >= min_dist,
            norm_distances < max_dist
        ).astype(np.float32)

        # Expand mask to 3 channels if needed
        if mask.ndim == 2 and image.ndim == 3:
            mask = np.expand_dims(mask, axis=2)
            mask = np.repeat(mask, 3, axis=2)

        # Add weighted contribution
        result += blurred_imgs[i] * mask

    # Add the original image in the center with a smooth transition
    center_weight = np.exp(-norm_distances * 5 * amount)
    if center_weight.ndim == 2 and image.ndim == 3:
        center_weight = np.expand_dims(center_weight, axis=2)
        center_weight = np.repeat(center_weight, 3, axis=2)

    result = result * (1 - center_weight) + image * center_weight

    return result.astype(np.uint8)


def tilt_shift_blur(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    angle: float = 0.0,
    center_y: Optional[float] = None,
    blur_width: Optional[float] = None,
    blur_amount: Optional[float] = None
) -> np.ndarray:
    """
    Apply a tilt-shift effect that simulates a shallow depth of field.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        angle: Rotation angle of the in-focus line in degrees
        center_y: Y position of the in-focus line (0-1), defaults to center
        blur_width: Width of the transition area (0-1)
        blur_amount: Strength of the blur (defaults to blur_radius)

    Returns:
        Tilt-shift blurred image as numpy array
    """
    if blur_amount is None:
        blur_amount = config.effect_params.blur_radius

    # Scale by configuration intensity
    blur_amount = blur_amount * config.effect_params.intensity

    if blur_amount <= 0:
        return image

    height, width = image.shape[:2]

    if center_y is None:
        center_y = 0.5

    if blur_width is None:
        blur_width = 0.2

    # Calculate center line position
    center_line = int(height * center_y)

    # Create a gradient mask for the blur effect
    y_coords = np.arange(height)

    # Calculate distance from center line
    distances = np.abs(y_coords - center_line) / height

    # Create the gradient using sigmoid function for smooth transition
    k = 1 / blur_width  # Controls transition sharpness
    gradient = 1 / (1 + np.exp(-k * (distances - blur_width)))

    # Convert to 3D if needed
    if image.ndim == 3:
        gradient = np.repeat(gradient[:, np.newaxis], width, axis=1)
        if image.shape[2] == 3:
            gradient = np.repeat(gradient[:, :, np.newaxis], 3, axis=2)

    # Apply rotation if needed
    if angle != 0:
        # Create rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(
            (width // 2, height // 2),
            angle,
            1.0
        )

        # Apply rotation to gradient
        gradient = cv2.warpAffine(
            gradient,
            rotation_matrix,
            (width, height),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT
        )

        if image.ndim == 3 and gradient.ndim == 2:
            gradient = np.repeat(gradient[:, :, np.newaxis], 3, axis=2)

    # Apply gaussian blur to the whole image
    blurred = cv2.GaussianBlur(
        image,
        (0, 0),
        blur_amount,
        borderType=cv2.BORDER_REFLECT
    )

    # Blend original and blurred based on the gradient
    result = image * (1 - gradient) + blurred * gradient

    return result.astype(np.uint8)
