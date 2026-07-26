import os
import random

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="Yarn Inspection Desk", page_icon="🧵", layout="centered")

if "batch_no" not in st.session_state:
    st.session_state.batch_no = f"{random.randint(10, 99)}-{random.randint(100, 999)}"

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.stApp {
    background-color: #F6F1E4;
    background-image:
        repeating-linear-gradient(0deg, rgba(43,38,34,0.035) 0px, rgba(43,38,34,0.035) 1px, transparent 1px, transparent 6px),
        repeating-linear-gradient(90deg, rgba(43,38,34,0.035) 0px, rgba(43,38,34,0.035) 1px, transparent 1px, transparent 6px);
    color: #2B2622;
}

.yarn-header {
    border-bottom: 3px double #2B2622;
    padding-bottom: 0.6rem;
    margin-bottom: 0.4rem;
}
.yarn-header h1 {
    font-family: 'Special Elite', monospace;
    font-size: 2rem;
    letter-spacing: 1px;
    color: #2E4057;
    margin-bottom: 0.1rem;
}
.yarn-header .batch {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: #B5541E;
    font-weight: 600;
    letter-spacing: 1px;
}

.stitch-divider {
    overflow: hidden;
    white-space: nowrap;
    letter-spacing: 6px;
    font-size: 0.7rem;
    color: #B5541E;
    opacity: 0.55;
    margin: 1.4rem 0;
    text-align: center;
}

.st-key-tag_card {
    background-color: #E8DCC8;
    border: 2px dashed #2B2622;
    border-radius: 6px;
    padding: 1.2rem 1.4rem 0.6rem;
    position: relative;
    transform: rotate(-0.3deg);
}
.st-key-tag_card::before {
    content: "";
    position: absolute;
    top: 14px;
    left: 14px;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #F6F1E4;
    border: 2px solid #2B2622;
}
.st-key-tag_card > div {
    padding-left: 1.6rem;
}
.st-key-tag_card label p {
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.75rem !important;
    color: #2E4057 !important;
    font-weight: 600 !important;
}
.st-key-tag_card input {
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    color: #2B2622 !important;
}
.st-key-tag_card [data-testid="stNumberInputContainer"],
.st-key-tag_card [data-testid="stSelectbox"] div[role="group"] {
    background-color: #F6F1E4 !important;
    border: 1px solid #2B2622 !important;
    border-radius: 3px !important;
}

div[data-testid="stButton"] button {
    font-family: 'Special Elite', monospace;
    text-transform: uppercase;
    letter-spacing: 2px;
    background-color: #B5541E;
    color: #F6F1E4;
    border: 2px solid #2B2622;
    border-radius: 2px;
    padding: 0.5rem 1.4rem;
    box-shadow: 2px 3px 0 rgba(43,38,34,0.3);
}
@media (prefers-reduced-motion: no-preference) {
    div[data-testid="stButton"] button {
        transform: rotate(-1.5deg);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="stButton"] button:hover {
        transform: rotate(-1.5deg) scale(1.03);
        box-shadow: 3px 4px 0 rgba(43,38,34,0.35);
    }
    div[data-testid="stButton"] button:active {
        transform: rotate(0deg) scale(0.97);
        box-shadow: 1px 1px 0 rgba(43,38,34,0.3);
    }
}
div[data-testid="stButton"] button:focus-visible {
    outline: 3px solid #2E4057;
    outline-offset: 2px;
}

.st-key-report_card {
    background-color: #F6F1E4;
    border: 1px solid #2B2622;
    border-left: 6px solid #2E4057;
    padding: 0.8rem 1.2rem;
}
.report-heading {
    font-family: 'Special Elite', monospace;
    color: #B5541E;
    letter-spacing: 2px;
    font-size: 0.95rem;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)


def stitch_divider():
    st.markdown('<div class="stitch-divider">' + " ✕" * 20 + "</div>", unsafe_allow_html=True)


st.markdown(
    f"""
    <div class="yarn-header">
        <h1>🧵 Yarn Inspection Desk</h1>
        <div class="batch">BATCH NO. {st.session_state.batch_no} &middot; AI-ASSISTED DEFECT ANALYSIS</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(key="tag_card"):
    st.markdown("**Measurement Slip**")
    col1, col2 = st.columns(2)
    with col1:
        yarn_count_value = st.number_input("Yarn count", min_value=0.0, value=0.0)
    with col2:
        yarn_count_unit = st.selectbox("Count system", ["Ne", "Tex", "Nm", "Denier"])

    thick_places = st.number_input("Thick places", min_value=0, value=0)
    thin_places = st.number_input("Thin places", min_value=0, value=0)
    neps = st.number_input("Neps", min_value=0, value=0)

    analyze = st.button("Analyze")

stitch_divider()

if analyze:
    prompt = (
        "You are a textile quality control expert reviewing a yarn testing report.\n"
        f"Yarn count: {yarn_count_value} {yarn_count_unit}\n"
        f"Thick places: {thick_places}\n"
        f"Thin places: {thin_places}\n"
        f"Neps: {neps}\n\n"
        "Acceptable defect levels vary a lot by yarn count (finer yarns typically tolerate "
        "fewer defects per km than coarser yarns), so factor the given count and its unit "
        "into your judgment of whether these numbers are actually high, normal, or low for "
        "this yarn, before explaining causes.\n\n"
        "Based on these defect counts, explain in plain language:\n"
        "1. Possible causes (e.g. carding issues, drafting tension, raw material contamination)\n"
        "2. Who should be notified (which department/role)\n"
        "3. What should be checked next\n"
        "Keep it concise and practical for a lab technician."
    )

    try:
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
        )
        with st.container(key="report_card"):
            st.markdown('<div class="report-heading">Inspection Findings</div>', unsafe_allow_html=True)
            st.write(interaction.output_text)
    except Exception as e:
        st.error(f"Something went wrong calling the AI: {e}")
