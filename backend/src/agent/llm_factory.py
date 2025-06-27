"""LLM factory for creating different model providers."""

import os
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from agent.configuration import Configuration


def create_llm(
    model_name: str,
    configuration: Configuration,
    temperature: float = 0.0,
    max_retries: int = 2,
    **kwargs: Any
) -> BaseChatModel:
    """Create an LLM instance based on the configuration provider.
    
    Args:
        model_name: The name/type of model (e.g., "query_generator", "reflection", "answer")
        configuration: The configuration object containing provider settings
        temperature: The sampling temperature
        max_retries: Maximum number of retries for API calls
        **kwargs: Additional arguments passed to the model constructor
    
    Returns:
        A configured LLM instance
    """
    models = configuration.get_models_for_provider()
    actual_model_name = models.get(model_name, model_name)
    
    if configuration.model_provider == "ollama":
        return ChatOllama(
            model=actual_model_name,
            base_url=configuration.ollama_base_url,
            temperature=temperature,
            **kwargs
        )
    else:  # gemini
        return ChatGoogleGenerativeAI(
            model=actual_model_name,
            temperature=temperature,
            max_retries=max_retries,
            api_key=os.getenv("GEMINI_API_KEY"),
            **kwargs
        )


def create_query_generator_llm(configuration: Configuration) -> BaseChatModel:
    """Create an LLM for query generation."""
    return create_llm("query_generator_model", configuration, temperature=1.0)


def create_reflection_llm(configuration: Configuration) -> BaseChatModel:
    """Create an LLM for reflection tasks."""
    return create_llm("reflection_model", configuration, temperature=1.0)


def create_answer_llm(configuration: Configuration) -> BaseChatModel:
    """Create an LLM for final answer generation."""
    return create_llm("answer_model", configuration, temperature=0.0)