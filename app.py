import streamlit as st


def process_query(query):
    """Temporary rule to test answering and escalation."""

    if "password" in query.lower():
        return {
            "action": "answer",
            "message": (
                "To reset your password:\n\n"
                "1. Open the login page.\n"
                "2. Select **Forgot password**.\n"
                "3. Enter your registered email address.\n"
                "4. Follow the instructions in the reset email."
            ),
        }

    return {
        "action": "escalate",
        "message": (
            "This issue requires human support. "
            "Ticket creation will be added in a later task."
        ),
    }


st.title("ResolveAI")
st.write("Ask a question about the supported product.")
st.caption("Prototype: responses currently use a temporary keyword rule.")

with st.form("support_query"):
    email = st.text_input("Email address")
    query = st.text_area("Describe your issue")
    submitted = st.form_submit_button("Submit")

if submitted:
    email = email.strip()
    query = query.strip()

    if not email or not query:
        st.error("Please enter your email address and question.")

    else:
        result = process_query(query)

        if result["action"] == "answer":
            st.success("A demo answer is available.")
            st.markdown(result["message"])

        else:
            st.warning(result["message"])
            st.write("**Your issue:**", query)
            st.write("**Contact email:**", email)