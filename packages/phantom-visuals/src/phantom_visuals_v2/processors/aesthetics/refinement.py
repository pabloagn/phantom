# apts/aesthetics/refinement.py

"""Aesthetic refinement module for enhancing artistic portraits with professional-level enhancements."""

import numpy as np
import torch
import cv2
from typing import Dict, List, Tuple, Optional, Any
import os
import sys


class AestheticRefinement:
    """
    Applies professional-level aesthetic enhancements to ensure
    high-quality, refined results for artistic portraits.
    """

    def __init__(self, config, device=None):
        """
        Initialize the aesthetic refinement module.

        Args:
            config: Configuration dictionary
            device: Computation device (CPU or CUDA)
        """
        self.config = config
        self.device = (
            device
            if device is not None
            else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )

        # Initialize enhancement parameters
        self.contrast_enhancement = config.get("contrast_enhancement", 0.1)
        self.detail_enhancement = config.get("detail_enhancement", 0.2)
        self.micro_contrast = config.get("micro_contrast", 0.15)
        self.color_grading = config.get("color_grading", True)
        self.denoise = config.get("denoise", 0.1)
        self.sharpen = config.get("sharpen", 0.2)
        self.vignette = config.get("vignette", 0.1)

        # Initialize color grading parameters
        self.color_temp = config.get("color_temp", 0.0)  # -1 to 1, cool to warm
        self.color_tint = config.get("color_tint", 0.0)  # -1 to 1, green to magenta
        self.saturation = config.get("saturation", 0.0)  # -1 to 1, less to more

        # Shadow/highlight parameters
        self.shadow_lift = config.get("shadow_lift", 0.0)  # -1 to 1
        self.highlight_reduce = config.get("highlight_reduce", 0.0)  # -1 to 1

        # Film grain parameters
        self.film_grain = config.get("film_grain", 0.1)  # 0 to 1

    def refine(self, state: Dict) -> Dict[str, Any]:
        """
        Apply aesthetic refinements to the image.

        Args:
            state: Current transformation state

        Returns:
            Updated state with refinements
        """
        result = {}

        # Ensure we have an image to work with
        if "composed_image" in state:
            image = state["composed_image"]
        elif "material_diffuse" in state:
            image = state["material_diffuse"]
        else:
            # Fallback to original image
            image = state["original_image"].astype(np.float32) / 255.0

        # Apply refinements
        refined = self._apply_refinements(image, state)
        result["refined_image"] = refined

        # Set as final image
        result["final_image"] = refined

        return result

    def _apply_refinements(self, image: np.ndarray, state: Dict) -> np.ndarray:
        """Apply refinement pipeline to image."""
        # Start with copy of input image
        refined = image.copy()

        # 1. Denoise if enabled
        if self.denoise > 0:
            refined = self._apply_denoise(refined)

        # 2. Contrast enhancement
        if self.contrast_enhancement != 0:
            refined = self._apply_contrast(refined)

        # 3. Detail enhancement
        if self.detail_enhancement > 0:
            refined = self._apply_detail_enhancement(refined)

        # 4. Color grading
        if self.color_grading:
            refined = self._apply_color_grading(refined)

        # 5. Shadow/highlight adjustment
        if self.shadow_lift != 0 or self.highlight_reduce != 0:
            refined = self._apply_shadow_highlight(refined)

        # 6. Micro contrast (clarity)
        if self.micro_contrast > 0:
            refined = self._apply_micro_contrast(refined)

        # 7. Sharpening
        if self.sharpen > 0:
            refined = self._apply_sharpening(refined)

        # 8. Vignette
        if self.vignette > 0:
            refined = self._apply_vignette(refined)

        # 9. Film grain
        if self.film_grain > 0:
            refined = self._apply_film_grain(refined)

        # 10. Final corrections
        refined = np.clip(refined, 0, 1)

        return refined

    def _apply_denoise(self, image: np.ndarray) -> np.ndarray:
        """Apply noise reduction."""
        # Convert to 8-bit for OpenCV processing
        img_8bit = (image * 255).astype(np.uint8)
        
        # Calculate strength based on image size
        h, w = image.shape[:2]
        h_luminance = int(self.denoise * 10) + 1  # Filter strength for luminance
        h_color = h_luminance      # Filter strength for color components
        template_window_size = 7   # Size in pixels of the template patch
        search_window_size = 21    # Size in pixels of the window to search for similar patches
        
        try:
            # Apply denoising with properly documented parameters
            denoised = cv2.fastNlMeansDenoisingColored(
                img_8bit,          # Input image
                None,              # Destination image (None = create new)
                h_luminance,       # Filter strength for luminance
                h_color,           # Filter strength for color
                template_window_size,  # Template window size
                search_window_size     # Search window size
            )
        except Exception as e:
            print(f"Warning: Error applying denoising: {e}")
            return image
        
        # Convert back to float
        return np.clip(denoised.astype(np.float32) / 255.0, 0, 1)

    def _apply_contrast(self, image: np.ndarray) -> np.ndarray:
        """Apply contrast enhancement."""
        # Apply sigmoid contrast curve
        # This gives more control than simple linear scaling
        if self.contrast_enhancement > 0:
            # Increase contrast
            alpha = 1.0 + self.contrast_enhancement * 2
            beta = -self.contrast_enhancement * 0.5
        else:
            # Decrease contrast
            alpha = 1.0 + self.contrast_enhancement
            beta = -self.contrast_enhancement * 0.25

        # Apply contrast adjustment
        adjusted = image * alpha + beta

        # Apply sigmoid curve for smoother contrast
        adjusted = 1.0 / (
            1.0 + np.exp(-(adjusted - 0.5) * (4.0 + abs(self.contrast_enhancement) * 4))
        )

        return adjusted

    def _apply_detail_enhancement(self, image: np.ndarray) -> np.ndarray:
        """Apply detail enhancement using bilateral filter."""
        # Convert to 8-bit for OpenCV processing
        img_8bit = (image * 255).astype(np.uint8)

        # Apply bilateral filter to get base
        h, w = image.shape[:2]
        d = max(
            3, min(9, int(min(h, w) / 100))
        )  # Automatic d value based on image size
        bilateral = cv2.bilateralFilter(img_8bit, d, 30, 30)

        # Extract detail layer
        detail = img_8bit.astype(np.float32) - bilateral.astype(np.float32)

        # Add scaled detail back to original
        enhanced = img_8bit.astype(np.float32) + detail * self.detail_enhancement

        # Convert back to float [0,1]
        return np.clip(enhanced / 255.0, 0, 1)

    def _apply_color_grading(self, image: np.ndarray) -> np.ndarray:
        """Apply color grading."""
        # Convert to 8-bit for OpenCV processing
        img_8bit = (image * 255).astype(np.uint8)

        # Convert to LAB colorspace
        lab = cv2.cvtColor(img_8bit, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)

        # Adjust color temperature (blue-yellow balance)
        if self.color_temp != 0:
            # Shift b channel (blue-yellow)
            b = np.clip(b + self.color_temp * 30, 0, 255).astype(np.uint8)

        # Adjust color tint (green-magenta balance)
        if self.color_tint != 0:
            # Shift a channel (green-magenta)
            a = np.clip(a + self.color_tint * 30, 0, 255).astype(np.uint8)

        # Merge channels
        lab = cv2.merge([l, a, b])

        # Convert back to RGB
        graded = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

        # Adjust saturation
        if self.saturation != 0:
            # Convert to HSV to adjust saturation
            hsv = cv2.cvtColor(graded, cv2.COLOR_RGB2HSV)
            h, s, v = cv2.split(hsv)

            # Adjust saturation
            if self.saturation > 0:
                # Increase saturation
                s = np.clip(s * (1 + self.saturation), 0, 255).astype(np.uint8)
            else:
                # Decrease saturation
                s = np.clip(s * (1 + self.saturation), 0, 255).astype(np.uint8)

            # Merge channels
            hsv = cv2.merge([h, s, v])

            # Convert back to RGB
            graded = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

        # Convert back to float [0,1]
        return graded.astype(np.float32) / 255.0

    def _apply_shadow_highlight(self, image: np.ndarray) -> np.ndarray:
        """Apply shadow and highlight adjustments."""
        # Make a copy of the image
        adjusted = image.copy()

        # Calculate luminance
        luminance = (
            0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]
        )

        # Shadow mask (nonlinear for better targeting)
        if self.shadow_lift != 0:
            shadows = 1.0 - np.power(luminance, 0.5)

            # Apply shadow lift
            adjustment = self.shadow_lift * shadows[:, :, np.newaxis]
            adjusted += adjustment

        # Highlight mask (nonlinear for better targeting)
        if self.highlight_reduce != 0:
            highlights = np.power(luminance, 2.0)

            # Apply highlight reduction
            adjustment = -self.highlight_reduce * highlights[:, :, np.newaxis]
            adjusted += adjustment

        # Ensure valid range
        adjusted = np.clip(adjusted, 0, 1)

        return adjusted

    def _apply_micro_contrast(self, image: np.ndarray) -> np.ndarray:
        """Apply micro contrast enhancement (clarity)."""
        # Convert to 8-bit
        img_8bit = (image * 255).astype(np.uint8)

        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(img_8bit, cv2.COLOR_RGB2GRAY)

        # Apply Laplacian filter to find edges
        laplacian = cv2.Laplacian(gray, cv2.CV_32F, ksize=3)

        # Scale Laplacian result
        scaled_lap = laplacian * self.micro_contrast

        # Add scaled Laplacian to each color channel
        enhanced = image.copy()
        for c in range(3):
            enhanced[:, :, c] += scaled_lap / 255.0

        # Ensure valid range
        enhanced = np.clip(enhanced, 0, 1)

        return enhanced

    def _apply_sharpening(self, image: np.ndarray) -> np.ndarray:
        """Apply sharpening."""
        # Convert to 8-bit
        img_8bit = (image * 255).astype(np.uint8)

        # Create sharpening kernel that preserves image brightness
        center = 1 + 8 * self.sharpen
        outer = -1 * self.sharpen
        kernel = np.array(
            [
                [outer, outer, outer],
                [outer, center, outer],
                [outer, outer, outer],
            ]
        )

        # Apply kernel
        try:
            sharpened = cv2.filter2D(img_8bit, -1, kernel)
        except Exception as e:
            print(f"Warning: Error applying sharpening: {e}")
            return image

        # Convert back to float
        return np.clip(sharpened.astype(np.float32) / 255.0, 0, 1)

    def _apply_vignette(self, image: np.ndarray) -> np.ndarray:
        """Apply vignette effect."""
        h, w = image.shape[:2]

        # Create vignette mask
        y, x = np.ogrid[0:h, 0:w]
        center_y, center_x = h / 2, w / 2

        # Calculate squared distance from center
        dist = (x - center_x) ** 2 / (w / 2) ** 2 + (y - center_y) ** 2 / (h / 2) ** 2

        # Create circular vignette
        mask = 1 - dist * self.vignette * 2
        mask = np.clip(mask, 0, 1)

        # Apply mask
        vignette = image * mask[:, :, np.newaxis]

        return vignette

    def _apply_film_grain(self, image: np.ndarray) -> np.ndarray:
        """Apply film grain effect."""
        h, w = image.shape[:2]

        # Generate noise
        noise = np.random.normal(0, 1, (h, w, 3)) * self.film_grain * 0.1

        # Add noise
        grainy = image + noise

        # Ensure valid range
        grainy = np.clip(grainy, 0, 1)

        return grainy
