from langgraph.graph import Graph
from typing import Dict, TypedDict, Annotated, Sequence
from typing_extensions import TypedDict
import operator
import asyncio
from config.config import Config
from data.stock_data import StockDataFetcher
from agents.fundamental_agent import FundamentalAnalysisAgent
from agents.technical_agent import TechnicalAnalysisAgent

# Define state type
class AgentState(TypedDict):
    symbol: str
    stock_data: Dict
    company_info: Dict
    fundamental_analysis: str | None
    technical_analysis: Dict | None

async def main():
    # Initialize agents
    fundamental_agent = FundamentalAnalysisAgent(Config.PERPLEXITY_API_KEY)
    technical_agent = TechnicalAnalysisAgent(Config.TECHNICAL_PARAMS)
    
    # Create workflow graph
    workflow = Graph()
    
    # Define node functions
    async def fetch_data(state: Dict) -> Dict:
        data_fetcher = StockDataFetcher()
        stock_data = data_fetcher.get_stock_data(state["symbol"], Config.PERIOD)
        company_info = data_fetcher.get_company_info(state["symbol"])
        
        return {
            **state,
            "stock_data": stock_data,
            "company_info": company_info
        }
    
    async def analyze_fundamentals(state: Dict) -> Dict:
        sentiment = await fundamental_agent.analyze_sentiment(state["company_info"])
        return {
            **state,
            "fundamental_analysis": sentiment
        }
    
    async def analyze_technicals(state: Dict) -> Dict:
        technical_analysis = technical_agent.analyze_technicals(state["stock_data"])
        print("technical analysis")
        print(technical_analysis)
        return {
            **state,
            "technical_analysis": technical_analysis
        }
    
    # Add nodes to graph
    workflow.add_node("fetch_data", fetch_data)
    workflow.add_node("analyze_fundamentals", analyze_fundamentals)
    workflow.add_node("analyze_technicals", analyze_technicals)
    
    # Define edges for sequential flow
    workflow.add_edge("fetch_data", "analyze_fundamentals")
    workflow.add_edge("analyze_fundamentals", "analyze_technicals")
    
    # Set the entry point
    workflow.set_entry_point("fetch_data")
    
    # Compile the graph
    app = workflow.compile()
    
    # Run analysis for both stocks
    results = {}
    for symbol in Config.SYMBOLS:
        initial_state = {
            "symbol": symbol,
            "stock_data": {},
            "company_info": {},
            "fundamental_analysis": None,
            "technical_analysis": None
        }
        result = await app.ainvoke(initial_state)

        results[symbol] = result
    
    return results

if __name__ == "__main__":
    results = asyncio.run(main())
    print(results) 