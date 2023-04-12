from pytube import YouTube
from moviepy.editor import *
import pprint
import pandas as pd
import concurrent.futures

from utils import *

df_link = pd.read_csv("./input/yt_list.csv")

print(df_link)
print(type(df_link))


class YT_Controller():
    def __init__(self) -> None:
        self.download_result_path = "./output/result/"
        pass

    # @timing_decorator
    def download(self, url: str, video_output_path: str = "./output/media/video", audio_output_path: str = "./output/media/audio") -> tuple[str, str]:
        yt = YouTube(url)

        # Filter for the desired video and audio streams
        video_stream = None
        audio_stream = None
        max_abr = 0

        # pprint.pprint(yt.streams)

        for stream in yt.streams:
            if stream.resolution == "1080p" and stream.mime_type == "video/mp4" and stream.video_codec.startswith("avc1"):
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
            output_path=video_output_path, filename=f"video_{video_id}.mp4")
        audio_path = audio_stream.download(
            output_path=audio_output_path, filename=f"audio_{video_id}.mp4")

        return video_path, audio_path
    
    def combine(self, video_input_path: str, audio_input_path: str) -> str:
        result_output_path = self.download_result_path + ''.join(video_input_path.split('/')[-1].split('_')[1:])
        print(result_output_path)

        # Load the video and audio files
        video_clip = VideoFileClip(video_input_path)
        audio_clip = AudioFileClip(audio_input_path)

        # Set the audio of the video clip to the loaded audio file
        video_with_audio = video_clip.set_audio(audio_clip)

        # Write the output video file with the combined audio and video
        video_with_audio.write_videofile(
            result_output_path, codec='libx264', audio_codec='aac')
        
        return result_output_path
    
    @timing_decorator
    def download_combine(self, url: str) -> str:
        return self.combine(*self.download(url))
    
    @timing_decorator
    def download_combine_multiple(self, url_list: list[str]) -> None:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.download_combine, url_list)


    


if __name__ == "__main__":
    yt = YT_Controller()
    # for idx, row in df_link.iterrows():
    #     yt.download_combine(row["link"])
    yt.download_combine_multiple(list(df_link["link"]))

