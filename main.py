from prompt import *
from utils import *

# assets = ['BND', 'GSG', 'VTI']
# model = ['GPT', 'GEMINI', 'LLAMA']
# category = ['eftr', 'pfopt']
# subcategory_eftr = ['ef', 'vol', 'ret', 'sr']
# subcategory_pfopt = ['vol', 'ret', 'sr', 'mdd', 'cvar']
assets = ['BND', 'GSG', 'VTI']
category = 'pfopt'
subcategory = 'ret'
start, end = random_date()

prompt = generate_question(category, subcategory, assets, start, end)
print(prompt)