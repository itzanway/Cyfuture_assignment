import random
from langchain_core.tools import tool

# --- MOCK DATABASE (Transactional Records) ---
MOCK_ORDERS = {
    "ORD-12345": {"status": "Shipped", "delivery_date": "2023-10-25", "items": ["Wireless Mouse"]},
    "ORD-67890": {"status": "Processing", "delivery_date": "TBD", "items": ["Monitor Stand"]},
    "ORD-11223": {"status": "Delivered", "delivery_date": "2023-10-20", "items": ["USB-C Cable"]}
}

# --- TOOL 1: Order Lookup (Operational) ---
@tool
def check_order_status(order_id: str):
    """Fetches the status of an order using its ID (Format: ORD-XXXXX)."""
    # REQUIREMENT: Validate identifiers
    if not order_id.startswith("ORD-"):
        return "Error: Invalid Order ID format. Order IDs must start with 'ORD-'."
    
    order = MOCK_ORDERS.get(order_id)
    if order:
        return f"Order {order_id} is currently {order['status']}. Items: {', '.join(order['items'])}."
    else:
        return "Order not found. Please check the ID."

# --- TOOL 2: Policy Search (Informational) ---
@tool
def search_policy(query: str):
    """Retrieves shipping and return policies from the knowledge base."""
    # In a real app, this would query a Vector DB (FAISS/Chroma).
    # For this assignment, we simulate a keyword search.
    policies = {
        "return": "You can return items within 30 days of receipt if they are unused.",
        "shipping": "Standard shipping takes 5-7 business days. Express is 2 days.",
        "payment": "We accept Visa, MasterCard, and PayPal."
    }
    
    for key, text in policies.items():
        if key in query.lower():
            return text
    return "I couldn't find a specific policy for that. Could you clarify?"

# --- TOOL 3: Human Handoff (Escalation) ---
@tool
def escalate_to_agent(issue_summary: str):
    """Escalates complex issues or angry users to a human agent."""
    return f"TICKET CREATED: A human agent has been notified about: '{issue_summary}'. They will contact you shortly."