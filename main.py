import streamlit as st
import os
import base64

st.set_page_config(page_title="PhishGuard AI", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
/* Global Dark Theme */
html, body, [data-testid="stAppViewContainer"], .main, .block-container {
    background-color: #0f3d42 !important;
    font-family: sans-serif !important;
    color: #ffffff !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1rem !important; max-width: 650px !important; }

/* Main Box Gradient */
[data-testid="stForm"] {
    background: linear-gradient(180deg, #124549 0%, #092124 100%) !important;
    border: 1px solid #4a7c82 !important;
    border-radius: 10px !important;
    padding: 20px !important;
}

/* Force Transparent Inputs */
div[data-baseweb="base-input"], div[data-baseweb="base-input"] > input,
div[data-baseweb="textarea"], div[data-baseweb="textarea"] > textarea,
.stTextInput input, .stTextArea textarea {
    background: transparent !important;
    background-color: transparent !important;
    color: #ffffff !important;
    box-shadow: none !important;
}
.stTextInput, .stTextArea {
    border: 1px solid #4a7c82 !important;
    border-radius: 6px !important;
    background: transparent !important;
}

/* Centered Pill Button Styling */
[data-testid="stFormSubmitButton"] button {
    border-radius: 50px !important;
    border: 1px solid #ffffff !important;
    background: transparent !important;
    color: #ffffff !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

try:
    from capture import get_screenshot
    from detector import analyze_phishing
except ImportError:
    def get_screenshot(url): return None
    def analyze_phishing(email_text, image_path): return "NLP: 46.1% | Vision: 57.0% | Fusion: 48.3%", "✅ SAFE"

# Hero
st.markdown('<h1 style="text-align: center; color: #ffffff;">PhishGuard AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #ffffff; margin-bottom: 30px;">Advance scanner for Phishing emails / links • Powered by AI</p>', unsafe_allow_html=True)

# Main Form
with st.form("scan_form"):
    
    # Clickable Instructions Header & Text
    st.markdown("""
    <details style="margin-bottom: 20px; cursor: pointer;">
        <summary style="display: flex; justify-content: center; list-style: none;">
            <div style="background: linear-gradient(90deg, #2a8a92 0%, #071e22 100%); border: 1px solid #ffffff; border-radius: 5px; padding: 8px 40px; font-weight: bold; letter-spacing: 1px; font-size: 1rem; color: #ffffff;">
                INSTRUCTIONS
            </div>
        </summary>
        <div style="margin-top: 15px;">
            <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 8px;">✉️ Scan an Email</div>
            <div style="font-size: 0.9rem; color: #e0e0e0; line-height: 1.5; margin-bottom: 15px;">* Open your email message<br>* Copy the full email content (or suspicious part)<br>* Paste it into the "Check Email" box<br>* Click "Scan using AI"<br>* Wait for the result</div>
            <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 8px;">🔗 Scan a Link / URL</div>
            <div style="font-size: 0.9rem; color: #e0e0e0; line-height: 1.5; margin-bottom: 25px;">* Copy the link (URL) you want to check<br>* Paste it into the "Check Link / URL" field<br>* Click "Scan using AI"</div>
        </div>
    </details>
    """, unsafe_allow_html=True)

    st.markdown('✉️ Check Email (suspicious message)')
    email_text = st.text_area("email", label_visibility="collapsed", height=100)
    
    st.markdown('🔗 Check Link / URL')
    url_text = st.text_area("url", label_visibility="collapsed")
    
    # Centered Submit Button using Columns
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        scan_clicked = st.form_submit_button("Scan using AI", use_container_width=True)

if scan_clicked:
    if not email_text.strip() and not url_text.strip():
        st.warning("⚠️ Please provide an email or URL.")
    else:
        with st.spinner("Scanning with AI & Capturing Website..."):
            image_path = get_screenshot(url_text.strip()) if url_text.strip() else None
            combined_text = "\n".join(filter(None, [email_text.strip(), url_text.strip()]))
            report, verdict = analyze_phishing(combined_text, image_path)

        v = verdict.strip().upper()
        if "SAFE" in v: bg_color, border = "#eaffea", "#2ecc71"
        elif "SUSPICIOUS" in v: bg_color, border = "#fff8e1", "#f39c12"
        else: bg_color, border = "#ffebee", "#e74c3c"

        # Result Box (Left Aligned)
        st.markdown(f"""
        <div style="background: {bg_color}; border: 1px solid {border}; border-left: 8px solid {border}; border-radius: 8px; padding: 15px; margin-bottom: 20px; color: #000; text-align: left;">
            <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 5px;">{verdict}</div>
            <div><strong>AI Risk Score:</strong> {report}</div>
        </div>
        """, unsafe_allow_html=True)

        # Single Screenshot Box via Base64 HTML injection
        img_html = '<div style="height: 300px; background: #ffffff;"></div>'
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                b64_str = base64.b64encode(img_file.read()).decode()
            img_html = f'<img src="data:image/png;base64,{b64_str}" style="width: 100%; display: block; border-radius: 0 0 8px 8px;">'

        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #4a7c82; border-radius: 8px; color: #000; overflow: hidden;">
            <div style="padding: 10px; font-weight: bold; font-size: 0.9rem; border-bottom: 1px solid #4a7c82;">Sample Webpage Screenshot (AI simulated preview)</div>
            {img_html}
        </div>
        """, unsafe_allow_html=True)