# packages/phantom-visuals/phantom_visuals/effects/artistic.py

"""Artistic effects for creating distinctive visual styles.

This module provides advanced image manipulation techniques for creating
unique, artistic visual transformations.
"""

import math
import random
from typing import Optional

import cv2
import numpy as np

from phantom_visuals.core.config import Configuration
from phantom_visuals.core.palette import ColorPalette


def posterize(
    image: np.ndarray, config: Configuration, palette: ColorPalette, levels: int = 4
) -> np.ndarray:
    """Reduce the number of colors in an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        levels: Number of color levels per channel

    Returns:
        Posterized image as numpy array
    """
    # Apply posterization by quantizing colors
    factor = 255 / (levels - 1)
    result = np.round(image / factor) * factor

    return result.astype(np.uint8)


def pixelate(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    block_size: Optional[int] = None,
) -> np.ndarray:
    """Apply pixelation effect to an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        block_size: Size of pixelation blocks (defaults to config.effect_params.pixelation)

    Returns:
        Pixelated image as numpy array
    """
    if block_size is None:
        block_size = config.effect_params.pixelation

    # If block size is 0 or 1, return the original image
    if block_size <= 1:
        return image

    height, width = image.shape[:2]

    # Calculate new dimensions
    h_blocks = max(1, height // block_size)
    w_blocks = max(1, width // block_size)
    h_new = h_blocks * block_size
    w_new = w_blocks * block_size

    # Resize down and then back up
    temp = cv2.resize(image, (w_blocks, h_blocks), interpolation=cv2.INTER_LINEAR)

    result = cv2.resize(temp, (w_new, h_new), interpolation=cv2.INTER_NEAREST)

    # Resize back to original dimensions if needed
    if h_new != height or w_new != width:
        result = cv2.resize(result, (width, height), interpolation=cv2.INTER_NEAREST)

    return result


def solarize(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    threshold: int = 128,
) -> np.ndarray:
    """Apply solarization effect (invert colors above a threshold).

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        threshold: Brightness threshold for inversion (0-255)

    Returns:
        Solarized image as numpy array
    """
    # Create a copy of the input image
    result = image.copy()

    # Invert pixels above the threshold
    mask = image >= threshold
    result[mask] = 255 - result[mask]

    return result


def apply_symmetry(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    axis: str = "both",
    center_offset: float = 0.0,
) -> np.ndarray:
    """Apply symmetry to an image along specified axes.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        axis: Symmetry axis ("horizontal", "vertical", "both", "radial")
        center_offset: Offset from center for non-centered symmetry (-1.0 to 1.0)

    Returns:
        Symmetrical image as numpy array
    """
    height, width = image.shape[:2]
    result = image.copy()

    # Calculate center with offset
    center_x = width // 2 + int(center_offset * width // 2)
    center_y = height // 2 + int(center_offset * height // 2)

    # Ensure centers are within image bounds
    center_x = max(0, min(width - 1, center_x))
    center_y = max(0, min(height - 1, center_y))

    if axis in ("horizontal", "both"):
        # Horizontal symmetry (mirror top/bottom)
        top_half = result[:center_y, :]
        flipped = cv2.flip(top_half, 0)  # Flip around x-axis

        # Copy the flipped part to the bottom half
        h = min(flipped.shape[0], height - center_y)
        result[center_y : center_y + h, :] = flipped[:h, :]

    if axis in ("vertical", "both"):
        # Vertical symmetry (mirror left/right)
        left_half = result[:, :center_x]
        flipped = cv2.flip(left_half, 1)  # Flip around y-axis

        # Copy the flipped part to the right half
        w = min(flipped.shape[1], width - center_x)
        result[:, center_x : center_x + w] = flipped[:, :w]

    if axis == "radial":
        # Radial symmetry (like kaleidoscope)
        # Define quadrants
        quadrant = result[:center_y, :center_x].copy()

        # Mirror to other quadrants
        q2 = cv2.flip(quadrant, 1)  # Top-right
        q3 = cv2.flip(quadrant, 0)  # Bottom-left
        q4 = cv2.flip(cv2.flip(quadrant, 0), 1)  # Bottom-right

        # Size of the quadrant images
        q_height, q_width = quadrant.shape[:2]

        # Ensure we don't go out of bounds
        h_right = min(q_height, height - center_y)
        w_right = min(q_width, width - center_x)

        # Place the quadrants
        result[:q_height, :q_width] = quadrant
        result[:q_height, center_x : center_x + w_right] = q2[:, :w_right]
        result[center_y : center_y + h_right, :q_width] = q3[:h_right, :]
        result[center_y : center_y + h_right, center_x : center_x + w_right] = q4[
            :h_right, :w_right
        ]

    return result


def ghost_trails(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    intensity: Optional[float] = None,
    direction: float = 45.0,
    length: int = 20,
) -> np.ndarray:
    """Create ghost trail effects by blending offset copies.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        intensity: Effect strength (defaults to config.effect_params.intensity)
        direction: Direction of the trails in degrees
        length: Length of the trails in pixels

    Returns:
        Image with ghost trails as numpy array
    """
    if intensity is None:
        intensity = config.effect_params.intensity

    # Convert direction to radians
    angle_rad = np.deg2rad(direction)

    # Calculate x and y offsets based on direction
    dx = int(math.cos(angle_rad) * length)
    dy = int(math.sin(angle_rad) * length)

    # Create a result canvas
    result = image.copy().astype(np.float32)

    # Number of ghost images
    num_trails = 5

    # Create and blend the ghost trails
    for i in range(1, num_trails + 1):
        # Scaled offset
        trail_dx = dx * i // num_trails
        trail_dy = dy * i // num_trails

        # Create an offset version of the image
        offset_image = np.zeros_like(image, dtype=np.float32)

        # Calculate source and destination regions for copying
        if trail_dx >= 0:
            src_x, dst_x = 0, trail_dx
            w = image.shape[1] - trail_dx
        else:
            src_x, dst_x = -trail_dx, 0
            w = image.shape[1] + trail_dx

        if trail_dy >= 0:
            src_y, dst_y = 0, trail_dy
            h = image.shape[0] - trail_dy
        else:
            src_y, dst_y = -trail_dy, 0
            h = image.shape[0] + trail_dy

        # Copy the valid region
        offset_image[dst_y : dst_y + h, dst_x : dst_x + w] = image[
            src_y : src_y + h, src_x : src_x + w
        ]

        # Calculate weight for this trail
        weight = (1.0 - i / (num_trails + 1)) * intensity / 2.0

        # Blend with the result
        result = result * (1.0 - weight) + offset_image * weight

    # Clip values and convert back to uint8
    return np.clip(result, 0, 255).astype(np.uint8)



def ethereal_glow(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    intensity: Optional[float] = None,
    radius: Optional[float] = None,
    highlight_boost: float = 1.2,
) -> np.ndarray:
    """Create an ethereal glow effect.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (used for glow color tinting)
        intensity: Glow strength (defaults to config.effect_params.intensity)
        radius: Glow radius (defaults to config.effect_params.blur_radius)
        highlight_boost: Brightness boost for highlights

    Returns:
        Image with ethereal glow effect as numpy array
    """
    if intensity is None:
        intensity = config.effect_params.intensity

    if radius is None:
        radius = config.effect_params.blur_radius

    if radius <= 0 or intensity <= 0:
        return image

    # Convert to float for calculations
    img_float = image.astype(np.float32) / 255.0

    # Create a blurred version for the glow
    glow = cv2.GaussianBlur(img_float, (0, 0), radius)

    # Enhance highlights in the glow
    glow_target: float = 0.5
    highlight_mask = glow > glow_target
    glow[highlight_mask] = glow[highlight_mask] * highlight_boost

    # Clip values
    glow = np.clip(glow, 0.0, 1.0)

    # Tint the glow with accent color if available
    if palette and hasattr(palette, "accent"):
        accent = np.array(palette.accent.as_normalized)

        # Create a hue-shifted version of the image based on the accent color
        ndim_target: int = 3
        if image.ndim == ndim_target:  # Only apply to color images
            # Convert to HSV
            hsv = cv2.cvtColor(glow, cv2.COLOR_RGB2HSV)

            # Get target hue from accent color
            accent_hsv = cv2.cvtColor(
                np.array([[accent * 255]]).astype(np.uint8), cv2.COLOR_RGB2HSV
            )[0, 0]

            # Apply subtle hue shift towards accent
            hsv_float = hsv.astype(np.float32)
            hsv_float[:, :, 0] = accent_hsv[0] * 0.3 + hsv_float[:, :, 0] * 0.7

            # Boost saturation slightly
            hsv_float[:, :, 1] = np.minimum(hsv_float[:, :, 1] * 1.2, 255)

            # Convert back to RGB
            glow = cv2.cvtColor(hsv_float.astype(np.uint8), cv2.COLOR_HSV2RGB) / 255.0

    # Blend the original image with the glow
    result = img_float + glow * intensity

    # Clip values and convert back to uint8
    result = np.clip(result, 0.0, 1.0)
    return (result * 255.0).astype(np.uint8)


def blur_regions(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    threshold: float = 0.5,
    blur_amount: Optional[float] = None,
    invert: bool = False,
) -> np.ndarray:
    """Selectively blur regions based on brightness threshold.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        threshold: Brightness threshold (0-1)
        blur_amount: Blur radius (defaults to config.effect_params.blur_radius)
        invert: If True, blur dark regions instead of bright regions

    Returns:
        Selectively blurred image as numpy array
    """
    if blur_amount is None:
        blur_amount = config.effect_params.blur_radius

    if blur_amount <= 0:
        return image

    # Convert to grayscale for detecting regions
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image.copy()

    # Normalize to 0-1
    gray = gray.astype(np.float32) / 255.0

    # Create a mask for the regions to blur
    mask = gray < threshold if invert else gray >= threshold

    # Create a blurred version of the image
    blurred = cv2.GaussianBlur(image, (0, 0), blur_amount)

    # Create a result canvas
    result = image.copy()

    # Apply the blurred version to the masked regions
    if image.ndim == 3:
        for c in range(3):  # RGB channels
            result[:, :, c] = np.where(mask, blurred[:, :, c], image[:, :, c])
    else:
        result = np.where(mask, blurred, image)

    return result


def double_exposure(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    second_image: np.ndarray,
    opacity: float = 0.5,
    blend_mode: str = "screen",
) -> np.ndarray:
    """Create a double exposure effect by blending two images.

    Args:
        image: Primary input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        second_image: Secondary image to blend
        opacity: Blend opacity of the second image
        blend_mode: Blending mode ("screen", "overlay", "soft_light", "add")

    Returns:
        Double exposure image as numpy array
    """
    # Ensure the second image is the same size as the first
    height, width = image.shape[:2]
    second_image = cv2.resize(second_image, (width, height))

    # Convert both images to float for blending
    img1 = image.astype(np.float32) / 255.0
    img2 = second_image.astype(np.float32) / 255.0

    # Apply the blend based on mode
    if blend_mode == "screen":
        blended = 1.0 - (1.0 - img1) * (1.0 - img2 * opacity)
    elif blend_mode == "overlay":
        mask = img1 < 0.5
        blended = np.zeros_like(img1)
        blended[mask] = 2 * img1[mask] * img2[mask] * opacity
        blended[~mask] = 1.0 - 2 * (1.0 - img1[~mask]) * (1.0 - img2[~mask] * opacity)
    elif blend_mode == "soft_light":
        blended = (1.0 - 2 * img2 * opacity) * img1**2 + 2 * img2 * opacity * img1
    elif blend_mode == "add":
        blended = img1 + img2 * opacity
    else:
        # Default to simple blend
        blended = img1 * (1 - opacity) + img2 * opacity

    # Clip values and convert back to uint8
    blended = np.clip(blended, 0.0, 1.0)
    return (blended * 255.0).astype(np.uint8)


def create_glitch_blocks(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    intensity: Optional[float] = None,
    block_size: tuple[int, int] = (20, 10),
    offset_range: int = 10,
    num_blocks: Optional[int] = None,
) -> np.ndarray:
    """Create digital glitch effect with offset blocks.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        intensity: Effect strength (defaults to config.effect_params.intensity)
        block_size: Size range (height, width) for the glitch blocks
        offset_range: Maximum pixel offset for blocks
        num_blocks: Number of glitch blocks to create

    Returns:
        Glitched image as numpy array
    """
    if intensity is None:
        intensity = config.effect_params.intensity

    # Set random seed if specified
    if config.effect_params.seed is not None:
        random.seed(config.effect_params.seed)

    # Create a copy of the input image
    result = image.copy()
    height, width = image.shape[:2]

    # Calculate number of blocks based on intensity if not specified
    if num_blocks is None:
        num_blocks = int(intensity * 20)

    # Apply the glitch effect
    for _ in range(num_blocks):
        # Random block position
        x = random.randint(0, width - block_size[1])
        y = random.randint(0, height - block_size[0])

        # Random block size
        h = min(random.randint(block_size[0] // 2, block_size[0]), height - y)
        w = min(random.randint(block_size[1] // 2, block_size[1]), width - x)

        # Extract the block
        block = image[y : y + h, x : x + w].copy()

        # Random RGBA channel shift
        if image.ndim == 3:
            channel = random.randint(0, image.shape[2] - 1)
            offset_x = random.randint(-offset_range, offset_range)
            offset_y = random.randint(-offset_range, offset_range)

            # Calculate target position
            target_x = max(0, min(width - w, x + offset_x))
            target_y = max(0, min(height - h, y + offset_y))

            # Apply the channel shift
            result[target_y : target_y + h, target_x : target_x + w, channel] = block[
                :, :, channel
            ]
        else:
            # For grayscale, just move the whole block
            offset_x = random.randint(-offset_range, offset_range)
            offset_y = random.randint(-offset_range, offset_range)

            # Calculate target position
            target_x = max(0, min(width - w, x + offset_x))
            target_y = max(0, min(height - h, y + offset_y))

            # Move the block
            result[target_y : target_y + h, target_x : target_x + w] = block

    return result
