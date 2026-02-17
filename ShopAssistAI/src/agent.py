from typing import Literal, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from src.tools import check_order_status, search_policy, escalate_to_agent

# Define the State (Memory)
class AgentState(TypedDict):
    messages: list
    intent: str

# 1. The "Reasoning" Node (Router)
def router_node(state: AgentState) -> Literal["policy", "order", "escalate", "general"]:
    last_message = state["messages"][-1].content.lower()
    
    # REQUIREMENT: Detect problem scenarios (Escalation)
    if any(word in last_message for word in ["angry", "broken", "scam", "human", "stupid"]):
        return "escalate"
        
    # REQUIREMENT: Validate User Input (Regex/Logic)
    import re
    if re.search(r"ord-\d+", last_message):
        return "order"
        
    if any(word in last_message for word in ["return", "policy", "shipping", "cost", "how to"]):
        return "policy"
        
    return "general"

# 2. Execution Nodes
def execution_node(state: AgentState):
    intent = router_node(state)
    last_message = state["messages"][-1].content
    
    if intent == "order":
        # Extract ID simply for this demo
        import re
        order_id = re.search(r"ORD-\d+", last_message, re.IGNORECASE).group(0).upper()
        response = check_order_status.invoke(order_id)
        
    elif intent == "policy":
        response = search_policy.invoke(last_message)
        
    elif intent == "escalate":
        response = escalate_to_agent.invoke(last_message)
        
    else:
        response = "I can help with Orders (provide ID) or Policies (returns, shipping)."
        
    return {"messages": [response]}