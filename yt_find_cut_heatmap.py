import requests
import pprint


def fetch_most_replayed_data(video_id):
    url = f"https://yt.lemnoslife.com/videos?part=mostReplayed&id={video_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pprint.pprint(data)
        most_replayed = data["items"][0].get("mostReplayed", None)
        return most_replayed
    else:
        print(f"Error: {response.status_code}")
        return None


# Example usage:
video_id = "YudHcBIxlYw"
most_replayed_data = fetch_most_replayed_data(video_id)
print()
print()
pprint.pprint(most_replayed_data)
