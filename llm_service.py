from dotenv import load_dotenv
from google import genai
import os


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file.")


# --------------------------------------------------
# 2. Create Gemini client
# --------------------------------------------------

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.8-flash"


# --------------------------------------------------
# 3. Generate an answer using Gemini
# --------------------------------------------------

def generate_answer(query, retrieved_results):
    """
    Generate a grounded response using Gemini.

    Gemini uses only the evidence retrieved from
    the knowledge base.

    If Gemini is unavailable, the system falls back
    to the retrieved knowledge-base answer.
    """

    if not retrieved_results:
        return {
            "answer": "I could not find relevant information in the knowledge base.",
            "source": "knowledge_base"
        }

    # Build the evidence that will be given to Gemini.
    evidence = ""

    for i, result in enumerate(retrieved_results, start=1):
        evidence += (
            f"\nEvidence {i}\n"
            f"Source: {result['source']}\n"
            f"Section: {result['section']}\n"
            f"Content:\n{result['text']}\n"
        )

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    prompt = f"""
You are a support assistant for CampusHelp.

Answer the user's question using ONLY the knowledge-base
evidence provided below.

Rules:
1. Do not invent information.
2. Do not use outside knowledge.
3. Do not contradict the knowledge base.
4. Give clear and concise instructions when appropriate.
5. If the evidence does not contain enough information,
   say that the information is not available in the knowledge base.
6. Do not mention embeddings, retrieval, ChromaDB,
   or internal system details.
7. Do not make decisions that the knowledge base says
   require human support.

User question:
{query}

Knowledge-base evidence:
{evidence}
"""

    # --------------------------------------------------
    # 4. Call Gemini
    # --------------------------------------------------

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return {
            "answer": response.text,
            "source": "gemini"
        }

    # --------------------------------------------------
    # 5. Fallback if Gemini is unavailable
    # --------------------------------------------------

    except Exception as error:

        print("\nGemini unavailable.")
        print("Error:", error)
        print("Using knowledge-base fallback.")

        # Use the most relevant retrieved chunk.
        top_result = retrieved_results[0]

        fallback_answer = (
            "According to the CampusHelp knowledge base:\n\n"
            f"{top_result['text']}\n\n"
            f"Source: {top_result['source']}"
        )

        return {
            "answer": fallback_answer,
            "source": "knowledge_base_fallback"
        }


# --------------------------------------------------
# 6. Test the service independently
# --------------------------------------------------

if __name__ == "__main__":

    test_query = "I forgot my password. How can I reset it?"

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

    result = generate_answer(
        test_query,
        test_results
    )

    print("\n" + "=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)

    print(result["answer"])

    print("\n" + "=" * 60)
    print("ANSWER SOURCE")
    print("=" * 60)

    print(result["source"])