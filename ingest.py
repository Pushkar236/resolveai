import chromadb
from sentence_transformers import SentenceTransformer

from kb_loader import load_knowledge_base
from chunker import split_into_chunks
from config import CHROMA_DB_DIR, EMBEDDING_MODEL_NAME


COLLECTION_NAME = "support_knowledge_base"


def create_embeddings(chunks, model):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()


def store_chunks(chunks, embeddings, collection):
    collection.upsert(
        ids=[chunk["chunk_id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "source": chunk["source"],
                "section": chunk["section"]
            }
            for chunk in chunks
        ]
    )


def main():
    print("Loading knowledge base...")

    documents = load_knowledge_base()
    chunks = split_into_chunks(documents)

    print(f"Loaded {len(documents)} documents.")
    print(f"Created {len(chunks)} chunks.")

    print("\nLoading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    print("Creating embeddings...")
    embeddings = create_embeddings(chunks, model)

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(
        path=str(CHROMA_DB_DIR)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    print("Storing chunks...")
    store_chunks(chunks, embeddings, collection)

    print("\nIngestion complete!")
    print(f"Total chunks in database: {collection.count()}")


if __name__ == "__main__":
    main()