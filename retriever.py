import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_DB_DIR, EMBEDDING_MODEL_NAME, TOP_K


COLLECTION_NAME = "support_knowledge_base"


class Retriever:

    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

        print("Connecting to ChromaDB...")
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DB_DIR)
        )

        self.collection = self.client.get_collection(
            name=COLLECTION_NAME
        )

    def search(self, query):

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        ).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=TOP_K,
            include=["documents", "metadatas", "distances"]
        )

        retrieved_chunks = []

        for i in range(len(results["documents"][0])):

            chunk = {
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "section": results["metadatas"][0][i]["section"],
                "distance": results["distances"][0][i]
            }

            retrieved_chunks.append(chunk)

        return retrieved_chunks


if __name__ == "__main__":

    retriever = Retriever()

    query = input("\nEnter your question: ")

    results = retriever.search(query)

    print("\n" + "=" * 60)
    print("RETRIEVAL RESULTS")
    print("=" * 60)

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")
        print("-" * 40)
        print("Source:", result["source"])
        print("Section:", result["section"])
        print("Distance:", result["distance"])
        print("Text:")
        print(result["text"])