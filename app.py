"""
================================================================================
STREAMLIT MASTERCLASS & GEMINI PLAYGROUND APP
================================================================================
This script is designed for students to learn core Streamlit concepts:
1. Page configuration and layouts.
2. Sidebar controls and Session State (retaining variables across reruns).
3. Tab navigation for splitting complex apps into logical sections.
4. Computer vision integration (Barcodes/QR scanning via pyzbar & PIL).
5. Generative AI integration using the official Google GenAI SDK with custom model selection.
6. Dataframes, interactive widgets, metrics, and data visualizations.
"""

import io
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import Google GenAI SDK for the Gemini API tab
try:
    from google import genai
    from google.genai import types
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    GEMINI_SDK_AVAILABLE = False

# Import pyzbar for scanning barcodes/QR codes from uploaded images
try:
    from pyzbar.pyzbar import decode as scan_barcode
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False


# =============================================================================
# 1. PAGE CONFIGURATION
# =============================================================================
# st.set_page_config() MUST be the very first Streamlit command in your script.
# It sets browser tab metadata, layout style ("wide" or "centered"), and sidebar state.
st.set_page_config(
    page_title="Streamlit Masterclass & Gemini Playground",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =============================================================================
# 2. SIDEBAR & SESSION STATE MANAGEMENT
# =============================================================================
# Streamlit reruns the entire Python script from top to bottom every time a user
# interacts with any widget. To remember values (like a click counter) across reruns,
# we use st.session_state (a dictionary-like object persistent across user interactions).
if "click_count" not in st.session_state:
    st.session_state.click_count = 0

# st.sidebar lets you place widgets in a dedicated sidebar column on the left.
with st.sidebar:
    st.header("⚙️ App Controls")

    # Simple text input widget that returns the typed string immediately
    user_name = st.text_input("Enter your name", value="Explorer")

    # Button widget returns True only on the exact click event
    if st.button("Increment Counter"):
        st.session_state.click_count += 1

    st.write(f"Button clicks saved in session: **{st.session_state.click_count}**")

    st.divider()
    st.caption("Built for students learning Python & Streamlit")


# =============================================================================
# 3. MAIN APPLICATION HEADER
# =============================================================================
# Dynamic Markdown strings allow embedding Python variables directly into UI text.
st.title(f"Welcome, {user_name}! 👋")
st.markdown("""
This application demonstrates core Streamlit features:
* **Computer Vision:** Scan barcodes/QR codes from uploaded images.
* **GenAI API:** Talk to Gemini with strict system instruction constraints & selectable models.
* **Interactive Widgets & Data:** Control widgets, render live DataFrames, and plot charts.
""")


# =============================================================================
# 4. TAB NAVIGATION
# =============================================================================
# st.tabs() organizes content into clean, clickable horizontal tabs, preventing
# long vertical scrolls and grouping related features together.
tab_barcode, tab_ai, tab_widgets, tab_data, tab_layout = st.tabs([
    "📷 Barcode Scanner",
    "🤖 Gemini Playground",
    "🎛️ Input Widgets",
    "📊 Data & Charts",
    "📐 Layouts & Status"
])

# =============================================================================
# TAB 1: BARCODE SCANNER + GEMINI VISION PRODUCT IDENTIFIER
# =============================================================================
with tab_barcode:
    st.header("📷 Barcode Scanner & Gemini Vision Lookup")
    st.write(
        "Upload an image containing a barcode. If external lookup fails, Gemini Vision will identify the product from the image.")

    uploaded_image = st.file_uploader(
        "Upload image with barcode",
        type=["png", "jpg", "jpeg", "webp"],
        key="barcode_uploader"
    )

    if uploaded_image is not None:
        col_img, col_res = st.columns([1, 1])

        with col_img:
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_image)
            st.image(image, width="stretch", caption="Source Image Preview")

        with col_res:
            st.subheader("Scan & Identification Results")
            if PYZBAR_AVAILABLE:
                with st.spinner("Scanning pixels for barcodes..."):
                    decoded_objects = scan_barcode(image)

                raw_payload = "No Barcode Detected"
                barcode_type = "N/A"

                if decoded_objects:
                    raw_payload = decoded_objects[0].data.decode("utf-8")
                    barcode_type = decoded_objects[0].type
                    st.success(f"Successfully decoded barcode: `{raw_payload}` ({barcode_type})")
                else:
                    st.warning("No standard barcode detected by pyzbar. Falling back to Gemini Vision identification.")

                # --- GEMINI VISION PRODUCT IDENTIFICATION ---
                with st.spinner("Identifying product using Gemini Vision..."):
                    product_name = "Unknown Product"
                    brand_name = "Unknown Brand"
                    description = "Could not identify product."

                    try:
                        api_key = os.getenv("GEMINI_API_KEY")
                        client = genai.Client(api_key=api_key) if api_key else genai.Client()

                        prompt = (
                            f"Analyze this image containing a barcode (decoded value: {raw_payload}). "
                            "Identify the exact product name, brand, and a short 1-sentence description. "
                            "Format your response strictly as: Brand | Product Name | Description"
                        )

                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=[image, prompt]
                        )

                        parts = response.text.split("|")
                        if len(parts) >= 3:
                            brand_name = parts[0].strip()
                            product_name = parts[1].strip()
                            description = parts[2].strip()
                        else:
                            product_name = response.text.strip()

                    except Exception as e:
                        product_name = f"Vision Error: {e}"

                # Display Results Card
                with st.expander(f"📦 Identified Product: {product_name}", expanded=True):
                    st.markdown(f"### **{product_name}**")
                    st.write(f"**Brand:** {brand_name}")
                    st.write(f"**Details:** {description}")
                    st.write(f"**Barcode Value:** `{raw_payload}`")

                # Summary Table
                st.subheader("Summary Table")
                st.dataframe(pd.DataFrame([{
                    "Product Name": product_name,
                    "Brand": brand_name,
                    "Barcode Type": barcode_type,
                    "Raw Code": raw_payload
                }]), width="stretch")

# =============================================================================
# TAB 2: GEMINI API PLAYGROUND (WITH DYNAMIC MODEL SELECTION)
# =============================================================================
with tab_ai:
    st.header("🤖 Gemini API Playground with Constraints & Model Selection")
    st.markdown("""
    This tab shows how to integrate the Google GenAI SDK into Streamlit. 
    Select your desired **Gemini model** from the dropdown below and submit your prompt.
    """)

    if not GEMINI_SDK_AVAILABLE:
        st.error(
            "⚠️ **google-genai package is not installed.**\n\n"
            "Run `pip install google-genai` and make sure your `GEMINI_API_KEY` is set in `.env`."
        )

    # Display the active behavioral prompt constraint inside an expander
    with st.expander("🔍 Inspect Active System Constraints"):
        st.code(
            """System Instruction Constraint Passed to Gemini:
"You are a sarcastic, hyper-critical Senior Software Architect. 
Your tone must be dry and witty. Every response must include a subtle software engineering joke, 
and you must conclude with a mandatory warning about technical debt or legacy code." """,
            language="text"
        )

    # Model selector dropdown widget allows students to pick different Gemini model endpoints
    selected_model = st.selectbox(
        "Choose Gemini Model:",
        options=[
            "gemini-3.8-flash"
        ],
        index=0,
        help="Select which Gemini model to handle your prompt."
    )

    # st.form groups inputs together so the page doesn't rerun on every keystroke.
    # Execution happens only when the user explicitly clicks the form submit button.
    with st.form("gemini_form"):
        user_prompt = st.text_area(
            "Ask Gemini an architectural question:",
            placeholder="e.g., Should I rewrite my legacy monolith app in a trendy new framework?"
        )
        submitted = st.form_submit_button("Generate Response")

    if submitted:
        if not user_prompt.strip():
            st.warning("Please type a question before submitting.")
        elif not GEMINI_SDK_AVAILABLE:
            st.error("Cannot query Gemini because the `google-genai` package is missing.")
        else:
            try:
                with st.spinner(f"Querying model '{selected_model}'..."):
                    # Initialize the Gemini client (reads GEMINI_API_KEY loaded via python-dotenv)
                    api_key = os.getenv("GEMINI_API_KEY")
                    if api_key:
                        client = genai.Client(api_key=api_key)
                    else:
                        client = genai.Client()

                    # Define strict persona constraint instructions
                    system_constraint = (
                        "You are a sarcastic, hyper-critical Senior Software Architect. "
                        "Your tone must be dry and witty. Every response must include a subtle software engineering joke, "
                        "and you must conclude with a mandatory warning about technical debt or legacy code."
                    )

                    # Call Gemini model chosen dynamically from the st.selectbox dropdown
                    response = client.models.generate_content(
                        model=selected_model,
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_constraint,
                            temperature=0.7,
                        )
                    )

                st.subheader(f"Architect's Verdict ({selected_model}):")
                st.write(response.text)

            except Exception as e:
                st.error(f"API Error ({selected_model}): {e}")
                st.info("Tip: If a specific model encounters temporary traffic spikes (503 error), try selecting a different model from the dropdown above.")


# =============================================================================
# TAB 3: INPUT WIDGETS
# =============================================================================
with tab_widgets:
    st.header("Interactive Widgets Showcase")
    st.write("Streamlit provides instant Python variables out of UI widgets without writing HTML/JS.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Text & Number Inputs")
        text_val = st.text_input("Text Input", placeholder="Type something...")
        num_val = st.number_input("Number Input", min_value=0, max_value=100, value=25)
        slider_val = st.slider("Slider Widget", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
        color_val = st.color_picker("Color Picker", "#00f900")

    with col2:
        st.subheader("Selection Widgets")
        choice = st.selectbox("Selectbox Dropdown", ["Option A", "Option B", "Option C"])
        multi_choice = st.multiselect("Multiselect List", ["Python", "Rust", "Go", "TypeScript"], default=["Python"])
        radio_choice = st.radio("Radio Buttons", ["Low", "Medium", "High"], horizontal=True)
        toggle_val = st.toggle("Toggle Switch")

    st.divider()
    st.subheader("Live State Payload (JSON)")
    # st.json renders a clean, interactive JSON viewer for python dictionaries
    st.json({
        "text": text_val,
        "number": num_val,
        "slider": slider_val,
        "color": color_val,
        "single_select": choice,
        "multi_select": multi_choice,
        "priority": radio_choice,
        "toggle": toggle_val
    })


# =============================================================================
# TAB 4: DATA & CHARTS
# =============================================================================
with tab_data:
    st.header("DataFrames, Metrics & Charting")

    # st.metric creates modern key-performance indicator cards with delta indicators
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Revenue", value="$45,200", delta="12%")
    m2.metric(label="Latency", value="120 ms", delta="-15 ms")
    m3.metric(label="Active Users", value="1,240", delta="0")

    st.divider()

    # Generate a random dataset using NumPy and Pandas
    np.random.seed(42)
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["Metric A", "Metric B", "Metric C"]
    )

    st.subheader("1. Interactive Table (Pandas DataFrame)")
    # st.dataframe provides sorting, column resizing, and searching out of the box
    st.dataframe(chart_data, width="stretch")

    st.subheader("2. Built-in Streamlit Line Chart")
    st.line_chart(chart_data)

    st.subheader("3. Native Matplotlib Integration")
    # Streamlit renders standard Matplotlib figures seamlessly via st.pyplot()
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.hist(chart_data["Metric A"], bins=10, color="skyblue", edgecolor="black")
    ax.set_title("Distribution of Metric A")
    st.pyplot(fig)


# =============================================================================
# TAB 5: LAYOUTS & STATUS MESSAGES
# =============================================================================
with tab_layout:
    st.header("Layout Control & Feedback Elements")

    # Expandable block for hiding long text instructions
    with st.expander("Click to view hidden instructions"):
        st.write("This block hides verbose text until the user expands it.")

    # Status alerts for user feedback
    st.subheader("Alert Banners")
    st.success("Success: Action completed successfully!")
    st.info("Info: Here is a helpful tip for students.")
    st.warning("Warning: Proceed with caution.")
    st.error("Error: An unexpected issue occurred.")

    # File download helper button
    st.subheader("File Download Button")
    sample_text = "Hello student! This file was dynamically generated in memory by Streamlit."
    st.download_button(
        label="Download Sample TXT",
        data=sample_text,
        file_name="sample_output.txt",
        mime="text/plain"
    )
