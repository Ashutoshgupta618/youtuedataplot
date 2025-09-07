import pandas as pd
import matplotlib.pyplot as plt
from googleapiclient.discovery import build


API_KEY = "AIzaSyD8sRilz0vPFcsARUqqa0D-wWIWsKA9vOs"

def get_channel_details(channel_name):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Step 1: Search for the channel to get channel ID
    search_response = youtube.search().list(
        part='snippet',
        q=channel_name,
        type='channel',
        maxResults=1
    ).execute()

    if not search_response['items']:
        print("Channel not found.")
        return None

    channel_id = search_response['items'][0]['snippet']['channelId']
    channel_response = youtube.channels().list(
        part='snippet,statistics,contentDetails',
        id=channel_id
    ).execute()

    channel = channel_response['items'][0]


    subscriber_count = channel['statistics'].get('subscriberCount')
    subscriber_count = int(subscriber_count) if subscriber_count else 0

    total_views = int(channel['statistics']['viewCount'])
    total_videos = int(channel['statistics']['videoCount'])

 
    channel_data = {
        'Channel Title': channel['snippet']['title'],
        'Subscribers': subscriber_count,
        'Total Views': total_views,
        'Total Videos': total_videos
        # 'Channel Title': channel['snippet']['title'],
        # 'Description': channel['snippet']['description'],
        # 'Published At': channel['snippet']['publishedAt'],
        # 'Country': channel['snippet'].get('country', 'N/A'),
        # 'Subscribers': channel['statistics'].get('subscriberCount', 'Hidden'),
        # 'Total Views': channel['statistics']['viewCount'],
        # 'Total Videos': channel['statistics']['videoCount'],
        # 'Uploads Playlist ID': channel['contentDetails']['relatedPlaylists']['uploads'],
        # 'Channel URL': f"https://www.youtube.com/channel/{channel_id}"
    }

    return channel_data


def plot_pie_chart(data):
    labels = ['Subscribers', 'Total Views', 'Total Videos']
    values = [data['Subscribers'], data['Total Views'], data['Total Videos']]

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct='%f%%', startangle=1)
    plt.title(f"Distribution of Stats for '{data['Channel Title']}'")
    # plt.axis('equal')  # Equal aspect ratio ensures pie is circular
    plt.show()

# Main
if __name__ == "__main__":
    channel_name = input("Enter YouTube channel name: ")
    details = get_channel_details(channel_name)

    if details:
        df = pd.DataFrame([details])
        print("\n📄 DataFrame:")
        print(df)
        plot_pie_chart(details)
