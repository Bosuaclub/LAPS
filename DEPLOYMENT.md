# FAO-Sim Deployment Guide

## ⚠️ Important: Platform Compatibility

**Streamlit Apps CANNOT be deployed to Vercel!**

Vercel is designed for:
- Static sites (HTML/CSS/JS)
- Next.js applications
- Serverless functions

Streamlit requires a **long-running Python server**, which Vercel doesn't support.

## ✅ Recommended: Streamlit Cloud (FREE & EASY)

### Why Streamlit Cloud?

- ✅ **100% Free** for public repos
- ✅ **Zero configuration** needed
- ✅ **Automatic HTTPS**
- ✅ **Built for Streamlit apps**
- ✅ **GitHub integration**
- ✅ **Secrets management**

### Step-by-Step Deployment

#### 1. Prepare Your Repository

```bash
# Make sure all files are committed
git add -A
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

#### 2. Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up" or "Continue with GitHub"
3. Authorize Streamlit Cloud to access your GitHub

#### 3. Deploy Your App

1. Click "New app"
2. Select your repository: `Bosuaclub/LAPS`
3. Branch: `claude/fb-ads-ai-optimization-Lgk6B` (or `main`)
4. Main file path: `faosim/ui/app.py`
5. Click "Deploy!"

#### 4. Configure Secrets

1. In Streamlit Cloud dashboard, click your app
2. Click "Settings" → "Secrets"
3. Add your secrets:

```toml
[openai]
api_key = "sk-..."

[anthropic]
api_key = "sk-ant-..."
```

4. Click "Save"

#### 5. Access Your App

Your app will be available at:
```
https://[your-app-name].streamlit.app
```

### Requirements for Streamlit Cloud

✅ **Already configured**:
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies
- `.streamlit/config.toml` - Streamlit config
- `.streamlit/secrets.toml.example` - Secrets template

### Updating Your Deployed App

Simply push to your repository:
```bash
git add .
git commit -m "Update app"
git push
```

Streamlit Cloud will automatically redeploy!

---

## Alternative 1: Heroku (Also Free)

### Setup

1. Install Heroku CLI:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. Create Heroku files:

**Procfile**:
```
web: sh setup.sh && streamlit run faosim/ui/app.py
```

**setup.sh**:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

---

## Alternative 2: Railway (Modern & Fast)

### Setup

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway will auto-detect Streamlit
5. Add environment variables in dashboard
6. Deploy!

---

## Alternative 3: Render (Free Tier Available)

### Setup

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run faosim/ui/app.py --server.port=$PORT --server.address=0.0.0.0`
5. Add environment variables
6. Deploy!

---

## Alternative 4: Google Cloud Run

### Setup

1. Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "faosim/ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Deploy:
```bash
gcloud run deploy faosim \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Alternative 5: AWS EC2

### Setup

1. Launch EC2 instance (Ubuntu 22.04)
2. SSH into instance:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. Install dependencies:
```bash
sudo apt update
sudo apt install -y python3-pip
```

4. Clone and setup:
```bash
git clone https://github.com/Bosuaclub/LAPS.git
cd LAPS
pip install -r requirements.txt
```

5. Run with screen:
```bash
screen -S faosim
streamlit run faosim/ui/app.py --server.port=8501 --server.address=0.0.0.0
# Press Ctrl+A, then D to detach
```

6. Configure security group to allow port 8501

---

## 🚫 Why Not Vercel?

Vercel limitations:
- ❌ No support for long-running processes
- ❌ No WebSocket support (required by Streamlit)
- ❌ Serverless functions timeout after 10-60 seconds
- ❌ No persistent connections

If you **must use Vercel**, see Option 6 below.

---

## Alternative 6: Vercel + FastAPI Backend (Advanced)

If you absolutely need Vercel, you'll need to:

1. **Deploy Backend Separately** (Railway/Render/Heroku):
   - Create FastAPI API
   - Host on Railway or Render
   - Expose optimization endpoints

2. **Deploy Frontend to Vercel**:
   - Create static HTML/JS frontend
   - Call backend API
   - Display results

**This is complex and NOT recommended for Streamlit apps.**

See `docs/VERCEL_ALTERNATIVE.md` for detailed guide.

---

## 📊 Platform Comparison

| Platform | Free Tier | Ease | Best For |
|----------|-----------|------|----------|
| **Streamlit Cloud** | ✅ Public repos | ⭐⭐⭐⭐⭐ | **RECOMMENDED** |
| Railway | ✅ $5 credit | ⭐⭐⭐⭐ | Modern UX |
| Render | ✅ Limited | ⭐⭐⭐⭐ | Simple |
| Heroku | ✅ Limited | ⭐⭐⭐ | Established |
| Google Cloud Run | ❌ Pay-as-go | ⭐⭐⭐ | Scalable |
| AWS EC2 | ❌ 1 year free | ⭐⭐ | Full control |
| Vercel | ✅ | ❌ | **NOT COMPATIBLE** |

---

## 🎯 Quick Start (Streamlit Cloud)

```bash
# 1. Push to GitHub (if not already)
git push origin main

# 2. Go to share.streamlit.io
# 3. Sign in with GitHub
# 4. Click "New app"
# 5. Select: Bosuaclub/LAPS
# 6. Main file: faosim/ui/app.py
# 7. Deploy!

# Done! Your app is live at:
# https://[your-app-name].streamlit.app
```

---

## 🔧 Troubleshooting

### "Module not found" error

Check `requirements.txt` includes all dependencies:
```bash
pip freeze > requirements-full.txt
# Compare with requirements.txt
```

### "Port already in use"

Streamlit Cloud handles ports automatically. For local testing:
```bash
streamlit run faosim/ui/app.py --server.port=8502
```

### API key errors

Add secrets in Streamlit Cloud dashboard:
1. Settings → Secrets
2. Add your API keys
3. Restart app

### Memory issues

Add to `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200
```

### Slow loading

Optimize imports and caching:
```python
@st.cache_data
def load_data():
    # Your data loading here
    pass
```

---

## 📚 Additional Resources

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Deployment Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy)
- [Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)

---

## 🆘 Need Help?

1. Check logs in Streamlit Cloud dashboard
2. Review this documentation
3. Open issue on GitHub
4. Contact support@streamlit.io

---

**Recommended Deployment: Streamlit Cloud** ⭐⭐⭐⭐⭐

It's free, easy, and purpose-built for Streamlit apps!
