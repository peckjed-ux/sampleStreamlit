"""
================================================================================
STREAMLIT DEEP DIVE: STANDALONE REFERENCE & DEMO APP (exampleApp.py)
================================================================================
This script covers every concept, component, and architectural pattern
presented across all slides of the "Streamlit Deep Dive" presentation (Slides 1-16).

Each section includes explicit inline code comments detailing the "WHY"
and referencing the specific slide from the deck.
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# =============================================================================
# SLIDE 1 & SLIDE 12: PAGE CONFIGURATION & TITLE
# WHY (Slide 1 & 12): st.set_page_config sets app metadata, browser icons, and layout width.
# It MUST be the very first Streamlit command executed in the script.
# =============================================================================
st.set_page_config(
    page_title="Streamlit Deep Dive Reference App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SLIDE 1 & 3: TITLE & OVERVIEW
# WHY (Slide 1 & 3): st.title and st.markdown establish the application title and introductory text
# explaining Streamlit as a pure-Python library to build web apps without HTML/CSS/JS experience.
st.title("🚀 Streamlit Deep Dive Reference App")
st.markdown("""
Welcome to **exampleApp.py**! This comprehensive app covers **all concepts and slides** from the 
**Streamlit Deep Dive** deck, ranging from core philosophy (Slides 3–6) to display components, 
widgets, charts, layout, caching, and state management.
""")

st.divider()


# =============================================================================
# SLIDE 14: PERFORMANCE CACHING DECORATORS (@st.cache_data & @st.cache_resource)
# WHY (Slide 14): Because Streamlit reruns the script top-to-bottom on every user interaction (Slide 6),
# heavy data loading or model initialization would cause lag. @st.cache_data caches data OUTPUT,
# while @st.cache_resource caches persistent RESOURCE objects (models, DB connections).
# =============================================================================

@st.cache_data(show_spinner="Loading demo dataset...")
def load_expensive_data():
    """
    WHY (Slide 14): @st.cache_data prevents re-executing heavy data loads or SQL queries
    on every widget interaction. Streamlit checks input parameters and returns cached results instantly.
    """
    time.sleep(1)  # Simulate expensive database query or computation
    np.random.seed(42)
    dates = pd.date_range("2026-01-01", periods=30)
    df = pd.DataFrame({
        "Date": dates,
        "Active_Users": np.random.randint(100, 500, size=30),
        "Revenue_USD": np.random.normal(5000, 1000, size=30).round(2),
        "Conversion_Rate": np.random.uniform(0.02, 0.08, size=30).round(4),
        "Region": np.random.choice(["North", "South", "East", "West"], size=30)
    })
    return df


@st.cache_resource
def get_model_resource():
    """
    WHY (Slide 14): @st.cache_resource ensures one-time initialization for unpicklable
    or stateful resources like machine learning models or database connections.
    """

    class MockMLModel:
        def predict(self, val):
            return round(val * 1.42, 2)

    return MockMLModel()


df_data = load_expensive_data()
ml_model = get_model_resource()

# =============================================================================
# SLIDE 15: STATE MANAGEMENT (st.session_state)
# WHY (Slide 15): Streamlit's rerun model (Slide 6) is stateless by default.
# st.session_state is a persistent dictionary-like object used to remember variables
# (e.g., login status, step results, counters) across reruns.
# =============================================================================
if "app_interactions" not in st.session_state:
    st.session_state.app_interactions = 0

if "submitted_user_notes" not in st.session_state:
    st.session_state.submitted_user_notes = []

# =============================================================================
# SLIDE 12: APP LAYOUT - SIDEBAR (st.sidebar)
# WHY (Slide 12): st.sidebar places controls, navigation, and filters into a collapsible sidebar,
# keeping the main content workspace clean and organized.
# =============================================================================
with st.sidebar:
    st.header("⚙️ App Navigation & Controls")

    region_filter = st.selectbox(
        "Filter Data by Region (Slide 9 & 12):",
        options=["All"] + list(df_data["Region"].unique()),
        index=0
    )

    if st.button("🔄 Increment Global Counter (Slide 9 & 15)"):
        st.session_state.app_interactions += 1
        st.success(f"Counter updated: {st.session_state.app_interactions}")

    st.write(f"**Total Session Interactions:** `{st.session_state.app_interactions}`")
    st.divider()

    st.info(
        "**Core Architecture:**\n"
        "- Script-as-App (Slide 6)\n"
        "- Top-to-Bottom Rerun (Slide 6)\n"
        "- No Callbacks Required (Slide 6)"
    )

if region_filter != "All":
    filtered_df = df_data[df_data["Region"] == region_filter]
else:
    filtered_df = df_data.copy()

# =============================================================================
# SLIDE 12: APP LAYOUT - TABS (st.tabs)
# WHY (Slide 12): st.tabs organizes multi-topic apps into clean horizontal tabs,
# preventing long vertical scrolling.
# =============================================================================
tab_philosophy, tab_overview, tab_widgets, tab_charts, tab_advanced = st.tabs([
    "💡 Core Philosophy (Slides 3-6)",
    "📊 Data & Metrics (Slide 8)",
    "🎛️ Interactive Widgets (Slides 9-10)",
    "📈 Charts & Media (Slide 11)",
    "⚡ State & Forms (Slides 14-16)"
])

# =============================================================================
# TAB 1: CORE PHILOSOPHY & ARCHITECTURE (SLIDES 3, 4, 5, 6)
# =============================================================================
with tab_philosophy:
    st.header("Slides 3–6: The Problem, The Solution & Core Philosophy")

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.subheader("Slide 3: What is Streamlit?")
        st.markdown("""
        * **WHY (Slide 3):** Turns standard data scripts into web apps in minutes without front-end (HTML/CSS/JS) experience.
        * **WHY (Slide 3):** Embraces simple, pure-Python scripting.
        * **WHY (Slide 3):** Ideal for rapid prototyping of interactive tools and dashboards.
        """)

        st.subheader("Slide 5: The Problem & Solution")
        st.markdown("""
        * **The Old Way (High Friction - Slide 5):** Analysis or ML models get trapped in Jupyter Notebooks or static scripts. Sharing requires static CSV/PPT reports or costly front-end teams (Flask/Django).
        * **The Streamlit Way (Low Friction - Slide 5):** Write a simple Python script rendered as a modern web app with instant interactivity.
        """)

    with col_p2:
        st.subheader("Slide 6: The Core Philosophy (How it Works)")
        st.markdown("""
        1. **Script-as-App (Slide 6):** 
           * *WHY:* Your Python script *is* the application. There is no separate front-end code; Streamlit renders elements sequentially as it encounters them.
        2. **Top-to-Bottom Rerun (Slide 6):** 
           * *WHY:* Every time a user interacts with a widget, the *entire script re-runs* from top to bottom. This simple execution model eliminates complex architectural state synchronization.
        3. **No Callbacks (Slide 6):** 
           * *WHY:* State is managed automatically. You don't need to write complex asynchronous callback event handlers; code flows in a linear, readable path.
        """)

        st.info(
            "💡 **Interactive Proof:** Try interacting with any widget in other tabs. Notice how the app instantly reruns from top to bottom to reflect your changes!")

# =============================================================================
# TAB 2: DATA DISPLAY & METRICS (SLIDE 8)
# =============================================================================
with tab_overview:
    st.header("Slide 8: Displaying Data & Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    total_rev = filtered_df["Revenue_USD"].sum()
    avg_users = int(filtered_df["Active_Users"].mean())
    avg_conv = filtered_df["Conversion_Rate"].mean() * 100

    # SLIDE 8: st.metric
    # WHY (Slide 8): st.metric displays Key Performance Indicators (KPIs) with an optional delta indicator.
    col1.metric(label="Total Revenue", value=f"${total_rev:,.2f}", delta="+12.4%")
    col2.metric(label="Avg Active Users", value=f"{avg_users:,}", delta="-3.1%")
    col3.metric(label="Avg Conv. Rate", value=f"{avg_conv:.2f}%", delta="+0.4%")
    col4.metric(label="Filtered Records", value=len(filtered_df))

    st.divider()

    st.subheader("Interactive Data Table (`st.dataframe` - Slide 8)")
    # SLIDE 8: st.dataframe
    # WHY (Slide 8): st.dataframe renders a Pandas DataFrame as an interactive table allowing
    # users to sort, column-resize, and scroll browser-side.
    st.dataframe(filtered_df, width="stretch")

    # SLIDE 8: st.write & st.markdown
    # WHY (Slide 8): st.write is the magic command that intelligently inspects any data type and renders it.
    with st.expander("🔍 View Raw Summary Stats using `st.write` (Slide 8 & 12)"):
        st.write("`st.write` automatically formatting a dictionary descriptor:", filtered_df.describe().to_dict())

# =============================================================================
# TAB 3: INTERACTIVE WIDGETS (SLIDES 9 & 10)
# =============================================================================
with tab_widgets:
    st.header("Slides 9 & 10: Building Blocks - Interactive Input Widgets")

    col_w1, col_w2 = st.columns(2)

    with col_w1:
        st.subheader("Slide 9 Widgets")

        # SLIDE 9: st.button
        # WHY (Slide 9): Simplest widget. Returns True only on the exact rerun turn when clicked.
        if st.button("Click Me to Trigger Event (Slide 9)"):
            st.session_state.app_interactions += 1
            st.balloons()
            st.success("Button clicked! Interaction logged.")

        # SLIDE 9: st.checkbox
        # WHY (Slide 9): Simple boolean toggle (True/False) useful for show/hide options.
        show_raw = st.checkbox("Show Raw Data Sample (Slide 9)", value=False)
        if show_raw:
            st.write(filtered_df.head(3))

        # SLIDE 9: st.selectbox
        # WHY (Slide 9): Dropdown list letting users pick one option from a collection.
        chosen_metric = st.selectbox(
            "Select Metric to Analyze (Slide 9):",
            options=["Active_Users", "Revenue_USD", "Conversion_Rate"]
        )
        st.info(f"Currently inspecting metric: **{chosen_metric}**")

    with col_w2:
        st.subheader("Slide 10 Widgets")

        # SLIDE 10: st.slider
        # WHY (Slide 10): Select numerical values from a range. Perfect for tuning model parameters or thresholds.
        slider_val = st.slider("Select Model Threshold (Slide 10):", min_value=0.0, max_value=100.0, value=50.0,
                               step=5.0)
        st.caption(f"Model prediction at threshold {slider_val}: `{ml_model.predict(slider_val)}`")

        # SLIDE 10: st.text_input
        # WHY (Slide 10): Captures a single line of text from the user (search box or label).
        user_query = st.text_input("Search / Filter Query (Slide 10):", placeholder="Type keywords here...")
        if user_query:
            st.write(f"Filter string captured: `{user_query}`")

        # SLIDE 10: st.file_uploader
        # WHY (Slide 10): Allows users to upload external files (CSV, image, etc.) for processing.
        uploaded_file = st.file_uploader("Upload External CSV File (Slide 10):", type=["csv"])
        if uploaded_file is not None:
            uploaded_df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(uploaded_df.head(2), width="stretch")

# =============================================================================
# TAB 4: CHARTS & MEDIA (SLIDE 11)
# =============================================================================
with tab_charts:
    st.header("Slide 11: Charts & Native Visualization Integration")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.subheader("1. Native Streamlit Line Chart (`st.line_chart` - Slide 11)")
        # SLIDE 11: st.line_chart
        # WHY (Slide 11): Native chart function providing rapid, zero-config interactive line plots.
        chart_data = filtered_df.set_index("Date")[["Active_Users", "Revenue_USD"]]
        st.line_chart(chart_data)

    with col_c2:
        st.subheader("2. Matplotlib Library Integration (`st.pyplot` - Slide 11)")
        # SLIDE 11: st.pyplot
        # WHY (Slide 11): Integrates existing Matplotlib / Seaborn figures into the Streamlit app layout.
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.hist(filtered_df["Revenue_USD"], bins=10, color="#4C72B0", edgecolor="black")
        ax.set_title("Revenue Distribution", fontsize=10)
        ax.set_xlabel("USD")
        ax.set_ylabel("Frequency")
        plt.tight_layout()
        st.pyplot(fig)

    st.divider()
    st.subheader("Media Elements (Slide 11)")
    st.caption(
        "WHY (Slide 11): `st.image()`, `st.audio()`, and `st.video()` work out-of-the-box for multimedia rendering.")

# =============================================================================
# TAB 5: STATE MANAGEMENT, FORMS & CACHING (SLIDES 14, 15 & 16)
# =============================================================================
with tab_advanced:
    st.header("Slides 14–16: Advanced Concepts (State, Caching & Forms)")

    col_adv1, col_adv2 = st.columns(2)

    with col_adv1:
        st.subheader("Slide 15: State Persistence (`st.session_state`)")
        st.markdown("""
        * **WHY (Slide 15):** Streamlit's rerun model is stateless. `st.session_state` preserves variables across reruns.
        * **Use Cases:** Tracking login status, passing results between steps, or initializing state (`if 'key' not in st.session_state:`).
        """)

        note_input = st.text_input("Enter a note to save into session state:")
        if st.button("Add Note to Session State"):
            if note_input.strip():
                st.session_state.submitted_user_notes.append(note_input.strip())
                st.session_state.app_interactions += 1
                st.success("Note saved!")

        st.write("**Stored Session Notes:**", st.session_state.submitted_user_notes)

    with col_adv2:
        st.subheader("Slide 16: Input Batching (`st.form`)")
        st.markdown("""
        * **WHY (Slide 16):** By default, every widget interaction triggers an immediate full script rerun. 
        * **Why `st.form`:** Batches multiple input widgets together so the app only reruns *once* when the user clicks `st.form_submit_button`. Essential for settings panels and data entry.
        """)

        # SLIDE 16: st.form & st.form_submit_button
        with st.form(key="user_profile_form"):
            st.write("#### Batch Settings Form")
            form_name = st.text_input("User Full Name")
            form_role = st.selectbox("Role", ["Data Scientist", "ML Engineer", "Business Analyst"])
            form_rate = st.slider("Target Learning Rate", 0.001, 0.100, 0.010, step=0.005)

            form_submitted = st.form_submit_button("Submit Form Batch")

        if form_submitted:
            st.session_state.app_interactions += 1
            st.success(f"Form submitted for **{form_name}** ({form_role}) with rate `{form_rate}`!")

# =============================================================================
# FOOTER & SUMMARY RECAP
# =============================================================================
st.divider()
st.caption("Streamlit Deep Dive • Complete Presentation Coverage (Slides 1–16) • exampleApp.py")