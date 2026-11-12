
import pathlib
import sys

sys.path.insert(
    0,
    str(pathlib.Path(__file__).resolve().parents[1])
)

from assistant import FAQAssistant


def test_track_order_is_answered_from_faq():
    r = FAQAssistant().ask("How do I track my order?")

    assert r.status == "answered"
    assert r.category == "orders"
    assert r.source["id"] == "ORD-1"


def test_paraphrased_decline_question():
    r = FAQAssistant().ask(
        "My card got declined, what should I do?"
    )

    assert r.category == "payments"
    assert r.source["id"] == "PAY-2"


def test_refund_timing():
    r = FAQAssistant().ask(
        "How long until my refund arrives?"
    )

    assert r.category == "refunds"
    assert r.source["id"] == "REF-1"


def test_return_question():
    r = FAQAssistant().ask(
        "How do I return an item?"
    )

    assert r.category == "returns"
    assert r.source["id"] == "RET-1"


def test_out_of_scope_question_is_not_invented():
    r = FAQAssistant().ask(
        "Can I get a discount for my birthday?"
    )

    assert r.status == "escalated"
    assert r.source is None
    assert r.answer


def test_greeting_is_smalltalk():
    assert FAQAssistant().ask("hi").status == "smalltalk"


def test_empty_input_is_handled():
    assert FAQAssistant().ask("   ").status == "smalltalk"


def test_html_in_question_is_kept_as_text():
    r = FAQAssistant().ask(
        "<script>alert(1)</script> refund timing"
    )

    assert r.question.startswith("<script>")
