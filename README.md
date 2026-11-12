
# Support Desk – AI FAQ Assistant

A modern customer support FAQ assistant built with Python and Streamlit.

The application uses a three-agent architecture to classify customer questions, retrieve relevant FAQ entries, and generate answers grounded in the available knowledge base.

## Features

- Three-agent FAQ architecture
- Customer question classification
- Knowledge base retrieval
- Grounded FAQ responses
- Confidence and match scores
- Partial-match detection
- Human support escalation
- Orders, payments, delivery, returns and refunds
- Modern responsive Streamlit interface
- Conversation history
- Transcript download
- Adjustable match sensitivity
- FAQ knowledge base browser
- Automated tests
- No external API key required

## Technology Stack

- Python
- Streamlit
- HTML
- CSS
- Dataclasses
- Regular Expressions
- Pytest

## Project Structure

```text
faq_assistant/
├── app.py
├── assistant.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
└── tests/
    └── test_assistant.py
```

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Run Tests

Install pytest:

```bash
pip install pytest
```

Run:

```bash
python -m pytest -q
```

## Customization

You can customize the FAQ questions and answers by editing the `FAQ_KB` list in `assistant.py`.

You can also adjust:

- Category keywords
- Matching threshold
- Similarity score
- Fallback response
- Small-talk response

## Architecture

1. FAQ Classifier: identifies the question category.
2. Knowledge Agent: retrieves relevant FAQ entries.
3. Response Agent: returns an answer from retrieved FAQ content.

If the knowledge base does not contain a suitable answer, the system escalates instead of guessing.

## Important

The included FAQ entries are sample policies. Replace them with your organization's approved customer support information before using the application in production.
