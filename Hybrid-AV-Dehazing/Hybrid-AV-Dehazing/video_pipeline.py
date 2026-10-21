import os
import cv2
import time
import argparse
from datetime import datetime

from kanet_kernel import KANetProcessor
from orama_wrapper import ORAMAProcessor
from daclip_wrapper import DAClipProcessor
from nighttime_wrapper import NighttimeDehazeProcessor


class VideoPipeline:
    def __init__(self, mode="hybrid"):
        """
        mode options:
        - kanet
        - daclip
        - nighttime
        - orama
        - hybrid   (kanet + orama)
        """
        self.mode = mode.lower()

        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_video = os.path.join(self.current_dir, "orama", "input", "video.mp4")
        self.output_dir = os.path.join(self.current_dir, "results")
        os.makedirs(self.output_dir, exist_ok=True)

        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_video = os.path.join(self.output_dir, f"{self.mode}_output_{self.timestamp}.mp4")

        # Initialize all processors once
        self.kanet = KANetProcessor()
        self.daclip = DAClipProcessor()
        self.nighttime = NighttimeDehazeProcessor()
        self.orama = ORAMAProcessor()

        print(f"[INFO] Mode selected: {self.mode}")
        print(f"[INFO] Input video: {self.input_video}")
        print(f"[INFO] Output video: {self.output_video}")

    def process_frame(self, frame):
        """
        Process a single frame depending on selected mode.
        """
        if self.mode == "kanet":
            return self.kanet.process_frame(frame)

        elif self.mode == "daclip":
            return self.daclip.process_frame(frame)

        elif self.mode == "nighttime":
            return self.nighttime.process_frame(frame)

        elif self.mode == "orama":
            annotated, _ = self.orama.process_frame(frame)
            return annotated

        elif self.mode == "hybrid":
            dehazed = self.kanet.process_frame(frame)
            annotated, _ = self.orama.process_frame(dehazed)
            return annotated

        else:
            return frame.copy()

    def run(self, show_window=False):
        """
        Run the selected mode on the input video.
        """
        if not os.path.exists(self.input_video):
            print(f"[ERROR] Input video not found: {self.input_video}")
            return

        cap = cv2.VideoCapture(self.input_video)
        if not cap.isOpened():
            print("[ERROR] Failed to open input video")
            return

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 25

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = cv2.VideoWriter(
            self.output_video,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )

        print(f"[INFO] Total frames: {total_frames}")
        print(f"[INFO] Processing mode: {self.mode}")
        print("[INFO] Processing started...")

        frame_idx = 0
        start_total = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_idx += 1
            start_frame = time.time()

            processed = self.process_frame(frame)

            # Overlay mode + frame count
            cv2.putText(
                processed,
                f"Mode: {self.mode.upper()} | Frame: {frame_idx}/{total_frames}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            frame_time_ms = (time.time() - start_frame) * 1000
            cv2.putText(
                processed,
                f"{frame_time_ms:.1f} ms/frame",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

            out.write(processed)

            if show_window:
                cv2.imshow(f"Hybrid AV Dehazing - {self.mode.upper()}", processed)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            if frame_idx % 30 == 0:
                print(f"[INFO] {self.mode.upper()} -> Processed {frame_idx}/{total_frames} frames")

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        total_time = time.time() - start_total
        print(f"[DONE] {self.mode.upper()} output saved at: {self.output_video}")
        print(f"[DONE] {self.mode.upper()} total processing time: {total_time:.2f} seconds")


def run_all_models(show_window=False):
    """
    Run all models one by one on the same input video.
    """
    all_modes = ["kanet", "daclip", "nighttime", "orama", "hybrid"]

    print("\n========== RUNNING ALL MODELS ==========\n")

    for mode in all_modes:
        print(f"\n========== STARTING: {mode.upper()} ==========\n")
        pipeline = VideoPipeline(mode=mode)
        pipeline.run(show_window=show_window)
        print(f"\n========== FINISHED: {mode.upper()} ==========\n")

    print("\n========== ALL MODELS COMPLETED ==========\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Hybrid AV Dehazing video pipeline")
    parser.add_argument(
        "--mode",
        type=str,
        default="hybrid",
        help="Choose mode: kanet, daclip, nighttime, orama, hybrid, all"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show video window while processing"
    )

    args = parser.parse_args()

    mode = args.mode.lower()

    if mode == "all":
        run_all_models(show_window=args.show)
    else:
        pipeline = VideoPipeline(mode=mode)
        pipeline.run(show_window=args.show)