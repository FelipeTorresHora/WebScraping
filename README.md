# REIT Analytics Dashboard - Análise de Fundos Imobiliários Brasileiros

## Main Features
- Advanced REIT filters
- Historical price analysis
- Price prediction using Prophet
- AI analysis using Google Gemini
- PDF report generation
- Email notifications

## Project Structure
```
├── ai_agent.py    # AI Analysis (Google Gemini)
├── dashboard.py   # Streamlit Interface
├── data.py       # Data Collection and Processing
├── envio.py      # Emails and PDF Reports
├── ml.py         # Prophet Predictions
└── requirements.txt
```

## How to Use

### Prerequisites
- Python 3.7+
- SMTP Access for emails
- Google Gemini API Key
- BRAPI Token
- Internet connection

### Installation
```bash
# Clone repository
git clone <repository-url>
cd <repository-name>

# Virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Create a `.env` file with:
```bash
BRAPI_TOKEN=your_token
gemini_api=your_gemini_key
Senha_Email=email_password
```

### Run
```bash
streamlit run dashboard.py
```
Access at `http://localhost:8501`

## Troubleshooting
1. **Data fetching error**: Check connection and BRAPI token
2. **AI analysis error**: Confirm Gemini key in .env
3. **Email sending error**: Verify SMTP credentials# REIT Analytics Dashboard - Brazilian Real Estate Investment Trusts Analysis

Dashboard in Streamlit for analyzing Brazilian REITs (FIIs). Combines real-time data analysis, machine learning price predictions, and AI-based insights to help investors.

## Main Features
- Advanced REIT filters
- Historical price analysis
- Price prediction using Prophet
- AI analysis using Google Gemini
- PDF report generation
- Email notifications

## Project Structure
```
├── ai_agent.py    # AI Analysis (Google Gemini)
├── dashboard.py   # Streamlit Interface
├── data.py       # Data Collection and Processing
├── envio.py      # Emails and PDF Reports
├── ml.py         # Prophet Predictions
└── requirements.txt
```

## How to Use

### Prerequisites
- Python 3.7+
- SMTP Access for emails
- Google Gemini API Key
- BRAPI Token
- Internet connection

### Installation
```bash
# Clone repository
git clone <repository-url>
cd <repository-name>

# Virtual environment
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Create a `.env` file with:
```bash
BRAPI_TOKEN=your_token
gemini_api=your_gemini_key
Senha_Email=email_password
```

### Run
```bash
streamlit run dashboard.py
```
Access at `http://localhost:8501`

## Troubleshooting
1. **Data fetching error**: Check connection and BRAPI token
2. **AI analysis error**: Confirm Gemini key in .env
3. **Email sending error**: Verify SMTP credentials