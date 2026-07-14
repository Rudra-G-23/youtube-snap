import yt_dlp

FOLDER_PATH: str = "outputs/videos/"
VIDEO_NAME: str = "langchain-job-drafting-loop-video"
MY_YT_URL: str = "https://youtu.be/L_ke8VG9zsM?si=Lg9UFtFLXdWBfEgH"

ydl_opts = {
    "format": "bv*[ext=mp4]/bv",
    "outtmpl": f"{FOLDER_PATH}/{VIDEO_NAME}.%(ext)s",
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([MY_YT_URL])
