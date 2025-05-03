# packages/phantom-visuals/phantom_visuals/core/config.py

"""Configuration module for Phantom Visuals.

Defines the configuration classes and types used throughout the system.
"""

import json
import os
import random
from enum import Enum
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel, Field


class StyleVariant(str, Enum):
    """Style variant options for image transformations."""
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
    # New mathematical styles
    FRACTAL = "fractal"
    FOURIER = "fourier"
    WAVE_FUNCTION = "wave_function"
    STATISTICAL = "statistical"
    # New style variations based on feedback
    GOTHIC_SUBTLE = "gothic_subtle"
    PHANTOM_SPECTRAL = "phantom_spectral"
    GLITCH_BALANCED = "glitch_balanced"
    SPECTRAL_VEIL = "spectral_veil"
    GHOST_TRAILS = "ghost_trails"
    # Long exposure phantasmagoric style
    PHANTOM_FLOW = "phantom_flow"
    TOPOGRAPHIC_WAVE = "topographic_wave" # Implementation for the first example (Joy Division style)
    SLIT_SCAN_DISTORT = "slit_scan_distort" # Implementation for the second/third examples (Slit-scan simulation)
    # Long exposure phantasmagoric style - Second run
    SMUDGE_FLOW = "smudge_flow" # Implementation for smear/smudge effects
    TOPOGRAPHIC_REFINED = "topographic_refined" # Refined Joy Division style
    LONG_EXPOSURE_SCAN = "long_exposure_scan"  # Slit-scan / Temporal blur simulation
    GHOSTLY_SMEAR = "ghostly_smear"
    # Third run
    TOPOGRAPHIC_DEPTH = "topographic_depth"
    TEMPORAL_FLOW = "temporal_flow"
    LIQUID_GHOST = "liquid_ghost"
    # Fourth Run
    TOPOGRAPHIC_MESH = "topographic_mesh"
    TEMPORAL_STREAK = "temporal_streak"
    ETHEREAL_SMUDGE = "ethereal_smudge"
    # Fifth Run
    PLOTTER_MESH_V3 = "plotter_mesh_v3"
    STREAK_ACCUMULATE_V3 = "streak_accumulate_v3"
    FLOW_SMUDGE_V3 = "flow_smudge_v3"
    CELESTIAL_DRIFT_V4 = "celestial_drift_v4"

class ColorScheme(str, Enum):
    """Color schemes available for transformations."""
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


class OutputFormat(str, Enum):
    """Available output formats."""
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"
    TIFF = "tiff"


class EffectParameters(BaseModel):
    """Parameters for specific effects."""
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

    def with_seed(self, seed: Optional[int] = None) -> "EffectParameters":
        """Create a copy with a specific seed."""
        params = self.model_copy()
        params.seed = seed if seed is not None else random.randint(0, 999999)
        return params


class Configuration(BaseModel):
    """Main configuration for the Phantom Visuals system."""
    style_variant: StyleVariant = StyleVariant.PHANTOM
    color_scheme: ColorScheme = ColorScheme.PHANTOM_CORE
    output_format: OutputFormat = OutputFormat.PNG
    output_quality: int = Field(95, ge=1, le=100)
    output_dir: str = "output"
    effect_params: EffectParameters = Field(default_factory=EffectParameters)

    @property
    def random_seed(self) -> int:
        """Get the random seed for reproducible effects."""
        if self.effect_params.seed is None:
            self.effect_params.seed = random.randint(0, 999999)
        return self.effect_params.seed

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "Configuration":
        """Load configuration from a JSON file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        return cls.model_validate(data)

    def to_file(self, path: Union[str, Path]) -> None:
        """Save configuration to a JSON file."""
        path = Path(path)
        os.makedirs(path.parent, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=2))

    def clone(self) -> "Configuration":
        """Create a deep copy of the configuration."""
        return self.model_copy(deep=True)
