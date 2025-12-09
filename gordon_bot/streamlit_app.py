import os
import streamlit as st
import requests
import re

# 設定頁面資訊
st.set_page_config(page_title="Gordon Bot（Groq）", layout="centered")

# --- 1. 定義輔助函式 (原本在 bot.py 的內容移到這裡) ---

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
    呼叫 Groq API (使用正確的 .com 網址)
    """
    # 修正重點：網址必須是 api.groq.com，且路徑包含 /openai
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# --- 2. Streamlit 主程式 ---

st.title("🔥 地獄廚神 Gordon — Groq 版")
st.write("輸入你的問題（示範保留強烈批評與粗口風格）")

# 取得 API key
env_key = os.getenv("GROQ_API_KEY")
streamlit_key = None
try:
    streamlit_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    streamlit_key = None

api_key = env_key or streamlit_key

# 判斷是否為 Mock 模式
mock_mode = os.getenv("GROQ_MOCK", "false").lower() in ("1", "true", "yes")

if mock_mode:
    st.info("🛠 使用 MOCK 模式：不會呼叫外部 API")
else:
    if api_key:
        st.success("✅ 已讀取到 API Key")
    else:
        st.warning("⚠️ 未找到 API Key。請在 Secrets 設定 GROQ_API_KEY")

# 修正重點：預設模型改為有效的 llama3-8b-8192，避免使用不存在的 groq-1
default_model = "llama3-8b-8192" 
model = os.getenv("GROQ_MODEL", st.secrets.get("GROQ_MODEL") if hasattr(st, "secrets") else default_model)

# 輸入區塊
user_input = st.text_area("你的問題 (例如：我看我的 Code 寫得怎樣？)", height=120)

if st.button("送出罵我") and user_input.strip():
    
    if not api_key and not mock_mode:
        st.error("無法執行：缺少 API Key")
        st.stop()

    with st.spinner("Gordon 正在準備罵人..."):
        messages = build_prompt(user_input)
        raw_response = ""

        try:
            if mock_mode:
                import time
                time.sleep(1)
                raw_response = "THOUGHTS: This input is garbage.\nGORDON: You call this code? My grandmother codes better than this!"
            else:
                raw_response = call_groq_api(messages, model=model, api_key=api_key)
        
        except Exception as e:
            st.error(f"API 呼叫失敗：{e}")
            raw_response = None

    if raw_response:
        # 解析回應
        st.subheader("完整回應")
        with st.expander("點擊展開原始內容"):
            st.code(raw_response)

        # 嘗試切割 THOUGHTS 和 GORDON
        # 使用更寬容的 Regex，避免大小寫或冒號格式導致失敗
        thoughts_match = re.search(r"THOUGHTS\s*[:\-]\s*(.*?)GORDON\s*[:\-]\s*(.*)", raw_response, re.DOTALL | re.IGNORECASE)
        
        if thoughts_match:
            thoughts_text = thoughts_match.group(1).strip()
            gordon_text = thoughts_match.group(2).strip()
            
            st.info(f"💭 **內心獨白 (Thoughts):**\n\n{thoughts_text}")
            st.error(f"🤬 **Gordon 暴怒:**\n\n{gordon_text}")
        else:
            st.warning("格式解析失敗，直接顯示內容：")
            st.write(raw_response)
