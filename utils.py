import random
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def random_date():
    start_year = random.randint(2007, 2020)
    start_month = random.randint(1, 12)
    start_date = datetime(start_year, start_month, 1)
    end_date = start_date + timedelta(days=5 * 365)
    
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def portfolio_metrics(weights, returns, purpose='volatility'):
    port_returns = returns @ weights
    # Return
    avg_return = port_returns.mean()
    # Volatility
    volatility = port_returns.std()
    # SR
    sharpe = avg_return / volatility if volatility > 0 else 0
    # MDD
    cumulative = (1 + port_returns).cumprod()
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak
    mdd = abs(drawdown.min())
    # CVaR
    alpha = 0.95
    losses = -port_returns
    var = np.quantile(losses, alpha)
    cvar = losses[losses >= var].mean()

    if purpose == 'volatility':
        return volatility
    elif purpose == 'return':
        return avg_return
    elif purpose == 'sharpe ratio':
        return sharpe
    elif purpose == 'mdd':
        return mdd
    elif purpose == 'cvar':
        return cvar
    
def get_returns(assets, start_date, end_date):
    data = yf.download(assets, start=start_date, end=end_date, progress=False, auto_adjust=False)['Adj Close']
    returns = data.pct_change().dropna()

    return returns

def generate_random_weights(n, num_assets):
    return np.random.dirichlet(alpha=np.ones(num_assets), size=n)