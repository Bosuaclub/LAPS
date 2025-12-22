# 🚀 Deploy FAO-Sim to Streamlit Cloud

## Quick Start (5 Minutes)

### Prerequisites
- ✅ GitHub account
- ✅ FAO-Sim code pushed to GitHub
- ✅ OpenAI API key

### Step 1: Go to Streamlit Cloud

Visit: **[share.streamlit.io](https://share.streamlit.io)**

### Step 2: Sign In

Click **"Continue with GitHub"**

### Step 3: Create New App

1. Click **"New app"**
2. Fill in:
   - **Repository**: `Bosuaclub/LAPS`
   - **Branch**: `claude/fb-ads-ai-optimization-Lgk6B` (or `main`)
   - **Main file path**: `faosim/ui/app.py`

### Step 4: Advanced Settings (Optional)

Click "Advanced settings" to configure:
- **Python version**: 3.9 (default)
- **Secrets**: Click "Add secrets"

### Step 5: Add Your API Keys

In the secrets section, paste:

```toml
[openai]
api_key = "sk-..."

[anthropic]
api_key = "sk-ant-..."
```

### Step 6: Deploy!

Click **"Deploy"** button

⏱️ Wait 2-3 minutes for deployment...

✅ **Done!** Your app is live at: `https://[your-app-name].streamlit.app`

## 🎯 Your App URL

After deployment, you'll get a URL like:
```
https://faosim-bosuaclub.streamlit.app
```

You can customize this in Settings.

## 📝 Accessing Secrets in Code

Your secrets are automatically available:

```python
import streamlit as st

# Access secrets
api_key = st.secrets["openai"]["api_key"]
```

## 🔧 Troubleshooting

### Module Not Found Error

**Problem**: `ModuleNotFoundError: No module named 'xxx'`

**Solution**: Check `requirements.txt` includes all dependencies:
```bash
# Make sure requirements.txt has:
streamlit>=1.30.0
plotly>=5.18.0
langchain>=0.1.0
# ... etc
```

### Memory Error

**Problem**: `MemoryError` or app crashes

**Solution 1**: Optimize imports
```python
# Only import what you need
from langchain.chains import RetrievalQA  # ✅ Good
# import langchain  # ❌ Imports everything
```

**Solution 2**: Use caching
```python
@st.cache_resource
def load_model():
    # Heavy model loading
    return model
```

### Timeout Error

**Problem**: App takes too long to start

**Solution**: Add to `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200

[browser]
gatherUsageStats = false
```

### API Key Not Working

**Problem**: `AuthenticationError`

**Solution 1**: Check secrets format:
```toml
# ✅ Correct:
[openai]
api_key = "sk-..."

# ❌ Wrong:
openai_api_key = "sk-..."
```

**Solution 2**: Restart app after adding secrets

## 📊 Monitoring Your App

### View Logs

1. Go to Streamlit Cloud dashboard
2. Click your app
3. Click "Manage app" → "Logs"

### Check Status

- Green dot = Running
- Yellow dot = Starting
- Red dot = Error

### View Analytics

- Settings → Analytics
- See visitor count, usage stats

## 🔄 Updating Your App

### Automatic Updates

Just push to GitHub:
```bash
git add .
git commit -m "Update app"
git push
```

Streamlit Cloud will automatically redeploy!

### Manual Reboot

1. Go to dashboard
2. Click your app
3. Click "Reboot" button

### Clear Cache

1. Settings → "Clear cache"
2. Or use `st.cache_data.clear()` in code

## 💰 Pricing

### Free Tier (Community)
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ Community support
- ✅ GitHub integration
- ❌ Private repos (need paid plan)

### Pricing (if needed)
- **Developer**: $20/month
  - Private repos
  - More resources
  - Priority support

For FAO-Sim, **free tier is enough!**

## 🎨 Customization

### Custom Domain

1. Settings → Domain
2. Add CNAME record:
   ```
   CNAME faosim.yourdomain.com → [your-app].streamlit.app
   ```
3. Verify in dashboard

### Custom Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### App Settings

Settings → General:
- App name
- Description
- Icon
- Theme

## 📱 Sharing Your App

### Public URL
```
https://your-app.streamlit.app
```

### Embed in Website
```html
<iframe src="https://your-app.streamlit.app"
        width="100%"
        height="800px">
</iframe>
```

### Social Preview

Add to your app:
```python
st.set_page_config(
    page_title="FAO-Sim",
    page_icon="🎯",
    layout="wide",
    menu_items={
        'Get Help': 'https://github.com/Bosuaclub/LAPS',
        'Report a bug': "https://github.com/Bosuaclub/LAPS/issues",
        'About': "FB Ads Optimization Tool"
    }
)
```

## 🔒 Security Best Practices

### 1. Never Commit Secrets
```bash
# Add to .gitignore:
.streamlit/secrets.toml
.env
*.key
```

### 2. Use Streamlit Secrets
```python
# ✅ Good:
api_key = st.secrets["openai"]["api_key"]

# ❌ Bad:
api_key = "sk-hardcoded-key"
```

### 3. Limit Access (Paid Feature)
- Settings → Access control
- Whitelist emails/domains

## 📈 Performance Tips

### 1. Cache Heavy Operations
```python
@st.cache_data
def load_data():
    return expensive_operation()

@st.cache_resource
def load_model():
    return heavy_model()
```

### 2. Optimize Imports
```python
# ✅ Import only what you need
from langchain.chains import RetrievalQA

# ❌ Don't import everything
import langchain
```

### 3. Use Session State
```python
# Persist data across reruns
if 'data' not in st.session_state:
    st.session_state.data = load_data()
```

## 🆘 Common Issues

### Issue: "App is sleeping"

**Why**: Inactive apps sleep after 7 days

**Fix**: Just visit the URL - it wakes automatically

**Prevention**: Share your app to keep it active

### Issue: "Resource limits exceeded"

**Why**: Using too much memory/CPU

**Fix**:
- Reduce batch sizes
- Use caching
- Optimize code

### Issue: "Build failed"

**Why**: Dependency conflicts or errors

**Fix**:
1. Check logs
2. Test locally first:
   ```bash
   pip install -r requirements.txt
   streamlit run faosim/ui/app.py
   ```
3. Fix errors
4. Push again

## 📚 Resources

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
- [Deployment Tutorial](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)

## 🎓 Video Tutorial

Coming soon: Step-by-step video walkthrough

## ✅ Checklist

Before deploying, make sure:
- [ ] Code is on GitHub
- [ ] `requirements.txt` is complete
- [ ] `faosim/ui/app.py` exists
- [ ] `.streamlit/config.toml` is configured
- [ ] Have OpenAI API key ready
- [ ] Tested locally

## 🎉 Success!

Your FAO-Sim app is now live and accessible worldwide!

Share your URL:
```
https://your-app.streamlit.app
```

---

**Need help?** Open an issue on [GitHub](https://github.com/Bosuaclub/LAPS/issues)
