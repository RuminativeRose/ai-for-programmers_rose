
from openai import OpenAI
import faiss

import numpy as np

import sys
import logging

logger = logging.Logger(__name__)
logger.addHandler(logging.NullHandler())

# Example documents about movies
texts = [
    "The Godfather is a classic mafia crime drama",
    "Inception explores dreams within dreams",
    "The Shawshank Redemption is a story about hope and friendship",
]


def get_embedding(text: str):
    # Implements the OpenAI embedding functionality
    # Documentation: https://platform.openai.com/docs/guides/embeddings
    # 1. Create an OpenAI client
    # 2. Make an API call to generate embeddings using the text-embedding-3-small model
    # 3. Return the embedding vector from the response
    
    # Placeholder for the actual implementation
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
        )

    return response.data[0].embedding # should have dimension of 1536 (why?)


def main():
    embeddings = [get_embedding(text) for text in texts]

    dimension = len(embeddings[0]) # should have dimension of 1536?
    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings, dtype='float32')) # so 32-bit float what used?

    query = 'Tell me about a prison movie'

    query_embedding = get_embedding(query)
    distances, indices = index.search(np.array([query_embedding], dtype='float32'), 3)

    for i in range(len(embeddings)):
        print(f"Match {i+1}, Distance: {distances[0][i]:.4f}")
        print(texts[indices[0][i]]) 
        
if __name__ == "__main__":
    logging.basicConfig(filename="movie_rag.log",level=logging.INFO)
    sys.exit(main())