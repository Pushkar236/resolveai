import uuid
from datetime import datetime, timezone

from retriever import Retriever
from confidence import evaluate_evidence
from llm_service import generate_answer
from n8n_client import create_support_ticket


class SupportAgent:
    def __init__(self):
        print("Initializing support agent...")
        self.retriever = Retriever()

    def search_knowledge_base(self, query):
        """
        Search the approved CampusHelp knowledge base.
        """
        results = self.retriever.search(query)
        return results

    def process_query(self, query, user_email="test@example.com"):
        """
        Main agent workflow.

        1. Search knowledge base.
        2. Evaluate evidence.
        3. If evidence is sufficient, generate an answer using Gemini.
        4. If Gemini is unavailable, use verified KB evidence as fallback.
        5. If human support is required, create a support ticket through n8n.
        """

        print("\nAgent is processing the request...")

        # Step 1: Search the knowledge base
        print("Searching knowledge base...")
        results = self.search_knowledge_base(query)

        # Step 2: Evaluate the retrieved evidence
        print("Evaluating evidence...")
        decision = evaluate_evidence(results)

        # Step 3: Answer when evidence is sufficient
        if decision["decision"] == "ANSWER":

            print("Decision: ANSWER")
            print("Generating grounded response with Gemini...")

            response = generate_answer(
                query,
                results
            )

            return {
                "decision": "ANSWER",
                "answer": response["answer"],
                "source": response["source"],
                "reason": decision["reason"],
                "retrieved_results": results
            }

        # Step 4: Escalate when human support is required
        print("Decision: ESCALATE")
        print("Human support is required.")
        print("Creating support ticket...")

        ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
        request_id = f"REQUEST-{uuid.uuid4().hex[:8].upper()}"

        retrieved_sources = ", ".join(
            result["source"]
            for result in results
        )

        suggested_reply = (
            "Your request has been forwarded to human support "
            "for further assistance."
        )

        ticket_response = create_support_ticket(
            ticket_id=ticket_id,
            request_id=request_id,
            user_email=user_email,
            query=query,
            issue_summary="User request requires human support",
            retrieved_sources=retrieved_sources,
            escalation_reason=decision["reason"],
            suggested_reply=suggested_reply
        )

        return {
            "decision": "ESCALATE",
            "answer": None,
            "source": None,
            "reason": decision["reason"],
            "retrieved_results": results,
            "ticket_id": ticket_id,
            "ticket_response": ticket_response
        }


def main():
    agent = SupportAgent()

    query = input("\nEnter your support question: ")

    result = agent.process_query(
        query,
        user_email="kanchan.shendage23@pccoepune.org"
    )

    print("\n" + "=" * 60)
    print("AGENT RESULT")
    print("=" * 60)

    print("Decision:", result["decision"])
    print("Reason:", result["reason"])

    if result["answer"]:
        print("\nAnswer:")
        print(result["answer"])

        print("\nAnswer source:")
        print(result["source"])

    if result["decision"] == "ESCALATE":
        print("\nSupport ticket created:")
        print(result["ticket_id"])

    print("\nRetrieved sources:")

    for result_item in result["retrieved_results"]:
        print(
            f"- {result_item['source']} "
            f"({result_item['section']})"
        )


if __name__ == "__main__":
    main()