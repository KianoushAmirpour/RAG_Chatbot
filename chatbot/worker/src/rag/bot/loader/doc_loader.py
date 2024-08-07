import os
import json
from uuid import uuid4
from pathlib import Path
from ...utils import setup_log
from typing import Dict, List, Union
from llama_index.core.schema import TextNode

logger = setup_log.setup_logger(__name__)


class Chunker:

    def __init__(self, data_dir: Path, max_words_per_node: int = 750) -> None:
        self.data_dir = data_dir
        self.documents_list = os.listdir(self.data_dir)
        self.max_words_per_node = max_words_per_node
        self.chunks = self._get_chunks_of_videos()
        self.nodes = self.create_nodes(self.chunks)

    def create_nodes(self, chunks: List[dict]) -> List[TextNode]:
        nodes = [
            TextNode(
                text=chunk["content"],
                id_=str(uuid4()),
                metadata=chunk['meta_data']
            )
            for chunk in chunks
        ]
        logger.info(f"{len(nodes)} nodes created.")
        return nodes

    def _get_chunks_of_videos(self) -> List[Dict[str, Union[str, Dict]]]:
        all_chunks = []
        ignored_files = ['channel_videos_info.json', 'transcripts.json']
        files_to_process = [
            file for file in self.documents_list if file not in ignored_files]
        for file in files_to_process:
            video_data: Dict[str, Union[str, List]
                             ] = self._load_json_file(file)
            video_metadata: Dict[str, str] = Chunker.extract_video_metadata(
                video_data)
            chunked_transcripts = self._get_chunks_of_video(
                video_data['transcripts'])
            for chunk in chunked_transcripts:
                chunk['meta_data'].update(video_metadata)
            all_chunks.append(chunked_transcripts)
        return [chunk for chunks_per_file in all_chunks for chunk in chunks_per_file]

    def _load_json_file(self, file_name: str) -> Dict[str, Union[str, List]]:
        file_path = self.data_dir / file_name
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found at {self.data_dir}.")

    def _chunk_transcript(self, text: str) -> List[str]:
        words = text.split(" ")
        chunks = []
        current_chunk = ""
        for word in words:
            if len(current_chunk) + len(word) > self.max_words_per_node:
                chunks.append(current_chunk)
                current_chunk = ""
            current_chunk += word + " "
        chunks.append(current_chunk)
        return chunks

    def _get_chunks_of_video(self, transcripts: List[Dict[str, Union[int, str]]]) -> List[Dict[str, Union[str, Dict]]]:
        chunked_transcripts = []
        for transcript in transcripts:
            text = transcript['text']
            words = text.split(" ")
            if len(words) > self.max_words_per_node:
                chunks = self._chunk_transcript(text)
                for chunk in chunks:
                    chunked_transcripts.append({
                        'content': chunk,
                        'meta_data': self.extract_transcripts_metadata(transcript)
                    })
            else:
                chunked_transcripts.append({
                    'content': text,
                    'meta_data': self.extract_transcripts_metadata(transcript)
                })
        return chunked_transcripts

    @staticmethod
    def extract_video_metadata(video_data: Dict[str, Union[str, List]]) -> Dict[str, str]:
        video_id = video_data["video_id"]
        published_at = video_data['published_at']
        return {'video_id': video_id, 'published_at': published_at}

    @staticmethod
    def extract_transcripts_metadata(transcript: Dict[str, Union[int, str]]) -> Dict[str, Union[int, str]]:
        timestamp = transcript['timestamp']
        sub_section_title = transcript['sub_title_section']
        return {'timestamp': timestamp, 'sub_section_title': sub_section_title}
