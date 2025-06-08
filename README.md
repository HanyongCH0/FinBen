# Evaluating LLMs Understanding of Portfolio Theory

## Example
![image](https://github.com/user-attachments/assets/ef894538-2b9f-4c97-93c1-77599efe40dc)

## Abstract
PortBench is a benchmark generation framework designed to evaluate investment decision-making capabilities based on portfolio theory.
Unlike existing financial benchmarks that primarily focus on natural language understanding, PortBench aims to provide a more practical evaluation grounded in real-world financial reasoning.
It assesses whether language models can perform asset allocation tasks based on financial theory, moving beyond simple language comprehension.
Users can generate and evaluate customized benchmarks flexibly by combining a variety of variables to suit their specific needs.

PortBench currently supports evaluation on two types of tasks: Efficient Frontier and Portfolio Optimization.
All evaluations are conducted in a zero-shot setting, without task-specific fine-tuning.

In Task 1 (Efficient Frontier), the models are evaluated on their ability to distinguish efficient portfolios.
Gemini and LLaMA outperforms GPT, showing the highest accuracy in identifying portfolios on the efficient frontier.
GPT, in contrast, demonstrates relatively low performance in this area.

In Task 2 (Portfolio Optimization), GPT outperforms Gemini and LLaMA, particularly excelling in risk-based objectives such as minimizing volatility or drawdown.
Gemini shows strength in return-based objectives, while all models struggle with composite objectives like maximizing the Sharpe Ratio, which require balancing both risk and return.

We plan to extend PortBench beyond its current multiple-choice format by introducing open-ended (free-form) and explanatory response tasks.
This will enable us to evaluate not only whether an LLM selects the correct portfolio, but also why it made that choice—assessing its reasoning and decision-making process.

In addition to portfolio optimization tasks, PortBench will be expanded to cover a broader range of financial theories, including:

- Capital Asset Pricing Model (CAPM)
- Multi-Factor Models (e.g., Fama-French 3-factor model)
- Other classical and modern asset pricing frameworks

Through this expansion, PortBench aims to become a comprehensive benchmark for evaluating the financial reasoning capabilities of large language models (LLMs).

## Results
### All questions (28,500 questions)
![image](https://github.com/user-attachments/assets/b6f45588-887a-470e-b5a8-7c861d708b8e)

### - Minimize volatility (5,700 questions)
![image](https://github.com/user-attachments/assets/8929dcdd-f511-472f-9cc0-45d1bf627c78)

### - Maximize return  (5,700 questions)
![image](https://github.com/user-attachments/assets/def31753-c62e-4edc-9d99-ff8b3ee0732b)

### - Maximize sharpe ratio (5,700 questions)
![image](https://github.com/user-attachments/assets/6d1455ce-a9e7-448f-9c37-88bdebe28190)

### - Minimize MDD (5,700 questions)
![image](https://github.com/user-attachments/assets/74f9cb00-42f4-4ed1-b812-344db1d8f542)

### - Minimize CVaR (5,700 questions)
![image](https://github.com/user-attachments/assets/a611fcfc-7868-4688-92a0-7534f752a52a)


## Usage
```
python main.py
```

## Parameters
- `assets`, default=`BND`,`GSG`,`VTI`, type=list, options: `VEA`, `VEA`, `VWO`, `VNQ`, ..., etc
  - Note: You may freely add any assets of your choice
- `category`, type=string, options: `eftr`, `pfopt`
  - `eftr`, Efficient Frontier
  - `pfopt`, Portfolio Optimization
- `subcategory`, type=string, options: `ef`, `vol`, `ret`, `sr`, `mdd`, `cvar`
  - `eftr`
    - `ef`: Select the portfolio located on the Efficient Frontier
    - `vol`: Select the portfolio with lowest volatility
    - `ret`: Select the portfolio with highest return
    - `sr`: Select the portfolio with highest sharpe ratio
  - `pfopt`
    - `vol`: Select the portfolio with lowest volatility
    - `ret`: Select the portfolio with highest return (e.g., Mean of Return)
    - `sr`: Select the portfolio with highest Risk-adjust Return (e.g., Sharpe Ratio)
    - `mdd`: Select the portfolio with lowest downside risk(e.g., Maximum Drawdown)
    - `cvar`: Select the portfolio with lowest conditional risk(e.g., Conditional Value-at-Risk)
- `date`, type=datetime
  - Note: Randomly selected 5-year period between 2007-01-01 and 2020-12-31

## Citation

## Contact
whgksdyd1@korea.ac.kr
