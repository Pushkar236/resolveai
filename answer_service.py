def generate_kb_answer(results):
    """
    Generate a direct answer using the retrieved
    knowledge-base content without using an LLM.
    """

    if not results:
        return "I could not find relevant information in the knowledge base."

    answer = "According to the CampusHelp knowledge base:\n\n"

    # Use the most relevant result as the primary answer.
    top_result = results[0]

    answer += top_result["text"]

    # Add the source for transparency.
    answer += f"\n\nSource: {top_result['source']}"

    return answer


if __name__ == "__main__":
    test_results = [
        {
            "source": "password_reset.md",
            "section": "Reset a forgotten password",
            "text": (
                "1. Open the CampusHelp login page.\n"
                "2. Select \"Forgot password\".\n"
                "3. Enter your registered email address.\n"
                "4. Open the password-reset email.\n"
                "5. Select the reset link and choose a new password.\n\n"
                "The reset link expires after 30 minutes."
            )
        }
    ]

    answer = generate_kb_answer(test_results)

    print("\n" + "=" * 60)
    print("KNOWLEDGE BASE ANSWER")
    print("=" * 60)
    print(answer)