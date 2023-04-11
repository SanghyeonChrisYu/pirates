from pytube import YouTube
from moviepy.editor import *
import pprint

url = 'https://www.youtube.com/watch?v=pG6iaOMV46I'
# url = 'https://www.youtube.com/watch?v=BBdC1rl5sKY'
# url = 'https://www.youtube.com/watch?v=nOAmBppk-kE'
url = 'https://www.youtube.com/watch?v=yOVQtBKOAIM&t=218s'
yt = YouTube(url)

# Filter the available streams by resolution (e.g., '1080p')
streams_1080p = yt.streams.filter(res="1080p",
                                  mime_type="video/mp4", progressive=False)
# streams_1080p = yt.streams.filter(res="1080p")
# Print the available 1080p streams
for line in streams_1080p:
    print(line)
# pprint.pprint(streams_1080p)


streams_1080p = yt.streams.filter(
    mime_type="audio/mp4", progressive=False)
# streams_1080p = yt.streams.filter(res="1080p")
# Print the available 1080p streams
# pprint.pprint(streams_1080p)
for line in streams_1080p:
    print(line)
    print(type(line))
# pprint.pprint(streams_1080p)

# print(yt.streams)

# for line in yt.streams:
#     print(line)

# # Choose the desired itag value from the available 1080p streams
# itag_value = 140  # Replace with the desired itag value for the 1080p stream

# video = yt.streams.get_by_itag(itag_value)
# video_path = video.download()
# print(video_path)

print(yt)


stream_video = yt.streams.get_by_itag(299)

stream_audio = yt.streams.get_by_itag(140)

video_path = stream_video.download(filename_prefix="video_")
audio_path = stream_audio.download(filename_prefix="audio_")
print(video_path)
print(audio_path)

output_path = "./output/" + stream_video.default_filename
print(output_path)

# Load the video and audio files
video_clip = VideoFileClip(video_path)
audio_clip = AudioFileClip(audio_path)

# Set the audio of the video clip to the loaded audio file
video_with_audio = video_clip.set_audio(audio_clip)

# Write the output video file with the combined audio and video
video_with_audio.write_videofile(
    output_path, codec='libx264', audio_codec='aac')

# # Replace with the desired output path for the MP3 file
# output_path = './audio.mp3'

# # Convert the video to MP3 using MoviePy
# video_clip = VideoFileClip(video_path)
# audio = video_clip.audio
# audio.write_audiofile(output_path)
