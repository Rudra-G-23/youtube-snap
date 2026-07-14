import os

import yt_dlp


class YTDownloader:
    """Download the YT Video from URL."""

    _FOLDER_PATH: str = "outputs/videos/"

    @classmethod
    def get_yt_source(cls, *, YT_URL: str, VIDEO_NAME: str = "video") -> str:
        """Take YT url and download the video only, store in output/videos and return the video path."""
        os.makedirs(cls._FOLDER_PATH, exist_ok=True)

        ydl_opts = {
            # Video Only
            "format": "bv*[ext=mp4]/bv",
            "outtmpl": f"{cls._FOLDER_PATH}/{VIDEO_NAME}.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url=YT_URL, download=True)
            file_path = ydl.prepare_filename(info_dict=info_dict)
            return file_path


if __name__ == "__main__":
    VIDEO_NAME: str = "langchain-job-drafting-loop-video2"
    MY_YT_URL: str = "https://youtu.be/L_ke8VG9zsM?si=Lg9UFtFLXdWBfEgH"

    print(
        "\nVideo Path:",
        YTDownloader.get_yt_source(VIDEO_NAME=VIDEO_NAME, YT_URL=MY_YT_URL),
    )
