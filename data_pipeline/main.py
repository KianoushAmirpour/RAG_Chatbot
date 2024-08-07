import utils
from youtube import YoutubeApi


def main():
    youtubeapi = YoutubeApi()
    videos = utils.load_json_file('channel_videos_info')
    transcripts = utils.load_json_file('transcripts')

    while True:
        playlist_response = youtubeapi.send_request_for_playlist_videos()
        for item in playlist_response['items']:
            video_id, title, description, published_at = utils.get_playlist_attrs(
                item)
            video_response = youtubeapi.send_request_for_videos(video_id)
            video_duration = utils.get_video_duration(video_response)
            if utils.check_short_videos(video_duration):
                if video_id not in videos:
                    videos[video_id] = {
                        "published_at": published_at,
                        "title": title,
                        "description": description
                    }
        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break
    list_video_ids = list(videos.keys())
    utils.write_as_json_file(videos, "channel_videos_info")
    utils.write_as_json_file(transcripts, "transcripts")

    for video_id in list_video_ids[0:20]:
        transcripts[video_id] = youtubeapi.get_transcripts(video_id)
        if transcripts[video_id]:
            timestamps_title = utils.extract_timestamps_title(video_id, videos)
            video_data = utils.get_transcripts_based_on_timestamps(video_id, timestamps_title,
                                                                   videos, transcripts)
            utils.write_as_json_file(video_data, video_id)


if __name__ == "__main__":
    main()
