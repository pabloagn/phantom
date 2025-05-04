# apts/flow/flow_generator.py

"""Flow generation module for creating advanced flow fields based on facial structure and image content."""

import numpy as np
import torch
import torch.nn.functional as F
import cv2
from typing import Dict, List, Tuple, Optional, Any
import os
import sys

# Try to import RAFT for optical flow
try:
    # Add RAFT path
    sys.path.append(os.environ.get("RAFT_PATH", "third_party/RAFT"))
    from raft_core.raft import RAFT
    from raft_core.utils.utils import InputPadder

    RAFT_AVAILABLE = True
except ImportError:
    RAFT_AVAILABLE = False


class FlowGenerator:
    """Generates advanced flow fields for guiding artistic transformations
    based on facial structure and image content.
    """

    def __init__(self, config, device=None):
        """Initialize the flow field generator.

        Args:
            config: Configuration dictionary for flow generation
            device: Computation device (CPU or CUDA)
        """
        self.config = config
        self.device = (
            device
            if device is not None
            else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )

        # Initialize RAFT for optical flow if available
        self.raft_model = None
        if RAFT_AVAILABLE and config.get("use_raft", True):
            try:
                model_path = config.get("raft_model_path", "models/raft-things.pth")
                if not os.path.exists(model_path):
                    # Try default paths
                    default_paths = [
                        "third_party/RAFT/models/raft-things.pth",
                        os.path.join(
                            os.environ.get("RAFT_PATH", ""), "models/raft-things.pth"
                        ),
                    ]
                    for path in default_paths:
                        if os.path.exists(path):
                            model_path = path
                            break

                if os.path.exists(model_path):
                    args = type(
                        "Args",
                        (),
                        {
                            "model": model_path,
                            "small": False,
                            "mixed_precision": True,
                            "alternate_corr": False,
                        },
                    )
                    self.raft_model = RAFT(args)
                    self.raft_model.to(self.device)
                    self.raft_model.eval()

                    # Load pretrained weights
                    pretrained_weights = torch.load(
                        model_path, map_location=self.device
                    )
                    self.raft_model.load_state_dict(pretrained_weights)
            except Exception as e:
                print(f"Failed to initialize RAFT: {e}")
                self.raft_model = None

    def generate_flow(self, image: np.ndarray, state: Dict) -> Dict[str, Any]:
        """Generate flow fields based on facial structure and image content.

        Args:
            image: Input RGB image
            state: Current transformation state containing face analysis

        Returns:
            Dictionary with flow fields and related data
        """
        result = {}
        h, w = image.shape[:2]

        # 1. Generate facial structure-guided flow field
        if "landmarks" in state:
            structure_flow = self._generate_structure_flow(image, state)
            result["structure_flow"] = structure_flow

        # 2. Generate neural flow field using RAFT if available
        if self.raft_model is not None:
            neural_flow = self._generate_neural_flow(image)
            result["neural_flow"] = neural_flow

            # Combine with structure flow if available
            if "structure_flow" in result:
                # Weighted blend based on config
                neural_weight = self.config.get("neural_flow_weight", 0.7)
                combined_flow = (
                    neural_weight * neural_flow
                    + (1 - neural_weight) * result["structure_flow"]
                )
                result["combined_flow"] = combined_flow

                # For convenience in later stages
                result["flow_field"] = combined_flow
            else:
                result["flow_field"] = neural_flow
        else:
            # Fallback to structure flow only
            if "structure_flow" in result:
                result["flow_field"] = result["structure_flow"]

        # 3. Generate specialized flow fields for specific effects
        if "effect_type" in self.config:
            effect_flow = self._generate_effect_flow(
                image, state, self.config["effect_type"]
            )
            result["effect_flow"] = effect_flow

            # Override main flow field if specified
            if self.config.get("use_effect_flow_as_primary", False):
                result["flow_field"] = effect_flow

        # 4. Generate flow field variations if requested
        if self.config.get("generate_variations", False):
            variations = []
            n_variations = self.config.get("num_variations", 3)

            for i in range(n_variations):
                seed = np.random.randint(0, 10000)
                np.random.seed(seed)

                # Create variation by perturbing main flow field
                if "flow_field" in result:
                    # Add controlled noise
                    noise_scale = self.config.get("variation_noise_scale", 0.2)
                    noise = np.random.normal(0, noise_scale, result["flow_field"].shape)

                    # Apply additional transformations
                    variation = result["flow_field"] + noise

                    # Optionally rotate or scale flow
                    if np.random.random() > 0.5:
                        angle = np.random.uniform(-30, 30)
                        center = (w / 2, h / 2)
                        M = cv2.getRotationMatrix2D(center, angle, 1.0)
                        variation_x = cv2.warpAffine(variation[:, :, 0], M, (w, h))
                        variation_y = cv2.warpAffine(variation[:, :, 1], M, (w, h))
                        variation = np.stack([variation_x, variation_y], axis=-1)

                    variations.append(
                        {
                            "flow": variation,
                            "seed": seed,
                            "transform_params": {"noise_scale": noise_scale},
                        }
                    )

            result["flow_variations"] = variations

        return result

    def _generate_structure_flow(self, image: np.ndarray, state: Dict) -> np.ndarray:
        """Generate flow field based on facial structure."""
        h, w = image.shape[:2]
        flow = np.zeros((h, w, 2), dtype=np.float32)

        # If we have 3D face information, use it
        if all(k in state for k in ["depth_map", "normal_map"]):
            # Resize normal map to image dimensions
            normal_map = cv2.resize(
                state["normal_map"], (w, h), interpolation=cv2.INTER_LINEAR
            )

            # Use normal map for flow direction (XY components)
            flow[:, :, 0] = normal_map[:, :, 0]
            flow[:, :, 1] = normal_map[:, :, 1]

            # Normalize flow vectors
            magnitude = np.sqrt(flow[:, :, 0] ** 2 + flow[:, :, 1] ** 2) + 1e-6
            flow[:, :, 0] /= magnitude
            flow[:, :, 1] /= magnitude

            # Scale flow based on depth information if available
            if "depth_map" in state:
                depth_map = cv2.resize(
                    state["depth_map"], (w, h), interpolation=cv2.INTER_LINEAR
                )
                # Normalize depth to 0-1 range
                depth_min, depth_max = depth_map.min(), depth_map.max()
                if depth_max > depth_min:
                    depth_norm = (depth_map - depth_min) / (depth_max - depth_min)
                else:
                    depth_norm = depth_map

                # Scale flow magnitude based on depth
                flow_scale = self.config.get("depth_flow_scale", 1.0)
                flow *= depth_norm[:, :, np.newaxis] * flow_scale

            return flow

        # Fallback: Use facial landmarks to generate flow
        if "landmarks" in state:
            landmarks = state["landmarks"]

            # Create sparse flow field at landmark positions
            sparse_flow = np.zeros((len(landmarks), 3))  # x, y, magnitude

            # Define key facial regions for flow direction
            if len(landmarks) >= 468:  # Full MediaPipe face mesh
                # Define key points
                nose_tip = landmarks[4][:2]
                left_eye = landmarks[33][:2]
                right_eye = landmarks[263][:2]
                chin = landmarks[152][:2]
                forehead = landmarks[10][:2]
                left_cheek = landmarks[50][:2]
                right_cheek = landmarks[280][:2]

                # Face center
                face_center = np.mean(
                    [nose_tip, left_eye, right_eye, chin, forehead], axis=0
                )

                # Set up flow vectors for different facial regions
                for i, lm in enumerate(landmarks):
                    pos = lm[:2]

                    # Vector from face center to landmark
                    vec = pos - face_center
                    vec_norm = np.linalg.norm(vec) + 1e-6
                    vec = vec / vec_norm

                    # Scale based on distance from center
                    dist_scale = min(1.0, vec_norm / 100)

                    # Store with magnitude
                    sparse_flow[i] = [vec[0], vec[1], dist_scale]

            # Interpolate sparse flow to dense grid
            grid_x, grid_y = np.meshgrid(np.arange(w), np.arange(h))
            grid_points = np.stack([grid_x.flatten(), grid_y.flatten()], axis=1)

            # Landmark positions
            points = np.array([lm[:2] for lm in landmarks])

            # Use scipy's griddata for interpolation
            from scipy.interpolate import griddata

            flow_x = griddata(
                points, sparse_flow[:, 0], grid_points, method="linear", fill_value=0
            )
            flow_y = griddata(
                points, sparse_flow[:, 1], grid_points, method="linear", fill_value=0
            )
            flow_mag = griddata(
                points, sparse_flow[:, 2], grid_points, method="linear", fill_value=0
            )

            # Reshape to image dimensions
            flow_x = flow_x.reshape(h, w)
            flow_y = flow_y.reshape(h, w)
            flow_mag = flow_mag.reshape(h, w)

            # Create final flow field
            flow[:, :, 0] = flow_x * flow_mag
            flow[:, :, 1] = flow_y * flow_mag

            return flow

        # Ultimate fallback: use simple structure tensor
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0

        # Calculate gradient
        grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)

        # Create structure tensor components
        tensor_xx = cv2.GaussianBlur(grad_x * grad_x, (0, 0), 2.0)
        tensor_xy = cv2.GaussianBlur(grad_x * grad_y, (0, 0), 2.0)
        tensor_yy = cv2.GaussianBlur(grad_y * grad_y, (0, 0), 2.0)

        # Calculate eigenvalues and eigenvectors at each pixel
        for y in range(h):
            for x in range(w):
                tensor = np.array(
                    [
                        [tensor_xx[y, x], tensor_xy[y, x]],
                        [tensor_xy[y, x], tensor_yy[y, x]],
                    ]
                )

                # Skip if tensor is zero
                if np.all(tensor == 0):
                    continue

                # Calculate eigenvalues and eigenvectors
                try:
                    eigenvalues, eigenvectors = np.linalg.eigh(tensor)

                    # Use eigenvector corresponding to smallest eigenvalue
                    # (direction along feature, not across it)
                    flow[y, x, 0] = eigenvectors[0, 0]
                    flow[y, x, 1] = eigenvectors[1, 0]

                    # Scale by eigenvalue ratio
                    if eigenvalues[1] > 0:
                        scale = 1.0 - eigenvalues[0] / (eigenvalues[1] + 1e-6)
                        flow[y, x] *= scale
                except:
                    continue

        return flow

    def _generate_neural_flow(self, image: np.ndarray) -> np.ndarray:
        """Generate neural flow field using RAFT."""
        h, w = image.shape[:2]

        if self.raft_model is None:
            # Return zero flow if RAFT is not available
            return np.zeros((h, w, 2), dtype=np.float32)

        # Create a slightly shifted version of the image
        shift_method = self.config.get("flow_shift_method", "translation")
        shift_amount = self.config.get("flow_shift_amount", 5)

        if shift_method == "translation":
            # Simple translation
            M = np.float32([[1, 0, shift_amount], [0, 1, shift_amount]])
            shifted_image = cv2.warpAffine(image, M, (w, h))
        elif shift_method == "zoom":
            # Zoom effect
            scale = 1.0 + shift_amount / 100
            M = cv2.getRotationMatrix2D((w / 2, h / 2), 0, scale)
            shifted_image = cv2.warpAffine(image, M, (w, h))
        elif shift_method == "rotation":
            # Rotation
            M = cv2.getRotationMatrix2D((w / 2, h / 2), shift_amount, 1.0)
            shifted_image = cv2.warpAffine(image, M, (w, h))
        else:
            # Default to translation
            M = np.float32([[1, 0, shift_amount], [0, 1, shift_amount]])
            shifted_image = cv2.warpAffine(image, M, (w, h))

        # Convert images to tensors
        img1 = torch.from_numpy(image).permute(2, 0, 1).float().to(self.device)
        img2 = torch.from_numpy(shifted_image).permute(2, 0, 1).float().to(self.device)

        # Add batch dimension
        img1 = img1.unsqueeze(0)
        img2 = img2.unsqueeze(0)

        # Normalize to [0, 1]
        rgb_mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1).to(self.device)
        rgb_std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1).to(self.device)
        img1 = (img1 / 255.0 - rgb_mean) / rgb_std
        img2 = (img2 / 255.0 - rgb_mean) / rgb_std

        # Pad images
        padder = InputPadder(img1.shape)
        img1, img2 = padder.pad(img1, img2)

        # Run RAFT inference
        with torch.no_grad():
            _, flow = self.raft_model(img1, img2, iters=20, test_mode=True)

        # Remove padding
        flow = padder.unpad(flow)

        # Convert to numpy
        flow = flow[0].permute(1, 2, 0).cpu().numpy()

        # Normalize flow vectors
        if self.config.get("normalize_flow", True):
            max_mag = np.max(np.sqrt(flow[:, :, 0] ** 2 + flow[:, :, 1] ** 2)) + 1e-6
            flow = flow / max_mag

        return flow

    def _generate_effect_flow(
        self, image: np.ndarray, state: Dict, effect_type: str
    ) -> np.ndarray:
        """Generate specialized flow fields for specific effects."""
        h, w = image.shape[:2]
        flow = np.zeros((h, w, 2), dtype=np.float32)

        if effect_type == "horizontal_smear":
            # Create horizontal flow field
            for y in range(h):
                for x in range(w):
                    # Distance from center
                    dx = x - w / 2
                    dy = y - h / 2
                    dist = np.sqrt(dx**2 + dy**2)

                    # Stronger effect in center
                    strength = max(0, 1.0 - dist / (w / 2))

                    # Horizontal flow, strength varies with distance
                    flow[y, x, 0] = strength

            # Apply face-aware modulation
            if "face_bbox" in state:
                x1, y1, x2, y2 = state["face_bbox"]
                face_center_x = (x1 + x2) / 2
                face_center_y = (y1 + y2) / 2

                for y in range(h):
                    for x in range(w):
                        # Distance from face center
                        dx = x - face_center_x
                        dy = y - face_center_y
                        face_dist = np.sqrt(dx**2 + dy**2)

                        # Flow strength inversely proportional to distance from face
                        face_factor = max(0, 1.0 - face_dist / (w / 3))
                        flow[y, x, 0] *= face_factor

        elif effect_type == "vertical_cascade":
            # Create vertical flow with increasing strength towards bottom
            for y in range(h):
                for x in range(w):
                    # Stronger effect at bottom
                    y_factor = y / h
                    flow[y, x, 1] = y_factor

            # Apply face-aware modulation
            if all(k in state for k in ["face_bbox", "landmarks"]):
                x1, y1, x2, y2 = state["face_bbox"]
                landmarks = state["landmarks"]

                # Create mask for facial features
                feature_mask = np.zeros((h, w), dtype=np.float32)

                # Add key facial features to mask
                if len(landmarks) >= 468:
                    # Eyes, nose, mouth landmarks
                    key_points = [
                        landmarks[4],  # Nose tip
                        landmarks[33],  # Left eye
                        landmarks[263],  # Right eye
                        landmarks[61],  # Inner mouth
                        landmarks[291],  # Inner mouth
                        landmarks[199],  # Upper lip
                    ]

                    for point in key_points:
                        x, y = int(point[0]), int(point[1])
                        if 0 <= x < w and 0 <= y < h:
                            # Add highlight area around point
                            radius = int(w * 0.05)
                            cv2.circle(feature_mask, (x, y), radius, 1.0, -1)

                # Blur mask
                feature_mask = cv2.GaussianBlur(feature_mask, (0, 0), w * 0.02)

                # Apply mask to flow
                for y in range(h):
                    for x in range(w):
                        # Stronger effect at facial features
                        flow[y, x, 1] *= 1.0 + feature_mask[y, x] * 2.0

        elif effect_type == "liquid":
            # Create flow field simulating liquid movement
            # Generate perlin noise for organic flow
            from noise import pnoise2

            scale = self.config.get("liquid_scale", 0.01)
            octaves = self.config.get("liquid_octaves", 4)
            persistence = self.config.get("liquid_persistence", 0.5)

            for y in range(h):
                for x in range(w):
                    # Generate noise value
                    nx = x * scale
                    ny = y * scale
                    noise_val = pnoise2(
                        nx, ny, octaves=octaves, persistence=persistence
                    )

                    # Convert to angle
                    angle = noise_val * np.pi * 2

                    # Convert to vector
                    flow[y, x, 0] = np.cos(angle)
                    flow[y, x, 1] = np.sin(angle)

            # Apply face-aware flow
            if "landmarks" in state:
                # Create flow from face center
                landmarks = state["landmarks"]
                if len(landmarks) >= 468:
                    # Calculate face center
                    face_center = np.mean(landmarks[:, :2], axis=0)
                    center_x, center_y = face_center

                    # Face-aware flow
                    face_flow = np.zeros((h, w, 2), dtype=np.float32)
                    for y in range(h):
                        for x in range(w):
                            # Vector from point to face center
                            dx = center_x - x
                            dy = center_y - y
                            dist = np.sqrt(dx**2 + dy**2) + 1e-6

                            # Normalize and scale by distance
                            face_flow[y, x, 0] = dx / dist
                            face_flow[y, x, 1] = dy / dist

                    # Blend with noise flow
                    face_weight = self.config.get("face_flow_weight", 0.5)
                    flow = face_flow * face_weight + flow * (1 - face_weight)

        elif effect_type == "crystallize":
            # Create flow field for crystalline effect
            # Uses Voronoi-like patterns for direction

            # Create seed points
            num_seeds = self.config.get("crystal_seeds", 50)
            seeds = np.random.rand(num_seeds, 2)
            seeds[:, 0] *= w
            seeds[:, 1] *= h

            # Add face landmarks as seeds if available
            if "landmarks" in state:
                landmarks = state["landmarks"]
                # Add subset of landmarks as seeds
                if len(landmarks) >= 468:
                    # Sample key points
                    indices = np.linspace(0, len(landmarks) - 1, 20).astype(int)
                    for idx in indices:
                        seeds = np.vstack([seeds, landmarks[idx, :2]])

            # Calculate flow based on closest seed direction
            for y in range(h):
                for x in range(w):
                    point = np.array([x, y])

                    # Find closest seed
                    dists = np.sqrt(np.sum((seeds - point) ** 2, axis=1))
                    closest_idx = np.argmin(dists)

                    # Vector from point to seed
                    seed = seeds[closest_idx]
                    vec = seed - point
                    dist = np.linalg.norm(vec) + 1e-6

                    # Direction to closest seed
                    flow[y, x, 0] = vec[0] / dist
                    flow[y, x, 1] = vec[1] / dist

            # Add noise for variation
            noise_scale = self.config.get("crystal_noise_scale", 0.3)
            noise = np.random.normal(0, noise_scale, flow.shape)
            flow += noise

            # Normalize
            magnitude = np.sqrt(flow[:, :, 0] ** 2 + flow[:, :, 1] ** 2) + 1e-6
            flow[:, :, 0] /= magnitude
            flow[:, :, 1] /= magnitude

        else:
            # Default: use structure flow
            if "structure_flow" in state:
                flow = state["structure_flow"].copy()

        return flow

    def visualize_flow(self, state: Dict) -> np.ndarray:
        """Create a visualization of the flow field for debugging."""
        if "flow_field" not in state:
            # Return empty visualization
            return np.zeros((300, 300, 3), dtype=np.uint8)

        flow = state["flow_field"]

        # Convert flow field to RGB visualization
        # Hue = direction, Saturation = magnitude, Value = constant
        h, w = flow.shape[:2]
        hsv = np.zeros((h, w, 3), dtype=np.uint8)

        # Calculate direction and magnitude
        mag, ang = cv2.cartToPolar(flow[:, :, 0], flow[:, :, 1])

        # Normalize magnitude for better visualization
        mag_max = np.max(mag) if np.max(mag) > 0 else 1.0
        mag_norm = np.minimum(1.0, mag / mag_max)

        # Set HSV values
        hsv[:, :, 0] = ang * 180 / np.pi / 2  # Hue = direction
        hsv[:, :, 1] = mag_norm * 255  # Saturation = magnitude
        hsv[:, :, 2] = 255  # Value = constant

        # Convert to RGB
        flow_vis = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

        return flow_vis
