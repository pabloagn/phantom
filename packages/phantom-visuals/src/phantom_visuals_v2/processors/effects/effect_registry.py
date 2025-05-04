# apts/effects/effect_registry.py

import importlib
from typing import Dict, Any, Optional
import inspect
import os
import sys


class EffectRegistry:
    """
    Registry for effects that can be applied in the transformation pipeline.
    This provides a centralized way to manage and instantiate different effect implementations.
    """

    def __init__(self, config):
        """
        Initialize the effect registry.

        Args:
            config: Configuration for effects
        """
        self.config = config
        self.effects = {}

        # Register built-in effects
        self._register_builtin_effects()

        # Register custom effects if defined in config
        if hasattr(config, "custom_effects_path") and config.custom_effects_path:
            self._register_custom_effects(config.custom_effects_path)

    def _register_builtin_effects(self):
        """Register built-in effect implementations."""
        # Import effect modules
        from apts.effects.horizontal_smear import HorizontalSmearEffect
        from apts.effects.vertical_cascade import VerticalCascadeEffect
        from apts.effects.data_glitch import DataGlitchEffect
        from apts.effects.liquid_transform import LiquidTransformEffect
        from apts.effects.crystallize import CrystallizeEffect
        from apts.effects.echo_motion import EchoMotionEffect
        from apts.effects.spectral_shift import SpectralShiftEffect
        from apts.effects.particle_disintegration import ParticleDisintegrationEffect

        # Register effects
        self.register_effect("horizontal_smear", HorizontalSmearEffect)
        self.register_effect("vertical_cascade", VerticalCascadeEffect)
        self.register_effect("data_glitch", DataGlitchEffect)
        self.register_effect("liquid", LiquidTransformEffect)
        self.register_effect("crystallize", CrystallizeEffect)
        self.register_effect("echo_motion", EchoMotionEffect)
        self.register_effect("spectral_shift", SpectralShiftEffect)
        self.register_effect("particle_disintegration", ParticleDisintegrationEffect)

    def _register_custom_effects(self, custom_path):
        """Register custom effects from the specified path."""
        # Ensure path exists
        if not os.path.exists(custom_path):
            print(f"Custom effects path does not exist: {custom_path}")
            return

        # Add path to sys.path for importing
        if custom_path not in sys.path:
            sys.path.append(custom_path)

        # Search for effect modules
        for filename in os.listdir(custom_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]  # Remove .py

                try:
                    # Import module
                    module = importlib.import_module(module_name)

                    # Look for effect classes
                    for name, obj in inspect.getmembers(module):
                        if (
                            inspect.isclass(obj)
                            and hasattr(obj, "apply")
                            and hasattr(obj, "visualize")
                        ):
                            # Register effect
                            self.register_effect(module_name, obj)
                except ImportError as e:
                    print(f"Error importing custom effect {module_name}: {e}")

    def register_effect(self, name, effect_class):
        """
        Register an effect with the registry.

        Args:
            name: Name of the effect
            effect_class: Effect class to register
        """
        self.effects[name] = effect_class

        # Initialize with config if section exists
        if hasattr(self.config, name):
            effect_config = getattr(self.config, name)
            instance = effect_class(effect_config)
        else:
            # Default initialization
            instance = effect_class({})

        # Store instance
        self.effects[name + "_instance"] = instance

    def get_effect(self, name) -> Optional[Any]:
        """
        Get a registered effect instance by name.

        Args:
            name: Name of the effect

        Returns:
            Effect instance or None if not found
        """
        instance_key = name + "_instance"
        if instance_key in self.effects:
            return self.effects[instance_key]

        # Effect registered but not instantiated
        if name in self.effects:
            # Create instance
            effect_class = self.effects[name]

            # Initialize with config if section exists
            if hasattr(self.config, name):
                effect_config = getattr(self.config, name)
                instance = effect_class(effect_config)
            else:
                # Default initialization
                instance = effect_class({})

            # Store and return instance
            self.effects[instance_key] = instance
            return instance

        return None

    def list_effects(self):
        """List all registered effects."""
        return [name for name in self.effects if not name.endswith("_instance")]
