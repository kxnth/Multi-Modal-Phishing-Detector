# Multi-Modal Phishing Detector (Email Text + Linked Website Screenshot Analysis)
**Combining text AI and visual AI to catch phishing from two angles at once**

Modern phishing attacks are sophisticated. A phishing email looks legitimate, and the linked website looks like a perfect copy of your bank's login page. This project builds a **two-part detection system** that analyzes emails and websites simultaneously:

1. **NLP Analysis** - Uses BERT to detect suspicious language patterns, urgency triggers, and spoofed sender techniques
2. **Vision Analysis** - Uses MobileNetV2 to identify cloned layouts and visual deception

When combined, they produce a **single confidence score** — like two security experts comparing notes to catch what one might miss alone.

## Project Structure
```
.
├── .streamlit/               # Streamlit app settings
├── dataset/                  # Training data (emails and website screenshots)
├── models/                   # Trained models (BERT for text, MobileNetV2 for images)
├── training/                 # Scripts to train the models
│   ├── train_nlp.py          # Train the text model
│   └── train_vision.py       # Train the image model
├── utils/                    # Core code
│   ├── capture.py            # Screenshot capture and web scraping
│   ├── detector.py           # Phishing detection logic
│   └── evaluate_models.py    # Test model accuracy
├── main.py                   # The web app
├── requirements.txt          # Python packages needed
└── README.md                 # Documentation
```

**1. Install Git LFS (required for large files):**
```bash
choco install git-lfs # Windows 
brew install git-lfs # Mac
```
**2. Clone and setup:**
```bash
#Github Link/Cloning
git clone https://github.com/kxnth/Multi-Modal-Phishing-Detector
cd Multi-Modal-Phishing-Detector
####
git lfs pull
python -m venv venv #Install Virtual Environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```
**3. Install and run:**
```bash
pip install -r requirements.txt
streamlit run main.py
```

open http://localhost:8501 in your browser and paste an email or URL to scan.

## Optional: Retraining
If you want to retrain from scratch:
```bash
python utils/preprocess.py         # Clean the dataset
python training/train_nlp.py       # Train text model
python training/train_vision.py    # Train image model
python utils/evaluate_models.py    # Check performance
```
## Model Performance
- **NLP Model (BERT)** - Fine-tuned on 15,000+ emails. F1-Score: 0.88+
- **Vision Model (MobileNetV2)** - Fine-tuned on website screenshots. F1-Score: 0.80+