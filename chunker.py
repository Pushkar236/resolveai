from kb_loader import load_knowledge_base
import re


def split_into_chunks(documents):

    chunks = []

    for document in documents:

        source = document["source"]
        content = document["content"]

        sections = re.split(r"## ", content)

        for i, section in enumerate(sections):

            if section.strip() == "":
                continue

            lines = section.strip().split("\n")

            section_title = lines[0].replace("#", "").strip()

            text = "\n".join(lines[1:]).strip()

            if not text:
                continue

            chunk = {
                "chunk_id": f"{source}_{i}",
                "source": source,
                "section": section_title,
                "text": text
            }

            chunks.append(chunk)

    return chunks


if __name__ == "__main__":

    docs = load_knowledge_base()

    chunks = split_into_chunks(docs)

    for chunk in chunks:
        print("=" * 60)
        print("ID:", chunk["chunk_id"])
        print("SOURCE:", chunk["source"])
        print("SECTION:", chunk["section"])
        print()
        print(chunk["text"])