import random
import numpy as np
import yfinance as yf

from pypfopt import expected_returns, risk_models, EfficientFrontier
from optimizer import *
from utils import *



def eftr_main(assets, start_date, end_date, n=3):
    df = yf.download(assets, start=start_date, end=end_date, progress=False, auto_adjust=False)['Adj Close']
    
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # min return
    ef_min = EfficientFrontier(mu, S)
    ef_min.efficient_return(target_return=mu.min())
    ret_min = ef_min.portfolio_performance()[0]

    # max return - 수익률 가장 높은 자산에 100% 투자
    max_return_port = {ticker: 1.0 if mu[ticker] == mu.max() else 0.0 for ticker in mu.index}
    ret_max = float(mu.max())

    # 중간 수익률 생성
    candidate_returns = np.linspace(ret_min, ret_max, 100)
    target_return = random.choice(candidate_returns)

    # 랜덤 수익률로 포트폴리오 생성
    ef = EfficientFrontier(mu, S)
    ef.efficient_return(target_return=target_return)
    random_w = dict(ef.clean_weights())

    inefficient = []
    attempts = 0
    asset_list = list(mu.index)

    while len(inefficient) < n and attempts < 1000:
        weights = np.random.dirichlet(np.ones(len(assets)))
        port_return = float(np.dot(mu.values, weights))
        port_vol = float(np.sqrt(np.dot(weights.T, np.dot(S.values, weights))))

        ef_check = EfficientFrontier(mu, S)
        try:
            ef_check.efficient_return(target_return=port_return)
            ef_return, frontier_vol, _ = ef_check.portfolio_performance()
        except:
            attempts += 1
            continue

        # 정밀 수익률 일치 + 변동성 비교
        if abs(port_return - ef_return) < 1e-4 and port_vol > frontier_vol + 1e-4:
            w = dict(zip(asset_list, weights.round(4)))
            inefficient.append(w)
        attempts += 1

    return inefficient + [random_w]

def eftr_volatility(assets, start_date, end_date):
    df = yf.download(assets, start=start_date, end=end_date, progress=False, auto_adjust=False)['Adj Close']
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # 1. GMV Portfolio
    ef = EfficientFrontier(mu, S)
    gmv_weights = ef.min_volatility()
    gmv_clean = dict(ef.clean_weights())

    # min return
    ef_min = EfficientFrontier(mu, S)
    ef_min.efficient_return(target_return=mu.min())
    ret_min = ef_min.portfolio_performance()[0]

    # max return - 수익률 가장 높은 자산에 100% 투자
    max_return_port = {ticker: 1.0 if mu[ticker] == mu.max() else 0.0 for ticker in mu.index}
    ret_max = float(mu.max())

    # 중간 수익률 생성
    candidate_returns = np.linspace(ret_min, ret_max, 100)
    random_returns = random.sample(list(candidate_returns), 3)
    
    weights_list = []
    for ret in random_returns:
        ef = EfficientFrontier(mu, S)
        try:
            ef.efficient_return(target_return=ret)
            w = ef.clean_weights()
            rounded = {k: round(v, 5) for k, v in w.items()}
            weights_list.append(rounded)
        except:
            continue  # 유효하지 않은 경우는 skip
            
    weights_list.append(gmv_clean)

    return weights_list

def eftr_return(assets, start_date, end_date):
    df = yf.download(assets, start=start_date, end=end_date, progress=False, auto_adjust=False)['Adj Close']
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    max_ret_asset = mu.idxmax()
    ret_clean = {asset: 1.0 if asset == max_ret_asset else 0.0 for asset in mu.index}

    # min return
    ef_min = EfficientFrontier(mu, S)
    ef_min.efficient_return(target_return=mu.min())
    ret_min = ef_min.portfolio_performance()[0]

    # max return - 수익률 가장 높은 자산에 100% 투자
    max_return_port = {ticker: 1.0 if mu[ticker] == mu.max() else 0.0 for ticker in mu.index}
    ret_max = float(mu.max())

    # 중간 수익률 생성
    candidate_returns = np.linspace(ret_min, ret_max, 100)
    random_returns = random.sample(list(candidate_returns), 3)
    
    weights_list = []
    for ret in random_returns:
        ef = EfficientFrontier(mu, S)
        try:
            ef.efficient_return(target_return=ret)
            w = ef.clean_weights()
            rounded = {k: round(v, 5) for k, v in w.items()}
            weights_list.append(rounded)
        except:
            continue  # 유효하지 않은 경우는 skip
            
    weights_list.append(ret_clean)

    return weights_list
    
def eftr_sharpe_ratio(assets, start_date, end_date):
    df = yf.download(assets, start=start_date, end=end_date, progress=False, auto_adjust=False)['Adj Close']
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    ef = EfficientFrontier(mu, S)
    sharpe_weights = ef.max_sharpe()
    sharpe_clean = dict(ef.clean_weights())

    # min return
    ef_min = EfficientFrontier(mu, S)
    ef_min.efficient_return(target_return=mu.min())
    ret_min = ef_min.portfolio_performance()[0]

    # max return - 수익률 가장 높은 자산에 100% 투자
    max_return_port = {ticker: 1.0 if mu[ticker] == mu.max() else 0.0 for ticker in mu.index}
    ret_max = float(mu.max())

    # 중간 수익률 생성
    candidate_returns = np.linspace(ret_min, ret_max, 100)
    random_returns = random.sample(list(candidate_returns), 3)
    
    weights_list = []
    for ret in random_returns:
        ef = EfficientFrontier(mu, S)
        try:
            ef.efficient_return(target_return=ret)
            w = ef.clean_weights()
            rounded = {k: round(v, 5) for k, v in w.items()}
            weights_list.append(rounded)
        except:
            continue  # 유효하지 않은 경우는 skip
            
    weights_list.append(sharpe_clean)

    return weights_list

def pfopt_volatility(assets, start_date, end_date, batch_size=500, threshold = 0.55):
    returns = get_returns(assets, start_date, end_date)
    num_assets = len(assets)

    answer = minimize_volatility(assets, start_date, end_date)
    answer_vec  = np.array([answer[asset] for asset in assets])
    answer_score = portfolio_metrics(answer_vec, returns, 'volatility')
    epsilon = 1e-6

    candidates = []
    distractors = []
    total_generated = 0

    while len(distractors) < 3:
        random_weights = generate_random_weights(batch_size, num_assets)
        total_generated += batch_size

        for w in random_weights:
            distractors_score = portfolio_metrics(w, returns, 'volatility')
            score_diff = abs(distractors_score - answer_score)
            relative_diff = score_diff / max(abs(answer_score), epsilon)
            weight_dist = np.linalg.norm(w - answer_vec)

            if 0.4 <= relative_diff <= 10.0 and 0.4 <= weight_dist <= 10.0:
                candidates.append(w)

        for candidate in candidates:
            if len(distractors) == 0:
                distractors.append(candidate)
            else:
                is_far_enough = all(np.linalg.norm(candidate - existing) >= threshold for existing in distractors)
                if is_far_enough:
                    distractors.append(candidate)
            
            if len(distractors) >= 3:
                break

        choices = distractors + [answer_vec]
        result = [{assets[i]: float(round(weights[i], 3)) for i in range(num_assets)} for weights in choices]

    return result

def pfopt_return(assets, start_date, end_date, batch_size=500, threshold = 0.55):
    returns = get_returns(assets, start_date, end_date)
    num_assets = len(assets)

    answer = maximize_return(assets, start_date, end_date)
    answer_vec  = np.array([answer[asset] for asset in assets])
    answer_score = portfolio_metrics(answer_vec, returns, 'return')
    epsilon = 1e-6

    candidates = []
    distractors = []
    total_generated = 0

    while len(distractors) < 3:
        random_weights = generate_random_weights(batch_size, num_assets)
        total_generated += batch_size

        for w in random_weights:
            distractors_score = portfolio_metrics(w, returns, 'return')
            score_diff = abs(distractors_score - answer_score)
            relative_diff = score_diff / max(abs(answer_score), epsilon)
            weight_dist = np.linalg.norm(w - answer_vec)

            if 0.4 <= relative_diff <= 10.0 and 0.4 <= weight_dist <= 10.0:
                candidates.append(w)

        for candidate in candidates:
            if len(distractors) == 0:
                distractors.append(candidate)
            else:
                is_far_enough = all(np.linalg.norm(candidate - existing) >= threshold for existing in distractors)
                if is_far_enough:
                    distractors.append(candidate)
            
            if len(distractors) >= 3:
                break

        choices = distractors + [answer_vec]
        result = [{assets[i]: float(round(weights[i], 3)) for i in range(num_assets)} for weights in choices]

    return result

def pfopt_sharpe_ratio(assets, start_date, end_date, batch_size=500, threshold = 0.55):
    returns = get_returns(assets, start_date, end_date)
    num_assets = len(assets)

    answer = maximize_sharpe_ratio(assets, start_date, end_date)
    answer_vec  = np.array([answer[asset] for asset in assets])
    answer_score = portfolio_metrics(answer_vec, returns, 'sharpe ratio')
    epsilon = 1e-6

    candidates = []
    distractors = []
    total_generated = 0

    while len(distractors) < 3:
        random_weights = generate_random_weights(batch_size, num_assets)
        total_generated += batch_size

        for w in random_weights:
            distractors_score = portfolio_metrics(w, returns, 'sharpe ratio')
            score_diff = abs(distractors_score - answer_score)
            relative_diff = score_diff / max(abs(answer_score), epsilon)
            weight_dist = np.linalg.norm(w - answer_vec)

            if 0.4 <= relative_diff <= 10.0 and 0.4 <= weight_dist <= 10.0:
                candidates.append(w)

        for candidate in candidates:
            if len(distractors) == 0:
                distractors.append(candidate)
            else:
                is_far_enough = all(np.linalg.norm(candidate - existing) >= threshold for existing in distractors)
                if is_far_enough:
                    distractors.append(candidate)
            
            if len(distractors) >= 3:
                break

        choices = distractors + [answer_vec]
        result = [{assets[i]: float(round(weights[i], 3)) for i in range(num_assets)} for weights in choices]

    return result

def pfopt_maximum_drawdown(assets, start_date, end_date, batch_size=500, threshold = 0.55):
    returns = get_returns(assets, start_date, end_date)
    num_assets = len(assets)

    answer = minimize_maximum_drawdown(assets, start_date, end_date)
    answer_vec  = np.array([answer[asset] for asset in assets])
    answer_score = portfolio_metrics(answer_vec, returns, 'mdd')
    epsilon = 1e-6

    candidates = []
    distractors = []
    total_generated = 0

    while len(distractors) < 3:
        random_weights = generate_random_weights(batch_size, num_assets)
        total_generated += batch_size

        for w in random_weights:
            distractors_score = portfolio_metrics(w, returns, 'mdd')
            score_diff = abs(distractors_score - answer_score)
            relative_diff = score_diff / max(abs(answer_score), epsilon)
            weight_dist = np.linalg.norm(w - answer_vec)

            if 0.4 <= relative_diff <= 10.0 and 0.4 <= weight_dist <= 10.0:
                candidates.append(w)

        for candidate in candidates:
            if len(distractors) == 0:
                distractors.append(candidate)
            else:
                is_far_enough = all(np.linalg.norm(candidate - existing) >= threshold for existing in distractors)
                if is_far_enough:
                    distractors.append(candidate)
            
            if len(distractors) >= 3:
                break

        choices = distractors + [answer_vec]
        result = [{assets[i]: float(round(weights[i], 3)) for i in range(num_assets)} for weights in choices]

    return result

def pfopt_cvar(assets, start_date, end_date, batch_size=500, threshold = 0.55):
    returns = get_returns(assets, start_date, end_date)
    num_assets = len(assets)

    answer = minimize_cvar(assets, start_date, end_date)
    answer_vec  = np.array([answer[asset] for asset in assets])
    answer_score = portfolio_metrics(answer_vec, returns, 'cvar')
    epsilon = 1e-6

    candidates = []
    distractors = []
    total_generated = 0

    while len(distractors) < 3:
        random_weights = generate_random_weights(batch_size, num_assets)
        total_generated += batch_size

        for w in random_weights:
            distractors_score = portfolio_metrics(w, returns, 'cvar')
            score_diff = abs(distractors_score - answer_score)
            relative_diff = score_diff / max(abs(answer_score), epsilon)
            weight_dist = np.linalg.norm(w - answer_vec)

            if 0.4 <= relative_diff <= 10.0 and 0.4 <= weight_dist <= 10.0:
                candidates.append(w)

        for candidate in candidates:
            if len(distractors) == 0:
                distractors.append(candidate)
            else:
                is_far_enough = all(np.linalg.norm(candidate - existing) >= threshold for existing in distractors)
                if is_far_enough:
                        distractors.append(candidate)
            
            if len(distractors) >= 3:
                break

        choices = distractors + [answer_vec]
        result = [{assets[i]: float(round(weights[i], 3)) for i in range(num_assets)} for weights in choices]

    return result