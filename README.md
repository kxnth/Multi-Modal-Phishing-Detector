# Multi-Modal Phishing Detector (Group 5)
**Combining Text AI and Visual AI to Catch Phishing**

Modern phishing attacks are sophisticated enough to bypass simple text filters by using perfectly cloned visual interfaces. This project is a two-part detection system: 
1. **NLP Component:** Analyzes email text using a fine-tuned BERT model.
2. **Vision Component:** Analyzes a screenshot of the linked URL using a fine-tuned MobileNetV2 CNN.

Together, they produce a combined phishing confidence score using a smart ensemble veto system.

---

## 🛠️ Features
* **Multi-Modal AI Fusion:** Combines DistilBERT (Text) and MobileNetV2 (Image) for high-accuracy threat detection.
* **Smart Ensemble Logic:** Uses a veto-override system (if one model is >85% confident, it overrides the average) to catch edge cases like hidden text or perfect visual clones.
* **Automated Web Scraping:** Uses Headless Selenium to safely visit URLs, capture screenshots, and scrape hidden DOM text.
* **Real-time Web UI:** Fully functional Streamlit web application for real-time analysis.

---

## 📂 Project Structure

phishing_detector_project/
│
├── .streamlit/               # Streamlit configuration settings
│   └── config.toml           # UI styling and theme configuration
├── dataset/                  # Contains all raw and cleaned training data
│   ├── images/               # Safe and phishing website screenshots
│   └── text/                 # Safe and phishing email CSV files
├── models/                   # Saved AI models and weights
│   ├── nlp_model_bert/       # Fine-tuned Hugging Face BERT model (Text)
│   ├── nlp_model.pkl         # Baseline Logistic Regression model (Legacy)
│   ├── vectorizer.pkl        # TF-IDF vectorizer (Legacy)
│   └── vision_model.keras    # Fine-tuned MobileNetV2 model (Vision)
├── results/                  # Evaluation outputs (e.g., vision_confusion_matrix.png)
├── results_nlp/              # Hugging Face Trainer checkpoints and training logs
├── screenshots/              # Temporary folder for Selenium to save captured live web pages
├── training/                 # Scripts specifically for training and isolated evaluation
│   ├── check_models.py       # API connection check script
│   ├── evaluate_vision.py    # Isolated evaluation script for the Vision model
│   ├── train_nlp.py          # Script to fine-tune DistilBERT on the text dataset
│   └── train_vision.py       # Script to train MobileNetV2 with image data augmentation
├── utils/                    # Core application logic and data pipelines
│   ├── capture.py            # Selenium headless browser script to screenshot and scrape text
│   ├── detector.py           # Core inference engine containing the Ensemble Fusion logic
│   ├── evaluate_models.py    # Master script to evaluate F1 metrics for both NLP and Vision
│   ├── fix_dataset.py        # Utility script to clean and rename raw image datasets
│   └── preprocess.py         # Cleans Kaggle email datasets (strips HTML, formats URLs)
├── venv/                     # Python virtual environment (Local dependencies)
├── .env                      # Hidden environment variables (e.g., API keys)
├── .gitattributes            # Git configuration for handling specific file types
├── .gitignore                # Tells Git to ignore large files (like /venv and /dataset)
├── main.py                   # Main Streamlit Web Application (The user interface)
├── README.md                 # Project documentation
└── requirements.txt          # Master list of required Python dependencies

## Run Instructions
**Clone the repository:**
git clone https://github.com/kxnth/Multi-Modal-Phishing-Detector
cd Multi-Modal-Phishing-Detector

Create venv:
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run the app:
streamlit run main.py

OPTIONAL: 

Generate & Clean the Data (Optional/Setup):
python utils/preprocess.py

Train the Models (Optional/Setup):
python training/train_nlp.py
python training/train_vision.py

Evaluate the Models (F1-Scores & Metrics):
python utils/evaluate_models.py

📊 Model Performance
NLP Model (DistilBERT): F1-Score >= 0.88
Vision Model (MobileNetV2): F1-Score >= 0.80
Detailed evaluation metrics and confusion matrices can be found in the /results folder.