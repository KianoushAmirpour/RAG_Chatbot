from pathlib import Path
from src.redis.cache import Cache
from src.redis.config import Redis
from src.rag.utils import setup_log
from src.redis.producer import Producer
from src.redis.stream import StreamConsumer
from src.schema.model import QueryResponse, Urls
from src.rag.bot.client.llm_client import Client
from src.rag.bot.loader.doc_loader import Chunker
from src.rag.bot.vectordb.manager import VectordbManager
from src.rag.bot.vectordb.search import SearchDocuments
from src.rag. bot.model.get_setting import get_model_settings, models
from src.rag.bot.embedder.get_embedding import (embed_models,
                                                get_embed_model_settings,
                                                get_Fast_embed_embedding)


root_folder = Path(__file__).resolve().parents[2]
model_folder = root_folder / "models"
data_folder = root_folder / 'data'

logger = setup_log.setup_logger(__name__)


def get_llm_settings():
    supported_models = list(models.keys())
    llm_model_name = supported_models[0]
    logger.info(f"`{llm_model_name}` was chosen as llm.")
    llm_settings = get_model_settings(llm_model_name)
    return llm_settings


def get_embeddings():
    supported_embed_models = list(embed_models.keys())
    embed_model_name = supported_embed_models[0]
    logger.info(f"`{embed_model_name}` was chosen as embedding model.")
    embed_model_setting = get_embed_model_settings(embed_model_name)
    embeddings = get_Fast_embed_embedding(embed_model_setting.model_name)
    return embed_model_setting, embeddings


def create_nodes():
    doc_chunker = Chunker(data_folder)
    nodes = doc_chunker.nodes
    return nodes


def create_index(nodes, embed_model_setting, embeddings):
    db_manager = VectordbManager(
        nodes=nodes, embed_settings=embed_model_setting, embed_model=embeddings)
    indices = db_manager.index
    return indices


def load_llm(llm_settings):
    llm_client = Client(model_path=model_folder / llm_settings.model_name,
                        model_settings=llm_settings)
    return llm_client


def generate_response(query, llm_client, indices, refine_answer: bool = False):
    multiple_queries = llm_client.generate_queries(query=query, num_queries=3)

    search_manager = SearchDocuments(indices)

    if refine_answer:
        retrieved_docs = search_manager.retrieve(multiple_queries)
        reranked_docs = search_manager.rerank_with_crossencoder(
            query, retrieved_docs)
        answer = llm_client.create_refine_answer(reranked_docs)
        return answer
    else:
        context, urls = search_manager.search(multiple_queries)
        answer = llm_client.generate_contexed_based_answer(query, context)
        return answer, urls


def retrieve_result(query: str):
    llm_settings = get_llm_settings()
    embed_model_setting, embeddings = get_embeddings()
    nodes = create_nodes()
    indices = create_index(nodes, embed_model_setting, embeddings)
    llm_client = load_llm(llm_settings)
    answer, urls = generate_response(
        query, llm_client, indices, refine_answer=False)

    return answer, urls


def main():
    redis = Redis().create_connection()
    consumer = StreamConsumer(redis)
    cache = Cache(redis)
    producer = Producer(redis)

    while True:
        response = consumer.consume_stream(
            stream_channel='query_channel', count=1)
        if response:
            for _, messages in response:
                for message in messages:
                    message_id = message[0]
                    token = [k.decode('utf-8')
                             for k, v in message[1].items()][0]
                    query = [v.decode('utf-8')
                             for k, v in message[1].items()][0]
                    msg = QueryResponse(msg=query)
                    cache.add_message_to_cache(
                        token=token, source="User", message=msg.model_dump())
                    data = cache.get_chat_history(token=token)
                    message_data = data['messages'][-2:]
                    query_with_history = " ".join(
                        ["" + i['msg'] for i in message_data])
                    answer, url = retrieve_result(query_with_history)
                    result = QueryResponse(
                        msg=answer
                    )
                    video_url = Urls(url=url)
                    stream_data = {}
                    stream_data[str(token)] = str(result.model_dump())
                    urls_video = {}
                    urls_video[str(token)] = str(video_url.model_dump())
                    producer.add_to_stream(stream_data, "response_channel")
                    producer.add_to_stream(urls_video, "urls_channel")
                    cache.add_message_to_cache(
                        token=token, source="Bot", message=result.model_dump())
                    cache.add_urls_to_cache(
                        token=token, urls=video_url.model_dump())
                    consumer.delete_message(
                        stream_channel="query_channel", message_id=message_id)


if __name__ == "__main__":
    main()
