import os
import streamlit as st
import requests
import re

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="Gordon Bot（Groq）", layout="centered")

# --- 2. 定義輔助函式 (API 與 Prompt 處理) ---

def build_prompt(user_text):
    """
    建立包含 System Prompt 的訊息列表，
    強制模型使用 THOUGHTS / GORDON 格式回應。
    """
    system_prompt = (
        "You are Gordon Ramsay. You are analyzing code or a situation. "
        "First, think step-by-step about the flaws in a 'THOUGHTS' section. "
        "Then, roast the user aggressively in a 'GORDON' section. "
        "Use harsh language, insults, and be extremely critical. "
        "Format your response exactly like this:\n"
        "THOUGHTS: [Your internal analysis]\n"
        "GORDON: [Your response to the user]"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_text}
    ]
    return messages

def call_groq_api(messages, model, api_key):
    """
    呼叫 Groq API (使用正確的 .com 網址與標準 OpenAI 格式)
    """
    # 修正：網址必須是 api.groq.com，且路徑包含 /openai
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    # 設定 30 秒 timeout 避免卡死
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        # 如果出錯，拋出詳細錯誤訊息以便除錯
        raise Exception(f"Error {response.status_code}: {response.text}")

# --- 3. Streamlit 主程式介面 ---

st.title("🔥 地獄廚神 Gordon — Groq 版")
st.write("輸入
