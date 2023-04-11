from pytube import YouTube
from moviepy.editor import *
import pprint
import pandas as pd

link_list = pd.read_csv("./input/yt_list.csv")

print(link_list)
print(type(link_list))


class Downloader():
    def __init__(self) -> None:
        pass

    def download(self, url: str, video_output_path: str = "./output/media/video", audio_output_path: str = "./output/media/audio") -> tuple[str, str]:
        yt = YouTube(url)

        # Filter for the desired video and audio streams
        video_stream = None
        audio_stream = None
        max_abr = 0

        for stream in yt.streams:
            if stream.resolution == "1080p" and stream.mime_type == "video/mp4" and stream.video_codec == "avc1.640028":
                video_stream = stream
            if stream.mime_type == "audio/mp4" and int(stream.abr.rstrip("kbps")) > max_abr:
                audio_stream = stream
                max_abr = int(stream.abr.rstrip("kbps"))

        # Ensure that both video and audio streams are found
        if not video_stream or not audio_stream:
            raise ValueError(
                "Could not find the desired video and/or audio stream.")

        # Download the video and audio streams
        video_id = yt.video_id
        video_path = video_stream.download(
            output_path=video_output_path, filename=f"video_{video_id}")
        audio_path = audio_stream.download(
            output_path=audio_output_path, filename=f"audio_{video_id}")

        return video_path, audio_path
