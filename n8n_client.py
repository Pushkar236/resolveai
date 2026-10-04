import requests
from datetime import datetime, timezone

N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/support-ticket"


def create_support_ticket(
    ticket_id,
    request_id,
    user_email,
    query,
    issue_summary,
    retrieved_sources,
    escalation_reason,
    suggested_reply
):
    payload = {
        "ticket_id": ticket_id,
        "request_id": request_id,
        "user_email": user_email,
        "query": query,
        "issue_summary": issue_summary,
        "retrieved_sources": retrieved_sources,
        "escalation_reason": escalation_reason,
        "suggested_reply": suggested_reply,
        "final_response": "",
        "status": "PENDING_REVIEW",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sent_at": "",
        "email_message_id": ""
    }

    response = requests.post(
        N8N_WEBHOOK_URL,
        json=payload,
        timeout=10
    )

    response.raise_for_status()

    return response.json()