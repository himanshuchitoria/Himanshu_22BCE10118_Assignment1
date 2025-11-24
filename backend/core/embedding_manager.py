import asyncio
from typing import List
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
import logging

logger = logging.getLogger(__name__)

class EmbeddingManager:
    def __init__(self, model_name: str, device: str = "cpu"):
        self.model_name = model_name
        self.device = device if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()
        logger.info(f"Loaded embedding model {model_name} on {self.device}")

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element contains hidden states
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        summed = torch.sum(token_embeddings * input_mask_expanded, dim=1)
        counts = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)
        return summed / counts

    async def embed_texts(self, texts: List[str], batch_size: int = 16) -> List[List[float]]:
        """
        Generate embeddings for a list of texts asynchronously in batches.
        Returns a list of floats (embeddings), each representing a text chunk.
        """
        embeddings = []

        def embed_batch(batch_texts):
            inputs = self.tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            ).to(self.device)

            with torch.no_grad():
                model_output = self.model(**inputs)
            return self._mean_pooling(model_output, inputs["attention_mask"]).cpu().numpy()

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            try:
                batch_embeddings = await asyncio.to_thread(embed_batch, batch)
                embeddings.extend(batch_embeddings.tolist())
            except Exception as exc:
                logger.error(f"Failed to embed batch starting at index {i}: {exc}")
                raise RuntimeError(f"Embedding failed at batch starting {i}: {exc}")

        return embeddings


_embedding_manager_instance: EmbeddingManager = None

def get_embedding_manager(model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> EmbeddingManager:
    """
    Singleton getter for EmbeddingManager instance
    """
    global _embedding_manager_instance
    if _embedding_manager_instance is None:
        _embedding_manager_instance = EmbeddingManager(model_name=model_name)
    return _embedding_manager_instance


async def generate_embeddings(text_chunks: List[str]) -> List[List[float]]:
    """
    Convenient async function to generate embeddings using singleton manager.
    """
    manager = get_embedding_manager()
    return await manager.embed_texts(text_chunks)
