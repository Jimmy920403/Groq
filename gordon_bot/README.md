# 地獄廚神（Gordon）對話機器人 — Groq 範例

這是一個以 Groq API 為主、模仿「地獄廚神」風格的簡單 Python 對話機器人範例。程式會把使用者輸入包在一個 persona prompt 裡，要求模型回傳「內心想法（THOUGHTS）+ 最終回應（GORDON）」兩段文字，以利觀察類似 chain-of-thought 的輸出。

重要：請勿把真實 API key 提交到版本控制系統（例如 GitHub）。請使用環境變數或 CI 的 secrets 來保存金鑰。

先決條件
- Python 3.11
- 已申請 Groq API key（放在 `GROQ_API_KEY`）

安裝

在 PowerShell 中（假設在 `c:\HW4-4\gordon_bot`）：

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

設定 API key

複製範例檔案並填入金鑰：

```powershell
copy .env.example .env
# 然後用編輯器把 .env 裡的 GROQ_API_KEY 改成你自己的 key
```

使用說明

```powershell
python bot.py
```

輸入提問（輸入 `exit` 或 `quit` 可離開）。程式會把模型回傳內容切分成 `THOUGHTS:` 與 `GORDON:`（若模型輸出包含該標記）。

端點說明與可替換部分
- `GROQ_API_URL` 預設為 `https://api.groq.ai/v1/models/{model}/completions`，若 Groq 官方文件有不同的路徑或參數請依照官方文件修改。
- `GROQ_MODEL` 可改為 Groq 提供的免費模型名稱（例如 `groq-1` 或他們當時提供的 free-tier model）。

內容警告
- 你要求保留強烈批評與粗口；程式會把 persona 設為嚴厲帶罵的風格。請注意遵守平台使用規範與當地法規，不要要求模型生成仇恨或違法內容。

如果你要我：
- 幫你把 Demo04 的原始檔案精確搬進來並做客製化，請允許我從網路複製或上傳原始碼（目前工作區沒有該 repo 的檔案）。
- 或是要我直接在此工作區內把範例調整成更完整的服務（包含 unit-test、Dockerfile、或 GitHub Actions），請告訴我要擴充哪些項目。

部署到 GitHub + Streamlit（密鑰與建議）

- 不要把 API key 提交到 GitHub。請把金鑰放在以下位置之一：
	- 本地測試：在專案根目錄建立 `.env`（範例檔為 `.env.example`），並把 `.env` 加入 `.gitignore`。
	- Streamlit Cloud：在 Streamlit Cloud 的 app Secrets (Settings → Secrets) 中新增 `GROQ_API_KEY`。部署後 Streamlit 會把這些 secrets 暴露給你的應用為 `st.secrets`。
	- GitHub Actions / 其他雲端 CI：在 GitHub repository 的 Settings → Secrets 中設定 `GROQ_API_KEY`，CI 工作流程再以環境變數傳給執行步驟。

- Streamlit 本地模擬：可以在本地建立 `.streamlit/secrets.toml`（但請不要提交到版本控制）：

```toml
# .streamlit/secrets.toml
GROQ_API_KEY = "your_real_key_here"
GROQ_MODEL = "groq-1"
```

- Groq 模型建議：
	- 常見且效果好的為 `groq-1`（若 Groq 提供更進階的付費模型，可根據官方文件選擇）。
	- 若想用免費模型或測試，可使用 Groq 提供的 free-tier model（名稱依 Groq 文件為準）。
	- 我建議先使用能產出較長回應的模型（例如 `groq-1`）來觀察 THOUGHTS/GORDON 分段，必要時降低 `GROQ_MAX_TOKENS` 或 `GROQ_TEMPERATURE` 以控制成本與風格。

- API URL：預設在 `.env.example` 中為：
	`https://api.groq.ai/v1/models/{model}/completions`
	- 把 `{model}` 替換為 `GROQ_MODEL`（例如 `groq-1`）。若 Groq 官方更新 REST 路徑或參數，請依官方文件修改 `GROQ_API_URL` 與 `call_groq_api` 的 payload。

- 部署流程大綱（Streamlit Cloud）:
	1. 把專案推到 GitHub（確保 `.env` 不在版本控制中）。
	2. 在 Streamlit Cloud 建立新 app，連結該 GitHub 倉庫分支。
	3. 在 Streamlit Cloud 的 Settings → Secrets 中新增 `GROQ_API_KEY`（和 `GROQ_MODEL` 如需要）。
	4. 部署後，Streamlit 會在運行時把 `st.secrets` 提供給應用；程式碼已在 `streamlit_app.py` 中使用 `st.secrets` 或環境變數讀取金鑰。

如果你要，我可以幫你：
- 在 repo 中新增一個簡單的 GitHub Actions CI，檢查 linter 與 `pip install -r requirements.txt`（不會包含金鑰）；或
- 幫你把此專案連結到 Streamlit Cloud 的部署步驟與檢查清單。
