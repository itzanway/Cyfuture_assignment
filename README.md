# ShopAssist AI - Intelligent E-Commerce Agent

## 📌 Project Overview
**ShopAssist AI** is an intelligent customer service agent designed for an online shopping platform. It utilizes a **Controller-Agent architecture** to intelligently route user queries, validate inputs, and manage state.

This project was designed to fulfill specific functional requirements:
1.  **Informational:** Answering policy questions using maintained knowledge sources.
2.  **Operational:** Retrieving live order status from transactional records.
3.  **Safety:** Validating identifiers (Regex) and detecting hostile sentiment for human escalation.

---

## 🏗️ Architecture & Design
The system follows a **Router-Controller Pattern** where a central "Brain" classifies intent before delegating to specific tools.

### Decision Flow
1.  **Input Guard:** The system first checks for valid identifiers (e.g., `ORD-XXXXX`).
2.  **Router (Reasoning Engine):** Analyzes the user's message to classify intent:
    * *Type A: Informational* → Queries the Policy Knowledge Base.
    * *Type B: Operational* → Queries the Order Database (only if ID is valid).
    * *Type C: Escalation* → Detects negative sentiment/keywords and hands off to a human.
3.  **Tool Execution:** The specific Python function is executed, and the result is returned to the user.

---

## ✅ Functional Requirements Met

| Requirement | Implementation Details |
| :--- | :--- |
| **Maintained Knowledge Sources** | Implemented via `search_policy` tool mimicking a Vector DB retrieval for shipping/return policies. |
| **Live Order Retrieval** | Implemented via `check_order_status` accessing a mock transactional database. |
| **Identifier Validation** | Strictly enforces `ORD-\d+` format using Regex before allowing API calls. |
| **Problem Detection** | Sentiment analysis detects keywords (e.g., "angry", "broken") to trigger `escalate_to_agent`. |

---

## 🛠️ Tech Stack & Justification

* **Python 3.10+:** Chosen for its dominance in AI/ML and rich library ecosystem.
* **LangGraph (State Management):** Used to manage the conversation state and routing logic, allowing for cyclic graphs (loops) unlike traditional linear chains.
* **Regex & Pydantic:** Used for strict input validation to ensure backend services are never queried with malformed data.

---

## 🚀 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/itzanway/Cyfuture_assignment.git](https://github.com/itzanway/Cyfuture_assignment.git)
    cd Cyfuture_assignment
    cd ShopAssistAI
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Agent**
    ```bash
    python main.py
    ```

---

## 🧪 Testing Guide (User Inputs)

Use the following inputs to verify that the agent meets all assignment criteria.

### 1. Test Operational Logic (Order Tracking)
* **Goal:** Retrieve live order data.
* **Input:** `Where is my order ORD-12345?`
* **Expected Output:** *"Order ORD-12345 is currently Shipped. Items: Wireless Mouse."*

### 2. Test Input Validation (Safety)
* **Goal:** Ensure the agent rejects invalid IDs.
* **Input:** `Where is order 12345?`
* **Expected Output:** *"I detected you are asking about an order, but I couldn't find a valid Order ID (e.g., ORD-12345)..."*

### 3. Test Informational Logic (Policies)
* **Goal:** Retrieve policy info from the knowledge base.
* **Input:** `What is your return policy?`
* **Expected Output:** *"You can return items within 30 days of receipt if they are unused."*

### 4. Test Escalation Logic (Problem Detection)
* **Goal:** Detect angry user/complex issue.
* **Input:** `I am angry because my package is broken.`
* **Expected Output:** *"TICKET CREATED: A human agent has been notified..."*

---

## 📂 Project Structure

```text
/ShopAssistAI
│
├── /src
│   ├── __init__.py      # Package initialization
│   ├── agent.py         # Main Logic: Routing & State Management
│   ├── tools.py         # Tools: Mock Database & Policy Search
│
├── main.py              # Application Entry Point
├── requirements.txt     # Dependencies
└── README.md            # Documentation
