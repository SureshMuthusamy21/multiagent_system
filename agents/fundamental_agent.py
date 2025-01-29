from typing import Dict
from openai import OpenAI

class FundamentalAnalysisAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )
    
    async def analyze_sentiment(self, company_data: Dict):
        """Analyze market sentiment using news and financial data"""
        news = company_data["news"]
        financials = company_data["financials"]
        
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a financial analyst expert specializing in fundamental "
                    "analysis and market sentiment analysis. Analyze the provided "
                    "data and provide detailed insights."
                )
            },
            {
                "role": "user",
                "content": f"""
                Analyze the market sentiment for this company based on:
                1. Recent news: {news}
                2. Financial metrics: {financials}
                
                Provide a detailed analysis including:
                - Overall market sentiment (bullish/bearish)
                - Key factors affecting the stock
                - Potential risks and opportunities
                - P/E ratio analysis
                - P/B ratio analysis
                - Revenue growth trends
                - Competitive position in the market
                """
            }
        ]
        
        response = self.client.chat.completions.create(
            model="sonar-pro",
            messages=messages,
            temperature=0.7
        )
        print("fundamental analysis")
        
        return response.choices[0].message.content 