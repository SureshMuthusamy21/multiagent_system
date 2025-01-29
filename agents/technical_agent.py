import pandas as pd
import numpy as np
from typing import Dict

class TechnicalAnalysisAgent:
    def __init__(self, params: Dict):
        self.params = params
    
    def analyze_technicals(self, stock_data: pd.DataFrame):
        """Perform technical analysis using Smart Money Concepts"""
        analysis = {
            "smc_levels": self._calculate_smc_levels(stock_data),
            "rsi": self._calculate_rsi(stock_data),
            "trend": self._analyze_trend(stock_data)
        }
        
        return self._generate_trade_recommendation(analysis, stock_data)
    
    def _calculate_smc_levels(self, data: pd.DataFrame):
        """Calculate Smart Money Concepts levels"""
        # Implementation of SMC strategy
        highs = data['High'].rolling(window=20).max()
        lows = data['Low'].rolling(window=20).min()
        
        return {
            "resistance": highs.iloc[-1],
            "support": lows.iloc[-1]
        }
    
    def _calculate_rsi(self, data: pd.DataFrame) -> float:
        """Calculate the Relative Strength Index"""
        # Get the period from params
        period = self.params['rsi_period']
        
        # Calculate price changes
        delta = data['Close'].diff()
        
        # Separate gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        # Calculate RS and RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return float(rsi.iloc[-1])
    
    def _analyze_trend(self, data: pd.DataFrame) -> dict:
        """Analyze the price trend"""
        # Calculate short and long-term moving averages
        short_ma = data['Close'].rolling(window=self.params['short_window']).mean()
        long_ma = data['Close'].rolling(window=self.params['long_window']).mean()
        
        # Determine trend direction
        current_short = short_ma.iloc[-1]
        current_long = long_ma.iloc[-1]
        
        return {
            "direction": "uptrend" if current_short > current_long else "downtrend",
            "strength": abs(current_short - current_long) / current_long * 100
        }
    
    def _generate_trade_recommendation(self, analysis: Dict, data: pd.DataFrame):
        current_price = data['Close'].iloc[-1]
        smc_levels = analysis['smc_levels']
        
        return {
            "entry_point": current_price,
            "target_price": self._calculate_target(current_price, analysis),
            "stop_loss": self._calculate_stop_loss(current_price, analysis),
            "position": "long" if analysis['trend']['direction'] == "uptrend" else "short",
            "risk_reward_ratio": self._calculate_risk_reward_ratio(current_price, analysis)
        }
    
    def _calculate_target(self, current_price: float, analysis: Dict) -> float:
        """Calculate target price based on technical analysis"""
        smc_levels = analysis['smc_levels']
        if analysis['trend']['direction'] == "uptrend":
            return current_price * 1.1  # 10% above current price for uptrend
        else:
            return current_price * 0.9  # 10% below current price for downtrend
    
    def _calculate_stop_loss(self, current_price: float, analysis: Dict) -> float:
        """Calculate stop loss level"""
        smc_levels = analysis['smc_levels']
        if analysis['trend']['direction'] == "uptrend":
            return smc_levels['support']
        else:
            return smc_levels['resistance']
    
    def _calculate_risk_reward_ratio(self, current_price: float, analysis: Dict) -> float:
        """Calculate risk/reward ratio"""
        target = self._calculate_target(current_price, analysis)
        stop_loss = self._calculate_stop_loss(current_price, analysis)
        
        potential_reward = abs(target - current_price)
        potential_risk = abs(stop_loss - current_price)
        
        return potential_reward / potential_risk if potential_risk != 0 else 0 