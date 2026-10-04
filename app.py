import streamlit as st

from agent import SupportAgent


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="CampusHelp - AI Support Assistant",
    page_icon="🎓",
    layout="centered"
)


# --------------------------------------------------
# Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            padding-top: 2rem;
        }

        .campus-title {
            text-align: center;
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 0;
        }

        .campus-subtitle {
            text-align: center;
            color: #666;
            font-size: 17px;
            margin-bottom: 2rem;
        }

        .result-box {
            padding: 1.2rem;
            border-radius: 12px;
            border: 1px solid #ddd;
            margin-top: 1rem;
        }

        .ticket-box {
            padding: 1.2rem;
            border-radius: 12px;
            border: 1px solid #f0c36d;
            background-color: #fff9ed;
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="campus-title">🎓 CampusHelp</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="campus-subtitle">'
    'AI-powered support for students and learners'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Input section
# --------------------------------------------------

st.subheader("How can we help you?")

user_email = st.text_input(
    "Email address",
    placeholder="you@example.com"
)

user_query = st.text_area(
    "Describe your issue",
    placeholder="For example: I forgot my password. How can I reset it?",
    height=130
)

submit = st.button(
    "Submit Request",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# Agent processing
# --------------------------------------------------

if submit:

    if not user_email.strip():
        st.warning("Please enter your email address.")

    elif not user_query.strip():
        st.warning("Please describe your issue.")

    else:

        with st.spinner("CampusHelp AI is processing your request..."):

            try:
                agent = SupportAgent()

                result = agent.process_query(
                    user_query.strip(),
                    user_email=user_email.strip()
                )

            except Exception as error:
                st.error(
                    "Something went wrong while processing your request."
                )

                st.exception(error)

            else:

                # ------------------------------------------
                # ANSWER
                # ------------------------------------------

                if result["decision"] == "ANSWER":

                    st.success("Your question has been answered!")

                    st.markdown(
                        '<div class="result-box">',
                        unsafe_allow_html=True
                    )

                    st.markdown("### 💡 Answer")

                    st.write(result["answer"])

                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("### 📚 Knowledge source")

                    st.write(result["source"])


                # ------------------------------------------
                # ESCALATION
                # ------------------------------------------

                elif result["decision"] == "ESCALATE":

                    st.warning(
                        "Your request requires human support."
                    )

                    st.markdown(
                        '<div class="ticket-box">',
                        unsafe_allow_html=True
                    )

                    st.markdown("### 🎫 Support ticket created")

                    st.write(
                        f"**Ticket ID:** `{result['ticket_id']}`"
                    )

                    st.write(
                        "Your request has been forwarded to our "
                        "support team for review."
                    )

                    st.write(
                        "You will receive the final response by email."
                    )

                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("### Why was this escalated?")

                    st.write(result["reason"])