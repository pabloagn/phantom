# packages/phantom-visuals/src/phantom_visuals_v2/processors/core/pipeline.py

"""Main pipeline for artistic portrait transformation.

This class orchestrates the entire transformation process by coordinating
the different modules and maintaining the transformation state.
"""

from typing import Any, Optional, Union

import numpy as np
import torch

from phantom_visuals_v2.processors.aesthetics.refinement import AestheticRefinement
from phantom_visuals_v2.processors.analysis.face_analyzer import FaceAnalyzer
from phantom_visuals_v2.processors.composition.compositor import Compositor
from phantom_visuals_v2.processors.effects.effect_registry import EffectRegistry
from phantom_visuals_v2.processors.flow.flow_generator import FlowGenerator
from phantom_visuals_v2.processors.material.material_simulator import MaterialSimulator
from phantom_visuals_v2.processors.temporal.coherence import TemporalCoherenceSystem


class TransformationPipeline:
    """Main pipeline for artistic portrait transformation.

    This class orchestrates the entire transformation process by coordinating
    the different modules and maintaining the transformation state.
    """

    def __init__(self, config: Any, device: Optional[torch.device] = None) -> None:
        """Initialize the transformation pipeline with the provided configuration.

        Args:
            config: Configuration object containing pipeline parameters
            device: Torch device to use (cuda or cpu)
        """
        self.config = config
        self.device = (
            device
            if device is not None
            else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )

        # Initialize transformation state dictionary
        self.state: dict[str, Any] = {}

        # Initialize pipeline components
        try:
            self.face_analyzer = FaceAnalyzer(
                getattr(config, "analysis", {}), device=self.device
            )
            self.flow_generator = FlowGenerator(
                getattr(config, "flow", {}), device=self.device
            )
            self.material_simulator = MaterialSimulator(
                getattr(config, "material", {}), device=self.device
            )
            self.compositor = Compositor(
                getattr(config, "composition", {}), device=self.device
            )
            self.temporal_system = TemporalCoherenceSystem(
                getattr(config, "temporal", {}), device=self.device
            )
            self.aesthetic_refinement = AestheticRefinement(
                getattr(config, "aesthetics", {}), device=self.device
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize pipeline components: {e}")

        # Initialize effect registry
        self.effect_registry = EffectRegistry(config.effects)

        # Load primary effect if specified
        self.primary_effect = None
        if hasattr(config, "primary_effect") and config.primary_effect:
            self.primary_effect = self.effect_registry.get_effect(config.primary_effect)

    def transform(
        self,
        image: np.ndarray,
        variation_seed: int | None = None,
        return_intermediates: bool = False,
    ) -> np.ndarray | tuple[np.ndarray, dict[str, Any]]:
        """Apply the full transformation pipeline to an input image.

        Args:
            image: Input RGB image as numpy array (H,W,3)
            variation_seed: Optional seed to create variations
            return_intermediates: Whether to return intermediate results

        Returns:
            Transformed image as numpy array, and optionally intermediate results
        """
        # Reset transformation state
        self.state = {"original_image": image.copy()}
        intermediates: dict[str, Any] | None = {} if return_intermediates else None

        # Set variation seed if provided
        if variation_seed is not None:
            np.random.seed(variation_seed)
            torch.manual_seed(variation_seed)
            self.state["variation_seed"] = variation_seed

        # Stage 1: Face and portrait analysis
        try:
            self.state.update(self.face_analyzer.analyze(image))
            if return_intermediates and intermediates is not None:
                intermediates['face_mesh'] = self.face_analyzer.visualize_mesh(image, self.state)
                intermediates['depth_map'] = self.face_analyzer.visualize_depth(self.state)
        except Exception as e:
            print(f"Face analysis failed: {e}")
            # Set a flag for fallback handling
            self.state['face_analysis_failed'] = True

        # Stage 2: Flow field generation
        self.state.update(self.flow_generator.generate_flow(image, self.state))
        if return_intermediates and intermediates is not None:
            intermediates["flow_field"] = self.flow_generator.visualize_flow(self.state)

        # Stage 3: Material simulation
        self.state.update(self.material_simulator.simulate(image, self.state))
        if return_intermediates and intermediates is not None:
            intermediates["material_map"] = self.material_simulator.visualize_materials(
                self.state
            )

        # Apply primary effect if specified
        if self.primary_effect:
            self.state.update(self.primary_effect.apply(image, self.state))
            if return_intermediates and intermediates is not None:
                intermediates["primary_effect"] = self.primary_effect.visualize(
                    self.state
                )

        # Stage 4: Composition
        self.state.update(self.compositor.compose(image, self.state))
        if return_intermediates and intermediates is not None:
            intermediates["composed"] = self.state.get("composed_image", image).copy()

        # Stage 5: Temporal coherence (for single images, this mainly handles edge cases)
        self.state.update(self.temporal_system.process(self.state))

        # Stage 6: Aesthetic refinement
        self.state.update(self.aesthetic_refinement.refine(self.state))
        if return_intermediates and intermediates is not None:
            intermediates["refined"] = self.state.get("refined_image", image).copy()

        # Extract final result
        result = self.state.get(
            "final_image",
            self.state.get("refined_image", self.state.get("composed_image", image)),
        )

        # Return transformed image and optionally intermediates
        if return_intermediates and intermediates is not None:
            return result, intermediates
        return result
