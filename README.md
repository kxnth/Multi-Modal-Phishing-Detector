# Integrated Phishing Detection System: Simultaneous Analysis of Email Text and Website Screenshots

**Multi-Modal Phishing Detector (Email Text + Linked Website Screenshot Analysis)**  
**Combining text AI and visual AI to catch phishing from two angles at once**

## Project Structure

```
.
├── data/                     # Training data (emails and website screenshots)
│   ├── images/
│   │   ├── phishing/         # Phishing website screenshots
│   │   └── safe/             # Safe website screenshots
│   └── text/                 # Email datasets
├── models/                   # Trained models (BERT for text, MobileNetV2 for images)
├── notebooks/                # Jupyter notebooks for exploration
├── results_nlp/              # NLP training checkpoints
├── src/                      # Source code
│   ├── main.py               # The web app
│   ├── training/
│   │   ├── train_nlp.py      # Train the text model
│   │   └── train_vision.py   # Train the image model
│   └── utils/
│       ├── capture.py        # Screenshot capture and web scraping
│       ├── detector.py       # Phishing detection logic
│       ├── evaluate_models.py # Test model accuracy
│       ├── fix_dataset.py    # Dataset preprocessing
│       └── preprocess.py     # Data preprocessing
├── requirements.txt          # Python packages needed
└── README.md                 # Documentation
```

## Datasets Used

To comply with repository size limits, the datasets are not hosted directly in this repository. Please download them from Kaggle using the links below:

- [Alam, N. A. (2024). Phishing Email Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)
- [Zac, Z. (n.d.). Phishing sites screenshot](https://www.kaggle.com/datasets/zackyzac/phishing-sites-screenshot)
- [pooriamst. (n.d.). Website Screenshots](https://www.kaggle.com/datasets/pooriamst/website-screenshots)

## Installation & Setup Guide

### Phase 1: Core Software Installation

These are the foundational tools required for machine learning on a fresh Windows PC.

**Git (for downloading code and models)**

- Link: https://git-scm.com/download/win
- Installation: Download the 64-bit setup and click "Next" through all the default options.

**Python 3.11 (The AI Industry Standard)**

- Link: https://www.python.org/downloads/release/python-3119/
- Installation: Scroll to the bottom files table and download the Windows installer (64-bit).  
  Important Step: On the very first screen of the installer, you must check the box that says "Add python.exe to PATH" before clicking Install.

*(Note: Always restart VS Code completely after installing these so the terminal recognizes them).*

### Phase 2: Project Setup & Environment

Open VS Code, open a New Terminal (Ctrl + ~), and run these commands one by one to download the project and isolate the dependencies.

```bash
# 1. Create a Projects folder and enter it
mkdir Projects
cd Projects

# 2. Download the code
git clone https://github.com/kxnth/Multi-Modal-Phishing-Detector
cd Multi-Modal-Phishing-Detector

# 3. Create a fresh Python virtual environment
python -m venv venv

# 4. Activate the environment (Type 'A' if Windows asks for permission)
.\venv\Scripts\activate

# 5. Install all the necessary AI libraries (TensorFlow, Streamlit, etc.)
pip install -r requirements.txt
```

### Phase 3: The Datasets

To rebuild the data that was ignored by GitHub, create the following folders manually inside your project:

- `data/text/`
- `data/images/safe/`
- `data/images/phishing/`

**The Image Datasets:**

- **Phishing Images:** Download the "Phishing sites screenshot" dataset by zackyzac on Kaggle. Extract the malicious website screenshots into your `data/images/phishing/` folder.
- **Safe Images:** Download the "Website Screenshots" dataset by pooriamst on Kaggle. Extract these legitimate website screenshots into your `data/images/safe/` folder.

**The Text Datasets:** Place your `safe_email.csv`, `phishing_emails.csv`, and `phishing_email.csv` files directly into the `data/text/` folder.

### Phase 4: Fixing Data & Retraining

Kaggle datasets contain hidden .webp files and nested subfolders that TensorFlow ignores. You must run the Deep Scan script to extract and convert thousands of images into readable .jpg files.

```bash
# 1. Install the image conversion tool
pip install Pillow

# 2. Run the deep scan to fix the Kaggle images
python src/utils/fix_dataset.py
```

(Wait for the terminal to confirm it has found and converted the 3,600+ Safe images and 650+ Phishing images).

Now that the AI can read the data, retrain the models:

```bash
# 3. Train the Vision Model (MobileNetV2)
python src/training/train_vision.py

# 4. Train the Text Model (BERT)
python src/training/train_nlp.py
```
### Phase 4.5: Evaluate the Models
To verify the accuracy and generate the Confusion Matrices for both models before launching the app, run the evaluation script. This will output the final F1-scores and metrics directly to your terminal.

```bash
python src/utils/evaluate_models.py

### Phase 5: Launch the Application

With the environment built, the data cleaned, and the models trained to a high F1 score, launch the final web interface:

```bash
streamlit run src/main.py
```

## Model Performance

After rigorous testing using the live evaluation script, both models significantly exceeded the project's baseline requirements:

- **NLP Model (BERT-Tiny)** - Fine-tuned on 15,000+ emails. 
  - **F1-Score:** **0.96** (Accuracy: 96%)
- **Vision Model (MobileNetV2)** - Fine-tuned on 4,100+ website screenshots. 
  - **F1-Score:** **0.90** (Accuracy: 84%)