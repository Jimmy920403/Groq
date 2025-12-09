import os
import requests
import json
from dotenv import load_dotenv


load_dotenv()

# 配置（可由 .env 覆寫）
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "groq-1")
GROQ_API_URL = os.getenv(
    "GROQ_API_URL", "https://api.groq.ai/v1/models/{model}/completions"
)
MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "512"))
TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.7"))


if not GROQ_API_KEY:
    raise SystemExit("請在環境變數中設定 GROQ_API_KEY（參考 .env.example）")


PERSONA_TEMPLATE = '''
你是「地獄廚神」風格的評審（Gordon）。你語氣直接、嚴厲、有時會使用粗口，但不得針對受保護群體或鼓勵暴力。
回應格式要求：
先輸出一段標記為 "THOUGHTS:"（模型的內心思考，允許描述評估細節與評判標準），
接著在新段落輸出標記為 "GORDON:"（對使用者的最終可閱讀回應，用戈登式語氣，可能帶有強烈批評與粗口）。

範例輸出：
THOUGHTS: 這道菜的火候沒掌握好，蛋白跟蛋黃分離，口感變水。
GORDON: 你到底在幹什麼？這個基本功都沒練還敢端出來，滾回去重做！

當你生成回應時，請同時遵守平台規範（不要生成仇恨言論或違法內容）。

現在，請閱讀使用者輸入並依照上述格式回應。'''


def call_groq_api(
    prompt: str,
    model: str = GROQ_MODEL,
    max_tokens: int = MAX_TOKENS,
    temperature: float = TEMPERATURE,
    api_key: str | None = None,
):
    """通用的 Groq API 呼叫範本 — 若官方 API 格式不同，請依照 Groq 文件調整此實作。

    目前預設向 `GROQ_API_URL.format(model=model)` 發送 POST，header 使用 Bearer token。
    """

    # Mock mode: 在無網路或要做本地測試時，設定環境變數 `GROQ_MOCK=true` 可回傳模擬回應
    mock_mode = os.getenv("GROQ_MOCK", "false").lower() in ("1", "true", "yes")
    if mock_mode:
        # 嘗試從 prompt 取一句摘要，並回傳含 THOUGHTS / GORDON 的模擬回應
        snippet = (prompt or "").strip().splitlines()[-1]
        thoughts = "THOUGHTS: 模擬回應 — 判斷食物調味與火候有明顯問題，需改進基本功。"
        gordon = (
            "GORDON: 這簡直是一災難，你的手藝像是剛學會拿鍋鏟，滾回去重練基本功！"
        )
        return f"{thoughts}\n\n{gordon}"

    url = GROQ_API_URL.format(model=model)
    used_key = api_key or GROQ_API_KEY
    if not used_key:
        raise RuntimeError("GROQ API key 未設定（請設定環境變數 GROQ_API_KEY 或透過參數傳入 api_key）")

    headers = {
        "Authorization": f"Bearer {used_key}",
        "Content-Type": "application/json",
    }

    payload = {
        # 許多 LLM REST API 使用 "input" 或 "prompt"；請依 Groq 官方文件調整
        "input": prompt,
        "max_output_tokens": max_tokens,
        "temperature": temperature,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    try:
        resp.raise_for_status()
    except Exception as e:
        print("API 請求失敗：", e)
        print("回應：", resp.text)
        return None

    data = resp.json()

    # 嘗試處理幾種常見的回應格式
    # 1) {"choices": [{"text": "..."}]}
    if isinstance(data, dict):
        if "choices" in data and isinstance(data["choices"], list):
            first = data["choices"][0]
            # 可能在 text 或 output
            for key in ("text", "output", "message", "content"):
                if key in first:
                    return first[key]
        # 2) {"output": [{"content": "..."}]}
        if "output" in data and isinstance(data["output"], list):
            parts = []
            for item in data["output"]:
                if isinstance(item, dict) and "content" in item:
                    parts.append(item["content"])
                elif isinstance(item, str):
                    parts.append(item)
            if parts:
                return "\n".join(parts)

    # fallback
    return json.dumps(data, ensure_ascii=False)


def build_prompt(user_input: str, history: list[str] | None = None) -> str:
    """把 persona 與使用者訊息整合成 prompt。可擴充加入對話歷史。
    """
    convo = "\n\n".join(history) if history else ""
    prompt = f"{PERSONA_TEMPLATE}\n\nCONTEXT:\n{convo}\n\nUSER: {user_input}\n\nRESPONSE:"
    return prompt


def parse_and_print(raw: str):
    """簡單解析 THOUGHTS / GORDON 區塊並輸出；若沒有標記則直接印出 raw。"""
    if not raw:
        print("(沒有回應)")
        return

    # 嘗試找 THOUGHTS: 與 GORDON: 標記
    lower = raw.lower()
    if "thoughts:" in lower or "gordon:" in lower:
        # 保持原始大小寫與段落，只用分割
        # 找到 THOUGHTS: 的起始位置
        try:
            # case-insensitive locate
            import re

            thoughts_match = re.search(r"(?i)thoughts:\s*", raw)
            gordon_match = re.search(r"(?i)gordon:\s*", raw)
            if thoughts_match and gordon_match:
                t_start = thoughts_match.end()
                g_start = gordon_match.start()
                thoughts_text = raw[t_start:g_start].strip()
                gordon_text = raw[gordon_match.end():].strip()
                print("--- THOUGHTS ---")
                print(thoughts_text)
                print("--- GORDON ---")
                print(gordon_text)
                return
        except Exception:
            pass

    # fallback: 直接印出
    print(raw)


def main():
    print("Gordon Bot（Groq） — 輸入 'exit' 離開")
    history: list[str] = []
    while True:
        try:
            user = input("你： ")
        except (KeyboardInterrupt, EOFError):
            print("\n離開")
            break
        if not user:
            continue
        if user.strip().lower() in ("exit", "quit"):
            print("離開")
            break

        prompt = build_prompt(user, history=history)
        print("-> 向 Groq 發送請求...")
        raw = call_groq_api(prompt)
        if raw is None:
            print("呼叫 API 發生錯誤，請檢查金鑰與網路。")
            continue

        parse_and_print(raw)

        # 簡單把使用者與模型回應加入歷史（方便 context）
        history.append(f"USER: {user}")
        history.append(f"MODEL: {raw}")


if __name__ == "__main__":
    main()
