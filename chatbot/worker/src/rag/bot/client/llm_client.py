from pathlib import Path
from llama_cpp import Llama
from typing import Any, Dict, List, Tuple
from ..model.model_settings import LlmBaseSettings


class Client:
    def __init__(self, model_path: Path, model_settings: LlmBaseSettings) -> None:
        self.model_path = model_path
        self.model_settings = model_settings
        self.llama_model = self._load_llama_model()

    def _load_llama_model(self) -> Any:
        model_config = self.model_settings.model_configs
        return Llama(model_path=str(self.model_path), **model_config)

    def generate_answer(self, prompt: str) -> str:
        answer_config = self.model_settings.text_generation_configs
        answer = self.llama_model(prompt, **answer_config)
        return answer

    def generate_contexed_based_answer(self, query: str, context: str) -> str:
        context_based_prompt = Client.generate_context_based_prompt(self.model_settings.context_based_prompt_template,
                                                                    context=context,
                                                                    query=query)
        response = self.generate_answer(context_based_prompt)
        response = Client.clean_text(response)
        return response

    def generate_queries(self, query: str, num_queries: int = 4) -> List[str]:
        query_generation_prompt = Client.generate_multiple_queries_prompt(self.model_settings.query_generation_prompt,
                                                                          query=query,
                                                                          num_queries=num_queries
                                                                          )
        response = self.generate_answer(query_generation_prompt)
        generated_queries = Client.clean_text(response)
        generated_queries = generated_queries.split("\n") + [query]
        generated_queries = [query for query in generated_queries if query]
        return generated_queries[1:]

    def create_refine_answer(self, user_query: str, reranked_docs: List[Tuple[str, Dict]]) -> str:
        current_response = None
        for idx in range(len(reranked_docs)):
            current_context = reranked_docs[idx][1]['text']
            if idx == 0:
                current_response = self.generate_contexed_based_answer(query=user_query,
                                                                       context=current_context)
            else:
                create_refine_prompt = self.generate_create_refine_prompt(self.model_settings.create_and_refine_prompt,
                                                                          query=user_query,
                                                                          existing_answer=current_response,
                                                                          context=current_context)
                response = self.generate_answer(create_refine_prompt)
                current_response = Client.clean_text(response)
        return current_response

    @staticmethod
    def generate_context_based_prompt(template: str, context: str, query: str) -> str:
        prompt = template.format(context=context, query=query)
        return prompt

    @staticmethod
    def generate_multiple_queries_prompt(template: str, num_queries: int, query: str) -> str:
        prompt = template.format(query=query, num_queries=num_queries)
        return prompt

    @staticmethod
    def generate_create_refine_prompt(template: str, query: str, existing_answer, context: str) -> str:
        prompt = template.format(
            query=query, existing_answer=existing_answer, context=context)
        return prompt

    @staticmethod
    def clean_text(response: Dict) -> str:
        return response['choices'][0]['text']
