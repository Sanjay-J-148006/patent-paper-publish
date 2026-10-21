import os
import cv2
import numpy as np


class NighttimeDehazeProcessor:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.night_dir = os.path.join(self.current_dir, "nighttime_dehaze")
        self.real_model_loaded = False

        print("[Nighttime Dehaze] Initialized")

        # NOTE:
        # If you later connect the real repo checkpoint + inference code,
        # we can replace this fallback with actual model inference.

    def process_frame(self, frame):
        """
        Practical nighttime dehaze / low-light enhancement fallback:
        - brightness lift
        - local contrast enhancement
        - mild dehazing effect
        """
        try:
            # Brightness/contrast adjustment
            alpha = 1.35
            beta = 25
            bright = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

            # LAB CLAHE
            lab = cv2.cvtColor(bright, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)

            clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
            l2 = clahe.apply(l)

            enhanced_lab = cv2.merge((l2, a, b))
            enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

            # Mild dehaze-like effect via dark channel style heuristic
            gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
            dark_channel = cv2.erode(gray, np.ones((5, 5), np.uint8))
            atmospheric_light = np.percentile(dark_channel, 90)

            transmission = 1 - 0.6 * (dark_channel / (atmospheric_light + 1e-6))
            transmission = np.clip(transmission, 0.35, 1.0)

            result = enhanced.copy().astype(np.float32)
            for c in range(3):
                result[:, :, c] = (result[:, :, c] - atmospheric_light) / (transmission + 1e-6) + atmospheric_light

            result = np.clip(result, 0, 255).astype(np.uint8)
            return result

        except Exception as e:
            print(f"[Nighttime Dehaze] Error: {e}")
            return frame.copy()