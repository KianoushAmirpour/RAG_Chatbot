import os
import re
import json
import pathlib
from typing import Dict, Any, List, Tuple

ROOT_DIR = pathlib.Path(__file__).parent.parent
DATA_FOLDER = ROOT_DIR / "data"


def write_as_json_file(file: Dict[str, Any], file_name: str) -> None:
    file_path = f"{file_name}.json"
    with open(DATA_FOLDER / file_path, "w", encoding="utf-8") as f:
        json.dump(file, f)


def load_json_file(file_name: str) -> Dict[str, Any]:
    file_path = f"{file_name}.json"
    if not os.path.isfile(DATA_FOLDER / file_path):
        return {}
    with open(DATA_FOLDER / file_path, "r", encoding="utf-8") as f:
        videos = json.load(f)
        return videos


def get_timestamps(description: str) -> List[str]:
    if 'Timestamps' in description:
        desc_after_timestamps = description.split("Timestamps")[1]
        desc_before_Hashtags = desc_after_timestamps.split("#HubermanLab")[0]
        timestamps = desc_before_Hashtags.split("\n")
        timestamps = [item for item in timestamps if item]
        return timestamps


def convert_str_time_to_seconds(string_time: str) -> int:
    # example of string_time:  "10:25:13", "51:36"
    parts_of_string_time = string_time.split(":")
    if len(parts_of_string_time) == 2:
        minute, seconds = map(int, parts_of_string_time)
        return (minute * 60) + seconds
    elif len(parts_of_string_time) == 3:
        hours, minute, seconds = map(int, parts_of_string_time)
        return (hours * 3600) + (minute * 60) + seconds
    else:
        raise ValueError("Invalid time format")


def check_starts_with_num(s: str) -> bool:
    return bool(re.match(r'^\s*\d', s))


def check_short_videos(video_duration: str) -> bool:
    return bool(re.match(r'^PT((\d+H.*)|([5-9]\d*M.*)|(\d{2,}M.*))$', video_duration))


def extract_timestamps_title(video_id: str, channel_videos_info: Dict[str, Dict]) -> List:
    values = channel_videos_info[video_id]
    timestamps_list = get_timestamps(values['description'])
    timestamps_title = []
    if timestamps_list:
        for item in timestamps_list:
            if not check_starts_with_num(item):
                continue
            timestamp, title = item.split(" ", maxsplit=1)
            timestamp = convert_str_time_to_seconds(timestamp)
            timestamps_title.append((timestamp, title))
        sorted_timestamps_title = sorted(timestamps_title, key=lambda x: x[0])
        return sorted_timestamps_title
    return None


def get_transcripts_based_on_timestamps(video_id: str,
                                        timestamps_title: List,
                                        channel_videos_info: Dict[str, Dict],
                                        transcripts: Dict[str, List]
                                        ):

    video_data = {}
    video_data['video_id'] = video_id
    video_data["title"] = channel_videos_info[video_id]["title"]
    video_data["published_at"] = channel_videos_info[video_id]["published_at"]
    video_data["transcripts"] = []

    transcripts_to_processed = transcripts[video_id]

    for idx in range(0, len(timestamps_title)):
        text_list = []
        if idx < len(timestamps_title) - 1:
            start_time = timestamps_title[idx][0]
            end_time = timestamps_title[idx+1][0]
        else:
            break

        for transcripts_item in transcripts_to_processed:
            temp = {}
            if start_time <= transcripts_item["start"] <= end_time:
                text_list.append(transcripts_item["text"])
            temp["timestamp"] = start_time
            temp["sub_title_section"] = timestamps_title[idx][1]
            temp["text"] = " ".join(text_list)
        video_data["transcripts"].append(temp)
    return video_data


def get_playlist_attrs(item: Dict) -> Tuple[str, str, str, str]:
    video_id = item['snippet']['resourceId']['videoId']
    title = item["snippet"]['title']
    description = item["snippet"]['description']
    published_at = item["snippet"]['publishedAt']
    return video_id, title, description, published_at


def get_video_duration(video_response: Dict) -> str:
    return video_response["items"][0]['contentDetails']['duration']


def get_playlist_id(response: Dict) -> str:
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
