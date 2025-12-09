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
    使用三重保險強制模型使用繁體中文。
    """
    system_prompt = (
        "You are Gordon Ramsay. You are analyzing code or a situation. "
        "First, think step-by-step about the flaws in a 'THOUGHTS' section. "
        "Then, roast the user aggressively in a 'GORDON' section. "
        "Use harsh language, insults, and be extremely critical. "
        
        "--- CRITICAL LANGUAGE RULE ---"
        "1. You MUST use Traditional Chinese (繁體中文) for the ENTIRE response."
        "2. Do NOT use Simplified Chinese characters (e.g., use '體' NOT '体', use '麼' NOT '么')."
        "3. Use Taiwan vocabulary and phrasing (台灣用語)."
        
        "Format your response exactly like this:\n"
        "THOUGHTS: [Your internal analysis in Traditional Chinese]\n"
        "GORDON: [Your response to the user in Traditional Chinese]"
    )
    
    # 技巧：在使用者輸入的後面，偷偷幫他加上「請用繁體中文」的指令
    # 這樣模型會認為是使用者當下的強烈要求，權重會比 System Prompt 更高
    user_content = f"{user_text} (Important: Please reply strictly in Traditional Chinese 繁體中文)"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]
    return messages

def call_groq_api(messages, model, api_key):
    """
    呼叫 Groq API
    """
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
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# --- 3. Streamlit 主程式介面 ---

st.title("🔥 地獄廚神 Gordon — Groq 版")
st.write("輸入你的問題（示範保留強烈批評與粗口風格）")

# 步驟 A: 取得 API Key
env_key = os.getenv("GROQ_API_KEY")
streamlit_key = None
try:
    streamlit_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    pass

api_key = env_key or streamlit_key

# 步驟 B: 設定模型 (CRITICAL UPDATE: 使用最新的 Llama 3.3)
# 舊的 llama3-8b-8192 已被淘汰
current_model = "llama-3.3-70b-versatile"

# 步驟 C: 檢查 Mock 模式
mock_mode = os.getenv("GROQ_MOCK", "false").lower() in ("1", "true", "yes")

if mock_mode:
    st.info("🛠 使用 MOCK 模式：不會呼叫外部 API")
else:
    if api_key:
        st.success(f"✅ 已讀取到 API Key (使用模型: {current_model})")
    else:
        st.warning("⚠️ 未找到 API Key。請在 Streamlit Cloud 的 'Settings -> Secrets' 中設定 GROQ_API_KEY。")

# 步驟 D: 使用者輸入區
user_input = st.text_area("你的問題 (例如：我的 Code 寫得好嗎？)", height=120)

if st.button("送出罵我") and user_input.strip():
    
    if not api_key and not mock_mode:
        st.error("❌ 無法執行：缺少 API Key，請先設定 Secrets。")
        st.stop()

    with st.spinner("Gordon 正在準備罵人..."):
        raw_response = ""
        try:
            if mock_mode:
                import time
                time.sleep(1)
                raw_response = "THOUGHTS: Simulation.\nGORDON: This is fake!"
            else:
                raw_response = call_groq_api(build_prompt(user_input), model=current_model, api_key=api_key)
        
        except Exception as e:
            st.error(f"API 呼叫失敗：{e}")
            raw_response = None

    # 步驟 E: 解析並顯示結果
    if raw_response:
        with st.expander("查看原始回應 (Raw Response)"):
            st.code(raw_response)

        pattern = r"THOUGHTS\s*[:\-]\s*(.*?)GORDON\s*[:\-]\s*(.*)"
        match = re.search(pattern, raw_response, re.DOTALL | re.IGNORECASE)
        
        if match:
            thoughts_text = match.group(1).strip()
            gordon_text = match.group(2).strip()
            
            st.info(f"💭 **內心獨白 (Thoughts):**\n\n{thoughts_text}")
            st.error(f"🤬 **Gordon 暴怒:**\n\n{gordon_text}")
        else:
            st.warning("模型回應未符合格式，直接顯示內容：")
            st.write(raw_response)
