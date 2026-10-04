from retriever import Retriever
from confidence import evaluate_evidence


def main():
    retriever = Retriever()

    query = input("\nEnter your question: ")

    print("\nSearching knowledge base...")
    results = retriever.search(query)

    print("\n" + "=" * 60)
    print("RETRIEVED EVIDENCE")
    print("=" * 60)

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("-" * 40)
        print("Source:", result["source"])
        print("Section:", result["section"])
        print("Distance:", result["distance"])

    decision = evaluate_evidence(results)

    print("\n" + "=" * 60)
    print("DECISION")
    print("=" * 60)

    print("Decision:", decision["decision"])
    print("Reason:", decision["reason"])


if __name__ == "__main__":
    main()