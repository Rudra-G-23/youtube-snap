import cv2

from youtube_snap.utils import TimeConverter


class VideoToFrame:
    _FRAME_PATH: str = "outputs/frames/"

    def get_frames(
        self,
        video_path: str,
        start_time: tuple[int, int, int],
        end_time: tuple[int, int, int],
        interval_in_sec: int = 5,
    ):
        """Convert Video into Frames."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError("Could not open the video file.")

        # Convert the Video timestamp into milliseconds for open cv preprocessing
        _start_hour, _start_min, _start_sec = start_time
        start_msec = TimeConverter.to_milliseconds(
            hour=_start_hour, minute=_start_min, second=_start_sec
        )

        _end_hour, _end_min, _end_sec = end_time
        end_msec = TimeConverter.to_milliseconds(
            hour=_end_hour, minute=_end_min, second=_end_sec
        )

        interval_msec = interval_in_sec * TimeConverter._MILLISECONDS_PER_SECONDS

        _photo_count = 1

        while start_msec <= end_msec:
            # Start from starting time stamp given by user
            cap.set(cv2.CAP_PROP_POS_MSEC, start_msec)

            # Capture teh frame
            success, frame = cap.read()
            if not success:
                print(f"Finished or Could not read the frame at {current_msec / 1000}")
                break

            # Save the frame
            file_name = f"{VideoToFrame._FRAME_PATH}/frame{_photo_count}.png"
            cv2.imwrite(file_name, frame)
            print(f"Saved: {file_name}")

            # Jump to next interval
            _photo_count += 1
            start_msec += interval_msec

        # Clean up resources
        cap.release()
        print("All Frames have been saved successfully!")


if __name__ == "__main__":
    pass
