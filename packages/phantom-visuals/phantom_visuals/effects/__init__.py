# packages/phantom-visuals/phantom_visuals/effects/__init__.py

"""Effects module for phantom-visuals.

This module contains various image processing effects that can be applied
to transform images to achieve the distinctive Phantom visual style.
"""

from phantom_visuals.effects.artistic import (
    apply_symmetry,
    blur_regions,
    create_glitch_blocks,
    ethereal_glow,
    ghost_trails,
    pixelate,
    posterize,
    solarize,
)
from phantom_visuals.effects.base import EffectChain
from phantom_visuals.effects.blur import (
    gaussian_blur,
    motion_blur,
    radial_blur,
    tilt_shift_blur,
)
from phantom_visuals.effects.color import (
    adjust_brightness,
    adjust_contrast,
    adjust_saturation,
    apply_color_filter,
    color_shift,
    duotone,
    gradient_map,
    invert_colors,
)
from phantom_visuals.effects.distortion import (
    displace,
    glitch,
    lens_distortion,
    pixel_sort,
    swirl,
    wave_distortion,
)
from phantom_visuals.effects.edge import (
    detect_edges,
    enhance_edges,
    threshold,
)
from phantom_visuals.effects.texture import (
    add_grain,
    add_halftone,
    add_noise,
    add_vignette,
)

__all__ = [
    "EffectChain",
    "gaussian_blur",
    "motion_blur",
    "radial_blur",
    "tilt_shift_blur",
    "duotone",
    "adjust_contrast",
    "adjust_brightness",
    "adjust_saturation",
    "invert_colors",
    "color_shift",
    "apply_color_filter",
    "gradient_map",
    "pixel_sort",
    "wave_distortion",
    "glitch",
    "displace",
    "lens_distortion",
    "swirl",
    "add_grain",
    "add_noise",
    "add_vignette",
    "add_halftone",
    "detect_edges",
    "enhance_edges",
    "threshold",
    "posterize",
    "solarize",
    "pixelate",
    "apply_symmetry",
    "blur_regions",
    "ghost_trails",
    "ethereal_glow",
    "create_glitch_blocks",
]
