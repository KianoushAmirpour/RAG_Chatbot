from abc import ABC


class EmbeddingBaseSettings(ABC):
    model_name: str
    dim: int
    max_token: int


class SentenceTransformer(EmbeddingBaseSettings):
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    dim = 384
    max_token = 512


class Intfloat(EmbeddingBaseSettings):
    model_name = "intfloat/multilingual-e5-large"
    dim = 1024
    max_token = 514


class BAAILarge(EmbeddingBaseSettings):
    model_name = "BAAI/bge-large-en-v1.5"
    dim = 1024
    max_token = 512


class BAAISmall(EmbeddingBaseSettings):
    model_name = "BAAI/bge-small-en-v1.5"
    dim = 384
    max_token = 512
