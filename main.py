import streamlit as st
from capture import get_screenshot
from detector import analyze_phishing
import os

st.set_page_config(page_title="Multi-Modal Phishing Detector", layout="wide")

st.title("📡 AI Phishing Intelligence System")
st.write("Ensuring compliance with Selenium, MobileNetV2, and TensorFlow/Keras stack.")

col1, col2 = st.columns(2)
with col1:
    email_input = st.text_area("Suspicious Email Content:", height=200)
with col2:
    url_input = st.text_input("Threat URL:", placeholder="https://example.com")

if st.button("🚀 RUN FULL SECURITY SCAN"):
    if not email_input or not url_input:
        st.error("Missing input fields.")
    else:
        with st.spinner("🔍 Selenium capturing live evidence..."):
            # 1. Capture using Selenium
            image_result = get_screenshot(url_input)
            
            if "Error" in image_result:
                st.warning(f"Scan Issue: {image_result}")
                image_to_show = "placeholder.png"
            else:
                image_to_show = image_result

            # 2. AI Analysis
            report, verdict = analyze_phishing(email_input, image_to_show)

            # 3. Display
            st.divider()
            c1, c2 = st.columns([1, 2])
            with c1:
                st.image(image_to_show, caption="Selenium Live Capture")
            with c2:
                if "PHISHING" in verdict:
                    st.error(f"### {verdict}")
                else:
                    st.success(f"### {verdict}")
                st.markdown(report)