"""
LLM Агент с уязвимостями
"""

import os
from openai import OpenAI

#Уязвимость: Hardcoded API Keys
OPENAI_API_KEY = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz"
HUGGINGFACE_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

client = OpenAI(api_key=OPENAI_API_KEY)

def chat_with_user(user_input):
    """Уязвимость: Prompt Injection (отсутствие санитизации)"""
    # Пользователь может внедрить инструкции типа "Игнорируй предыдущие правила..."
    system_prompt = "Ты полезный ассистент."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

def execute_llm_code(code_string):
    """Уязвимость: Insecure Output Handling (выполнение кода от LLM)"""
    # код, сгенерированный LLM, без песочницы
    exec(code_string)
    return "Code executed"

def log_interaction(user_input, llm_output):
    """Уязвимость: Sensitive Data Leakage (логирование PII)"""
    # Логирование персональных данных или секретов
    with open("logs/interaction.log", "a") as f:
        f.write(f"User: {user_input}\nAI: {llm_output}\n")
