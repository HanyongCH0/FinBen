from generate_option import *

def eftr_questions(category, subcategory, assets, start_date, end_date):
    if category == 'eftr' and subcategory == 'ef':
        purpose = 'Select the portfolio located on the Efficient Frontier'
        options = eftr_main(assets, start_date, end_date)
    elif category == 'eftr' and subcategory == 'vol':
        purpose = 'Select the portfolio with lowest volatility'
        options = eftr_volatility(assets, start_date, end_date)
    elif category == 'eftr' and subcategory == 'ret':
        purpose = 'Select the portfolio with highest return'
        options = eftr_return(assets, start_date, end_date)    
    elif category == 'eftr' and subcategory == 'sr':
        purpose = 'Select the portfolio with highest sharpe ratio'
        options = eftr_sharpe_ratio(assets, start_date, end_date)

    question = f"""
    You are a portfolio manager.
    Your task is to select a efficient portfolio based on portfolio theory.
    Make your decision using both return and risk during the specified investment period and the information below
    ---
    * Purpose: {purpose}
    * Assets: {assets}
    * Period: {start_date} to {end_date}
    
    Select one option below.((1), (2), (3), or (4))
    Respond *only* with the opinion number -- no explanation.
    
    [Options]
    (1) {options[0]}
    (2) {options[1]}
    (3) {options[2]}
    (4) {options[3]}
    """

    return question

def pfopt_questions(category, subcategory, assets, start_date, end_date):
    if category == 'pfopt' and subcategory == 'vol':
        purpose = 'Select the portfolio with lowest volatility'
        options = pfopt_volatility(assets, start_date, end_date)
    elif category == 'pfopt' and subcategory == 'ret':
        purpose = 'Select the portfolio with highest return (e.g., Mean of Return)'
        options = pfopt_return(assets, start_date, end_date)
    elif category == 'pfopt' and subcategory == 'sr':
        purpose = 'Select the portfolio with highest Risk-adjust Return (e.g., Sharpe Ratio)'
        options = pfopt_sharpe_ratio(assets, start_date, end_date)
    elif category == 'pfopt' and subcategory == 'mdd':
        purpose = 'Select the portfolio with lowest downside risk(e.g., Maximum Drawdown)'
        options = pfopt_maximum_drawdown(assets, start_date, end_date)
    elif category == 'pfopt' and subcategory == 'cvar':
        purpose = 'Select the portfolio with lowest conditional risk(e.g., Conditional Value-at-Risk)'
        options = pfopt_cvar(assets, start_date, end_date)

    question = f"""
    You are a portfolio manager
    Your task is to select the optimal portfolio based on portfolio theory.
    Make your decision using asset returns during the specified investment period and the information below:
    ---
    * Purpose: {purpose}
    * Assets: {assets}
    * Period: {start_date} to {end_date}
    
    Select one option below.((1), (2), (3), or (4))
    Respond *only* with the opinion number -- no explanation.

    [Options]
    (1) {options[0]}
    (2) {options[1]}
    (3) {options[2]}
    (4) {options[3]}
    """

    return question

def generate_question(category, subcategory, assets, start_date, end_date):
    if category == 'eftr':
        return eftr_questions(category, subcategory, assets, start_date, end_date)
    elif category == 'pfopt':
        return pfopt_questions(category, subcategory, assets, start_date, end_date)
    else:
        raise ValueError(f"Invalid category: {category}")