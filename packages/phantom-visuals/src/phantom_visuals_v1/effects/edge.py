# packages/phantom-visuals/phantom_visuals/effects/edge.py

"""Edge effects for detecting and enhancing contours and boundaries.

This module provides functions for edge detection, thresholding, and
other boundary enhancement techniques that create stark minimalist aesthetics.
"""

from typing import List, Optional, Tuple, Union

import cv2
import numpy as np

from phantom_visuals.core.config import Configuration
from phantom_visuals.core.palette import ColorPalette, RGBColor


def detect_edges(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    amount: Optional[float] = None,
    method: str = "canny",
    color: Optional[RGBColor] = None,
) -> np.ndarray:
    """Detect edges in an image using various algorithms.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (for edge coloring)
        amount: Edge detection sensitivity (defaults to config.effect_params.edge_detection)
        method: Edge detection method ("canny", "sobel", "prewitt", "laplacian")
        color: Color for edges (defaults to palette.primary)

    Returns:
        Image with edges as numpy array
    """
    if amount is None:
        amount = config.effect_params.edge_detection

    # If amount is 0, return the original image
    if amount <= 0:
        return image

    # Convert to grayscale if color image
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image.copy()

    # Apply edge detection algorithm
    if method == "canny":
        # Scale amount to appropriate thresholds for Canny
        low_threshold = int(100 * (1 - amount))
        high_threshold = int(200 * (1 - amount / 2))

        edges = cv2.Canny(gray, low_threshold, high_threshold)

    elif method == "sobel":
        # Apply Sobel operator
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        # Calculate gradient magnitude
        magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

        # Normalize to 0-255
        magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(
            np.uint8
        )

        # Apply threshold based on amount
        threshold_value = int(255 * (1 - amount))
        _, edges = cv2.threshold(magnitude, threshold_value, 255, cv2.THRESH_BINARY)

    elif method == "prewitt":
        # Custom Prewitt kernels
        kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])

        # Apply kernels
        prewitt_x = cv2.filter2D(gray, cv2.CV_64F, kernel_x)
        prewitt_y = cv2.filter2D(gray, cv2.CV_64F, kernel_y)

        # Calculate gradient magnitude
        magnitude = np.sqrt(prewitt_x**2 + prewitt_y**2)

        # Normalize to 0-255
        magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(
            np.uint8
        )

        # Apply threshold based on amount
        threshold_value = int(255 * (1 - amount))
        _, edges = cv2.threshold(magnitude, threshold_value, 255, cv2.THRESH_BINARY)

    elif method == "laplacian":
        # Apply Laplacian filter
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)

        # Take absolute value and convert to uint8
        magnitude = np.abs(laplacian)
        magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(
            np.uint8
        )

        # Apply threshold based on amount
        threshold_value = int(255 * (1 - amount))
        _, edges = cv2.threshold(magnitude, threshold_value, 255, cv2.THRESH_BINARY)

    else:
        # Default to Canny if method not recognized
        edges = cv2.Canny(gray, 100, 200)

    # Create output image
    if image.ndim == 3:
        # Set color for edges
        if color is None:
            color = palette.primary

        # Create RGB output
        result = np.zeros_like(image)

        # Set edge color
        result[edges > 0] = color.as_tuple
    else:
        # For grayscale images, just return the edges
        result = edges

    return result


def enhance_edges(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    amount: Optional[float] = None,
    method: str = "unsharp",
) -> np.ndarray:
    """Enhance edges in an image without full edge detection.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (not used in this effect)
        amount: Enhancement strength (defaults to config.effect_params.edge_detection)
        method: Enhancement method ("unsharp", "highpass", "emboss")

    Returns:
        Edge-enhanced image as numpy array
    """
    if amount is None:
        amount = config.effect_params.edge_detection

    # If amount is 0, return the original image
    if amount <= 0:
        return image

    # Copy the input image
    result = image.copy()

    if method == "unsharp":
        # Apply Gaussian blur
        blur_radius = 3
        blurred = cv2.GaussianBlur(image, (0, 0), blur_radius)

        # Calculate unsharp mask
        unsharp_mask = image.astype(np.float32) - blurred.astype(np.float32)

        # Enhance edges by adding the mask back to the original
        result = image.astype(np.float32) + unsharp_mask * amount

        # Clip values to valid range
        result = np.clip(result, 0, 255).astype(np.uint8)

    elif method == "highpass":
        # Apply Gaussian blur for lowpass filter
        blur_radius = 3
        lowpass = cv2.GaussianBlur(image, (0, 0), blur_radius)

        # Calculate highpass (edges)
        highpass = image.astype(np.float32) - lowpass.astype(np.float32)

        # Scale the highpass and add back to original
        result = image.astype(np.float32) + highpass * amount

        # Clip values to valid range
        result = np.clip(result, 0, 255).astype(np.uint8)

    elif method == "emboss":
        # Define emboss kernel
        kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])

        # Apply emboss filter
        if image.ndim == 3:
            # Process each channel separately
            for c in range(image.shape[2]):
                channel = image[:, :, c]
                embossed = cv2.filter2D(channel, -1, kernel)
                result[:, :, c] = embossed
        else:
            result = cv2.filter2D(image, -1, kernel)

        # Normalize and adjust contrast
        result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX)

        # Blend with original image based on amount
        result = cv2.addWeighted(image, 1 - amount, result, amount, 0)

    return result


def threshold(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    threshold_value: float = 0.5,
    adaptive: bool = False,
    invert: bool = False,
) -> np.ndarray:
    """Apply binary thresholding to an image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (for foreground/background colors)
        threshold_value: Threshold level (0-1)
        adaptive: If True, use adaptive thresholding
        invert: If True, invert the result

    Returns:
        Thresholded image as numpy array
    """
    # Convert threshold from 0-1 to 0-255
    threshold_abs = int(threshold_value * 255)

    # Convert to grayscale if color image
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image.copy()

    # Apply thresholding
    if adaptive:
        binary = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,  # Block size
            2,  # Constant subtracted from mean
        )
    else:
        _, binary = cv2.threshold(gray, threshold_abs, 255, cv2.THRESH_BINARY)

    # Invert if requested
    if invert:
        binary = 255 - binary

    # For grayscale output, return binary mask
    if image.ndim < 3:
        return binary

    # For color images, map to palette colors
    result = np.zeros_like(image)

    # Set foreground/background colors
    fg_color = palette.foreground.as_tuple
    bg_color = palette.background.as_tuple

    if invert:
        fg_color, bg_color = bg_color, fg_color

    # Apply colors to binary mask
    result[binary == 0] = bg_color
    result[binary == 255] = fg_color

    return result


def outline(
    image: np.ndarray,
    config: Configuration,
    palette: ColorPalette,
    thickness: int = 1,
    color: Optional[RGBColor] = None,
    method: str = "contour",
) -> np.ndarray:
    """Create outline effect around shapes in the image.

    Args:
        image: Input image as numpy array
        config: Configuration settings
        palette: Color palette (for outline color)
        thickness: Outline thickness in pixels
        color: Outline color (defaults to palette.primary)
        method: Outline method ("contour", "canny")

    Returns:
        Outlined image as numpy array
    """
    # Set default color
    if color is None:
        color = palette.primary

    # Convert to grayscale if color image
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) if image.ndim == 3 else image.copy()

    # Create blank canvas for the outlines
    height, width = gray.shape[:2]
    outlines = np.zeros((height, width), dtype=np.uint8)

    if method == "contour":
        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Draw contours on blank canvas
        cv2.drawContours(outlines, contours, -1, 255, thickness)

    elif method == "canny":
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 100, 200)

        # Dilate edges to the desired thickness
        if thickness > 1:
            kernel = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (thickness, thickness)
            )
            outlines = cv2.dilate(edges, kernel)
        else:
            outlines = edges

    # Create result image
    if image.ndim == 3:
        # For color images, blend outlines with original
        result = image.copy()

        # Apply outline color
        for c in range(3):
            channel = result[:, :, c]
            channel[outlines > 0] = color.as_tuple[c]
    else:
        # For grayscale images, just return the outlines
        result = outlines

    return result
