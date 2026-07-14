import cv2

from youtube_snap.utils import TimeConverter


class VideoToFrame:
    _FRAME_PATH: str = "outputs/frames/"

    def _get_video(self, video_path) -> cv2.VideoCapture:
        """Get the video from the video path."""
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise FileNotFoundError("Could not open the video file.")

        return cap

    def _get_video_length(self, cap: cv2.VideoCapture) -> float:
        """Length of the video in milliseconds."""
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        total_fps = cap.get(cv2.CAP_PROP_FPS)

        if total_fps == 0:
            raise ValueError("Video FPS Zero can't. Can't calculate length.")

        video_length_msec = (total_frames / total_fps) * 1000

        return video_length_msec

    def _get_timestamps(
        self,
        cap: cv2.VideoCapture,
        start_time: tuple[int, int, int] | None = None,
        end_time: tuple[int, int, int] | None = None,
        interval_in_sec: int = 5,
    ) -> tuple[int, int, int]:
        """Get the Start Timestamp, End Timestamp, and Interval in milliseconds."""

        if start_time and end_time is not None:
            _start_hour, _start_min, _start_sec = start_time
            start_msec = TimeConverter.to_milliseconds(
                hour=_start_hour, minute=_start_min, second=_start_sec
            )

            _end_hour, _end_min, _end_sec = end_time
            end_msec = TimeConverter.to_milliseconds(
                hour=_end_hour, minute=_end_min, second=_end_sec
            )
        else:
            start_msec = 0
            end_msec = self._get_video_length(cap)

        interval_msec = interval_in_sec * TimeConverter._MILLISECONDS_PER_SECONDS

        return start_msec, end_msec, interval_msec

    def get_frames(
        self,
        video_path: str,
        start_time: tuple[int, int, int] | None = None,
        end_time: tuple[int, int, int] | None = None,
        interval_in_sec: int = 5,
    ):
        """Convert Video into Frames."""
        cap = self._get_video(video_path)

        start_msec, end_msec, interval_msec = self._get_timestamps(
            cap, start_time, end_time, interval_in_sec
        )

        _photo_count = 1

        while start_msec <= end_msec:
            # Start from starting time stamp given by user
            cap.set(cv2.CAP_PROP_POS_MSEC, start_msec)

            # Capture teh frame
            success, frame = cap.read()
            if not success:
                print(f"Finished or Could not read the frame at {start_msec / 1000}")
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
    video_path = r"/home/rudra/projects/youtube-snap/outputs/videos/langchain-job-drafting-loop-video.mp4"
    VideoToFrame.get_frames(
        "/home/rudra/projects/youtube-snap/outputs/videos/langchain-job-drafting-loop-video.mp4"
    )
