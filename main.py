from pathlib import Path

from youtube_snap.downloader import YTDownloader
from youtube_snap.extractor import VideoToFrame
from youtube_snap.pdf_generator import PDFGenerator

yt_url: str = "https://youtu.be/6ArSys5qHAU?si=dPykvwCrzq1nSYlD"
video_name: str = "ann"
video_path = Path("outputs/videos") / f"{video_name}.mp4"
pdf_name: str = "ann-yt-note"

downloader = YTDownloader()
downloader.get_yt_source(VIDEO_NAME=video_name, YT_URL=yt_url)

extractor = VideoToFrame()
extractor.get_frames(video_path, interval_in_sec=30)

generator = PDFGenerator()
generator.get_pdf()
