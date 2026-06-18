# FGMD — Funeral Goods Management Dashboard

Streamlit demo app **상조물품현황** for regional funeral-goods inventory and order management.

## Quick start

```powershell
cd C:\Users\SKILLSUPPORT\fgmd
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
streamlit run app.py
```

Open http://localhost:8501

## Deploy to Streamlit Cloud (public URL)

1. Open **[share.streamlit.io](https://share.streamlit.io)** → sign in with GitHub.
2. **Workspaces** → **Connect GitHub account** → **Authorize streamlit**.
   - Do **not** use `github.com/apps/streamlit` (404). Auth happens inside Streamlit.
3. **Create app** → **Yup, I have an app** → set repo `seunghoobang-prog/fgmd`, branch `main`, file `app.py`.
4. Optional subdomain `fgmd` → `https://fgmd.streamlit.app`
5. Add SMTP secrets in app Settings (see [DEPLOY_STREAMLIT.md](DEPLOY_STREAMLIT.md)).

## Docs (development plan)

| Document | Local path | GitHub |
|----------|------------|--------|
| Development plan (markdown) | `DEVELOPMENT_PLAN.md` | [View on GitHub](https://github.com/seunghoobang-prog/fgmd/blob/main/DEVELOPMENT_PLAN.md) |
| Original design plan | `PLAN.md` | [View on GitHub](https://github.com/seunghoobang-prog/fgmd/blob/main/PLAN.md) |
| Presentation (PPTX) | `docs/FGMD_Development_Plan.pptx` | [Download from GitHub](https://github.com/seunghoobang-prog/fgmd/raw/main/docs/FGMD_Development_Plan.pptx) |
| Plan index (browser) | `docs/index.html` | Open locally after `streamlit run` or double-click Desktop shortcut |

**Desktop shortcut:** `C:\Users\SKILLSUPPORT\Desktop\FGMD-Plans\` — double-click `OPEN_PLANS.bat` to open the plan hub and PPT.