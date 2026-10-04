from n8n_client import create_support_ticket


result = create_support_ticket(
    ticket_id="PYTHON-001",
    request_id="PYTHON-REQUEST-001",
    user_email="python-test@example.com",
    query="I forgot my password",
    issue_summary="User needs help resetting their password",
    retrieved_sources="password_reset.md",
    escalation_reason="Testing Python to n8n integration",
    suggested_reply="Please use the Forgot password option on the CampusHelp login page."
)

print("n8n response:")
print(result)