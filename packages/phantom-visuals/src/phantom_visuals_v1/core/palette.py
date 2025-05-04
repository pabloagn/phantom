# packages/phantom-visuals/phantom_visuals/core/palette.py

"""
Color palette management for Phantom Visuals.

Provides sophisticated color manipulation for maintaining consistent
aesthetics across transformations.
"""

from typing import Dict, List, Tuple, Optional, Union, Any
import colorsys
import random
from pydantic import BaseModel, Field

from phantom_visuals.core.config import ColorScheme


class RGBColor(BaseModel):
    """RGB color representation with values from 0-255."""
    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)

    @property
    def as_tuple(self) -> Tuple[int, int, int]:
        """Return the color as an RGB tuple."""
        return (self.r, self.g, self.b)

    @property
    def as_hex(self) -> str:
        """Return the color as a hex string."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    @property
    def as_normalized(self) -> Tuple[float, float, float]:
        """Return the color as normalized RGB values between 0 and 1."""
        return (self.r / 255.0, self.g / 255.0, self.b / 255.0)

    @classmethod
    def from_hex(cls, hex_color: str) -> "RGBColor":
        """Create a color from a hex string."""
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return cls(r=r, g=g, b=b)

    def adjust_brightness(self, factor: float) -> "RGBColor":
        """Adjust the brightness of the color."""
        h, s, v = colorsys.rgb_to_hsv(*self.as_normalized)
        v = max(0.0, min(1.0, v * factor))
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return RGBColor(r=int(r * 255), g=int(g * 255), b=int(b * 255))

    def adjust_saturation(self, factor: float) -> "RGBColor":
        """Adjust the saturation of the color."""
        h, s, v = colorsys.rgb_to_hsv(*self.as_normalized)
        s = max(0.0, min(1.0, s * factor))
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return RGBColor(r=int(r * 255), g=int(g * 255), b=int(b * 255))

    def shift_hue(self, amount: float) -> "RGBColor":
        """Shift the hue of the color by a specified amount (0-1)."""
        h, s, v = colorsys.rgb_to_hsv(*self.as_normalized)
        h = (h + amount) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return RGBColor(r=int(r * 255), g=int(g * 255), b=int(b * 255))

    def complement(self) -> "RGBColor":
        """Get the complementary color."""
        return self.shift_hue(0.5)


class ColorPalette(BaseModel):
    """A color palette containing a set of colors for a specific scheme."""
    primary: RGBColor
    secondary: RGBColor
    accent: RGBColor
    background: RGBColor
    foreground: RGBColor
    additional: Dict[str, RGBColor] = Field(default_factory=dict)

    @classmethod
    def create_phantom_core(cls) -> "ColorPalette":
        """Create the default Phantom Core color palette."""
        return cls(
            primary=RGBColor(r=15, g=15, b=20),       # Near black with blue tint
            secondary=RGBColor(r=220, g=220, b=225),  # Off-white
            accent=RGBColor(r=70, g=80, b=110),       # Muted blue-grey
            background=RGBColor(r=240, g=240, b=245), # Very light grey
            foreground=RGBColor(r=30, g=30, b=35),    # Dark grey
            additional={
                "highlight": RGBColor(r=120, g=130, b=160),  # Muted lavender
                "shadow": RGBColor(r=10, g=10, b=15),        # Deep shadow
                "mist": RGBColor(r=200, g=200, b=210),       # Misty grey
                "ethereal": RGBColor(r=180, g=190, b=210),   # Ethereal blue-grey
            }
        )

    @classmethod
    def create_gothic(cls) -> "ColorPalette":
        """Create a gothic-inspired color palette."""
        return cls(
            primary=RGBColor(r=20, g=10, b=15),         # Deep burgundy-black
            secondary=RGBColor(r=190, g=180, b=170),    # Aged parchment
            accent=RGBColor(r=90, g=30, b=40),          # Dark blood red
            background=RGBColor(r=30, g=25, b=30),      # Deep purple-black
            foreground=RGBColor(r=210, g=200, b=190),   # Faded ivory
            additional={
                "shadow": RGBColor(r=5, g=0, b=10),       # Absolute darkness
                "mist": RGBColor(r=100, g=90, b=110),     # Twilight mist
                "accent2": RGBColor(r=130, g=110, b=90),  # Aged bronze
                "highlight": RGBColor(r=230, g=210, b=180), # Candlelight
            }
        )

    @classmethod
    def create_modernist(cls) -> "ColorPalette":
        """Create a modernist-inspired color palette."""
        return cls(
            primary=RGBColor(r=240, g=240, b=240),      # Clean white
            secondary=RGBColor(r=20, g=20, b=20),       # Deep black
            accent=RGBColor(r=200, g=50, b=30),         # Bold red
            background=RGBColor(r=245, g=245, b=245),   # Gallery white
            foreground=RGBColor(r=40, g=40, b=40),      # Rich black
            additional={
                "accent2": RGBColor(r=30, g=90, b=150),  # Bold blue
                "accent3": RGBColor(r=250, g=200, b=0),  # Vibrant yellow
                "grid": RGBColor(r=220, g=220, b=220),   # Grid grey
                "highlight": RGBColor(r=255, g=100, b=50), # Orange highlight
            }
        )

    @classmethod
    def create_ethereal(cls) -> "ColorPalette":
        """Create an ethereal, dreamlike color palette."""
        return cls(
            primary=RGBColor(r=220, g=230, b=245),      # Pale sky blue
            secondary=RGBColor(r=250, g=245, b=255),    # Almost white
            accent=RGBColor(r=180, g=200, b=230),       # Soft periwinkle
            background=RGBColor(r=240, g=245, b=255),   # Ice blue
            foreground=RGBColor(r=100, g=110, b=140),   # Muted blue-grey
            additional={
                "mist": RGBColor(r=200, g=210, b=230),    # Misty blue
                "highlight": RGBColor(r=255, g=250, b=245), # Bright white
                "shadow": RGBColor(r=170, g=180, b=210),  # Soft shadow
                "accent2": RGBColor(r=210, g=190, b=220), # Soft lavender
            }
        )

    @classmethod
    def from_scheme(cls, scheme: ColorScheme) -> "ColorPalette":
        """Create a color palette based on the specified scheme."""
        if scheme == ColorScheme.PHANTOM_CORE:
            return cls.create_phantom_core()
        elif scheme == ColorScheme.DARK:
            return cls.create_gothic()
        elif scheme == ColorScheme.LIGHT:
            return cls.create_ethereal()
        elif scheme == ColorScheme.VIBRANT:
            return cls.create_modernist()
        else:
            # Default to phantom core
            return cls.create_phantom_core()

    def get_random_color(self, seed: Optional[int] = None) -> RGBColor:
        """Get a random color from the palette."""
        if seed is not None:
            random.seed(seed)

        all_colors = [
            self.primary,
            self.secondary,
            self.accent,
            self.background,
            self.foreground,
            *self.additional.values()
        ]

        return random.choice(all_colors)

    def get_complementary_pair(self) -> Tuple[RGBColor, RGBColor]:
        """Get a complementary color pair from the palette."""
        return (self.primary, self.accent)

    def get_triadic_colors(self) -> Tuple[RGBColor, RGBColor, RGBColor]:
        """Get a triadic color scheme based on the primary color."""
        return (
            self.primary,
            self.primary.shift_hue(1/3),
            self.primary.shift_hue(2/3)
        )

    def get_analogous_colors(self, count: int = 3) -> List[RGBColor]:
        """Get analogous colors based on the primary color."""
        colors = [self.primary]
        step = 0.05

        for i in range(1, count):
            if i % 2 == 0:
                colors.append(self.primary.shift_hue(step * (i // 2)))
            else:
                colors.append(self.primary.shift_hue(-step * ((i + 1) // 2)))

        return colors
