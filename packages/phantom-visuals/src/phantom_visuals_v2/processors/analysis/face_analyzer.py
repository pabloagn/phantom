# apts/analysis/face_analyzer.py

"""Face analysis module for extracting 3D face information,
landmarks, expressions, and more from portrait images.
"""

import os
import sys
from typing import Any

import cv2
import mediapipe as mp
import numpy as np
import torch

# Try to import EMOCA if available
try:
    from omegaconf import OmegaConf

    # Add paths for EMOCA
    sys.path.append(os.environ.get("EMOCA_PATH", "third_party/EMOCA"))
    from gdl.models.EMOCA import EMOCA
    from gdl.models.FLAME import FLAME

    EMOCA_AVAILABLE = True
except ImportError:
    EMOCA_AVAILABLE = False

# Try to import InsightFace for advanced face reconstruction
try:
    import insightface
    from insightface.app import FaceAnalysis

    INSIGHTFACE_AVAILABLE = True
except ImportError:
    INSIGHTFACE_AVAILABLE = False


class FaceAnalyzer:
    """Advanced face analysis module for extracting 3D face information,
    landmarks, expressions, and more from portrait images.
    """

    def __init__(self, config, device=None):
        """Initialize the face analyzer with specified configuration.

        Args:
            config: Configuration options for face analysis
            device: Computation device (CPU or CUDA)
        """
        self.config = config
        self.device = (
            device
            if device is not None
            else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )

        # Initialize MediaPipe Face Mesh as fallback
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        # Initialize EMOCA for 3D face reconstruction if available and enabled
        self.emoca = None
        self.flame = None
        if EMOCA_AVAILABLE and config.get("use_emoca", True):
            try:
                model_path = config.get("emoca_model_path", "emoca_v2_lr_mse_20.ckpt")
                config_path = config.get(
                    "emoca_config_path",
                    "models/EMOCA/cfg/model/emoca_v2_lr_mse_20.yaml",
                )

                if not os.path.exists(config_path):
                    # Try default paths
                    default_paths = [
                        "config/emoca_config.yaml",
                        os.path.join(
                            os.environ.get("EMOCA_PATH", ""), "config/emoca_config.yaml"
                        ),
                    ]
                    for path in default_paths:
                        if os.path.exists(path):
                            config_path = path
                            break

                if os.path.exists(config_path):
                    emoca_config = OmegaConf.load(config_path)
                    self.emoca = EMOCA(config=emoca_config)
                    self.emoca.to(self.device)
                    self.emoca.eval()

                    # Load FLAME model for mesh operations
                    flame_config = emoca_config.model.flame
                    self.flame = FLAME(config=flame_config)
                    self.flame.to(self.device)
                    self.flame.eval()
            except Exception as e:
                print(f"Failed to initialize EMOCA: {e}")
                self.emoca = None

        # Initialize InsightFace for advanced face analysis if available
        self.insight_face = None
        if INSIGHTFACE_AVAILABLE and config.get("use_insightface", True):
            try:
                self.insight_face = FaceAnalysis(name="buffalo_l")
                self.insight_face.prepare(
                    ctx_id=0 if str(device).startswith("cuda") else -1,
                    det_size=(640, 640),
                )
            except Exception as e:
                print(f"Failed to initialize InsightFace: {e}")
                self.insight_face = None

    def analyze(self, image: np.ndarray) -> dict[str, Any]:
        """Analyze a portrait image to extract face information.

        Args:
            image: RGB input image as numpy array

        Returns:
            Dictionary containing analysis results
        """
        result = {}

        # Get image dimensions
        h, w = image.shape[:2]
        result["image_shape"] = (h, w)

        # 1. Basic MediaPipe landmarks for reliability
        mp_results = self.mp_face_mesh.process(image)
        if mp_results.multi_face_landmarks:
            landmarks = mp_results.multi_face_landmarks[0].landmark
            landmarks_array = np.array(
                [(lm.x * w, lm.y * h, lm.z * w) for lm in landmarks]
            )
            result["landmarks"] = landmarks_array

            # Estimate face bounding box
            x_min, y_min = np.min(landmarks_array[:, :2], axis=0)
            x_max, y_max = np.max(landmarks_array[:, :2], axis=0)
            result["face_bbox"] = [int(x_min), int(y_min), int(x_max), int(y_max)]
        else:
            # No face detected
            return {"error": "No face detected with MediaPipe"}

        # 2. Advanced 3D reconstruction with EMOCA if available
        if self.emoca is not None:
            try:
                # Crop and preprocess face for EMOCA
                x_min, y_min, x_max, y_max = result["face_bbox"]
                # Add padding
                padding = 0.2
                w_pad = int((x_max - x_min) * padding)
                h_pad = int((y_max - y_min) * padding)
                x_min = max(0, x_min - w_pad)
                y_min = max(0, y_min - h_pad)
                x_max = min(w, x_max + w_pad)
                y_max = min(h, y_max + h_pad)

                face_image = image[y_min:y_max, x_min:x_max]
                face_image = cv2.resize(face_image, (224, 224))

                # Convert to tensor
                face_tensor = (
                    torch.tensor(face_image)
                    .float()
                    .permute(2, 0, 1)
                    .unsqueeze(0)
                    .to(self.device)
                )
                face_tensor = face_tensor / 255.0

                # Run EMOCA inference
                with torch.no_grad():
                    codedict = self.emoca.encode(face_tensor)
                    opdict = self.emoca.decode(codedict)

                    # Extract and store 3D face parameters
                    result["flame_params"] = {
                        "shape": codedict["shape"].cpu().numpy(),
                        "exp": codedict["exp"].cpu().numpy(),
                        "pose": codedict["pose"].cpu().numpy(),
                        "cam": codedict["cam"].cpu().numpy(),
                    }

                    # Extract and store 3D geometry
                    result["vertices"] = opdict["verts"].cpu().numpy()[0]
                    result["faces"] = self.flame.faces_tensor.cpu().numpy()

                    # Extract depth and normal maps
                    result["depth_map"] = opdict["depth_map"].cpu().numpy()[0, 0]
                    result["normal_map"] = (
                        opdict["normal_map"].cpu().numpy()[0].transpose(1, 2, 0)
                    )

                    # Scale and align 3D mesh to original image coordinates
                    # This is a simplified version - more sophisticated registration would be better
                    verts = result["vertices"].copy()
                    # Scale to face bounding box
                    verts[:, 0] = verts[:, 0] * (x_max - x_min) + x_min
                    verts[:, 1] = verts[:, 1] * (y_max - y_min) + y_min
                    result["aligned_vertices"] = verts
            except Exception as e:
                print(f"EMOCA analysis failed: {e}")

        # 3. Additional analysis with InsightFace if available
        if self.insight_face is not None:
            try:
                faces = self.insight_face.get(image)
                if faces:
                    # Get largest face
                    face = max(
                        faces,
                        key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]),
                    )

                    # Extract and store face attributes
                    result["insightface"] = {
                        "bbox": face.bbox,
                        "landmark": face.landmark,
                        "gender": face.gender,
                        "age": face.age,
                    }

                    # Store face embedding for potential future use
                    if hasattr(face, "embedding") and face.embedding is not None:
                        result["face_embedding"] = face.embedding
            except Exception as e:
                print(f"InsightFace analysis failed: {e}")

        # 4. Calculate additional face measurements
        if "landmarks" in result:
            landmarks = result["landmarks"]

            # Face orientation estimation (basic)
            if len(landmarks) >= 468:  # Full MediaPipe face mesh
                # Use nose, eyes, and chin for estimation
                nose_tip = landmarks[4]
                left_eye = landmarks[33]
                right_eye = landmarks[263]
                chin = landmarks[152]

                # Calculate rough orientation
                dx = right_eye[0] - left_eye[0]
                dy = right_eye[1] - left_eye[1]
                face_angle = np.degrees(np.arctan2(dy, dx))

                # Estimate head pose (very basic)
                result["head_pose"] = {
                    "yaw": face_angle,
                    "pitch": 0,  # Need better estimation
                    "roll": 0,  # Need better estimation
                }

        # 5. Generate expression-based weights for different effects
        if "flame_params" in result:
            exp_params = result["flame_params"]["exp"][0]

            # Calculate expression intensities for different emotions
            # These mappings are approximate - a proper classifier would be better
            exp_weights = {
                "neutral": max(0, 1.0 - np.sum(np.abs(exp_params)) * 0.1),
                "smile": max(0, exp_params[1]),
                "frown": max(0, -exp_params[1]),
                "surprise": max(0, exp_params[2]),
                "anger": max(0, exp_params[4]),
                "tension": max(0, np.mean([exp_params[6], exp_params[9]])),
            }

            # Normalize weights
            total = sum(exp_weights.values()) + 1e-6
            exp_weights = {k: v / total for k, v in exp_weights.items()}

            result["expression_weights"] = exp_weights

        return result

    def visualize_mesh(self, image: np.ndarray, state: dict) -> np.ndarray:
        """Create a visualization of the facial mesh for debugging."""
        if "landmarks" not in state:
            return image.copy()

        vis_img = image.copy()
        landmarks = state["landmarks"]

        # Draw landmarks
        for i, (x, y, _) in enumerate(landmarks):
            cv2.circle(vis_img, (int(x), int(y)), 1, (0, 255, 0), -1)

        # If we have 3D mesh, draw it
        if "aligned_vertices" in state and "faces" in state:
            verts = state["aligned_vertices"]
            faces = state["faces"]

            # Draw a subset of faces for visualization
            for i in range(0, len(faces), 10):  # Only draw every 10th face
                f = faces[i]
                v0 = verts[f[0]]
                v1 = verts[f[1]]
                v2 = verts[f[2]]

                # Draw triangle
                cv2.line(
                    vis_img,
                    (int(v0[0]), int(v0[1])),
                    (int(v1[0]), int(v1[1])),
                    (0, 0, 255),
                    1,
                )
                cv2.line(
                    vis_img,
                    (int(v1[0]), int(v1[1])),
                    (int(v2[0]), int(v2[1])),
                    (0, 0, 255),
                    1,
                )
                cv2.line(
                    vis_img,
                    (int(v2[0]), int(v2[1])),
                    (int(v0[0]), int(v0[1])),
                    (0, 0, 255),
                    1,
                )

        return vis_img

    def visualize_depth(self, state: dict) -> np.ndarray:
        """Create a visualization of the depth map for debugging."""
        if "depth_map" not in state:
            return np.zeros((224, 224), dtype=np.uint8)

        depth = state["depth_map"].copy()

        # Normalize for visualization
        depth_min = depth.min()
        depth_max = depth.max()
        if depth_max > depth_min:
            depth_norm = (depth - depth_min) / (depth_max - depth_min)
        else:
            depth_norm = depth

        # Convert to color visualization
        depth_vis = (depth_norm * 255).astype(np.uint8)
        depth_color = cv2.applyColorMap(depth_vis, cv2.COLORMAP_INFERNO)

        return depth_color
