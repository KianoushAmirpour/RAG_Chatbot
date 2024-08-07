from .model_settings import LlmBaseSettings, LlamaThreeSettings

models = {
    "llama_3_8b_instruct": LlamaThreeSettings,
}


def get_model_settings(model_name: str) -> LlmBaseSettings:
    if model_name not in models:
        raise KeyError(
            f"Model '{model_name}' is not available."
            f"Choose from: {list(models.keys())}"
        )
    return models[model_name]
