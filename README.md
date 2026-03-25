# Multi-Modal Phishing Detector
**Catching phishing attacks with text analysis and visual recognition**

This is a two-part system that detects phishing attempts:
1. **Text Analysis:** Uses BERT to analyze email content
2. **Visual Analysis:** Uses MobileNetV2 to analyze website screenshots

Both models work together to give you a final risk score.

## Features
* **Dual AI models** - text and image analysis combined
* **Web scraping** - automatically captures screenshots of URLs
* **Web interface** - simple Streamlit app for checking suspicious emails/links
* **Accurate** - F1 scores of 0.88+ for text, 0.80+ for images

## Project Structure

```
.
├── .streamlit/               # Streamlit app settings (UI theme, colors, etc.)
├── dataset/                  # Training data (emails and website screenshots)
├── models/                   # Trained models (BERT for text, MobileNetV2 for images)
├── training/                 # Scripts to train the models
│   ├── train_nlp.py          # Train the text model
│   └── train_vision.py       # Train the image model
├── utils/                    # Core code
│   ├── capture.py            # Screenshot capture and web scraping
│   ├── detector.py           # Phishing detection logic
│   └── evaluate_models.py    # Test model accuracy
├── main.py                   # Start here! The web app
├── requirements.txt          # Python packages needed
└── README.md                 # Documentation
```

**1. Clone and setup:**
```bash
#Github Link
git clone https://github.com/kxnth/Multi-Modal-Phishing-Detector
cd Multi-Modal-Phishing-Detector
python -m venv venv #Install Virtual Environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**2. Install and run:**
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
- **NLP Model (DistilBERT)/Text model:** ~88% accurate on test data (F1-Score >= 0.88)
- **Vision Model (MobileNetV2)/Image model:** ~80% accurate on test data (F1-Score >= 0.80)