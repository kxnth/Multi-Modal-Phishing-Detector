# 🛡️ Multi-Modal Phishing Detector

Analyzes emails and linked URLs using DistilBERT and MobileNetV2.

## Structure
- `/datasets`: CSVs and images (Stored via Git LFS)
- `/models`: Saved `.keras` and BERT files (Stored via Git LFS)
- `/results`: Reports and matrices

## Run Instructions
**Clone the repository:**
   git clone https://github.com/kxnth/Multi-Modal-Phishing-Detector
   cd [INSERT_YOUR_FOLDER_NAME_HERE]

Create and activate a virtual environment:
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