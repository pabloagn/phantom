# packages/phantom-visuals/src/phantom_visuals_v2/processors/utils/visualization.py

"""Visualization utilities for phantom_visuals_v2."""

from typing import Any

import cv2
import numpy as np


def create_debug_visualization(
    original_image: np.ndarray, transformation_state: dict[str, Any]
) -> np.ndarray:
    """Create a debug visualization combining multiple stages of processing.

    Args:
        original_image: Original input image
        transformation_state: Current transformation state

    Returns:
        Debug visualization image
    """
    # Default visualization is just the original image
    # This is a placeholder and would normally create a grid of visualizations
    height, width = original_image.shape[:2]
    result = np.zeros((height, width * 2, 3), dtype=np.uint8)

    # Copy the original image in the left half
    result[:, :width] = original_image

    # Get the final image (if available) for the right half
    final_image = transformation_state.get(
        "final_image",
        transformation_state.get(
            "refined_image",
            transformation_state.get(
                "composed_image", original_image
            )
        )
    )

    # Copy the processed image to the right half
    result[:, width:] = final_image

    # Add a dividing line
    cv2.line(result, (width, 0), (width, height), (255, 255, 255), 1)

    # Add labels
    cv2.putText(
        result, "Original", (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2
    )
    cv2.putText(
        result, "Processed", (width + 10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2
    )

    return result
