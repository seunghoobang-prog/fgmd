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

1. Sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub.
2. Click **Connect GitHub account** → **Authorize streamlit**.
3. Use this deploy link (repo is already on GitHub):

**https://share.streamlit.io/deploy?repository=seunghoobang-prog/fgmd&branch=main&mainModule=app.py**

4. Set app subdomain to `fgmd` if available → live at `https://fgmd.streamlit.app`
5. Add SMTP secrets in app Settings (see [DEPLOY_STREAMLIT.md](DEPLOY_STREAMLIT.md)).

## Docs (development plan)

| Document | Local path | GitHub |
|----------|------------|--------|
| Development plan (markdown) | `DEVELOPMENT_PLAN.md` | [View on GitHub](https://github.com/seunghoobang-prog/fgmd/blob/main/DEVELOPMENT_PLAN.md) |
| Original design plan | `PLAN.md` | [View on GitHub](https://github.com/seunghoobang-prog/fgmd/blob/main/PLAN.md) |
| Presentation (PPTX) | `docs/FGMD_Development_Plan.pptx` | [Download from GitHub](https://github.com/seunghoobang-prog/fgmd/raw/main/docs/FGMD_Development_Plan.pptx) |
| Plan index (browser) | `docs/index.html` | Open locally after `streamlit run` or double-click Desktop shortcut |

**Desktop shortcut:** `C:\Users\SKILLSUPPORT\Desktop\FGMD-Plans\` — double-click `OPEN_PLANS.bat` to open the plan hub and PPT.