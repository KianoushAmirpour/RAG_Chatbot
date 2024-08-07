import qdrant_client
from typing import List
from ...utils import setup_log
from llama_index.core.schema import TextNode
from qdrant_client.models import Distance, VectorParams
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from ..embedder.embedding_config import EmbeddingBaseSettings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.fastembed import FastEmbedEmbedding

logger = setup_log.setup_logger(__name__)


class VectordbManager:
    def __init__(self,
                 nodes: List[TextNode],
                 embed_settings: EmbeddingBaseSettings,
                 embed_model: HuggingFaceEmbedding | FastEmbedEmbedding,
                 collection_name: str = 'youtube_rag_chatbot',
                 ) -> None:
        
        self.embeddings = embed_model
        self.embed_settings = embed_settings
        self.collection_name = collection_name
        self.qdrant_client = self.create_qdrant_client()
        if not self.ensure_collection_exists:
            self.qdrant_client.create_collection(collection_name=self.collection_name,
                                                 vectors_config=VectorParams(
                                                     size=self.embed_settings.dim,
                                                     distance=Distance.COSINE,
                                                     on_disk=True
                                                 )
                                                 )
            logger.info(
                f'Collection "{self.collection_name}" does not exist. Creating a new collection.')
        self.index = self.index_nodes(nodes)

    def create_qdrant_client(self) -> qdrant_client.QdrantClient:
        return qdrant_client.QdrantClient("localhost", port=6333)

    @property
    def ensure_collection_exists(self) -> bool:
        return self.qdrant_client.collection_exists(self.collection_name)

    def index_nodes(self, nodes) -> VectorStoreIndex:
        vector_store = QdrantVectorStore(client=self.qdrant_client,
                                         collection_name=self.collection_name)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store)
        index = VectorStoreIndex(
            nodes, storage_context=storage_context, embed_model=self.embeddings)
        return index
