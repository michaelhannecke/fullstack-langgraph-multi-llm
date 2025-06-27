import os
from pydantic import BaseModel, Field
from typing import Any, Optional, Literal

from langchain_core.runnables import RunnableConfig


class Configuration(BaseModel):
    """The configuration for the agent."""

    model_provider: Literal["gemini", "ollama"] = Field(
        default="gemini",
        metadata={
            "description": "The model provider to use: 'gemini' for Google Gemini or 'ollama' for local Ollama."
        },
    )

    ollama_base_url: str = Field(
        default="http://localhost:11434",
        metadata={
            "description": "The base URL for the Ollama server."
        },
    )

    query_generator_model: str = Field(
        default="gemini-2.0-flash",
        metadata={
            "description": "The name of the language model to use for the agent's query generation."
        },
    )

    reflection_model: str = Field(
        default="gemini-2.5-flash",
        metadata={
            "description": "The name of the language model to use for the agent's reflection."
        },
    )

    answer_model: str = Field(
        default="gemini-2.5-pro",
        metadata={
            "description": "The name of the language model to use for the agent's answer."
        },
    )

    number_of_initial_queries: int = Field(
        default=3,
        metadata={"description": "The number of initial search queries to generate."},
    )

    max_research_loops: int = Field(
        default=2,
        metadata={"description": "The maximum number of research loops to perform."},
    )

    def get_models_for_provider(self) -> dict[str, str]:
        """Get the appropriate model names based on the provider."""
        if self.model_provider == "ollama":
            return {
                "query_generator_model": "llama3.2:latest",
                "reflection_model": "llama3.2:latest", 
                "answer_model": "llama3.2:latest",
            }
        else:  # gemini
            return {
                "query_generator_model": self.query_generator_model,
                "reflection_model": self.reflection_model,
                "answer_model": self.answer_model,
            }

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )

        # Get raw values from environment or config
        raw_values: dict[str, Any] = {
            name: os.environ.get(name.upper(), configurable.get(name))
            for name in cls.model_fields.keys()
        }

        # Special handling for model_provider from MODEL_PROVIDER env var
        if os.environ.get("MODEL_PROVIDER"):
            raw_values["model_provider"] = os.environ.get("MODEL_PROVIDER")

        # Filter out None values
        values = {k: v for k, v in raw_values.items() if v is not None}

        return cls(**values)
