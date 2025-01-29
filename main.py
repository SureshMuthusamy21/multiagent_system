from langgraph.graph import Graph
from typing import Dict, TypedDict, Annotated, Sequence
from typing_extensions import TypedDict
import operator
import asyncio
from config.config import Config
from data.stock_data import StockDataFetcher
from agents.fundamental_agent import FundamentalAnalysisAgent
from agents.technical_agent import TechnicalAnalysisAgent

outputs = {}
outputs_list = []

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
        global outputs
        state["stock_data"] = stock_data
        state["company_info"] = company_info
        outputs["symbol"] = state["symbol"]
        outputs["stock_data"] = stock_data
        outputs["company_info"] = company_info
        return state
    
    async def analyze_fundamentals(state: Dict) -> Dict:
        sentiment = await fundamental_agent.analyze_sentiment(state["company_info"])
        state["fundamental_analysis"] = sentiment
        outputs["fundamental_analysis"] = sentiment
        return state
    
    async def analyze_technicals(state: Dict) -> Dict:
        technical_analysis = technical_agent.analyze_technicals(state["stock_data"])

        def generate_report(technical_analysis):
            """Generates a detailed technical analysis report."""

            entry = technical_analysis["entry_point"]
            target = technical_analysis["target_price"]
            stop_loss = technical_analysis["stop_loss"]
            position = technical_analysis["position"]
            risk_reward_ratio = technical_analysis["risk_reward_ratio"]
            
            # Determine market structure based on trend direction
            market_structure = "Bullish" if position == "long" else "Bearish"
            liquidity_zones = "Key liquidity grab areas around support and resistance zones."
            supply_demand_zones = (
                "Price is reacting near a high-demand zone (support) suggesting a long trade."
                if position == "long"
                else "Price is reacting near a supply zone (resistance) indicating a short trade."
            )
            
            report = f"""
            **Technical Analysis Report**
            ------------------------------------
            **Market Structure:** {market_structure}
            **Liquidity Zones:** {liquidity_zones}
            **Supply & Demand Zones:** {supply_demand_zones}
            
            **Trade Recommendation:**
            - **Entry Point:** {entry:.2f}
            - **Target Price:** {target:.2f}
            - **Stop Loss:** {stop_loss:.2f}
            - **Risk-to-Reward Ratio:** {risk_reward_ratio:.2f}
            - **Trade Direction:** {'📈 Long (Buy)' if position == 'long' else '📉 Short (Sell)'}
            
            **Trade Justification:**
            - The market structure indicates a **{market_structure} trend**.
            - **Liquidity zones** suggest institutional interest around these price levels.
            - **Supply & Demand zones** confirm potential price reaction areas.
            - Risk management is applied with a clear **Stop Loss and Risk-to-Reward Ratio**.
            """
            return report
        
        analysis_report = generate_report(technical_analysis)
        outputs["technical_analysis"] = analysis_report
        state["technical_analysis"] = analysis_report
        return state
    
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
        print(outputs)
        outputs_list.append(outputs)

        results[symbol] = result
    return outputs_list
    

if __name__ == "__main__":
    results = asyncio.run(main())
    print(results) 