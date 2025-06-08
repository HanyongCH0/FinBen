from optimizer import *

from pypfopt import EfficientFrontier, expected_returns, risk_models
from scipy.optimize import minimize
import yfinance as yf
import cvxpy as cp
import numpy as np

def minimize_volatility(assets, start, end):
    data = yf.download(assets, start=start, end=end, progress=False, auto_adjust=False)['Adj Close']
    data = data[assets]
    returns = data.pct_change().dropna()
    cov_matrix = returns.cov().values
    num_assets = len(assets)
    w = cp.Variable(num_assets)
    portfolio_volatility = cp.quad_form(w, cov_matrix)
    constraints = [cp.sum(w) == 1, w >= 0]
    problem = cp.Problem(cp.Minimize(portfolio_volatility), constraints)
    problem.solve(solver=cp.CPLEX)
    weights = w.value
    weight_dict = {assets[i]: round(weights[i], 4) for i in range(len(assets))}

    return weight_dict

def maximize_return(assets, start, end):
    data = yf.download(assets, start=start, end=end, progress=False, auto_adjust=False)['Adj Close']  
    data = data[assets]       
    returns = data.pct_change().dropna()   
    expected_returns = returns.mean().values
    num_assets = len(assets)  
    w = cp.Variable(num_assets)  
    portfolio_return = expected_returns @ w  
    constraints = [cp.sum(w) == 1, w >= 0]
    problem = cp.Problem(cp.Maximize(portfolio_return), constraints)
    problem.solve(solver=cp.CPLEX)
    weights = w.value
    weight_dict = {assets[i]: round(weights[i], 4) for i in range(len(assets))}

    return weight_dict

def maximize_sharpe_ratio(assets, start, end):
    data = yf.download(assets, start=start, end=end, progress=False, auto_adjust=False)['Adj Close']
    data = data[assets]
    mu = expected_returns.mean_historical_return(data)
    S = risk_models.sample_cov(data)
    ef = EfficientFrontier(mu, S)
    n_assets = len(mu)
    ef.add_constraint(lambda w: w.sum() == 1)
    ef.add_constraint(lambda w: w >= 0)
    w_opt = ef.max_sharpe()
    w_raw = ef.weights
    w_np = {assets[i]: round(np.float64(w_raw[i]),4) for i in range(len(assets))}

    return w_np

def minimize_maximum_drawdown(assets, start, end):
    data = yf.download(assets, start=start, end=end, progress=False, auto_adjust=False)['Adj Close']
    data = data[assets]
    returns = data.pct_change().dropna()
    
    def mdd_objective(weights):
        portfolio_returns = returns @ weights
        cumulative = (1 + portfolio_returns).cumprod()
        peak = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - peak) / peak
        mdd = drawdown.min()
        return abs(mdd)
        
    n_assets = len(assets)
    x0 = np.ones(n_assets) / n_assets
    bounds = [(0, 1)] * n_assets
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    result = minimize(
        mdd_objective,
        x0=x0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    weight_dict = {assets[i]: round(result.x[i], 4) for i in range(len(assets))}

    return weight_dict

def minimize_cvar(assets, start, end, alpha=0.95):
    data = yf.download(assets, start=start, end=end, progress=False, auto_adjust=False)['Adj Close']  
    data = data[assets]
    returns = data.pct_change().dropna()
    n, m = returns.shape
    w = cp.Variable(m)
    z = cp.Variable(n)
    VaR = cp.Variable()
    portfolio_returns = returns.values @ w
    loss = -portfolio_returns
    constraints = [
        cp.sum(w) == 1,
        w >= 0,
        z >= 0,
        z >= loss - VaR
    ]
    cvar = VaR + (1 / ((1 - alpha) * n)) * cp.sum(z)
    problem = cp.Problem(cp.Minimize(cvar), constraints)
    problem.solve()
    weights = w.value
    weight_dict = {assets[i]: round(weights[i], 4) for i in range(len(assets))}

    return weight_dict