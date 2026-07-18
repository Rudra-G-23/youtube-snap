import logging
import os
import random
import time
from pathlib import Path

import yt_dlp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("YTDownloader")


class YTDownloader:
    """Download the YT Video from URL — hardened for IP / account safety."""

    _FOLDER_PATH: str = Path("outputs/videos")

    # -- Safety tuning knobs (edit here, not inline in ydl_opts) --------
    _MIN_SLEEP_BETWEEN_DOWNLOADS = 5  # seconds, floor before starting next download
    _MAX_SLEEP_BETWEEN_DOWNLOADS = 15  # seconds, ceiling before starting next download
    _MAX_RETRIES_ON_FAILURE = 3
    _BACKOFF_BASE_SECONDS = 30  # doubles each retry: 30s, 60s, 120s

    @classmethod
    def _build_ydl_opts(cls, VIDEO_NAME: str) -> dict:
        return {
            "cookiefile": "cookies.txt",
            # Keep this list minimal — requesting many player clients per
            # request looks more like probing/bot behavior to YouTube than
            # a normal browser session.
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"],
                }
            },
            # Video only
            "format": "bv*[ext=mp4]/bv",
            "outtmpl": f"{cls._FOLDER_PATH}/{VIDEO_NAME}.%(ext)s",
            # --- Rate-limit friendly behavior ---
            # Random delay between internal requests yt-dlp makes
            # (fragment fetches, playlist entries, etc.)
            "sleep_interval": 3,
            "max_sleep_interval": 8,
            "sleep_interval_requests": 2,
            # Retry network hiccups instead of hammering / re-triggering
            # instantly (which is what makes YouTube suspicious).
            "retries": 5,
            "fragment_retries": 5,
            "file_access_retries": 3,
            # Don't blast concurrent fragment requests — sequential is
            # slower but far less likely to trip rate limits.
            "concurrent_fragment_downloads": 1,
            # Quieter logging to avoid unnecessary extra requests for
            # things like extended metadata.
            "quiet": False,
            "no_warnings": False,
        }

    @classmethod
    def _human_delay(cls) -> None:
        """Randomized pause before a download, so requests don't look scripted."""
        delay = random.uniform(
            cls._MIN_SLEEP_BETWEEN_DOWNLOADS, cls._MAX_SLEEP_BETWEEN_DOWNLOADS
        )
        logger.info(f"Waiting {delay:.1f}s before starting download (safety pacing)...")
        time.sleep(delay)

    @classmethod
    def get_yt_source(cls, *, YT_URL: str, VIDEO_NAME: str = "video") -> str:
        """
        Take YT url and download the video only, store in output/videos
        and return the video path.

        Includes:
          - pacing delay before each download
          - retry with exponential backoff on 429 / 403 style failures
        """
        os.makedirs(cls._FOLDER_PATH, exist_ok=True)
        ydl_opts = cls._build_ydl_opts(VIDEO_NAME)

        cls._human_delay()

        last_error: Exception | None = None
        for attempt in range(1, cls._MAX_RETRIES_ON_FAILURE + 1):
            try:
                logger.info(
                    f"YT Video Download started (attempt {attempt}/{cls._MAX_RETRIES_ON_FAILURE})"
                )
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url=YT_URL, download=True)
                    file_path = ydl.prepare_filename(info_dict=info_dict)
                logger.info("Video downloaded successfully!")
                return file_path

            except yt_dlp.utils.DownloadError as e:
                last_error = e
                msg = str(e).lower()

                # 429 / 403 / "sign in to confirm" are signals to back off,
                # not to retry immediately.
                if any(
                    flag in msg for flag in ["429", "403", "sign in", "confirm you"]
                ):
                    wait = cls._BACKOFF_BASE_SECONDS * (2 ** (attempt - 1))
                    logger.warning(
                        f"Possible rate limit / block signal detected: {e}\n"
                        f"Backing off for {wait}s before retrying. "
                        f"If this keeps happening, STOP and refresh cookies.txt "
                        f"or wait a few hours instead of retrying more."
                    )
                    time.sleep(wait)
                    continue

                # Unknown error
                logger.error(f"Download failed with non-rate-limit error: {e}")
                raise

        raise RuntimeError(
            f"Failed after {cls._MAX_RETRIES_ON_FAILURE} attempts. "
            f"Last error: {last_error}"
        )


if __name__ == "__main__":
    VIDEO_NAME: str = "langchain-job-drafting-loop-video2"
    MY_YT_URL: str = "https://youtu.be/L_ke8VG9zsM?si=Lg9UFtFLXdWBfEgH"

    print(
        "\nVideo Path:",
        YTDownloader.get_yt_source(VIDEO_NAME=VIDEO_NAME, YT_URL=MY_YT_URL),
    )
