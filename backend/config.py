import os
from pydantic import BaseSettings, Field, validator
from typing import Optional

class Settings(BaseSettings):
    # Storage paths
    storage_dir: str = Field(
        default="data/storage",
        description="Base directory for storing uploaded files and processed data"
    )

    # Embeddings related
    embedding_model_name: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Hugging Face embedding model name"
    )
    embedding_chunk_size: int = Field(
        default=500,
        gt=100,
        lt=2000,
        description="Max tokens per chunk for embedding"
    )

    # Vector database config
    vector_store_name: str = Field(
        default="chroma",
        description="Vector database in use: 'chroma', 'faiss', or 'qdrant'"
    )
    vector_store_path: str = Field(
        default="data/vectorstore",
        description="Filepath/directory for storing vector database"
    )

    # LLM API or local model config
    llm_model_name: str = Field(
        default="local-llm",
        description="Model identifier or API to use for RAG and script generation"
    )
    llm_api_key: Optional[str] = Field(
        default=None,
        description="API key for external LLM service if applicable"
    )

    # Debugging and logging
    log_level: str = Field(
        default="INFO",
        regex=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Log level for the application"
    )

    # Allowed CORS origins (optional override)
    allowed_origins: str = Field(
        default="*",
        description="Comma-separated list of allowed origins for CORS"
    )

    @validator("storage_dir", "vector_store_path")
    def ensure_dir_exists(cls, v: str) -> str:
        if not os.path.exists(v):
            os.makedirs(v, exist_ok=True)
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Dependency for FastAPI
def get_settings():
    return Settings()
