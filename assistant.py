
"""
FAQ Assistant core logic.

Three cooperating agents:
1. FAQClassifier
2. KnowledgeAgent
3. ResponseAgent

Runs locally without external API keys.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Optional


CATEGORIES = {
    "orders": {"label": "Orders", "icon": "📦", "color": "#6366f1"},
    "payments": {"label": "Payments", "icon": "💳", "color": "#0ea5e9"},
    "delivery": {"label": "Delivery", "icon": "🚚", "color": "#10b981"},
    "returns": {"label": "Returns", "icon": "↩️", "color": "#f59e0b"},
    "refunds": {"label": "Refunds", "icon": "💰", "color": "#ec4899"},
    "general": {"label": "General", "icon": "💬", "color": "#64748b"},
}


FAQ_KB = [
    {
        "id": "ORD-1",
        "category": "orders",
        "question": "How can I track my order?",
        "keywords": ["status", "tracking", "where", "locate"],
        "answer": (
            "You can track your order from the 'My Orders' page. "
            "Open the order and select 'Track Shipment' to see its latest status."
        ),
    },
    {
        "id": "ORD-2",
        "category": "orders",
        "question": "How do I cancel an order?",
        "keywords": ["stop", "change", "cancellation", "undo"],
        "answer": (
            "Go to 'My Orders', select the order and choose 'Cancel Order'. "
            "Cancellation is possible only before the order has been dispatched."
        ),
    },
    {
        "id": "ORD-3",
        "category": "orders",
        "question": "Can I change my order after placing it?",
        "keywords": ["edit", "update", "modify", "wrong"],
        "answer": (
            "Orders can be edited from 'My Orders' only before dispatch. "
            "After dispatch, please contact support and we will review your request."
        ),
    },
    {
        "id": "PAY-1",
        "category": "payments",
        "question": "What payment methods do you accept?",
        "keywords": [
            "credit", "debit", "bank", "transfer", "checkout", "methods"
        ],
        "answer": (
            "We accept credit cards, debit cards and bank transfers. "
            "Available options are shown at checkout."
        ),
    },
    {
        "id": "PAY-2",
        "category": "payments",
        "question": "Why was my payment declined?",
        "keywords": [
            "card", "declined", "charged", "failed", "bank", "rejected"
        ],
        "answer": (
            "Payments can be declined because of insufficient funds, "
            "incorrect card details, or restrictions set by your bank. "
            "Please check your details or contact your bank, then try again."
        ),
    },
    {
        "id": "PAY-3",
        "category": "payments",
        "question": "I was charged twice for one order. What should I do?",
        "keywords": ["duplicate", "double", "twice", "extra", "billing"],
        "answer": (
            "Please contact support with your order number and a screenshot "
            "of the duplicate charge so we can review it."
        ),
    },
    {
        "id": "DEL-1",
        "category": "delivery",
        "question": "How long does delivery take?",
        "keywords": ["shipping", "arrive", "days", "timeline", "standard"],
        "answer": "Standard delivery usually takes 3 to 5 business days.",
    },
    {
        "id": "DEL-2",
        "category": "delivery",
        "question": "Do you deliver to my area?",
        "keywords": ["area", "location", "city", "available", "country"],
        "answer": (
            "Delivery availability is shown at checkout once you enter your address."
        ),
    },
    {
        "id": "RET-1",
        "category": "returns",
        "question": "How do I return an item?",
        "keywords": ["send", "back", "exchange", "policy"],
        "answer": "Start a return from 'My Orders' within 14 days of delivery.",
    },
    {
        "id": "RET-2",
        "category": "returns",
        "question": "Which items cannot be returned?",
        "keywords": ["final", "sale", "exclude", "non-returnable"],
        "answer": (
            "Items marked as final sale or non-returnable on their product page "
            "cannot be returned."
        ),
    },
    {
        "id": "REF-1",
        "category": "refunds",
        "question": "When will I receive my refund?",
        "keywords": ["money", "timing", "processed", "credited", "arrive"],
        "answer": (
            "Refunds are processed within 5 to 7 business days "
            "after we receive the returned item."
        ),
    },
    {
        "id": "REF-2",
        "category": "refunds",
        "question": "Can I get my refund to my original payment method?",
        "keywords": ["original", "method", "card", "bank"],
        "answer": (
            "Yes. Refunds are returned to the original payment method whenever possible."
        ),
    },
]


STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "am",
    "i", "me", "my", "we", "our", "you", "your", "it", "its", "do",
    "does", "did", "to", "of", "for", "on", "in", "at", "and", "or",
    "how", "what", "when", "where", "why", "who", "can", "could",
    "would", "should", "will", "there", "this", "that", "with", "if",
    "so", "from", "get", "got", "have", "has", "please", "pls", "just",
    "any", "long", "until", "about", "really", "some", "by", "as",
}


CANONICAL = {
    "order": "order",
    "orders": "order",
    "ordered": "order",

    "cancel": "cancel",
    "cancelled": "cancel",
    "canceled": "cancel",
    "cancellation": "cancel",

    "track": "track",
    "tracking": "track",
    "tracked": "track",
    "status": "track",

    "pay": "payment",
    "paid": "payment",
    "payments": "payment",
    "payment": "payment",
    "billing": "payment",
    "bank": "payment",
    "charge": "payment",
    "charged": "payment",

    "card": "card",
    "cards": "card",
    "credit": "card",
    "debit": "card",

    "decline": "decline",
    "declined": "decline",
    "failed": "decline",
    "rejected": "decline",

    "deliver": "delivery",
    "delivered": "delivery",
    "delivery": "delivery",
    "delivering": "delivery",
    "shipping": "delivery",
    "shipped": "delivery",
    "ship": "delivery",
    "arrive": "delivery",
    "arrives": "delivery",
    "arrival": "delivery",
    "courier": "delivery",
    "dispatch": "delivery",
    "dispatched": "delivery",

    "return": "return",
    "returns": "return",
    "returned": "return",
    "returning": "return",
    "exchange": "return",
    "exchanges": "return",

    "refund": "refund",
    "refunds": "refund",
    "refunded": "refund",
    "reimburse": "refund",
    "reimbursed": "refund",
    "reimbursement": "refund",
    "money": "refund",
}


GREETINGS = {
    "hi", "hello", "hey", "thanks", "thank", "you", "bye",
    "good", "morning", "afternoon", "evening", "ok", "okay",
    "much", "great", "cheers", "that", "helped",
}


CATEGORY_KEYWORDS = {
    "refunds": {"refund"},
    "returns": {"return"},
    "payments": {"payment", "card", "decline"},
    "orders": {"order", "cancel", "track"},
    "delivery": {"delivery", "address"},
}


FALLBACK_MESSAGE = (
    "I couldn't find this in our FAQ, so I'd rather not guess. "
    "I've noted your question for our support team. "
    "Please contact our customer support team directly for help "
    "with this request."
)


SMALLTALK_MESSAGE = (
    "Hello! 👋 I can help with orders, payments, delivery, "
    "returns and refunds. What would you like to know?"
)


MAX_QUESTION_CHARS = 500
ANSWER_CONFIDENT_SCORE = 0.5


def tokenize(text: str) -> list[str]:
    """Convert text into normalized searchable terms."""

    terms = []

    for word in re.findall(r"[a-z]+", text.lower()):

        if word in STOPWORDS:
            continue

        terms.append(CANONICAL.get(word, word))

    return terms


def content_terms(text: str) -> set[str]:
    return set(tokenize(text))


def is_smalltalk(text: str) -> bool:
    words = set(re.findall(r"[a-z]+", text.lower()))
    return bool(words) and words <= GREETINGS


@dataclass
class Classification:
    category: str
    label: str
    confidence: float
    matched_terms: list[str] = field(default_factory=list)


@dataclass
class Match:
    entry: dict
    score: float


@dataclass
class AssistantResponse:
    question: str
    category: str
    category_label: str
    confidence: float
    status: str
    answer: str
    source: Optional[dict] = None
    score: float = 0.0
    related: list[str] = field(default_factory=list)
    matched_terms: list[str] = field(default_factory=list)


class FAQClassifier:
    """Classifies a customer question into a support category."""

    def classify(self, question: str) -> Classification:

        terms = content_terms(question)

        best_cat = "general"
        best_hits = 0
        best_matched = []

        for cat, keywords in CATEGORY_KEYWORDS.items():

            matched = sorted(terms & keywords)

            if len(matched) > best_hits:
                best_cat = cat
                best_hits = len(matched)
                best_matched = matched

        confidence = (
            best_hits / (best_hits + 1)
            if best_hits else 0.0
        )

        return Classification(
            category=best_cat,
            label=CATEGORIES[best_cat]["label"],
            confidence=round(confidence, 2),
            matched_terms=best_matched,
        )


class KnowledgeAgent:
    """Finds the most relevant FAQ entries."""

    def __init__(self, kb=None, threshold: float = 0.3, top_k: int = 3):

        self.kb = list(kb if kb is not None else FAQ_KB)
        self.threshold = threshold
        self.top_k = top_k

        self._index = [
            (
                entry,
                content_terms(entry["question"])
                | content_terms(" ".join(entry.get("keywords", [])))
            )
            for entry in self.kb
        ]

    def search(
        self,
        question: str,
        category: str = "general"
    ) -> list[Match]:

        query = content_terms(question)

        if not query:
            return []

        matches = []

        for entry, terms in self._index:

            overlap = len(query & terms)

            if not overlap:
                continue

            score = overlap / math.sqrt(
                len(query) * len(terms)
            )

            if category != "general" and entry["category"] == category:
                score *= 1.15

            matches.append(
                Match(
                    entry=entry,
                    score=round(score, 3)
                )
            )

        matches.sort(
            key=lambda match: match.score,
            reverse=True
        )

        return [
            match
            for match in matches[:self.top_k]
            if match.score >= self.threshold
        ]


class ResponseAgent:
    """Generates answers only from retrieved FAQ entries."""

    def compose(
        self,
        question: str,
        cls: Classification,
        matches: list[Match]
    ) -> AssistantResponse:

        base = dict(
            question=question,
            category=cls.category,
            category_label=cls.label,
            confidence=cls.confidence,
            matched_terms=cls.matched_terms,
        )

        if not matches:

            return AssistantResponse(
                status="escalated",
                answer=FALLBACK_MESSAGE,
                **base
            )

        top = matches[0]

        status = (
            "answered"
            if top.score >= ANSWER_CONFIDENT_SCORE
            else "partial"
        )

        answer = top.entry["answer"]

        if status == "partial":

            answer += (
                "\n\n*This may not fully match your question. "
                "If it doesn't help, please contact our support team.*"
            )

        return AssistantResponse(
            status=status,
            answer=answer,
            source={
                "id": top.entry["id"],
                "question": top.entry["question"],
                "category": top.entry["category"],
            },
            score=top.score,
            related=[
                match.entry["question"]
                for match in matches[1:]
            ],
            **base
        )

    def smalltalk(self, question: str) -> AssistantResponse:

        return AssistantResponse(
            question=question,
            category="general",
            category_label=CATEGORIES["general"]["label"],
            confidence=0.0,
            status="smalltalk",
            answer=SMALLTALK_MESSAGE,
        )


class FAQAssistant:
    """Coordinates all three FAQ agents."""

    def __init__(self, kb=None, threshold: float = 0.3):

        self.classifier = FAQClassifier()

        self.knowledge = KnowledgeAgent(
            kb=kb,
            threshold=threshold
        )

        self.responder = ResponseAgent()

    def ask(self, question: str) -> AssistantResponse:

        question = (question or "").strip()[:MAX_QUESTION_CHARS]

        if not question or is_smalltalk(question):
            return self.responder.smalltalk(question)

        cls = self.classifier.classify(question)

        matches = self.knowledge.search(
            question,
            cls.category
        )

        return self.responder.compose(
            question,
            cls,
            matches
        )
