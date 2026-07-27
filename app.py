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

/* KEYFRAMES FOR TEXTILE ANIMATIONS */
@keyframes spool-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes needle-stitch {
    0%, 100% { transform: translateY(0px) rotate(-10deg); }
    50% { transform: translateY(-5px) rotate(5deg); }
}

@keyframes thread-weave {
    0% { background-position: 0 0; }
    100% { background-position: 24px 0; }
}

@keyframes skeleton-weave {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* STREAMLIT BUILT-IN SPINNER OVERRIDE (st.spinner) */
[data-testid="stSpinner"], .stSpinner {
    background-color: #E8DCC8 !important;
    border: 2px dashed #B5541E !important;
    border-radius: 6px !important;
    padding: 1.1rem 1.4rem !important;
    margin: 1.2rem 0 !important;
    box-shadow: 2px 3px 0 rgba(43,38,34,0.2) !important;
    position: relative !important;
}

/* Hide default circular SVG spinner ring */
[data-testid="stSpinner"] svg,
.stSpinner svg {
    display: none !important;
}

[data-testid="stSpinner"] > div {
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
}

/* Animated Spinning Yarn Spool before the text */
[data-testid="stSpinner"] > div::before {
    content: "🧵";
    font-size: 1.8rem;
    display: inline-block;
    animation: spool-spin 1.2s linear infinite;
    transform-origin: center center;
    flex-shrink: 0;
}

/* Animated Dashed Thread Line after the text */
[data-testid="stSpinner"] > div::after {
    content: "";
    display: inline-block;
    height: 4px;
    width: 50px;
    background: repeating-linear-gradient(
        90deg,
        #B5541E 0px,
        #B5541E 6px,
        transparent 6px,
        transparent 12px
    );
    background-size: 24px 4px;
    animation: thread-weave 0.5s linear infinite;
    border-radius: 2px;
    margin-left: 8px;
    flex-shrink: 0;
}

[data-testid="stSpinner"] p, 
[data-testid="stSpinner"] span {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #2E4057 !important;
    letter-spacing: 0.5px !important;
}

/* TOP HEADER SEWING THREAD RIBBON */
div[data-testid="stDecoration"] {
    background: repeating-linear-gradient(
        90deg,
        #B5541E 0px,
        #B5541E 8px,
        #2E4057 8px,
        #2E4057 16px,
        #E8DCC8 16px,
        #E8DCC8 22px
    ) !important;
    height: 4px !important;
}

/* HIDE STREAMLIT TOP-RIGHT STATUS WIDGET COMPLETELY */
[data-testid="stStatusWidget"],
.stStatusWidget,
header[data-testid="stHeader"] [data-testid="stStatusWidget"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

/* CUSTOM UIVERSE.IO FLYING FILE LOADER ANIMATION */
.loader-con {
  position: relative;
  width: 100%;
  max-width: 300px;
  height: 80px;
  overflow: hidden;
  margin: 0 auto;
}

.pfile {
  position: absolute;
  bottom: 15px;
  width: 36px;
  height: 46px;
  background: linear-gradient(90deg, #B5541E, #2E4057);
  border-radius: 4px;
  transform-origin: center;
  animation: flyRight 2.6s ease-in-out infinite;
  opacity: 0;
  box-shadow: 2px 2px 4px rgba(43,38,34,0.25);
}

.pfile::before {
  content: "";
  position: absolute;
  top: 6px;
  left: 6px;
  width: 24px;
  height: 4px;
  background-color: #ffffff;
  border-radius: 2px;
}

.pfile::after {
  content: "";
  position: absolute;
  top: 13px;
  left: 6px;
  width: 16px;
  height: 4px;
  background-color: #ffffff;
  border-radius: 2px;
}

@keyframes flyRight {
  0% {
    left: -10%;
    transform: scale(0);
    opacity: 0;
  }
  50% {
    left: 45%;
    transform: scale(1.15);
    opacity: 1;
  }
  100% {
    left: 100%;
    transform: scale(0);
    opacity: 0;
  }
}

.pfile {
  animation-delay: calc(var(--i) * 0.6s);
}



/* STREAMLIT INITIAL APP LOADING / SKELETON OVERRIDE */
[data-testid="stSkeleton"] {
    background: linear-gradient(90deg, #E8DCC8 25%, #F6F1E4 50%, #E8DCC8 75%) !important;
    background-size: 200% 100% !important;
    animation: skeleton-weave 1.5s infinite !important;
}

[data-testid="stAppLoading"] {
    background-color: #F6F1E4 !important;
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
        loader = st.empty()
        loader.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 1rem 0;">
                <div class="loader-con">
                    <div class="pfile" style="--i: 1;"></div>
                    <div class="pfile" style="--i: 2;"></div>
                    <div class="pfile" style="--i: 3;"></div>
                </div>
                <div style="font-family: 'IBM Plex Mono', monospace; font-size: 0.85rem; color: #2E4057; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.4rem;">
                    Analyzing yarn sample & compiling report...
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
        )
        loader.empty()
        with st.container(key="report_card"):
            st.markdown('<div class="report-heading">Inspection Findings</div>', unsafe_allow_html=True)
            st.write(interaction.output_text)
    except Exception as e:
        loader.empty()
        st.error(f"Something went wrong calling the AI: {e}")

