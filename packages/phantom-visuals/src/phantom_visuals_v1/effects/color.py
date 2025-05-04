# packages/phantom-visuals/phantom_visuals/effects/color.py

"""
Color manipulation effects.

This module provides a collection of effects for manipulating
the colors in images to create distinctive visual styles.
"""

from typing import Optional, Tuple, List, Union
import numpy as np
import cv2

from phantom_visuals.core.config import Configuration
from phantom_visuals.core.palette import ColorPalette, RGBColor


def adjust_contrast(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    amount: Optional[float] = None
) -> np.ndarray:
    """
    Adjust the contrast of an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        amount: Contrast adjustment factor (defaults to config.effect_params.contrast)

    Returns:
        Contrast-adjusted image as numpy array
    """
    if amount is None:
        amount = config.effect_params.contrast

    # Convert to float for calculation
    img_float = image.astype(np.float32) / 255.0

    # Apply contrast adjustment: f(x) = (x - 0.5) * amount + 0.5
    result = (img_float - 0.5) * amount + 0.5

    # Clip values to valid range
    result = np.clip(result, 0.0, 1.0)

    # Convert back to uint8
    return (result * 255.0).astype(np.uint8)


def adjust_brightness(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    amount: Optional[float] = None
) -> np.ndarray:
    """
    Adjust the brightness of an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        amount: Brightness adjustment factor (defaults to config.effect_params.brightness)

    Returns:
        Brightness-adjusted image as numpy array
    """
    if amount is None:
        amount = config.effect_params.brightness

    # Convert to float for calculation
    img_float = image.astype(np.float32) / 255.0

    # Apply brightness adjustment: f(x) = x * amount
    result = img_float * amount

    # Clip values to valid range
    result = np.clip(result, 0.0, 1.0)

    # Convert back to uint8
    return (result * 255.0).astype(np.uint8)


def adjust_saturation(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    amount: Optional[float] = None
) -> np.ndarray:
    """
    Adjust the saturation of an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        amount: Saturation adjustment factor (defaults to config.effect_params.saturation)

    Returns:
        Saturation-adjusted image as numpy array
    """
    if amount is None:
        amount = config.effect_params.saturation

    # Convert to HSV for easier saturation adjustment
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)

    # Apply saturation adjustment
    hsv[:, :, 1] = hsv[:, :, 1] * amount

    # Clip values to valid range
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)

    # Convert back to RGB
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)


def color_shift(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    hue_shift: Optional[float] = None
) -> np.ndarray:
    """
    Shift the hue of an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        hue_shift: Hue shift amount (0-1, defaults to config.effect_params.hue_shift)

    Returns:
        Hue-shifted image as numpy array
    """
    if hue_shift is None:
        hue_shift = config.effect_params.hue_shift

    # Convert to HSV for hue manipulation
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)

    # Apply hue shift (hue is 0-179 in OpenCV)
    hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift * 180) % 180

    # Convert back to RGB
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)


def invert_colors(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette
) -> np.ndarray:
    """
    Invert the colors of an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)

    Returns:
        Color-inverted image as numpy array
    """
    # Simple inversion: 255 - pixel value
    return 255 - image


def duotone(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    color1: Optional[RGBColor] = None,
    color2: Optional[RGBColor] = None
) -> np.ndarray:
    """
    Apply a duotone effect to an image using two colors.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette
        color1: First color (defaults to palette.primary)
        color2: Second color (defaults to palette.accent)

    Returns:
        Duotone image as numpy array
    """
    if color1 is None:
        color1 = palette.primary

    if color2 is None:
        color2 = palette.accent

    # Convert to grayscale
    if image.ndim == 3:
        grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        grayscale = image.copy()

    # Normalize to float in range 0-1
    grayscale = grayscale.astype(np.float32) / 255.0

    # Create an empty RGB image
    height, width = grayscale.shape
    result = np.zeros((height, width, 3), dtype=np.float32)

    # Extract colors as normalized RGB
    c1 = np.array(color1.as_normalized)
    c2 = np.array(color2.as_normalized)

    # Map grayscale values to colors
    # Dark values map to color1, bright values map to color2
    for i in range(3):  # RGB channels
        result[:, :, i] = grayscale * c2[i] + (1 - grayscale) * c1[i]

    # Convert back to uint8
    return (result * 255.0).astype(np.uint8)


def apply_color_filter(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    color: Optional[RGBColor] = None,
    blend_mode: str = "multiply",
    opacity: float = 0.5
) -> np.ndarray:
    """
    Apply a color filter over the image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette
        color: Filter color (defaults to palette.accent)
        blend_mode: Blend mode ("multiply", "screen", "overlay", "soft_light")
        opacity: Filter opacity (0-1)

    Returns:
        Color-filtered image as numpy array
    """
    if color is None:
        color = palette.accent

    # Create a solid color image
    height, width = image.shape[:2]
    color_image = np.zeros((height, width, 3), dtype=np.float32)
    color_image[:, :] = color.as_normalized

    # Convert input image to float
    img_float = image.astype(np.float32) / 255.0

    # Apply blend based on mode
    if blend_mode == "multiply":
        blended = img_float * color_image
    elif blend_mode == "screen":
        blended = 1.0 - (1.0 - img_float) * (1.0 - color_image)
    elif blend_mode == "overlay":
        mask = img_float < 0.5
        blended = np.zeros_like(img_float)
        blended[mask] = 2 * img_float[mask] * color_image[mask]
        blended[~mask] = 1.0 - 2 * (1.0 - img_float[~mask]) * (1.0 - color_image[~mask])
    elif blend_mode == "soft_light":
        blended = (1.0 - 2 * color_image) * img_float**2 + 2 * color_image * img_float
    else:
        # Default to multiply
        blended = img_float * color_image

    # Apply opacity
    result = img_float * (1 - opacity) + blended * opacity

    # Clip and convert back to uint8
    result = np.clip(result, 0.0, 1.0)
    return (result * 255.0).astype(np.uint8)


def gradient_map(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    colors: Optional[List[RGBColor]] = None,
    stops: Optional[List[float]] = None
) -> np.ndarray:
    """
    Map image luminance to a multi-color gradient.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette
        colors: List of colors for gradient (defaults to palette colors)
        stops: List of gradient stop positions (0-1)

    Returns:
        Gradient-mapped image as numpy array
    """
    # Default to palette colors if none provided
    if colors is None:
        colors = [
            palette.primary,
            palette.accent,
            palette.secondary
        ]

    # Create stops if not provided
    if stops is None:
        stops = np.linspace(0, 1, len(colors))
    else:
        # Ensure stops are between 0 and 1
        stops = np.clip(stops, 0, 1)

    # Convert to grayscale for mapping
    if image.ndim == 3:
        grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        grayscale = image.copy()

    # Normalize to 0-1
    grayscale = grayscale.astype(np.float32) / 255.0

    # Create output image
    height, width = grayscale.shape
    result = np.zeros((height, width, 3), dtype=np.float32)

    # Convert colors to numpy arrays
    color_values = np.array([c.as_normalized for c in colors])

    # For each pixel, find its position in the gradient
    for y in range(height):
        for x in range(width):
            value = grayscale[y, x]

            # Find the gradient segment this value falls into
            for i in range(len(stops) - 1):
                if stops[i] <= value <= stops[i + 1]:
                    # Calculate position within this segment
                    segment_pos = (value - stops[i]) / (stops[i + 1] - stops[i])

                    # Interpolate between colors
                    result[y, x] = color_values[i] * (1 - segment_pos) + color_values[i + 1] * segment_pos
                    break

            # Edge case for max value
            if value >= stops[-1]:
                result[y, x] = color_values[-1]

    # Convert back to uint8
    return (result * 255.0).astype(np.uint8)


def selective_color(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    target_color: RGBColor,
    tolerance: float = 0.2,
    replacement_color: Optional[RGBColor] = None,
    keep_luminance: bool = True
) -> np.ndarray:
    """
    Replace a specific color in the image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette
        target_color: Color to be replaced
        tolerance: How similar colors must be to match (0-1)
        replacement_color: New color (defaults to palette.accent)
        keep_luminance: Whether to preserve original luminance

    Returns:
        Selectively colored image as numpy array
    """
    if replacement_color is None:
        replacement_color = palette.accent

    # Convert to float for calculations
    img_float = image.astype(np.float32) / 255.0

    # Target color as array
    target = np.array(target_color.as_normalized)
    replacement = np.array(replacement_color.as_normalized)

    # Calculate color distance for each pixel (Euclidean distance in RGB space)
    distances = np.sqrt(np.sum((img_float - target)**2, axis=2))

    # Create a mask for pixels that are close to the target color
    mask = distances < tolerance

    # Create a copy of the input image for output
    result = img_float.copy()

    if keep_luminance:
        # Convert target and replacement to HSV
        target_hsv = cv2.cvtColor(
            np.array([[target]]) * 255,
            cv2.COLOR_RGB2HSV
        )[0, 0].astype(np.float32) / 255.0

        replacement_hsv = cv2.cvtColor(
            np.array([[replacement]]) * 255,
            cv2.COLOR_RGB2HSV
        )[0, 0].astype(np.float32) / 255.0

        # Convert image to HSV
        hsv = cv2.cvtColor((img_float * 255).astype(np.uint8), cv2.COLOR_RGB2HSV)
        hsv = hsv.astype(np.float32) / 255.0

        # For masked pixels, replace hue and saturation but keep value
        if mask.any():
            # Update hue and saturation
            temp_hsv = hsv.copy()
            temp_hsv[mask, 0] = replacement_hsv[0]  # Hue
            temp_hsv[mask, 1] = replacement_hsv[1]  # Saturation

            # Convert back to RGB
            temp_rgb = cv2.cvtColor(
                (temp_hsv * 255).astype(np.uint8),
                cv2.COLOR_HSV2RGB
            )
            result[mask] = temp_rgb[mask].astype(np.float32) / 255.0
    else:
        # Simply replace the color
        for i in range(3):  # RGB channels
            channel = result[:, :, i]
            channel[mask] = replacement[i]

    # Return as uint8
    return (result * 255.0).astype(np.uint8)
