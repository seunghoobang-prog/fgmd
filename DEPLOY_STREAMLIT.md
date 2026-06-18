# Deploy FGMD to Streamlit Community Cloud

Yes — **Streamlit Cloud must be connected to your GitHub repo** to deploy. Local `localhost:8501` only runs on your PC.

## One-click deploy (after GitHub login)

Open this link while signed into [share.streamlit.io](https://share.streamlit.io):

**https://share.streamlit.io/deploy?repository=seunghoobang-prog/fgmd&branch=main&mainModule=app.py**

## Manual steps

1. Go to https://share.streamlit.io and sign in with **GitHub** (`seunghoobang-prog`).
2. Click **Connect GitHub account** → **Authorize streamlit**.
3. Click **Create app** → **Yup, I have an app**.
4. Set:
   - **Repository:** `seunghoobang-prog/fgmd`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (optional):** `fgmd` → `https://fgmd.streamlit.app`
5. Click **Deploy**.

## SMTP secrets (for ORDER email)

In the app → **Settings** → **Secrets**, paste:

```toml
[smtp]
host = "smtp.example.com"
port = 587
username = "your@email.com"
password = "your-password"
from_email = "your@email.com"
to_email = "240027@samchully.co.kr"
use_tls = true
```

## Expected live URL

After deploy: **https://fgmd.streamlit.app** (if subdomain `fgmd` is available)

Or auto-generated: `https://seunghoobang-prog-fgmd-app-xxxxx.streamlit.app`