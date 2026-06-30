#  AI Meeting Coordination Agent

An Agentic AI application that automates meeting scheduling by reading Gmail messages, checking Google Calendar availability, drafting intelligent responses, and incorporating Human-in-the-Loop (HITL) approval before sending emails.

The project demonstrates how LangGraph can be used to build long-running, stateful AI workflows integrated with real-world services like Gmail and Google Calendar.

---

## Features

-  Automatically polls Gmail for new emails
-  Classifies whether an email is a meeting request
-  Extracts structured meeting information using LLM Structured Output
-  Checks Google Calendar availability
-  Finds the closest available meeting slots
-  Drafts professional meeting responses
-  Human-in-the-Loop approval using LangGraph Interrupt/Resume
-  Edit the generated draft before sending
-  Sends emails through Gmail API
-  Marks processed emails as read
-  Stores conversation history in SQLite
-  Automatically creates Google Calendar events when meeting confirmations are received

---

# System Architecture

```

User sends Email
        │
        ▼
 Gmail Poller
        │
        ▼
Intent Classification
        │
        ├──────────────► Non Meeting Email
        │
        ▼
Meeting Detail Extraction
        │
        ▼
Google Calendar
        │
        ▼
Available Slot Generation
        │
        ▼
Best Slot Selection
        │
        ▼
Draft Reply
        │
        ▼
LangGraph Interrupt
        │
        ▼
Pending Approval Database
        │
        ▼
Gradio Dashboard
        │
        ▼
Human Approval / Editing
        │
        ▼
LangGraph Resume
        │
        ▼
Send Email
        │
        ▼
Conversation Database

```

---

# 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| LLM | GPT-5 / GPT-5 Nano |
| Agent Framework | LangGraph |
| UI | Gradio |
| Email | Gmail API |
| Calendar | Google Calendar API |
| Authentication | OAuth 2.0 |
| Database | SQLite |
| Language | Python |
| State Management | LangGraph StateGraph |
| HITL | LangGraph Interrupt / Resume |

---

# Project Structure

```

project/
│
├── graph_builders/
├── nodes/
│
├── services/
│
├── states/
│
├── email_data/
│
├── ui.py
├── poller.py
└── requirements.txt

```

---

# Workflow

### Fresh Meeting Request

1. Poll Gmail for unread emails
2. Classify email intent
3. Extract meeting details
4. Fetch Google Calendar events
5. Compute available meeting slots
6. Rank best matching slots
7. Draft email reply
8. Pause execution using LangGraph Interrupt
9. Human reviews/edits draft in Gradio
10. Resume workflow
11. Send email
12. Save conversation to database

---

### Meeting Confirmation Workflow

1. Detect reply email
2. Extract selected meeting slot
3. Ask for final approval
4. Create Google Calendar event
5. Update conversation status


# Installation

## Clone the repository

```bash
git clone https://github.com/arpitt-bharti/AI-Meeting-Coordination-Agent.git
cd ai-meeting-coordination-agent
```

## Create a virtual environment

```bash
python -m venv .venv
```

## Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configure environment variables

Create a `.env` file and add:

```text
OPENAI_API_KEY=your_api_key
```

## Configure Google OAuth

1. Enable Gmail API and Google Calendar API.
2. Download `credentials.json`.
3. Place it in the project root.
4. Run the authentication flow once to generate `token.json`.

## Run the application

Start the email poller:

```bash
python poller.py
```

In another terminal, start the approval dashboard:

```bash
python ui.py
```

---

# Design Decisions

### Why LangGraph?

The application consists of multiple sequential steps, conditional routing, and a Human-in-the-Loop approval stage. LangGraph provides durable execution, checkpointing, and resumability, making it a natural choice for long-running workflows.

### Why SQLite?

SQLite is sufficient for an MVP and allows lightweight persistence without introducing external infrastructure. It stores conversation history, workflow state, and pending approvals.

### Why Human-in-the-Loop?

Sending emails autonomously carries business risk. The workflow pauses before sending, allowing a human to review and edit the generated draft before execution.

---

# Future Improvements

- Support rescheduling conversations
- Handle clarification requests for ambiguous meeting times
- Replace polling with Gmail Push Notifications
- Add asynchronous processing for higher throughput
- Introduce structured logging and monitoring
- Deploy using Docker and a cloud-hosted database
- Unify both workflows under a common approval dashboard

---

# License

This project is intended for educational and portfolio purposes.

