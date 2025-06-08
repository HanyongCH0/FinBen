import os
import json
import openai
from llamaapi import LlamaAPI
import google.generativeai as genai

def GPT(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model="gpt-4o", messages=messages)

    return response.choices[0].message.content

def GEMINI(prompt):
    model = genai.GenerativeModel('gemini-1.5-pro') 
    response = model.generate_content(prompt)

    return response.text

def LLAMA(prompt):
    api_request = {"model": "llama3.1-70b", "messages": [{"role": "user", "content": prompt}]}
    response = llama.run(api_request)
    response = json.loads(response.text)
    
    return response["choices"][0]["message"]["content"]