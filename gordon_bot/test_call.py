from dotenv import load_dotenv
from bot import build_prompt, call_groq_api
import os


def main():
    load_dotenv()
    prompt = build_prompt("請用一句話嚴厲評論這道菜，並保留戈登風格。")
    print("--- Prompt (截段) ---")
    print(prompt[:400])
    print("--- 呼叫 Groq API ---")
    resp = call_groq_api(prompt)
    print("--- Response ---")
    print(resp)


if __name__ == "__main__":
    main()
