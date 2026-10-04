from config import TOP_K

# Maximum distance we consider relevant evidence.
MAX_RELEVANT_DISTANCE = 1.0

# Knowledge-base sections that explicitly require human support.
HUMAN_SUPPORT_SECTIONS = {
    "Refund requests",
    "Enrollment transfer/manual restore",
    "Change registered email",
    "Restore deleted account",
    "Account-specific suspension/disabled investigation",
    "Duplicate charge",
}


def evaluate_evidence(results):
    """
    Decide whether retrieved knowledge is strong enough
    to support an automatic response.
    """

    if not results:
        return {
            "decision": "ESCALATE",
            "reason": "No relevant knowledge was retrieved."
        }

    top_result = results[0]

    # Step 1: Check whether the best retrieved result is relevant enough.
    if top_result["distance"] > MAX_RELEVANT_DISTANCE:
        return {
            "decision": "ESCALATE",
            "reason": "Retrieved evidence is not sufficiently relevant."
        }

    # Step 2: Check whether the retrieved knowledge explicitly
    # requires human support.
    for result in results:
        if result["section"] in HUMAN_SUPPORT_SECTIONS:
            return {
                "decision": "ESCALATE",
                "reason": (
                    f"Knowledge base requires human support for: "
                    f"{result['section']}"
                )
            }

    # Step 3: Evidence is relevant and no human-review policy applies.
    return {
        "decision": "ANSWER",
        "reason": "Relevant knowledge was found and no human-review policy applies."
    }


if __name__ == "__main__":
    print("confidence.py loaded successfully.")
    print("TOP_K:", TOP_K)
    print("Maximum relevant distance:", MAX_RELEVANT_DISTANCE)