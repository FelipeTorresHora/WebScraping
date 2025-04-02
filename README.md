# REIT Analytics Dashboard: Comprehensive Analysis of Brazilian Real Estate Investment Trusts

The REIT Analytics Dashboard is a powerful Streamlit-based application that provides in-depth analysis and insights for Brazilian Real Estate Investment Trusts (REITs/FIIs). It combines real-time data analysis, machine learning forecasting, and AI-powered insights to help investors make informed decisions about their REIT investments.

The dashboard offers comprehensive features including advanced filtering capabilities, historical price analysis, price forecasting using Prophet, and AI-assisted analysis powered by Google's Gemini model. Users can generate detailed PDF reports and receive automated email notifications, making it an essential tool for both novice and experienced REIT investors.

## Repository Structure
```
.
├── ai_agent.py          # Handles AI-powered REIT analysis using Google's Gemini model
├── dashboard.py         # Main application entry point and Streamlit UI implementation
├── data.py             # Data fetching and processing from external REIT sources
├── envio.py            # Email notification and PDF report generation functionality
├── ml.py              # Machine learning models for price forecasting using Prophet
└── requirements.txt    # Project dependencies and package specifications
```

## Usage Instructions
### Prerequisites
- Python 3.7 or higher
- SMTP server access for email functionality
- Google Gemini API key for AI analysis
- BRAPI token for historical data
- Internet connection for real-time data fetching

Required Python packages:
```
requests
beautifulsoup4
pandas
streamlit
fpdf
plotly
python-dotenv
google-generativeai
prophet
sklearn
```

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and credentials
```

### Quick Start
1. Configure your environment variables:
```bash
BRAPI_TOKEN=your_brapi_token
gemini_api=your_gemini_api_key
Senha_Email=your_email_password
```

2. Run the dashboard:
```bash
streamlit run dashboard.py
```

3. Access the dashboard at `http://localhost:8501`

### More Detailed Examples

1. **Advanced Filtering**
```python
# Example filter configuration
min_cotacao = 30.0
min_dy = 9.0
min_valor_mercado = 100000000.0
min_liquidez = 10000.0
min_qt_imoveis = 1
max_vacancia = 20.0
```

2. **Price Forecasting**
```python
# Get historical data and forecast
fii_code = "MXRF11"
df_historical = get_historical_data(fii_code)
forecast = prever_preco_prophet(df_historical)
```

### Troubleshooting

1. **Data Fetching Issues**
- Problem: "Error fetching REIT data"
- Solution: 
  ```python
  # Check your internet connection
  # Verify BRAPI token in .env file
  # Try with different User-Agent in headers
  ```

2. **AI Analysis Errors**
- Problem: "API key not found"
- Solution: Ensure Gemini API key is properly set in .env file

3. **Email Sending Failures**
- Problem: "SMTP authentication error"
- Solution: 
  - Verify email credentials in .env
  - Enable "Less secure app access" for Gmail
  - Check SMTP server settings

## Data Flow
The dashboard processes REIT data through multiple stages, from raw data collection to AI-powered analysis and visualization.

```ascii
[External Sources] -> [Data Fetching] -> [Processing] -> [Analysis] -> [Visualization]
    |                     |                  |              |               |
    |                     |                  |              |               |
    v                     v                  v              v               v
Fundamentus API -> Raw REIT Data -> Cleaned Data -> ML Models -> Interactive Dashboard
BRAPI API                                            AI Analysis    PDF Reports
```

Key Component Interactions:
1. Data fetching module retrieves real-time REIT data from Fundamentus
2. Historical price data is obtained from BRAPI API
3. Prophet model processes historical data for price forecasting
4. Gemini AI analyzes REIT fundamentals and provides insights
5. Dashboard presents processed data through interactive visualizations
6. PDF generation and email modules handle report distribution
7. All components communicate through standardized data structures
8. Error handling and logging across all integration points