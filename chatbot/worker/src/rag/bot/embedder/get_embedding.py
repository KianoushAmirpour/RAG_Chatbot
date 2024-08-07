from ...utils import setup_log
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from .embedding_config import (
    EmbeddingBaseSettings,
    SentenceTransformer,
    Intfloat,
    BAAILarge,
    BAAISmall
)

logger = setup_log.setup_logger(__name__)

embed_models = {
    "sentencetransformer": SentenceTransformer,
    'Intfloat': Intfloat,
    'baailarge': BAAILarge,
    'baaismall': BAAISmall,
}


def get_available_embed_models():
    return list(embed_models.keys())


def get_embed_model_settings(model_name: str) -> EmbeddingBaseSettings:
    try:
        embed_model_setting = embed_models.get(model_name)
        return embed_model_setting
    except KeyError as e:
        logger.exception(f"failed to get the embedding model settings, due to {e} \
                         Choose from: {get_available_embed_models()}")
        raise


def get_huggingface_embedding(model_name: str) -> HuggingFaceEmbedding:
    try:
        return HuggingFaceEmbedding(model_name=model_name)
    except Exception as e:
        logger.exception(
            f'Failed to get the embeddings from Huggingface, due to {e}.')
        raise


def get_Fast_embed_embedding(model_name: str) -> FastEmbedEmbedding:
    try:
        return FastEmbedEmbedding(model_name=model_name)
    except Exception as e:
        logger.exception(
            f'Failed to get the embeddings from FastEmbedEmbedding, due to {e}.')
        raise
