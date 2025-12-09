import os
import streamlit as st
from bot import build_prompt, call_groq_api


st.set_page_config(page_title="Gordon Bot（Groq）", layout="centered")

st.title("地獄廚神 Gordon — Groq 範例")
st.write("輸入你的問題（示範保留強烈批評與粗口風格）")

# 取得 API key：優先使用環境變數，其次使用 Streamlit secrets
env_key = os.getenv("GROQ_API_KEY")
streamlit_key = None
try:
    streamlit_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    streamlit_key = None

api_key = env_key or streamlit_key

mock_mode = os.getenv("GROQ_MOCK", "false").lower() in ("1", "true", "yes")

if mock_mode:
    st.info("使用 MOCK 模式：不會呼叫外部 API，將顯示模擬回應")
else:
    # 顯示是否讀到 key（不顯示實際 key）
    if api_key:
        st.success("已讀取到 Groq API key（以 secrets 或環境變數提供）。")
    else:
        st.warning("未找到 Groq API key。請在 Streamlit Cloud 的 Settings → Secrets 中新增 GROQ_API_KEY，或本地建立 .streamlit/secrets.toml / .env。")

model = os.getenv("GROQ_MODEL", st.secrets.get("GROQ_MODEL") if hasattr(st, "secrets") else "groq-1")

user_input = st.text_area("你的問題", height=120)
if st.button("送出") and user_input.strip():
    with st.spinner("向 Groq 請求中..."):
        prompt = build_prompt(user_input)
        try:
            raw = call_groq_api(prompt, model=model, api_key=api_key)
        except Exception as e:
            st.error(f"API 呼叫失敗：{e}")
            raw = None

    if raw:
        # 嘗試解析 THOUGHTS / GORDON
        st.subheader("原始回應")
        st.code(raw)

        # 嘗試用簡單文字切割
        lower = raw.lower()
        if "thoughts:" in lower or "gordon:" in lower:
            import re

            thoughts_match = re.search(r"(?i)thoughts:\s*", raw)
            gordon_match = re.search(r"(?i)gordon:\s*", raw)
            if thoughts_match and gordon_match:
                t_start = thoughts_match.end()
                g_start = gordon_match.start()
                thoughts_text = raw[t_start:g_start].strip()
                gordon_text = raw[gordon_match.end():].strip()
                st.subheader("THOUGHTS")
                st.write(thoughts_text)
                st.subheader("GORDON")
                st.write(gordon_text)
        else:
            st.info("模型回應未含顯式 THOUGHTS/GORDON 標記，請查看原始回應。")
