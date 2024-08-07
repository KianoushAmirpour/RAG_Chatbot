from abc import ABC
from typing import Dict, Any


class LlmBaseSettings(ABC):
    model_name: str
    huggingface_url: str
    model_configs: Dict[str, Any]
    text_generation_configs: Dict[str, Any]
    context_based_prompt_template: str
    query_generation_prompt: str
    create_and_refine_prompt: str


class LlamaThreeSettings(LlmBaseSettings):
    model_name = 'Meta-Llama-3-8B-Instruct.Q5_K_M.gguf'
    huggingface_url = 'https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/tree/main'
    model_configs = {
        'n_ctx': 5000,
        # llama 3 8b has 32 layer. if -1, all layers will be offloaded to gpu.
        'n_gpu_layers': -1,
        "verbose": False
    }
    text_generation_configs = {'max_tokens': 500, 'temperature': 0.3, "top_p": 0.6,
                               'echo': False, 'seed': 11111, 'stream': False}

    context_based_prompt_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a helpful and respectful AI assistant which answers questions based on provided context.
        <|eot_id|><|start_header_id|>user<|end_header_id|>\n
        the provided context is below:\n
        {context}\n
        By only using the provided context and not prior knowledge, answer the below question.
        if you don't find any useful information from the context, related to the question
        you should not answer.\n
        question: {query}
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
    query_generation_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a helpful and respectful AI assistant that generate multiple search queries based on a 
        single input query. You don't need to answer them.
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        Generate {num_queries} search queries, related to the following input query:
        Query: {query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """

    create_and_refine_prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a helpful and respectful AI assistant that is able to refine the answer of a question
        <|eot_id|><|start_header_id|>user<|end_header_id|>
        The original query is as follows: {query}
        We have provided an existing answer: {existing_answer}
        We have the opportunity to refine the existing answer (only if needed) with some more context below:
        ------------
        {context}
        ------------
        Given the new context, refine the original answer to better answer the query.
        If the context isn't useful, return the original answer.
        Refined Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """
