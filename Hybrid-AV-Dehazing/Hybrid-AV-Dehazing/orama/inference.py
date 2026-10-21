from ultralytics import YOLO
import cv2
import numpy as np
import logging
from datetime import datetime
import time
import os
import argparse

# ---------------- ARGUMENTS ----------------
parser = argparse.ArgumentParser(description="Inference script for ORAMA project")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()

# ---------------- PATH SETUP ----------------
current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(current_dir, "output")
input_path = os.path.join(current_dir, "input", "video.mp4")
model_path = os.path.join(current_dir, "runs", "train", "weights", "best.pt")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ---------------- LOGGING ----------------
log_path = os.path.join(output_dir, f"inference_log_{timestamp}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ---------------- WEATHER DETECTION ----------------
def detect_weather(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return "night" if np.mean(gray) < 50 else "fog"

def preprocess_fog(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dark_channel = cv2.erode(gray, np.ones((5, 5), np.uint8))
        atmospheric_light = np.percentile(dark_channel, 90)
        transmission = 1 - 0.75 * (dark_channel / (atmospheric_light + 1e-6))
        transmission = np.clip(transmission, 0.2, 1)

        dehazed = frame.astype(float)
        for c in range(3):
            dehazed[:, :, c] = (dehazed[:, :, c] - atmospheric_light) / (transmission + 1e-6) + atmospheric_light

        return np.clip(dehazed, 0, 255).astype(np.uint8)
    except Exception as e:
        logger.error(f"Fog preprocessing error: {e}")
        return frame

def preprocess_night(frame):
    try:
        return cv2.convertScaleAbs(frame, alpha=1.5, beta=50)
    except Exception as e:
        logger.error(f"Night preprocessing error: {e}")
        return frame

# ---------------- RISK SYSTEM ----------------
def estimate_distance(box_height, frame_height):
    reference_height = 1.5
    focal_length = frame_height
    distance = (reference_height * focal_length) / max(box_height, 1)
    return max(1, min(50, distance))

def determine_direction(x_center, frame_width):
    center = frame_width / 2
    if x_center < center - frame_width * 0.1:
        return "left"
    elif x_center > center + frame_width * 0.1:
        return "right"
    return "center"

# ---------------- DRAW FUNCTION ----------------
def draw_text(img, text, pos, scale=0.4, color=(255,255,255)):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX,
                scale, color, 1, cv2.LINE_AA)

# ---------------- MAIN ----------------
cap = None
out = None

try:
    model = YOLO(model_path)
    logger.info("Model loaded successfully")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise FileNotFoundError("Video not found")

    frame_width = 480
    frame_height = 320
    combined_width = frame_width * 2

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0:
        fps = 25

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    output_video_path = os.path.join(output_dir, f"output_inference_{timestamp}.mp4")

    out = cv2.VideoWriter(
        output_video_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (combined_width, frame_height)
    )

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        frame = cv2.resize(frame, (frame_width, frame_height))

        start_time = time.time()

        weather = detect_weather(frame)
        processed = preprocess_fog(frame) if weather == "fog" else preprocess_night(frame)

        results = model(processed, conf=0.4)

        annotated = processed.copy()

        collision_classes = ['car', 'truck', 'motorcycle', 'person']

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            class_name = results[0].names[cls_id]

            if class_name not in collision_classes:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            box_height = y2 - y1
            x_center = (x1 + x2) / 2

            distance = estimate_distance(box_height, frame_height)
            risk_percentage = max(0, min(100, (50 - distance) / 50 * 100))

            color = (0, 0, 255) if risk_percentage > 60 else (0, 255, 0)

            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            draw_text(annotated, f"{class_name} {risk_percentage:.1f}%", (x1, y1 - 5), 0.4, color)

        combined = np.hstack((frame, annotated))

        draw_text(combined, "Raw Video", (10, 15))
        draw_text(combined, "Processed", (frame_width + 10, 15))
        draw_text(combined, f"Frame: {frame_count}/{total_frames}", (10, 35))

        if args.debug:
            processing_time = (time.time() - start_time) * 1000
            draw_text(combined, f"{processing_time:.1f} ms", (frame_width + 10, frame_height - 10))

        out.write(combined)
        cv2.imshow("Orama Output", combined)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    logger.info("Processing complete")

except Exception as e:
    logger.error(f"Main error: {e}")

finally:
    if cap:
        cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()
