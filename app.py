
import html
from datetime import datetime

import streamlit as st
from assistant import CATEGORIES, FAQ_KB, AssistantResponse, FAQAssistant


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Support Desk",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM DARK GRID UI
# --------------------------------------------------

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #080b12;
    --panel: #0e1420;
    --line: #202c40;
    --text: #e8edf7;
    --muted: #8794aa;
    --accent: #8b7cff;
    --accent2: #39c6b0;
}

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp {
    background-color: var(--bg);
    background-image:
        linear-gradient(rgba(120,139,173,.075) 1px, transparent 1px),
        linear-gradient(90deg, rgba(120,139,173,.075) 1px, transparent 1px),
        radial-gradient(ellipse at 70% -15%, rgba(108,91,220,.18), transparent 42%);
    background-size: 32px 32px, 32px 32px, auto;
    background-attachment: fixed;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: rgba(8,11,18,.7);
}

.block-container {
    max-width: 1440px;
    padding: 1.4rem 2.2rem 3rem;
}

[data-testid="stSidebar"] {
    background: #0b111c;
    border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.4rem 1rem;
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #aab5c8;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 5px 25px;
    border-bottom: 1px solid var(--line);
    margin-bottom: 20px;
}

.brand-logo {
    width: 43px;
    height: 43px;
    border: 1px solid #6257b5;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font: 700 14px 'DM Mono';
    color: #c5beff;
    background: rgba(139,124,255,.13);
    box-shadow: 0 0 24px rgba(139,124,255,.12);
}

.brand-name {
    font: 700 17px 'Space Grotesk';
    color: #f4f6fc;
}

.brand-sub {
    font-size: 11px;
    color: #7f8da4;
    margin-top: 4px;
}

.side-kicker {
    color: #7788a4;
    font: 500 10px 'DM Mono';
    letter-spacing: 1.4px;
    text-transform: uppercase;
    margin: 20px 0 9px;
}

.side-note {
    padding: 13px;
    border: 1px solid var(--line);
    border-radius: 10px;
    background: #101927;
    font-size: 11px;
    line-height: 1.6;
    color: #99a7bd;
}

.side-note strong {
    display: block;
    font-size: 12px;
    color: #e7ecf6;
    margin-bottom: 4px;
}

[data-testid="stSidebar"] .stButton button,
[data-testid="stSidebar"] .stDownloadButton button {
    border-radius: 8px !important;
    border: 1px solid #26344a !important;
    background: #101927 !important;
    color: #cbd5e5 !important;
    min-height: 39px;
    font-size: 11px;
    text-align: left;
    justify-content: flex-start;
    transition: .18s ease;
}

[data-testid="stSidebar"] .stButton button:hover,
[data-testid="stSidebar"] .stDownloadButton button:hover {
    border-color: #8275e8 !important;
    background: #171e32 !important;
    color: white !important;
}

[data-testid="stSidebar"] [data-testid="stSlider"] label {
    color: #cbd5e5 !important;
    font-size: 11px;
}

[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: 1px solid var(--line);
    border-radius: 9px;
    background: #0e1623;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin: 2px 0 20px;
    color: #dce4f2;
    font-size: 13px;
    font-weight: 700;
}

.topbar .small {
    font-size: 11px;
    color: #7f8da4;
    font-weight: 400;
    margin-top: 4px;
}

.ai-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 11px;
    border: 1px solid #24443f;
    border-radius: 6px;
    background: rgba(57,198,176,.07);
    color: #6bdac7;
    font: 500 10px 'DM Mono';
}

.live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #39c6b0;
    display: inline-block;
    box-shadow: 0 0 10px #39c6b0;
}

.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid #29334a;
    border-radius: 14px;
    padding: 34px 36px;
    color: white;
    margin-bottom: 25px;
    min-height: 200px;
    background: linear-gradient(115deg, rgba(18,25,43,.97), rgba(20,25,48,.94));
    box-shadow: 0 18px 50px rgba(0,0,0,.22);
}

.hero:before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(90deg, transparent 49.8%, rgba(139,124,255,.07) 50%, transparent 50.2%),
        linear-gradient(0deg, transparent 49.8%, rgba(139,124,255,.07) 50%, transparent 50.2%);
    background-size: 30px 30px;
    mask-image: linear-gradient(90deg, transparent, black);
}

.hero:after {
    content: "SUPPORT / 01";
    position: absolute;
    right: 28px;
    bottom: 22px;
    color: rgba(196,190,255,.28);
    font: 500 11px 'DM Mono';
    letter-spacing: 2px;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 760px;
}

.hero-eyebrow {
    font: 500 10px 'DM Mono';
    letter-spacing: 2px;
    color: #a99fff;
}

.hero h1 {
    font: 700 clamp(27px,3vw,39px) 'Space Grotesk';
    letter-spacing: -1px;
    color: #f3f5fb;
    margin: 14px 0 10px;
    line-height: 1.15;
}

.hero p {
    font-size: 13px;
    line-height: 1.8;
    color: #aab5c8;
    margin: 0;
    max-width: 680px;
}

.hero-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 19px;
}

.hero-tag {
    border: 1px solid #303b55;
    background: #151d2e;
    padding: 6px 10px;
    border-radius: 5px;
    font: 400 10px 'DM Mono';
    color: #c4cce0;
}

.section-heading {
    font: 600 16px 'Space Grotesk';
    color: #e8edf7;
    margin: 22px 0 8px;
}

.section-sub {
    font-size: 11px;
    color: #7f8da4;
    margin: 0 0 14px;
}

.topic-card {
    height: 112px;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #263248;
    background: rgba(14,20,32,.94);
    box-shadow: 0 8px 24px rgba(0,0,0,.12);
    transition: .18s ease;
}

.topic-card:hover {
    transform: translateY(-2px);
    border-color: #7064cb;
}

.topic-icon {
    width: 31px;
    height: 28px;
    border: 1px solid #3c4164;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font: 500 10px 'DM Mono';
    color: #b8afff;
    margin-bottom: 12px;
}

.topic-name {
    font: 600 12px 'Space Grotesk';
    color: #e4e9f3;
}

.topic-count {
    font: 400 10px 'DM Mono';
    color: #77859c;
    margin-top: 5px;
}

.info-panel {
    border: 1px solid #263248;
    border-radius: 12px;
    background: rgba(14,20,32,.94);
    padding: 18px;
}

[data-testid="stButton"] button {
    border-radius: 8px;
    border: 1px solid #28364d;
    background: #101927;
    color: #cbd5e5;
    font-weight: 500;
    font-size: 11px;
    min-height: 40px;
    transition: all .18s ease;
}

[data-testid="stButton"] button:hover {
    color: #fff;
    border-color: #8275e8;
    background: #171f32;
}

[data-testid="stChatMessage"] {
    border: 1px solid #263248;
    border-radius: 12px;
    background: #0e1623;
    padding: 14px 16px;
    margin: 10px 0;
}

[data-testid="stChatMessage"] p {
    line-height: 1.7;
    color: #d2dbea;
    font-size: 12px;
}

[data-testid="stChatInput"] {
    border: 1px solid #34415c !important;
    border-radius: 10px !important;
    background: #0e1623 !important;
    box-shadow: 0 8px 28px rgba(0,0,0,.2) !important;
}

[data-testid="stChatInput"] textarea {
    font-size: 12px !important;
    color: #e8edf7 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #72819a !important;
}

.metric-card {
    border: 1px solid #263248;
    border-radius: 10px;
    padding: 14px 16px;
    background: #0e1623;
}

.metric-label {
    font: 500 9px 'DM Mono';
    color: #8190a8;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    font: 600 25px 'Space Grotesk';
    color: #f0f3fa;
    margin-top: 6px;
}

.status-badge {
    display: inline-block;
    border-radius: 5px;
    padding: 5px 8px;
    color: #fff;
    font: 500 9px 'DM Mono';
    margin: 0 6px 8px 0;
}

[data-testid="stExpander"] {
    border: 1px solid #263248;
    border-radius: 9px;
    background: #0e1623;
}

[data-testid="stExpander"] summary {
    color: #d5deed;
}

.stMarkdown p, .stMarkdown li {
    color: #c3cede;
}

.stCaption {
    color: #8190a8 !important;
}

hr {
    border-color: #263248 !important;
}

@media(max-width:900px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }
    .hero {
        padding: 25px 22px;
    }
    .topic-card {
        height: 105px;
    }
}
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def esc(value):
    return html.escape(str(value))


STATUS_STYLE = {
    "answered": ("Answered from FAQ", "#169b73"),
    "partial": ("Closest match", "#c98524"),
    "escalated": ("Needs human support", "#d34d69"),
    "smalltalk": ("Welcome", "#7866b6"),
}

SAMPLE_QUESTIONS = [
    "How do I track my order?",
    "My card got declined, what should I do?",
    "How long until my refund arrives?",
    "Can I return an item I already opened?",
    "Can I get a discount for my birthday?",
]

TOPIC_META = {
    "orders": ("01", "#141b2b", "#b8afff"),
    "payments": ("02", "#141b2b", "#b8afff"),
    "delivery": ("03", "#141b2b", "#b8afff"),
    "returns": ("04", "#141b2b", "#b8afff"),
    "refunds": ("05", "#141b2b", "#b8afff"),
}


def badge(text, color):
    return (
        f'<span class="status-badge" '
        f'style="background:{color}">{esc(text)}</span>'
    )


def build_transcript(history):
    lines = [
        f"Support Desk transcript - {datetime.now():%Y-%m-%d %H:%M}",
        ""
    ]

    for msg in history:
        if msg["role"] == "user":
            lines.append(f"Customer: {msg['content']}")
        else:
            response = msg["response"]
            lines.append(
                f"Assistant [{response.category_label} | "
                f"{response.status}]: {response.answer}"
            )
        lines.append("")

    return "\n".join(lines)


def render_assistant(response: AssistantResponse):
    status_label, status_color = STATUS_STYLE.get(
        response.status,
        STATUS_STYLE["escalated"]
    )

    category = CATEGORIES.get(
        response.category,
        CATEGORIES["general"]
    )

    tags = badge(category["label"], category["color"])
    tags += badge(status_label, status_color)

    if response.confidence > 0:
        tags += badge(
            f"Category confidence {round(response.confidence * 100)}%",
            "#6554a6"
        )

    st.markdown(tags, unsafe_allow_html=True)
    st.markdown(response.answer)

    if response.source:
        with st.expander(
            f"Answer source · {response.source['id']} · "
            f"{response.source['question']}"
        ):
            st.markdown(
                f"**Match score:** `{response.score:.2f}`  \n"
                f"**FAQ category:** "
                f"{CATEGORIES[response.source['category']]['label']}"
            )

    if response.related:
        st.caption(
            "You may also find these helpful: "
            + " · ".join(response.related)
        )


def render_metric(label, value, number):
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">{number} &nbsp;{esc(label)}</div>'
        f'<div class="metric-value">{value}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

st.session_state.setdefault("history", [])
st.session_state.setdefault("threshold", 0.30)

clicked = None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="brand-row">'
        '<div class="brand-logo">SD</div>'
        '<div>'
        '<div class="brand-name">Support Desk</div>'
        '<div class="brand-sub">Your customer care assistant</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-kicker">Assistant settings</div>',
        unsafe_allow_html=True
    )

    threshold = st.slider(
        "Match sensitivity",
        0.10,
        0.60,
        st.session_state.threshold,
        0.05,
        help="Lower values match more questions. Higher values are more selective.",
        key="threshold",
    )

    st.markdown(
        '<div class="side-kicker">Popular questions</div>',
        unsafe_allow_html=True
    )

    for i, question in enumerate(SAMPLE_QUESTIONS):
        if st.button(
            question,
            key=f"quick_{i}",
            use_container_width=True
        ):
            clicked = question

    st.markdown(
        '<div class="side-kicker">Your conversation</div>',
        unsafe_allow_html=True
    )

    if st.button("New conversation", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    st.download_button(
        "Download conversation",
        data=(
            build_transcript(st.session_state.history)
            if st.session_state.history else ""
        ),
        file_name=(
            f"support_transcript_{datetime.now():%Y%m%d_%H%M%S}.txt"
        ),
        mime="text/plain",
        disabled=not st.session_state.history,
        use_container_width=True,
    )

    st.markdown(
        '<div class="side-kicker">Knowledge base</div>',
        unsafe_allow_html=True
    )

    with st.expander(f"Browse all {len(FAQ_KB)} FAQ entries"):

        for category_key, meta in CATEGORIES.items():

            entries = [
                entry for entry in FAQ_KB
                if entry["category"] == category_key
            ]

            if not entries:
                continue

            st.markdown(f"**{meta['label']}**")

            for entry in entries:
                st.markdown(
                    f"- `{esc(entry['id'])}` "
                    f"{esc(entry['question'])}"
                )

    st.markdown(
        '<div class="side-note">'
        '<strong>Need a little more help?</strong>'
        'If the answer is not in our FAQ, the assistant will let you know '
        'instead of guessing.'
        '</div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

prompt = st.chat_input(
    "Type your question about orders, payments, delivery, returns or refunds..."
)

question = clicked or prompt

if question:
    assistant = FAQAssistant(threshold=threshold)

    st.session_state.history.append({
        "role": "user",
        "content": question
    })

    st.session_state.history.append({
        "role": "assistant",
        "response": assistant.ask(question)
    })


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    '<div class="topbar">'
    '<div>SMART SUPPORT / INSTANT ANSWERS'
    '<div class="small">A simpler way to get help with your order</div>'
    '</div>'
    '<div class="ai-pill">'
    '<span class="live-dot"></span> AI ASSISTANT ONLINE'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown(
    '<section class="hero">'
    '<div class="hero-content">'
    '<div class="hero-eyebrow">'
    'CUSTOMER CARE · HERE WHEN YOU NEED US'
    '</div>'
    '<h1>Welcome to Support Desk</h1>'
    '<p>Get quick, clear answers about your orders, payments, delivery, '
    'returns and refunds. We only answer from our support knowledge base '
    '— no made-up information.</p>'
    '<div class="hero-tags">'
    '<span class="hero-tag">01 &nbsp; Instant answers</span>'
    '<span class="hero-tag">02 &nbsp; FAQ-grounded support</span>'
    '<span class="hero-tag">03 &nbsp; Always available</span>'
    '</div>'
    '</div></section>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------

history = st.session_state.history

if not history:

    st.markdown(
        '<div class="section-heading">Explore support topics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">'
        'Choose a topic to see what we can help you with.'
        '</div>',
        unsafe_allow_html=True
    )

    columns = st.columns(5)

    for col, key in zip(
        columns,
        ["orders", "payments", "delivery", "returns", "refunds"]
    ):

        number, bg, accent = TOPIC_META[key]

        count = sum(
            1 for entry in FAQ_KB
            if entry["category"] == key
        )

        col.markdown(
            f'<div class="topic-card">'
            f'<div class="topic-icon" '
            f'style="background:{bg};color:{accent}">'
            f'{number}</div>'
            f'<div class="topic-name">'
            f'{CATEGORIES[key]["label"]}</div>'
            f'<div class="topic-count">'
            f'{count} helpful FAQ articles</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-heading">Popular questions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">'
        'Tap a question below or ask us anything in the message box.'
        '</div>',
        unsafe_allow_html=True
    )

    question_columns = st.columns(2)

    for i, sample_question in enumerate(SAMPLE_QUESTIONS):

        with question_columns[i % 2]:

            if st.button(
                sample_question,
                key=f"main_quick_{i}",
                use_container_width=True
            ):
                st.session_state.pending_question = sample_question
                st.rerun()

    if st.session_state.get("pending_question"):

        pending = st.session_state.pop("pending_question")

        assistant = FAQAssistant(threshold=threshold)

        st.session_state.history.extend([
            {
                "role": "user",
                "content": pending
            },
            {
                "role": "assistant",
                "response": assistant.ask(pending)
            },
        ])

        st.rerun()

    st.markdown(
        '<div class="info-panel" '
        'style="margin-top:16px;text-align:center">'
        '<b style="color:#c5beff">We are ready when you are</b>'
        '<div style="font-size:12px;color:#8794aa;margin-top:5px">'
        'Use the message box at the bottom to start your support conversation.'
        '</div></div>',
        unsafe_allow_html=True,
    )

else:

    answers = [
        message["response"]
        for message in history
        if message["role"] == "assistant"
    ]

    columns = st.columns(4)

    metrics = [
        ("Questions", len(answers), "01"),
        (
            "Answered",
            sum(r.status == "answered" for r in answers),
            "02"
        ),
        (
            "Closest matches",
            sum(r.status == "partial" for r in answers),
            "03"
        ),
        (
            "Escalated",
            sum(r.status == "escalated" for r in answers),
            "04"
        ),
    ]

    for col, (label, value, number) in zip(columns, metrics):
        with col:
            render_metric(label, value, number)

    st.markdown(
        '<div class="section-heading">'
        'Your support conversation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-sub">'
        'Answers are based on the available FAQ knowledge base.'
        '</div>',
        unsafe_allow_html=True
    )

    for message in history:

        if message["role"] == "user":

            # No custom avatar path: avoids Streamlit image errors.
            with st.chat_message("user"):
                st.markdown(message["content"])

        else:

            # No custom avatar path: avoids Streamlit image errors.
            with st.chat_message("assistant"):
                render_assistant(message["response"])


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    '<div style="text-align:center;color:#77859c;'
    'font-size:10px;margin-top:24px">'
    'SUPPORT DESK &nbsp;·&nbsp; SMART ANSWERS, HUMAN-READY SUPPORT'
    '</div>',
    unsafe_allow_html=True,
)
