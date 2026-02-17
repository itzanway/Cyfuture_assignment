# ShopAssist AI - Intelligent E-Commerce Agent

## 1. Architecture Overview
This project implements a **Controller-Agent architecture** using a central router to classify user intent and delegate tasks to specialized tools.

### Flow
1.  **Input Guard:** Validates user input (Regex for Order IDs).
2.  **Router (Reasoning Engine):** Classifies query into:
    * *Transactional* (Order Status)
    * *Informational* (Policy RAG)
    * *Escalation* (Human Handoff)
3.  **Tool Execution:** Calls the specific Python function.

## 2. Functional Requirements Met
* **Maintained Knowledge Sources:** Implemented via `search_policy` tool mimicking a Vector DB retrieval.
* **Live Order Retrieval:** Implemented via `check_order_status` accessing a mock transactional database.
* **Identifier Validation:** Uses Regex (`ORD-\d+`) to validate input before API calls.
* **Problem Detection:** Sentiment keywords trigger the `escalate_to_agent` tool.

## 3. Tech Stack & Justification
* **Python:** Chosen for its rich ecosystem of AI libraries.
* **LangGraph (State Machine):** Used to manage the conversation flow and routing logic efficiently.
* **Pydantic:** Used for strict data validation to ensure API safety.
