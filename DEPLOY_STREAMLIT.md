# Deploy FGMD to Streamlit Community Cloud

`localhost:8501` is **local only**. For a public URL you must deploy via **Streamlit Community Cloud** connected to GitHub.

> **Do NOT use** `https://github.com/apps/streamlit` — that page returns 404.  
> GitHub authorization happens **inside** share.streamlit.io after you sign in.

## Step-by-step (correct flow)

### 1. Sign in

Open: **https://share.streamlit.io**

Click **Continue to sign-in** → **Continue with GitHub** → log in as `seunghoobang-prog`.

### 2. Connect GitHub (required)

1. Top-left: click **Workspaces** (warning icon).
2. Click **Connect GitHub account**.
3. GitHub opens → click **Authorize streamlit**.

### 3. Deploy your repo

1. Top-right: click **Create app**.
2. Choose **Yup, I have an app**.
3. Fill in manually:

| Field | Value |
|-------|-------|
| Repository | `seunghoobang-prog/fgmd` |
| Branch | `main` |
| Main file path | `app.py` |
| App URL (optional) | `fgmd` |

4. Click **Deploy!** Wait 2–5 minutes.

### 4. SMTP secrets (for ORDER email)

App → **Settings** (⚙) → **Secrets**:

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

- `https://fgmd.streamlit.app` (if subdomain `fgmd` is free)
- Or auto-generated: `https://seunghoobang-prog-fgmd-app-xxxxx.streamlit.app`

## Repo (already ready)

https://github.com/seunghoobang-prog/fgmd