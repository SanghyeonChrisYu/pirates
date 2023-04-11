from pytube import YouTube
from moviepy.editor import *
import pprint

# from moviepy.editor import VideoFileClip, concatenate_videoclips

# Load the video
video = VideoFileClip('./output/충주시 누칼협.mp4')

# Slice the video into parts using subclip(start_time, end_time)
part1 = video.subclip(3, 4.2)  # First 10 seconds
part2 = video.subclip(13, 17)  # From 20 seconds to 30 seconds

# Concatenate the parts together
concatenated_video = concatenate_videoclips([part1, part2])

# Save the concatenated video
concatenated_video.write_videofile(
    './output/충주시 누칼협 edit.mp4', codec='libx264')
