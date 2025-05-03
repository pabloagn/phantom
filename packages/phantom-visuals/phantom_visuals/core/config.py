# packages/phantom-visuals/phantom_visuals/core/config.py

"""Configuration for the Phantom Visuals system."""

import json
import os
import random
from enum import Enum
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel, Field


# --- StyleVariant Enum ---
class StyleVariant(str, Enum):
    """Style variants for the Phantom Visuals system."""

    PHANTOM = "phantom"
    MINIMAL = "minimal"
    DUOTONE = "duotone"
    ABSTRACT = "abstract"
    GLITCH = "glitch"
    ETHEREAL = "ethereal"
    MODERNIST = "modernist"
    GOTHIC = "gothic"
    SYMMETRICAL = "symmetrical"
    CONTOUR = "contour"
    WAVE = "wave"
    MINIMAL_ORGANIC = "minimal_organic"
    ABSTRACT_WILD = "abstract_wild"
    GLITCH_REFINED = "glitch_refined"
    ETHEREAL_ORGANIC = "ethereal_organic"
    MODERNIST_ORGANIC = "modernist_organic"
    PHANTOM_ENHANCED = "phantom_enhanced"
    GOTHIC_DISTORTED = "gothic_distorted"
    FRACTAL = "fractal"
    FOURIER = "fourier"
    WAVE_FUNCTION = "wave_function"
    STATISTICAL = "statistical"
    GOTHIC_SUBTLE = "gothic_subtle"
    PHANTOM_SPECTRAL = "phantom_spectral"
    GLITCH_BALANCED = "glitch_balanced"
    SPECTRAL_VEIL = "spectral_veil"
    GHOST_TRAILS = "ghost_trails"
    PHANTOM_FLOW = "phantom_flow"
    TOPOGRAPHIC_WAVE = "topographic_wave"
    SLIT_SCAN_DISTORT = "slit_scan_distort"
    SMUDGE_FLOW = "smudge_flow"
    TOPOGRAPHIC_REFINED = "topographic_refined"
    LONG_EXPOSURE_SCAN = "long_exposure_scan"
    GHOSTLY_SMEAR = "ghostly_smear"
    TOPOGRAPHIC_DEPTH = "topographic_depth"
    TEMPORAL_FLOW = "temporal_flow"
    LIQUID_GHOST = "liquid_ghost"
    TOPOGRAPHIC_MESH = "topographic_mesh"
    TEMPORAL_STREAK = "temporal_streak"
    ETHEREAL_SMUDGE = "ethereal_smudge"
    PLOTTER_MESH_V3 = "plotter_mesh_v3"
    STREAK_ACCUMULATE_V3 = "streak_accumulate_v3"
    FLOW_SMUDGE_V3 = "flow_smudge_v3"
    CELESTIAL_DRIFT_V4 = "celestial_drift_v4"
    PLOTTER_MESH_V3B = "plotter_mesh_v3b"
    TOPO_STREAK_WEAVE = "topo_streak_weave"
    ENHANCED_PARTICLE_WEAVE = "enhanced_particle_weave"
    FLOW_FIELD_BLUR = "flow_field_blur"
    MASKED_DIFFUSION_SMEAR = "masked_diffusion_smear"
    MESH_OVERLAY_FUSION = "mesh_overlay_fusion"


# --- ColorScheme Enum ---
class ColorScheme(str, Enum):
    """Color schemes for the Phantom Visuals system."""

    DEFAULT = "default"
    LIGHT = "light"
    DARK = "dark"
    MONOCHROME = "monochrome"
    HIGH_CONTRAST = "high_contrast"
    MUTED = "muted"
    VIBRANT = "vibrant"
    NEON = "neon"
    RETRO = "retro"
    PHANTOM_CORE = "phantom_core"


# --- OutputFormat Enum ---
class OutputFormat(str, Enum):
    """Output formats for the Phantom Visuals system."""

    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"
    TIFF = "tiff"


# --- EffectParameters Model (Ensure all tunable params are listed with defaults) ---
class EffectParameters(BaseModel):
    """Effect parameters for the Phantom Visuals system."""

    intensity: float = Field(0.75, ge=0.0, le=1.0)
    blur_radius: float = Field(0.0, ge=0.0, le=50.0)
    noise_level: float = Field(0.0, ge=0.0, le=1.0)
    contrast: float = Field(1.0, ge=0.0, le=3.0)
    brightness: float = Field(1.0, ge=0.0, le=3.0)
    saturation: float = Field(1.0, ge=0.0, le=3.0)
    hue_shift: float = Field(0.0, ge=0.0, le=1.0)
    pixelation: int = Field(0, ge=0, le=100)
    edge_detection: float = Field(0.0, ge=0.0, le=1.0)
    distortion: float = Field(0.0, ge=0.0, le=1.0)
    grain: float = Field(0.0, ge=0.0, le=1.0)
    vignette: float = Field(0.0, ge=0.0, le=1.0)
    symmetry: bool = False
    invert: bool = False
    seed: Optional[int] = None

    def with_seed(
        self: "EffectParameters", seed: Optional[int] = None
    ) -> "EffectParameters":
        """Create a copy with a specific seed."""
        params = self.model_copy()
        params.seed = seed if seed is not None else random.randint(0, 999999)
        return params


# --- Configuration Model ---
class Configuration(BaseModel):
    """Main configuration for the Phantom Visuals system."""

    style_variant: StyleVariant = StyleVariant.PHANTOM
    color_scheme: ColorScheme = ColorScheme.PHANTOM_CORE
    output_format: OutputFormat = OutputFormat.PNG
    output_quality: int = Field(95, ge=1, le=100)
    output_dir: str = "output"  # Default output dir for single transforms
    effect_params: EffectParameters = Field(default_factory=EffectParameters)

    @property
    def random_seed(self: "Configuration") -> int:
        """Get the random seed for reproducible effects."""
        # Generate a seed only if needed and not set
        if self.effect_params.seed is None:
            self.effect_params.seed = random.randint(0, 999999)
        return self.effect_params.seed

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "Configuration":
        """Load configuration from a JSON file."""
        # TODO: Could be extended to load from TOML too if needed for single runs
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            return cls.model_validate(data)
        except Exception as e:
            # Log error here if logger is accessible
            raise OSError(f"Error reading or parsing config file {path}: {e}") from e

    def to_file(self: "Configuration", path: Union[str, Path]) -> None:
        """Save configuration to a JSON file."""
        path = Path(path)
        os.makedirs(path.parent, exist_ok=True)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.model_dump_json(indent=2))
        except Exception as e:
            # Log error here if logger is accessible
            raise OSError(f"Error writing config file {path}: {e}") from e

    def clone(self: "Configuration") -> "Configuration":
        """Create a deep copy of the configuration."""
        return self.model_copy(deep=True)
