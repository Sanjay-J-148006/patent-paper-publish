import os
import cv2

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None


class ORAMAProcessor:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.orama_dir = os.path.join(self.current_dir, "orama")
        self.model_path = os.path.join(self.orama_dir, "runs", "train", "weights", "best.pt")

        self.model = None
        self.class_names = {}
        self.collision_classes = ['car', 'truck', 'motorcycle', 'person', 'bus', 'bicycle']

        if YOLO is not None and os.path.exists(self.model_path):
            try:
                self.model = YOLO(self.model_path)
                print(f"[ORAMA] Model loaded: {self.model_path}")
            except Exception as e:
                print(f"[ORAMA] Failed to load model: {e}")
        else:
            print("[ORAMA] YOLO or model file not available, detection disabled")
            print(f"[ORAMA] Expected model path: {self.model_path}")

    def estimate_distance(self, box_height, frame_height):
        reference_height = 1.5
        focal_length = frame_height
        if box_height <= 0:
            return 50.0
        distance = (reference_height * focal_length) / box_height
        return max(1.0, min(50.0, distance))

    def determine_direction(self, x_center, frame_width):
        frame_center = frame_width / 2
        if x_center < frame_center - frame_width * 0.1:
            return "left"
        elif x_center > frame_center + frame_width * 0.1:
            return "right"
        return "center"

    def process_frame(self, frame):
        """
        Run ORAMA detection on a frame and return:
        (annotated_frame, detections)
        """
        annotated = frame.copy()

        if self.model is None:
            cv2.putText(
                annotated,
                "ORAMA model unavailable",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )
            return annotated, []

        try:
            results = self.model(frame, conf=0.4, verbose=False)
            boxes = results[0].boxes
            self.class_names = results[0].names

            detections = []

            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = self.class_names.get(cls_id, str(cls_id))

                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                color = (0, 255, 0)
                risk_text = ""

                if label in self.collision_classes:
                    box_height = y2 - y1
                    frame_h, frame_w = frame.shape[:2]
                    distance = self.estimate_distance(box_height, frame_h)
                    direction = self.determine_direction((x1 + x2) / 2, frame_w)
                    risk = max(0, min(100, (50 - distance) / 50 * 100))

                    if risk > 50:
                        color = (0, 0, 255)
                    elif risk > 25:
                        color = (0, 255, 255)

                    risk_text = f" | Risk:{risk:.1f}% | {distance:.1f}m | {direction}"

                    detections.append({
                        "label": label,
                        "conf": conf,
                        "risk": risk
                    })

                cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

                text = f"{label} {conf:.2f}{risk_text}"
                cv2.putText(
                    annotated,
                    text,
                    (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2
                )

            return annotated, detections

        except Exception as e:
            cv2.putText(
                annotated,
                f"ORAMA Error: {str(e)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )
            return annotated, []