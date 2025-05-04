# apts/temporal/coherence.py

"""Temporal coherence module for maintaining consistency across transformations."""

from typing import Any, Dict

import cv2
import numpy as np
import torch


class TemporalCoherenceSystem:
    """Ensures temporal coherence and consistency for transformations,
    particularly important for consistent results across related images.
    """
    
    def __init__(self, config, device=None):
        """Initialize the temporal coherence system.

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

        # Initialize parameters
        self.enable_temporal_smoothing = config.get('enable_temporal_smoothing', True)
        self.smoothing_window = config.get('smoothing_window', 5)
        self.motion_consistency = config.get('motion_consistency', 0.8)
        
        # Initialize state history
        self.history = []
        self.max_history = config.get('max_history', 10)
    
    def process(self, state: Dict) -> Dict[str, Any]:
        """Process the current state for temporal coherence.
        
        Args:
            state: Current transformation state
            
        Returns:
            Updated state with temporal coherence
        """
        result = {}
        
        # For single image processing, focus on consistency
        result.update(self._ensure_consistency(state))
        
        # Update history
        self._update_history(state)
        
        return result
    
    def _ensure_consistency(self, state: Dict) -> Dict[str, Any]:
        """Ensure consistency within a single transformation."""
        result = {}
        
        # Handle potential edge cases and inconsistencies
        
        # Ensure composed image exists
        if 'composed_image' not in state:
            if 'material_diffuse' in state:
                result['composed_image'] = state['material_diffuse'].copy()
            else:
                # Fallback to original image
                result['composed_image'] = state['original_image'].astype(np.float32) / 255.0
        
        # Check for NaN or Inf values in composed image
        if 'composed_image' in state:
            composed = state['composed_image']
            if np.any(np.isnan(composed)) or np.any(np.isinf(composed)):
                # Replace problematic values
                composed_fixed = np.nan_to_num(composed, nan=0.0, posinf=1.0, neginf=0.0)
                result['composed_image'] = composed_fixed
        
        # Set final image if needed
        if 'composed_image' in state or 'composed_image' in result:
            source = state.get('composed_image', result.get('composed_image'))
            result['final_image'] = source.copy()
        
        return result
    
    def _update_history(self, state: Dict) -> None:
        """Update the state history."""
        # Create simplified state for history
        history_state = {
            'timestamp': state.get('timestamp', 0),
            'variation_seed': state.get('variation_seed', None),
        }
        
        # Add key transform parameters
        if 'flow_field' in state:
            # Store average flow direction as compact representation
            flow = state['flow_field']
            avg_flow = np.mean(flow, axis=(0, 1))
            history_state['avg_flow'] = avg_flow
        
        if 'expression_weights' in state:
            history_state['expression_weights'] = state['expression_weights']
        
        # Add to history
        self.history.append(history_state)
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
