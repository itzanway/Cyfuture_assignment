#  AI-Powered E-Commerce Support Agent

A production-ready, multi-layered AI customer support system designed for e-commerce platforms.

This system intelligently handles:

-  Order Tracking (Transactional Queries)
-  Policy & FAQ Queries (RAG-based)
-  Multi-turn Conversations with State
-  Frustration Detection & Escalation
-  PII Redaction & Guardrails
-  Secure Tool Calling with Validation

Built using:

- LangGraph
- FastAPI
- GPT-4o / Gemini 1.5 Pro
- Pinecone / Milvus
- Pydantic
- SQL Database

---

#  System Architecture

The architecture is divided into **four distinct layers**:

```
Interface Layer → Cognitive Layer → Service Layer → Data Layer
```

---

# 🛡 Layer 1: Interface & Guardrails (The Gatekeeper)

This layer protects the system before any data reaches the LLM.

## Responsibilities

### 1️⃣ Input Sanitization
- Removes injection patterns
- Blocks system prompt overrides
- Cleans malicious payloads

### 2️⃣ PII Redaction
- Detects:
  - Credit Card Numbers
  - Phone Numbers
  - Emails
- Masks sensitive data unless explicitly required for verification

### 3️⃣ Safety Filtering
- Detects toxic/manipulative content
- Prevents competitor comparison queries
- Blocks out-of-scope instructions

---

# 🧠 Layer 2: Cognitive Orchestrator (The Brain)

The decision-making engine.

> It decides what to do. It does NOT execute.

## Components

### Intent Classifier
Classifies user input into:

- `POLICY_QUERY`
- `ORDER_STATUS`
- `ESCALATION`

### Context Manager
Maintains:

- Conversation state
- Previously provided order IDs
- Follow-up tracking
- Retry count

### Slot / Entity Filler
Ensures required parameters exist before tool execution.

Example:
- Order ID required for `ORDER_STATUS`
- If missing → Ask user

---

# 🛠 Layer 3: Functional Workers (The Tools)

Triggered by the Orchestrator.

---

## 🔎 RAG Worker (Knowledge Retrieval)

Used for informational queries.

### Flow

1. Convert user query → vector embedding
2. Search vector database
3. Retrieve top 3 relevant chunks
4. LLM synthesizes response

---

## 📦 API Worker (Transactional Queries)

Handles live order tracking.

### Flow

1. Validate Order ID format
2. Call backend API
3. Return structured JSON
4. Convert JSON → Natural language

---

## 🙋 Escalation Worker

Triggered when:
- High user frustration
- Repeated failure
- Refund demand
- Negative sentiment spike

### Actions

- Log conversation summary
- Create CRM ticket
- Generate ticket ID
- Notify human agent

---

# 🗄 Layer 4: Data & Backend

| Component | Technology | Purpose |
|------------|------------|----------|
| LLM | GPT-4o / Gemini 1.5 Pro | Reasoning & Tool Calling |
| Framework | LangGraph | Cyclic workflows |
| Backend | FastAPI | Async API handling |
| Vector DB | Pinecone / Milvus | RAG retrieval |
| DB | PostgreSQL / MongoDB | Orders & users |
| Validation | Pydantic + RegEx | Strict schema enforcement |
| Guardrails | NeMo Guardrails | Safety enforcement |

---

# 🔄 Reasoning Loop

The system follows:

```
Observe → Classify → Evaluate → Validate → Act → Synthesize
```

---

# 📊 Process Flows

---

## Flow A: Informational Query (RAG)

**User:**  
"What is your return policy for electronics?"

1. Intent → POLICY_QUERY
2. Route → RAG Worker
3. Retrieve top chunks
4. Generate response

**Output:**
"Electronics can be returned within 15 days if unopened..."

---

## Flow B: Operational Query (Happy Path)

**User:**  
"Check status for Order #ABC-123"

1. Intent → ORDER_STATUS
2. Extract order_id = ABC-123
3. Validate format
4. Call API
5. Format response

**Output:**
"Your order #ABC-123 is Out for Delivery and will arrive by 5 PM."

---

## Flow C: Missing Information (Loop)

**User:**  
"Where is my order?"

1. Intent → ORDER_STATUS
2. No order_id found
3. Ask follow-up

**Agent:**  
"Please provide your Order ID."

(User provides ID → Loop back to Flow B)

---

## Flow D: Escalation

**User:**  
"I’ve asked three times and my order is still missing! I want a refund!"

1. Sentiment analysis detects high negativity
2. Trigger ESCALATION_PROTOCOL
3. Create CRM ticket

**Response:**
"I apologize for the frustration. I am escalating this to a human specialist. Your ticket ID is #999."

---

# 🏗 Step-by-Step Implementation

---

## Step 1: Knowledge Ingestion

- Scrape Help & Policy pages
- Chunk text into 500-token segments
- Generate embeddings
- Store in Vector DB

---

## Step 2: Define Tools

```python
from pydantic import BaseModel, Field

class OrderInput(BaseModel):
    order_id: str = Field(
        ...,
        pattern=r"^[A-Z]{3}-\d{3}$",
        description="The order ID format XXX-000"
    )

def get_order_status(order_id: str):
    """
    Fetch live order status from database.
    """
    return {
        "status": "Shipped",
        "delivery_date": "2023-10-25"
    }
```

---

## Step 3: Build Router Prompt

```
You are a routing assistant.

If the query requires account-specific data → output TOOL.
If the query is about general policy → output RAG.
If the user is angry or demanding refund → output ESCALATE.
```

---

## Step 4: LangGraph State Graph

Nodes:

- Start Node
- Router Node
- RAG Node
- Tool Node
- Escalation Node
- Response Node

Supports cyclic loops for missing parameters.

---

## Step 5: Integration & Testing

- Connect to frontend chat widget
- Implement async FastAPI endpoints
- Perform red teaming:
  - Invalid Order IDs
  - Prompt injection
  - Toxic language
  - Repeated refund demands

---

# 🔒 Security Considerations

- Strict Pydantic validation before API calls
- Regex pattern enforcement
- No direct DB exposure to LLM
- Tool-call only architecture
- Guardrails against competitor queries

---

# 📈 Why This Architecture Works

✅ Separation of reasoning & execution  
✅ Cyclic state handling  
✅ No hallucinated transactional data  
✅ Secure tool invocation  
✅ Scalable microservice-friendly design  

---

# 🚀 Future Improvements

- Multi-language support
- Voice input support
- Auto-refund workflow automation
- Analytics dashboard for conversation trends
- Proactive order delay alerts

---

# 🏁 Conclusion

This system demonstrates:

- Production-grade AI orchestration
- Safe LLM integration
- Robust tool-calling
- Enterprise-level guardrails
- Scalable conversational architecture

It is designed not just to answer questions —  
but to reason, validate, act, and recover intelligently.

---

**Author:** Anway  
**Architecture Type:** Agentic + RAG + Tool Calling  
**Use Case:** E-Commerce AI Support System  
