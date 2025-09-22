import litellm
from langchain_core.embeddings import Embeddings

response = litellm.embedding(
    model = "gemini/text-embedding-004", 
    input = ["What is the meaning of life?"]
)

# Correctly access the embedding data
print("✅ Embedding generated successfully!")
print(f"Model: {response.model}")
print(f"Number of embeddings: {len(response.data)}")
print(f"Embedding dimension: {len(response.data[0].embedding)}")
print(f"First few values: {response.data[0].embedding[:5]}")
print(f"Token usage: {response.usage.total_tokens} tokens")