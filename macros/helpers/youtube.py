import requests
import isodate
import re

def get_video_duration(video_url, video_id):
    api_key = 'AIzaSyBjfRTR_Tfe9fl6r7pZGbDX_iT26WCJcX0'
    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={api_key}"
    response = requests.get(api_url).json()

    if not response.get("items"):
        raise ValueError("Video topilmadi yoki API kaliti noto‘g‘ri.")

    duration_iso = response['items'][0]['contentDetails']['duration']
    duration_obj = isodate.parse_duration(duration_iso)
    return str(duration_obj)





