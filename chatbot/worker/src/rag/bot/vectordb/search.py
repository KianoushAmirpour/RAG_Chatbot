from typing import List, Dict, Union, Tuple
from llama_index.core import VectorStoreIndex
from sentence_transformers import CrossEncoder
from llama_index.core.retrievers import VectorIndexRetriever


class SearchDocuments:
    def __init__(self,
                 index: VectorStoreIndex,
                 top_similarity: int = 5) -> None:
        self.index = index
        self.top_similarity = top_similarity
        self.semantic_retriever = self._get_semantic_retriever()

    def _get_semantic_retriever(self) -> VectorIndexRetriever:
        semantic_retriever = self.index.as_retriever(
            similarity_top_k=self.top_similarity)
        return semantic_retriever

    def retrieve(self, queries: List[str]) -> Dict[str, Dict[str, Union[str, int]]]:
        retrieved_results = {}
        for query in queries:
            retrived_nodes = self.semantic_retriever.retrieve(query)
            for node in retrived_nodes:
                if node.id_ not in retrieved_results:
                    retrieved_results[node.id_] = {'text': node.text,
                                                   'video_id': node.metadata['video_id'],
                                                   'timestamp': node.metadata['timestamp']}
        return retrieved_results

    def rerank_with_crossencoder(self, user_query, retrieved_results) -> List[Tuple[str, Dict]]:
        cross_encoder_model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-12-v2")
        query_answer_pair = [
            [user_query, retrieved_results[node]['text']] for node in retrieved_results]
        similarity_scores = cross_encoder_model.predict(query_answer_pair)
        for node_id, score in zip(retrieved_results.keys(), similarity_scores):
            retrieved_results[node_id]['similarity_score'] = score
        retrieved_results_sorted = sorted(retrieved_results.items(
        ), key=lambda x: x[1]['similarity_score'], reverse=True)
        return retrieved_results_sorted

    def search(self, queries: List[str]) -> Tuple[str, str]:
        user_query = queries[-1]
        retrieved_docs = self.retrieve(queries)
        reranked_docs = self.rerank_with_crossencoder(
            user_query, retrieved_docs)
        urls = []
        context = ''
        for doc in reranked_docs:
            context += doc[1]['text']
            context += ","
            urls.append(SearchDocuments.create_youtube_url(
                doc[1]['video_id'], doc[1]['timestamp']))
        return context, urls[0]

    @staticmethod
    def create_youtube_url(video_id: str, timestamp: int) -> str:
        return f"https://www.youtube.com/embed/{video_id}&t={timestamp}s"
