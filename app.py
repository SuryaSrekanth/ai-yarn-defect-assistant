import importlib
import os
import random

import pdf_generator
import streamlit as st
from dotenv import load_dotenv
from google import genai

importlib.reload(pdf_generator)
from pdf_generator import generate_pdf_report

load_dotenv()

st.set_page_config(page_title="Yarn Inspection Desk", page_icon="🧵", layout="centered")

if "batch_no" not in st.session_state:
    st.session_state.batch_no = f"{random.randint(10, 99)}-{random.randint(100, 999)}"

if "inspection_data" not in st.session_state:
    st.session_state.inspection_data = None

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
    transform: none !important;
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
.st-key-tag_card [data-testid="stNumberInput"],
.st-key-tag_card [data-testid="stSelectbox"] {
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-end !important;
}
.st-key-tag_card label {
    min-height: 2.2rem !important;
    display: flex !important;
    align-items: flex-end !important;
    margin-bottom: 0.35rem !important;
}
.st-key-tag_card label p {
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.75rem !important;
    color: #2E4057 !important;
    font-weight: 600 !important;
    line-height: 1.25 !important;
    margin: 0 !important;
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
.st-key-tag_card [data-baseweb="select"] > div {
    background-color: #F6F1E4 !important;
    border: 1px solid #2B2622 !important;
    border-radius: 3px !important;
}
.section-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #B5541E;
    margin-top: 1rem;
    margin-bottom: 0.35rem;
    border-bottom: 1px dashed rgba(181, 84, 30, 0.45);
    padding-bottom: 3px;
}

div[data-testid="stButton"] button {
    font-family: 'Special Elite', monospace;
    text-transform: uppercase;
    letter-spacing: 2px;
    background-color: #B5541E;
    color: #F6F1E4;
    border: 2px solid #2B2622;
    border-radius: 4px;
    padding: 0.55rem 1.4rem;
    box-shadow: 2px 3px 0 rgba(43,38,34,0.3);
    transform: none !important;
    white-space: nowrap !important;
    transition: background-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
}
@media (prefers-reduced-motion: no-preference) {
    div[data-testid="stButton"] button:hover {
        background-color: #9C4314;
        transform: translateY(-2px) !important;
        box-shadow: 2px 5px 0 rgba(43,38,34,0.35);
    }
    div[data-testid="stButton"] button:active {
        transform: translateY(1px) !important;
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
.lab-error-card {
    background-color: #FDF6E2;
    border: 2px solid #B5541E;
    border-left: 6px solid #B5541E;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-family: 'IBM Plex Sans', sans-serif;
    color: #2B2622;
}
.lab-error-card .error-title {
    font-family: 'Special Elite', monospace;
    font-size: 1rem;
    color: #B5541E;
    letter-spacing: 1px;
    margin-bottom: 0.3rem;
}
.lab-error-card .error-body {
    font-size: 0.88rem;
    line-height: 1.45;
    color: #4A3E3D;
}
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)


def stitch_divider():
    st.markdown('<div class="stitch-divider">' + " ✕" * 20 + "</div>", unsafe_allow_html=True)


def generate_rule_based_analysis(yarn_type: str, specs: dict, machinery: dict, defects: dict) -> str:
    causes = []
    notify = []
    next_checks = []

    if "Single" in yarn_type:
        count_val = specs.get("count_val", 0.0)
        count_unit = specs.get("count_unit", "Ne")

        thick = defects.get("thick_places", 0)
        thin = defects.get("thin_places", 0)
        neps = defects.get("neps", 0)
        total_defects = thick + thin + neps

        if thick > 35:
            causes.append(f"- **Elevated Thick Places (+50% = {thick}/km)**: Indicates damaged or grooved top roller drafting cots, worn/cracked drafting aprons, or loose lint/fly accumulating in the drafting zone and getting drafted into the yarn strand.")
        if thin > 25:
            causes.append(f"- **High Thin Places (-50% = {thin}/km)**: Indicates inappropriate ring traveler weight/size causing excessive spinning tension, spindle eccentricity, or irregular roving piecings.")
        if neps > 45:
            causes.append(f"- **Excessive Neps (+200% = {neps}/km)**: Points to worn carding wire clothing, improper flat-to-cylinder gauge settings, or high seed-coat / immature fiber content in the raw cotton mix.")
        if not causes:
            causes.append("- **Normal Defect Range**: All defect metrics are within standard commercial tolerances for this Ring Spun yarn count.")

        notify = [
            "- Ring Frame Spinning Shift Supervisor (Frame & Spindle inspection)",
            "- QA / Physical Testing Laboratory Manager",
            "- Carding & Preparatory Master (if Nep count is elevated)",
            "- Maintenance Engineer (Roller cot buffing & apron replacement cycle)",
        ]

        next_checks = [
            "1. Run a Spectrogram / Uster Mass Diagram to detect periodic drafting faults corresponding to top roller (7-8 cm wavelength) or apron (4-5 cm wavelength).",
            "2. Inspect Ring Travelers on running spindles for yarn groove wear, bluing from thermal friction, or fiber fly jamming.",
            "3. Inspect top roller cots for Shore hardness (standard 68-70 Shore A), cuts, gouges, or lubrication oil contamination.",
            "4. Verify roving count uniformity (CVm%) and spacer size in the ring frame drafting zone.",
        ]

        title = f"# QUALITY ASSESSMENT & TROUBLESHOOTING REPORT: {count_val} {count_unit} RING SPUN SINGLE YARN"

    elif "Double" in yarn_type or "Plied" in yarn_type:
        res_str = specs.get("resultant_str", "")
        single_count = specs.get("single_count", 40.0)
        plies = specs.get("plies", 2)
        count_unit = specs.get("count_unit", "Ne")

        thick = defects.get("thick_places", 0)
        thin = defects.get("thin_places", 0)
        snarls = defects.get("snarls", 0)
        total_defects = thick + thin + snarls

        if snarls > 8:
            causes.append(f"- **High Twist Liveliness / Snarling ({snarls}/km)**: Unbalanced ply twist combined with inadequate or uneven steam conditioning (YCP). Residual torsional torque causes spontaneous kinking during post-winding or weaving.")
        if thin > 10:
            causes.append(f"- **Thin Places / Dropped Single-Ply ({thin}/km)**: Single-end yarn breaks during doubling/assembly winding where the stop-motion detector failed to trip, resulting in dropped-ply sections in plied yarn.")
        if thick > 18:
            causes.append(f"- **Plied Slubs / Entrapped Tails ({thick}/km)**: Excessive pneumatic splicer tail length or loose fiber fly trapped inside the TFO spindle flyer or balloon pot.")
        if not causes:
            causes.append("- **Normal Defect Range**: Plied yarn metrics and twist parameters are well within standard industrial quality thresholds.")

        notify = [
            "- TFO Twisting Department In-Charge & Shift Supervisor",
            "- Assembly Doubling / Winding Supervisor (check dropped-ply detectors)",
            "- Autoclave Yarn Conditioning (YCP) Plant Operator",
            "- QA Physical Testing Laboratory Head",
        ]

        next_checks = [
            "1. Check Autoclave Steam Conditioning (YCP) recipe: ensure full vacuum (-0.85 bar) followed by saturated steam at 58-62°C for 35-45 minutes to set twist liveliness.",
            "2. Inspect assembly doubler stop-motion sensors and ceramic yarn cutters to prevent single-ply runouts from feeding into TFO.",
            "3. Test pneumatic air splicer joints on the pull-tester to ensure retained joint strength exceeds 85% with clean trimmed tails (<3mm).",
            "4. Inspect TFO spindle ceramic flyers, capsule tension discs, and balloon rings for grooving or lint buildup.",
        ]

        title = f"# QUALITY ASSESSMENT & TROUBLESHOOTING REPORT: {res_str} TFO PLIED YARN"

    else:  # Open-End Rotor
        count_val = specs.get("count_val", 20.0)
        count_unit = specs.get("count_unit", "Ne")

        thick = defects.get("thick_places", 0)
        thin = defects.get("thin_places", 0)
        neps = defects.get("neps", 0)
        trash = defects.get("trash_particles", 0)
        total_defects = thick + thin + neps + trash

        if trash > 20:
            causes.append(f"- **Rotor Groove Micro-Dust Encrustation ({trash} trash/dust units)**: Ineffective trash extraction at opening roller or high micro-dust in sliver. Dust builds up in the rotor V-groove, displacing fibers and generating recurring periodic defects.")
        if thick > 25:
            causes.append(f"- **Rotor Slubs / Thick Places (+50% = {thick}/km)**: Seed coat fragment deposition in rotor collecting groove shedding intermittently, or uneven sliver delivery from drawframe.")
        if thin > 18:
            causes.append(f"- **Thin Places (-50% = {thin}/km)**: Localized fiber starvation caused by opening roller wire loading or intermittent delivery roller slippage.")
        if neps > 40:
            causes.append(f"- **High Rotor Neps (+200% = {neps}/km)**: Opening roller speed is overly aggressive for the fiber staple length, causing fiber damage/curling rather than clean individualization.")
        if not causes:
            causes.append("- **Normal Defect Range**: Defect counts and rotor spinning metrics are within normal benchmark tolerances for OE yarn.")

        notify = [
            "- OE Rotor Spinning Section Shift Supervisor",
            "- Carding & Blowroom Department (Trash & dust extraction efficiency)",
            "- Spinning Maintenance Team (Rotor cup & navel cleaning / replacement team)",
            "- Quality Assurance Laboratory Manager",
        ]

        next_checks = [
            "1. Stop selected spin-box positions and inspect the rotor groove under a 10x illuminated magnifier for trash crusting; clean or replace rotor cups.",
            "2. Inspect ceramic navel for ceramic glaze wear, chipped inserts, or groove scoring.",
            "3. Verify opening roller wire tooth sharpness and check trash extraction chute pneumatic suction pressure (>700 Pa).",
            "4. Verify drawframe sliver evenness (U% and CVm%) and check feeding condenser alignment.",
        ]

        title = f"# QUALITY ASSESSMENT & TROUBLESHOOTING REPORT: {count_val} {count_unit} OPEN-END (ROTOR) YARN"

    return (
        f"{title}\n"
        f"**Summary**: Total defect index is **{total_defects}** per 1,000m. "
        f"({'High defect density detected requiring immediate machine inspection.' if total_defects > 70 else 'Defect profile is within standard operational tolerances.'})\n\n"
        f"## 1. POSSIBLE CAUSES & ROOT MECHANISMS\n" + "\n".join(causes) + "\n\n"
        f"## 2. WHO TO NOTIFY\n" + "\n".join(notify) + "\n\n"
        f"## 3. WHAT TO CHECK NEXT ON THE SHOP FLOOR\n" + "\n".join(next_checks)
    )


st.markdown(
    f"""
    <div class="yarn-header">
        <h1>🧵 Yarn Inspection Desk</h1>
        <div class="batch">BATCH NO. {st.session_state.batch_no} &middot; AI DEFECT ANALYSIS &middot; DEVELOPED BY SURYA SREKANTH</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(key="tag_card"):
    st.markdown("**Measurement Slip**")

    yarn_type_selected = st.selectbox(
        "Yarn Manufacturing Process",
        [
            "🧵 Single Yarn (Ring Spun / Combed / Carded)",
            "🪢 Double / Plied Yarn (TFO - Two-For-One Twisted)",
            "🌀 Open-End Yarn (OE / Rotor Spun)",
        ],
        index=0,
    )

    specs_data = {}
    machinery_data = {}
    defects_data = {}
    pdf_params = []
    main_count_val = 0.0
    main_count_unit = "Ne"
    main_thick = 0
    main_thin = 0
    main_neps = 0
    clean_yarn_type = ""

    if "Single" in yarn_type_selected:
        clean_yarn_type = "Single Yarn (Ring Spun)"
        st.markdown('<div class="section-tag">YARN SPECIFICATIONS</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            yarn_count_val = st.number_input("Yarn Count", min_value=1.0, max_value=200.0, value=30.0, step=1.0)
        with col2:
            count_unit_val = st.selectbox("Count System", ["Ne", "Tex", "Nm", "Denier"])

        st.markdown('<div class="section-tag">DEFECT MEASUREMENT (PER 1,000 METERS)</div>', unsafe_allow_html=True)
        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            thick_val = st.number_input("Thick Places (+50%)", min_value=0, value=25, step=1)
        with dc2:
            thin_val = st.number_input("Thin Places (-50%)", min_value=0, value=15, step=1)
        with dc3:
            neps_val = st.number_input("Neps (+200%)", min_value=0, value=40, step=1)

        main_count_val = float(yarn_count_val)
        main_count_unit = count_unit_val
        main_thick = thick_val
        main_thin = thin_val
        main_neps = neps_val

        specs_data = {"count_val": yarn_count_val, "count_unit": count_unit_val}
        machinery_data = {}
        defects_data = {"thick_places": thick_val, "thin_places": thin_val, "neps": neps_val}

        pdf_params = [
            ("Yarn Process", "Single Yarn (Ring Spun)", "Manufacturing Type"),
            ("Yarn Count", f"{yarn_count_val}", count_unit_val),
            ("Thick Places (+50%)", f"{thick_val}", "per 1,000 m"),
            ("Thin Places (-50%)", f"{thin_val}", "per 1,000 m"),
            ("Neps Count (+200%)", f"{neps_val}", "per 1,000 m"),
        ]

    elif "Double" in yarn_type_selected:
        clean_yarn_type = "Double / Plied Yarn (TFO)"
        st.markdown('<div class="section-tag">PLIED YARN SPECIFICATIONS</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            single_count_val = st.number_input("Single Yarn Count", min_value=1.0, max_value=200.0, value=40.0, step=1.0)
        with col2:
            plies_val = st.selectbox("Number of Plies", [2, 3, 4], format_func=lambda x: f"{x}-Ply (Folded)")
        with col3:
            count_unit_val = st.selectbox("Count System", ["Ne", "Tex", "Nm", "Denier"])

        if "Ne" in count_unit_val:
            res_str = f"{plies_val}/{int(single_count_val) if single_count_val.is_integer() else single_count_val} Ne (equiv. {single_count_val/plies_val:.1f} Ne)"
            calc_count = round(single_count_val / plies_val, 2)
        elif "Tex" in count_unit_val:
            res_str = f"{single_count_val * plies_val:.1f} Tex (from {single_count_val} Tex x {plies_val})"
            calc_count = round(single_count_val * plies_val, 2)
        else:
            res_str = f"{plies_val}/{single_count_val} {count_unit_val}"
            calc_count = round(single_count_val / plies_val, 2)

        st.caption(f"🧵 Resultant Plied Count: **{res_str}**")

        st.markdown('<div class="section-tag">DEFECT MEASUREMENT (PER 1,000 METERS)</div>', unsafe_allow_html=True)
        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            thick_val = st.number_input("Plied Thick (+50%)", min_value=0, value=16, step=1)
        with dc2:
            thin_val = st.number_input("Plied Thin (-50%)", min_value=0, value=6, step=1)
        with dc3:
            snarls_val = st.number_input("Snarls / Twist Faults", min_value=0, value=4, step=1)

        main_count_val = float(calc_count)
        main_count_unit = count_unit_val
        main_thick = thick_val
        main_thin = thin_val
        main_neps = snarls_val

        specs_data = {"single_count": single_count_val, "plies": plies_val, "count_unit": count_unit_val, "resultant_str": res_str, "calc_res_count": calc_count}
        machinery_data = {}
        defects_data = {"thick_places": thick_val, "thin_places": thin_val, "snarls": snarls_val}

        pdf_params = [
            ("Yarn Process", "Double / Plied Yarn (TFO)", "Manufacturing Type"),
            ("Resultant Plied Count", f"{res_str}", count_unit_val),
            ("Single Yarn Count", f"{single_count_val} ({plies_val}-ply)", count_unit_val),
            ("Plied Thick (+50%)", f"{thick_val}", "per 1,000 m"),
            ("Plied Thin (-50%)", f"{thin_val}", "per 1,000 m"),
            ("Snarls / Twist Faults", f"{snarls_val}", "per 1,000 m"),
        ]

    else:  # Open-End Rotor
        clean_yarn_type = "Open-End Yarn (OE / Rotor)"
        st.markdown('<div class="section-tag">OE ROTOR YARN SPECIFICATIONS</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            yarn_count_val = st.number_input("OE Yarn Count", min_value=4.0, max_value=80.0, value=20.0, step=1.0)
        with col2:
            count_unit_val = st.selectbox("Count System", ["Ne", "Tex", "Nm", "Denier"])

        st.markdown('<div class="section-tag">DEFECT MEASUREMENT (PER 1,000 METERS)</div>', unsafe_allow_html=True)
        dc1, dc2, dc3, dc4 = st.columns(4)
        with dc1:
            thick_val = st.number_input("Thick Places (+50%)", min_value=0, value=18, step=1)
        with dc2:
            thin_val = st.number_input("Thin Places (-50%)", min_value=0, value=10, step=1)
        with dc3:
            neps_val = st.number_input("Neps Count (+200%)", min_value=0, value=30, step=1)
        with dc4:
            trash_val = st.number_input("Trash / Dust Count", min_value=0, value=14, step=1)

        main_count_val = float(yarn_count_val)
        main_count_unit = count_unit_val
        main_thick = thick_val
        main_thin = thin_val
        main_neps = neps_val

        specs_data = {"count_val": yarn_count_val, "count_unit": count_unit_val}
        machinery_data = {}
        defects_data = {"thick_places": thick_val, "thin_places": thin_val, "neps": neps_val, "trash_particles": trash_val}

        pdf_params = [
            ("Yarn Process", "Open-End Yarn (OE / Rotor)", "Manufacturing Type"),
            ("OE Yarn Count", f"{yarn_count_val}", count_unit_val),
            ("Thick Places (+50%)", f"{thick_val}", "per 1,000 m"),
            ("Thin Places (-50%)", f"{thin_val}", "per 1,000 m"),
            ("Neps Count (+200%)", f"{neps_val}", "per 1,000 m"),
            ("Trash / Dust Particles", f"{trash_val}", "per 1,000 m"),
        ]

    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns([2.5, 1.2])
    with btn_col1:
        analyze = st.button("Analyze", use_container_width=True)
    with btn_col2:
        if st.button("🔄 New Batch", use_container_width=True):
            st.session_state.batch_no = f"{random.randint(10, 99)}-{random.randint(100, 999)}"
            st.session_state.inspection_data = None
            st.rerun()

stitch_divider()

if analyze:
    if main_count_val <= 0.0:
        st.markdown(
            """
            <div class="lab-error-card">
                <div class="error-title">⚠️ MEASUREMENT INPUT REQUIRED</div>
                <div class="error-body">Please enter a valid Yarn Count (e.g. 30.0 Ne) before running defect analysis.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        if "Single" in yarn_type_selected:
            prompt = (
                "You are a textile spinning quality control expert and laboratory technologist reviewing a Ring Spun yarn inspection slip.\n"
                f"Yarn Process: Single Yarn (Ring Spun / Combed / Carded)\n"
                f"Yarn Count: {specs_data['count_val']} {specs_data['count_unit']}\n"
                f"Thick Places (+50%): {defects_data['thick_places']} per 1,000m\n"
                f"Thin Places (-50%): {defects_data['thin_places']} per 1,000m\n"
                f"Neps (+200%): {defects_data['neps']} per 1,000m\n\n"
                "Diagnostic Focus Mandate:\n"
                "- Ring traveler wear, frictional thermal bluing, traveler weight calibration for count\n"
                "- Top roller cot cuts/gouges, apron cracking, drafting cradle tension\n"
                "- Roving piecing slubs, roving count CV%, and drafting zone fly accumulation\n\n"
                "Provide a concise, practical troubleshooting report for a spinning mill technician:\n"
                "1. Quality evaluation (explain if these levels are normal/high for this count)\n"
                "2. Root causes specific to ring spinning machinery and preparatory sliver\n"
                "3. Who to notify (specific roles/sections)\n"
                "4. Immediate maintenance & check steps on the shop floor\n\n"
                "Formatting Guideline: If you include any schematic or flow diagram, enclose it inside a standard markdown code block (``` ... ```) using simple ASCII characters (+, -, |, -->) and keep line widths under 55 characters so it formats crisply in PDF laboratory reports."
            )
        elif "Double" in yarn_type_selected:
            prompt = (
                "You are a textile twisting quality control expert and laboratory technologist reviewing a TFO (Two-For-One) plied yarn inspection slip.\n"
                f"Yarn Process: Double / Plied Yarn (TFO Folded)\n"
                f"Resultant Plied Count: {specs_data['resultant_str']}\n"
                f"Single Count: {specs_data['single_count']} {specs_data['count_unit']} ({specs_data['plies']}-ply)\n"
                f"Plied Thick Places / Slubs: {defects_data['thick_places']} per 1,000m\n"
                f"Thin Places / Dropped Ends: {defects_data['thin_places']} per 1,000m\n"
                f"Snarls / Twist Faults: {defects_data['snarls']} per 1,000m\n\n"
                "Diagnostic Focus Mandate:\n"
                "- Single end breaks (dropped-ply defects) in assembly winding\n"
                "- Twist liveliness, snarling, torque balance, and autoclave steam conditioning cycle (YCP)\n"
                "- Air splicer tail length, splice retention strength, and joint knotting\n"
                "- TFO tension capsule friction, ceramic flyer wear, and balloon stability\n\n"
                "Provide a concise, practical troubleshooting report for a twisting mill technician:\n"
                "1. Quality evaluation (torque balance, plied defects)\n"
                "2. Root causes specific to TFO twisting, assembly winding, and conditioning\n"
                "3. Who to notify (specific roles/sections)\n"
                "4. Immediate corrective checks on the twisting floor\n\n"
                "Formatting Guideline: If you include any schematic or flow diagram, enclose it inside a standard markdown code block (``` ... ```) using simple ASCII characters (+, -, |, -->) and keep line widths under 55 characters so it formats crisply in PDF laboratory reports."
            )
        else:
            prompt = (
                "You are a textile rotor spinning quality control expert and laboratory technologist reviewing an Open-End (OE) yarn inspection slip.\n"
                f"Yarn Process: Open-End Yarn (OE / Rotor Spun)\n"
                f"Yarn Count: {specs_data['count_val']} {specs_data['count_unit']}\n"
                f"Thick Places (+50%): {defects_data['thick_places']} per 1,000m\n"
                f"Thin Places (-50%): {defects_data['thin_places']} per 1,000m\n"
                f"Neps (+200%): {defects_data['neps']} per 1,000m\n"
                f"Trash / Dust Particles: {defects_data['trash_particles']} per 1,000m\n\n"
                "Diagnostic Focus Mandate:\n"
                "- Rotor V-groove micro-dust and trash buildup leading to recurring slubs\n"
                "- Wrapper fibers and corkscrew defects caused by navel wear or incorrect groove geometry\n"
                "- Opening roller wire wear or excessive combing speed causing fiber damage/neps\n"
                "- Trash extraction suction pressure and sliver preparation quality\n\n"
                "Provide a concise, practical troubleshooting report for an OE spinning technician:\n"
                "1. Quality evaluation (rotor yarn structure, dust influence)\n"
                "2. Root causes specific to rotor spin-box, navel, opening roller, and sliver\n"
                "3. Who to notify (specific roles/sections)\n"
                "4. Immediate maintenance & check steps on the rotor floor\n\n"
                "Formatting Guideline: If you include any schematic or flow diagram, enclose it inside a standard markdown code block (``` ... ```) using simple ASCII characters (+, -, |, -->) and keep line widths under 55 characters so it formats crisply in PDF laboratory reports."
            )

        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
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

        ai_success = False
        output_text = ""
        if api_key:
            try:
                client = genai.Client(api_key=api_key)
                interaction = client.interactions.create(
                    model="gemini-3.6-flash",
                    input=prompt,
                )
                output_text = interaction.output_text
                ai_success = True
            except Exception:
                ai_success = False

        loader.empty()

        if not ai_success:
            st.markdown(
                """
                <div class="lab-error-card">
                    <div class="error-title">⚠️ QUALITY DIAGNOSTIC ENGINE NOTICE</div>
                    <div class="error-body">The online AI analysis engine is currently undergoing maintenance or network configuration. An offline rule-based report has been generated below so you can proceed with quality analysis and PDF export.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            output_text = generate_rule_based_analysis(clean_yarn_type, specs_data, machinery_data, defects_data)

        st.session_state.inspection_data = {
            "batch_no": st.session_state.batch_no,
            "yarn_type": clean_yarn_type,
            "parameters": pdf_params,
            "yarn_count": main_count_val,
            "count_unit": main_count_unit,
            "thick_places": main_thick,
            "thin_places": main_thin,
            "neps": main_neps,
            "output_text": output_text,
        }

if st.session_state.inspection_data:
    data = st.session_state.inspection_data
    with st.container(key="report_card"):
        st.markdown('<div class="report-heading">Inspection Findings</div>', unsafe_allow_html=True)
        st.write(data["output_text"])

    try:
        importlib.reload(pdf_generator)
        pdf_bytes = pdf_generator.generate_pdf_report(
            batch_no=data["batch_no"],
            yarn_type=data.get("yarn_type", "Single Yarn (Ring Spun)"),
            parameters=data.get("parameters", []),
            ai_report_text=data["output_text"],
            yarn_count=data.get("yarn_count", 0.0),
            count_unit=data.get("count_unit", "Ne"),
            thick_places=data.get("thick_places", 0),
            thin_places=data.get("thin_places", 0),
            neps=data.get("neps", 0),
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Download PDF Inspection Report",
            data=pdf_bytes,
            file_name=f"yarn_inspection_batch_{data['batch_no']}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception:
        st.markdown(
            """
            <div class="lab-error-card">
                <div class="error-title">⚠️ PDF EXPORT NOTICE</div>
                <div class="error-body">Unable to compile PDF document at this moment. Please click 'Analyze' or '🔄 New Batch' again.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br><hr style='border: 1px dashed #2B2622; opacity: 0.35;'><div style='text-align: center; font-family: \"IBM Plex Mono\", monospace; font-size: 0.8rem; color: #2E4057; font-weight: 500;'>Developed by <strong>Surya Srekanth</strong> &middot; AI Yarn Defect Assistant</div>", unsafe_allow_html=True)


