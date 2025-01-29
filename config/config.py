import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    
    # Stock symbols to analyze
    SYMBOLS = ["AAPL", "MSFT"]
    
    # Time period for analysis
    PERIOD = "1mo"
    
    # Technical analysis parameters
    TECHNICAL_PARAMS = {
        "short_window": 20,
        "long_window": 50,
        "rsi_period": 14
    }
    
    # Perplexity API Configuration
    PERPLEXITY_MODEL = "pplx-7b-online" 