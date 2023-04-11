from googleapiclient.discovery import build
import re
from collections import defaultdict
import pprint
import time
from functools import wraps
import numpy as np
import pandas as pd
import isodate
import os
from dotenv import load_dotenv


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.2f} seconds to execute.")
        return result
    return wrapper


def convert_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds


def find_outliers(data):
    # Calculate the first quartile (Q1)
    q1 = np.percentile(data, 25)

    # Calculate the third quartile (Q3)
    q3 = np.percentile(data, 75)

    # Calculate the interquartile range (IQR)
    iqr = q3 - q1

    # Calculate the lower and upper bounds for outliers
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Find the outliers
    outliers = [value for value in data if value <
                lower_bound or value > upper_bound]

    return outliers


load_dotenv()

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

youtube = build("youtube", "v3",
                developerKey=ALLOWED_HOSTS[0])


@timing_decorator
def fetch_youtube_comments(youtube, videoId):
    comments_list = []
    time_list = []
    page_token = None
    time_comment_tup_list = []
    data = []

    # Retrieve video length, channel name, video title, and video created date
    video_response = youtube.videos().list(
        part="contentDetails,snippet,statistics",
        id=videoId
    ).execute()

    video_duration = video_response["items"][0]["contentDetails"]["duration"]
    video_length_seconds = int(
        isodate.parse_duration(video_duration).total_seconds())

    channel_name = video_response["items"][0]["snippet"]["channelTitle"]
    video_title = video_response["items"][0]["snippet"]["title"]
    video_created_date = video_response["items"][0]["snippet"]["publishedAt"]
    number_of_comments = int(
        video_response["items"][0]["statistics"]["commentCount"])

    video_title = re.sub(r"[\\/:\*\?\"<>|]", "", video_title)

    iteration_number = max(number_of_comments / 100 * 0.6, 100)
    iteration_number = min(iteration_number, 1000)
    # iteration_number = min(number_of_comments / 100 * 0.6, 100)
    # iteration_number = min(number_of_comments / 100 * 0.6, 1)
    print(
        f"Total commnets: {number_of_comments}, I'll analyze {iteration_number * 100} comments")

    for new_index in range(int(iteration_number)):  # Iterate up to 10,000 comments
        if (new_index+1) % 10 == 0:
            print(f"working on {(new_index+1)*100}th comments...")
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=videoId,
            maxResults=100,
            pageToken=page_token,
            textFormat="plainText"
        ).execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            user_name = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            profile_img_url = item["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"]
            comment_date = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            like_count = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
            match = re.findall(r'\d+:\d+', comment)
            if match:
                for time_str in match:
                    data.append((comment, user_name, profile_img_url,
                                comment_date, like_count, time_str))

        if "nextPageToken" in response:
            page_token = response["nextPageToken"]
        else:
            break

    if len(data) == 0:
        return False

    df = pd.DataFrame(data, columns=[
                      "comment", "user_name", "profile_img_url", "comment_date", "like_count", "time_str"])

    # Create a new column "seconds" by converting the "time_str" column into seconds
    df['seconds'] = df['time_str'].apply(convert_to_seconds)

    # Remove rows where "seconds" is greater than or equal to video_length_seconds
    df = df[df['seconds'] < video_length_seconds]

    # Calculate the interval_idx for each row in the DataFrame
    df['interval_idx'] = (df['seconds'] - 0) // 5

    # Group by 'interval_idx' and calculate the count and mean of 'seconds'
    grouped_df = df.groupby('interval_idx').agg(
        interval_count=('seconds', 'count'),
        seconds_mean=('seconds', 'mean')
    ).reset_index()

    # Round the 'seconds_mean' column to 2 decimal places
    grouped_df['seconds_mean'] = grouped_df['seconds_mean'].round(2)

    # Sort the DataFrame by 'interval_count' and keep only the top 5 rows
    top_5_grouped_df = grouped_df.nlargest(5, 'interval_count')
    top_5_grouped_df.set_index(["interval_idx"], inplace=True)

    # Find the max_count and count how many rows have max_count
    max_count = top_5_grouped_df['interval_count'].max()
    max_count_rows = top_5_grouped_df[top_5_grouped_df['interval_count'] == max_count]

    # If only one row has max_count, save that row
    if len(max_count_rows) <= 1:
        max_row = max_count_rows.iloc[0]
    else:
        # If multiple rows have max_count, choose the one closest to middle_of_video
        middle_of_video = video_length_seconds / 2
        try:
            max_row = max_count_rows.iloc[(
                max_count_rows['seconds_mean'] - middle_of_video).abs().idxmin()]
        except Exception as e:
            max_row = max_count_rows.iloc[0]
            print(str(e))
            print((max_count_rows['seconds_mean'] -
                  middle_of_video).abs().idxmin())

    # 'max_row' now contains the desired row

    # Filter the original DataFrame based on the interval indices in top_5_grouped_df
    filtered_df = df[df['interval_idx'].isin(top_5_grouped_df.index)]

    # Create a dictionary mapping interval indices to their corresponding mean seconds
    mean_seconds_dict = top_5_grouped_df['seconds_mean'].to_dict()

    # Add the 'mean_seconds' column to the filtered_df
    filtered_df['mean_seconds'] = filtered_df['interval_idx'].map(
        mean_seconds_dict)

    # Sort the DataFrame so that rows with the same interval index are together
    sorted_df = filtered_df.sort_values(by=['interval_idx', 'seconds'])

    # Get the interval index of max_row
    max_row_interval_idx = max_row.name

    # Create a new column 'is_max_row' in sorted_df with True or False values
    sorted_df['is_max_row'] = sorted_df['interval_idx'] == max_row_interval_idx

    pprint.pprint(top_5_grouped_df)
    pprint.pprint(sorted_df)

    # top_5_grouped_df.to_csv(
    #     f'top_5_grouped_df - {video_title}.csv', encoding='utf-8')
    # sorted_df.to_csv(
    #     f'sorted_df - {video_title}.csv', encoding='utf-8-sig', index=False, sep='|')

    top_5_grouped_df.to_excel(
        f'top_5_grouped_df - {video_title}.xlsx', engine='openpyxl')
    sorted_df.to_excel(
        f'sorted_df - {video_title}.xlsx', index=False, engine='openpyxl')

    return top_5_grouped_df, sorted_df


# Example usage:
# video_id = "pG6iaOMV46I"
video_id_list = ["pG6iaOMV46I", "YudHcBIxlYw", "nOI67IDlNMQ"]
# video_id_list = ["nOI67IDlNMQ"]
# # video_id_list = ["maevSSGrJtk", "PnFi3o1ZluQ", "j5gO2kf6sh8"]
video_id_list = ["LSIOcCcEVaE", "ZLLcxNiQ9Yg", "6dW4d0IcQ3k"]
# # video_id_list = ["u6wOyMUs74I"]
video_id_list = ["23g5HBOg3Ic", "2TVXi_9Bvlg", "PAKFzFqJa58"]
# video_id_list = ["6dW4d0IcQ3k"]
# video_id_list = ["LSIOcCcEVaE", "ZLLcxNiQ9Yg", "6dW4d0IcQ3k", "2TVXi_9Bvlg"]
video_id_list = ["TGgcC5xg9YI", "HmAsUQEFYGI", "mNEUkkoUoIA"]
video_id_list = ["pG6iaOMV46I", "YudHcBIxlYw", "nOI67IDlNMQ", "LSIOcCcEVaE", "ZLLcxNiQ9Yg",
                 "6dW4d0IcQ3k", "23g5HBOg3Ic", "2TVXi_9Bvlg", "PAKFzFqJa58", "TGgcC5xg9YI", "HmAsUQEFYGI", "mNEUkkoUoIA"]
video_id_list = ["ZLLcxNiQ9Yg",
                 "6dW4d0IcQ3k", "23g5HBOg3Ic", "2TVXi_9Bvlg", "PAKFzFqJa58", "TGgcC5xg9YI", "HmAsUQEFYGI", "mNEUkkoUoIA"]
for video_id in video_id_list:
    result = fetch_youtube_comments(youtube, video_id)
    print(f"----------- ----------- -------------------")
    print(result)
    print()
    print()
    print()
