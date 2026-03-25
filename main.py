import os
import logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
logging.getLogger('tensorflow').setLevel(logging.ERROR)
import streamlit as st
import base64
import re

st.set_page_config(page_title="PhishGuard AI", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .main, .block-container {
    background-color: #0f3d42 !important;
    font-family: sans-serif !important;
    color: #ffffff !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 1rem !important; max-width: 650px !important; }

[data-testid="stForm"] {
    background: linear-gradient(180deg, #124549 0%, #092124 100%) !important;
    border: 1px solid #4a7c82 !important;
    border-radius: 10px !important;
    padding: 20px !important;
}

div[data-baseweb="input"], div[data-baseweb="input"] * ,
div[data-baseweb="base-input"], div[data-baseweb="base-input"] * ,
div[data-baseweb="textarea"], div[data-baseweb="textarea"] * ,
.stTextInput input, .stTextArea textarea {
    background: transparent !important;
    background-color: transparent !important;
    color: #ffffff !important;
    caret-color: #ffffff !important; 
    box-shadow: none !important;
}

.stTextInput > div > div, .stTextArea > div > div,
.stTextInput, .stTextArea {
    border: 1px solid #4a7c82 !important;
    border-radius: 6px !important;
    background: transparent !important;
    background-color: transparent !important;
}

::placeholder, input::placeholder, textarea::placeholder {
    color: #ffffff !important;
    opacity: 0.7 !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="base-input"]:focus-within,
div[data-baseweb="textarea"]:focus-within,
.stTextInput input:focus, 
.stTextArea textarea:focus {
    border-color: #2ecc71 !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="InputInstructions"] {
    display: none !important;
}

[data-testid="stFormSubmitButton"] button {
    border-radius: 50px !important;
    border: 1px solid #ffffff !important;
    background: transparent !important;
    color: #ffffff !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

from utils.capture import get_screenshot
from utils.detector import analyze_phishing

st.markdown('<h2 style="text-align: center; color: #ffffff; margin-bottom: 0px; padding-bottom: 0px;">PhishGuard AI</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #ffffff; margin-top: 5px; margin-bottom: 30px; font-size: 0.9rem;">Advance scanner for Phishing emails / links • Powered by AI</p>', unsafe_allow_html=True)

with st.form("scan_form"):
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

    st.markdown('✉️Check Email (suspicious message)')
    email_text = st.text_area("email", label_visibility="collapsed", height=100, placeholder="Input at least 50 characters...")
    
    st.markdown('🔗Check Link / URL')
    url_text = st.text_input("url", label_visibility="collapsed")
    
    st.markdown('<br>', unsafe_allow_html=True) 
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        scan_clicked = st.form_submit_button("⚙️ Scan using AI", use_container_width=True)

if scan_clicked:
    email_val = email_text.strip()
    url_val = url_text.strip()
    
    email_err = ""
    url_err = ""

    # Validate email: must not be empty and at least 50 characters
    if not email_val:
        email_err = "⚠️ Please input an email message to scan."
    elif len(email_val) < 50:
        email_err = "⚠️ Email is too short. Please input at least 50 characters."

    # Validate URL: must be at least 15 characters and contain a dot
    if not url_val:
        url_err = "⚠️ Please input a Link / URL to scan."
    elif len(url_val) < 15 or "." not in url_val:
        url_err = "⚠️ This is an invalid link. Try again."

    # Display validation errors and highlight invalid fields
    if email_err or url_err:
        error_html = '<div id="phish-error-box" style="background-color: rgba(255, 51, 51, 0.2); border: 2px solid #ff3333; color: #ff3333; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-weight: bold;">'
        dynamic_css = '<style id="phish-error-style">'
        
        if email_err:
            error_html += f"{email_err}<br>"
            dynamic_css += 'div[data-baseweb="textarea"] { border-color: #ff3333 !important; box-shadow: 0 0 5px #ff3333 !important; } '
            
        if url_err:
            error_html += f"{url_err}"
            dynamic_css += '.stTextInput > div > div, div[data-baseweb="input"] { border-color: #ff3333 !important; box-shadow: 0 0 5px #ff3333 !important; } '
            
        error_html += '</div>'
        dynamic_css += "</style>"
        
        # Display the errors and inject the red boxes
        st.markdown(error_html, unsafe_allow_html=True)
        st.markdown(dynamic_css, unsafe_allow_html=True)

        # Clear errors when user starts typing
        import streamlit.components.v1 as components
        components.html("""
        <script>
        const doc = window.parent.document;
        const inputs = doc.querySelectorAll('textarea, input');
        
        inputs.forEach(input => {
            // The millisecond the user clicks or types in the box, wipe the errors!
            ['input', 'focus'].forEach(evt => {
                input.addEventListener(evt, function() {
                    const errorBox = doc.getElementById('phish-error-box');
                    if (errorBox) errorBox.style.display = 'none';
                    
                    const errorStyle = doc.getElementById('phish-error-style');
                    if (errorStyle) errorStyle.innerHTML = '';
                });
            });
        });
        </script>
        """, height=0, width=0)
            
    else:
        # Scan is valid, proceed with analysis
        with st.spinner("Scanning with AI & Capturing Website..."):
            image_path = None
            scraped_text = ""
            
            if url_text.strip():
                capture_result = get_screenshot(url_text.strip())
                if capture_result:
                    image_path, scraped_text = capture_result

            combined_text = "\n".join(filter(None, [email_text.strip(), url_text.strip(), scraped_text]))
            report, verdict = analyze_phishing(combined_text, image_path)

        v = verdict.strip().upper()
        if "SAFE" in v: 
            bg_color, border = "#eaffea", "#2ecc71"
        elif "SUSPICIOUS" in v: 
            bg_color, border = "#fff8e1", "#f39c12"
        else: 
            bg_color, border = "#ffebee", "#e74c3c"

        st.markdown(f"""
        <div style="background: {bg_color}; border: 1px solid {border}; border-left: 8px solid {border}; border-radius: 8px; padding: 15px; margin-bottom: 20px; color: #000; text-align: left;">
            <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 5px;">{verdict}</div>
            <div><strong>AI Risk Score:</strong> {report}</div>
        </div>
        """, unsafe_allow_html=True)

        img_html = '<div style="height: 300px; background: #ffffff;"></div>'
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                b64_str = base64.b64encode(img_file.read()).decode()
            img_html = f'<img src="data:image/png;base64,{b64_str}" style="width: 100%; display: block; border-radius: 0 0 8px 8px;">'

        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #4a7c82; border-radius: 8px; color: #000; overflow: hidden;">
            <div style="padding: 10px; font-weight: bold; font-size: 0.9rem; text-align: left; color: #09515C;">Sample Webpage Screenshot (AI simulated preview)</div>
            <div style="border-bottom: 2px solid #09515C; width: 97%; margin: 0 auto 12px auto;"></div>
            {img_html}
        </div>
        """, unsafe_allow_html=True)