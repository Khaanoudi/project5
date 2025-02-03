import pandas as pd
import streamlit as st
from typing import Dict, List

class TickerChartData:
    def __init__(self, session):
        self.session = session
        self.base_url = "https://www.tickerchart.net/api/v1"

    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_market_data(self, symbol: str) -> pd.DataFrame:
        """Get market data for a symbol"""
        try:
            response = self.session.get(
                f"{self.base_url}/market/data",
                params={"symbol": symbol}
            )
            data = response.json()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Failed to fetch market data: {e}")
            return pd.DataFrame()

    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_symbols(self) -> List[Dict]:
        """Get list of available symbols"""
        try:
            response = self.session.get(f"{self.base_url}/symbols")
            return response.json()
        except Exception as e:
            st.error(f"Failed to fetch symbols: {e}")
            return []
