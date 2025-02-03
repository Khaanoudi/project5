import plotly.graph_objects as go
import pandas as pd

def create_candlestick_chart(df: pd.DataFrame) -> go.Figure:
    """Create candlestick chart using plotly"""
    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    
    fig.update_layout(
        title="Stock Price Chart",
        yaxis_title="Price",
        xaxis_title="Date"
    )
    
    return fig
