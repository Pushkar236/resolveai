from pathlib import Path


KNOWLEDGE_BASE_DIR = Path("knowledge_base")


def load_knowledge_base():
    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "source": file_path.name,
            "content": content
        })

    return documents


if __name__ == "__main__":
    documents = load_knowledge_base()

    for document in documents:
        print("=" * 60)
        print("SOURCE:", document["source"])
        print("=" * 60)
        print(document["content"])