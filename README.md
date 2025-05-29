# Evaluating LLMs Understanding of Portfolio Theory
![image](https://github.com/user-attachments/assets/85d9d99c-1de8-435f-a46d-ccca12cb0a24)

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
### Task1: Efficient Frontier
![image](https://github.com/user-attachments/assets/9967ccdc-7d3f-4d03-9ecd-191d5480ede4)

### Task2: Portfolio Optimization
![image](https://github.com/user-attachments/assets/465f8212-1dee-4da1-8b2c-8cc58440bbfc)

## Usage

## Citation

## Contact
whgksdyd1@korea.ac.kr
