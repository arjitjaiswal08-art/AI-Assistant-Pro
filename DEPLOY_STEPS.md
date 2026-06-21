# 🚀 Deploy AI Assistant Pro to Streamlit Cloud

## Step-by-Step Guide (15 minutes)

### ✅ Step 1: Get Groq API Key (2 minutes)

1. Open browser and go to: **https://console.groq.com/**
2. Click **"Sign Up"** or **"Login"**
3. Click **"API Keys"** in the left menu
4. Click **"Create API Key"**
5. **Copy the key** and save it somewhere safe!

---

### ✅ Step 2: Prepare Your Files (3 minutes)

Open Terminal and run these commands:

```bash
# Go to your project folder
cd /Users/arjitjaiswal/Downloads/local-ai-chatbot-main

# Use the cloud-ready version
cp app_cloud.py app.py

# Use cloud requirements
cp requirements_cloud.txt requirements.txt

# Create secrets folder
mkdir -p .streamlit

# Create secrets file (replace YOUR_API_KEY with your actual key)
echo 'GROQ_API_KEY = "YOUR_API_KEY_HERE"' > .streamlit/secrets.toml
```

---

### ✅ Step 3: Create GitHub Repository (3 minutes)

#### A. In Terminal:
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "AI Assistant Pro - Ready for deployment"
```

#### B. On GitHub Website:
1. Go to: **https://github.com/new**
2. Repository name: **ai-assistant-pro**
3. Make it **Public**
4. **Don't** check "Initialize with README"
5. Click **"Create repository"**

#### C. Push to GitHub:
```bash
# Add GitHub as remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/ai-assistant-pro.git

# Push code
git branch -M main
git push -u origin main
```

---

### ✅ Step 4: Deploy on Streamlit Cloud (5 minutes)

1. Go to: **https://share.streamlit.io/**

2. Click **"New app"**

3. If not logged in:
   - Click **"Continue with GitHub"**
   - Allow access to your repositories

4. Fill in the form:
   - **Repository**: Select `ai-assistant-pro`
   - **Branch**: `main`
   - **Main file path**: `app.py`

5. Click **"Advanced settings..."**

6. In the **Secrets** box, paste:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```
   (Replace with your actual API key from Step 1)

7. Click **"Deploy!"**

---

### ✅ Step 5: Wait for Deployment (2 minutes)

- You'll see a building progress bar
- Takes 2-5 minutes
- Once done, your app will open automatically!

---

### 🎉 You're Live!

Your app URL will be something like:
```
https://ai-assistant-pro-YOUR-USERNAME.streamlit.app
```

You can now:
- ✅ Share this URL with anyone
- ✅ Access it from any device
- ✅ Chat with AI using Groq models
- ✅ Upload PDFs for RAG

---

## 🔧 Quick Troubleshooting

### Problem: "Module not found"
**Solution:** 
```bash
# Make sure requirements.txt is correct
cat requirements.txt

# Should show:
# streamlit
# groq
# pymupdf
# sentence-transformers
# numpy
```

### Problem: "API Key Error"
**Solution:**
1. Go to your Streamlit app
2. Click ⋮ (three dots) → Settings
3. Click "Secrets"
4. Add your Groq API key

### Problem: "Failed to push to GitHub"
**Solution:**
```bash
# Set up GitHub authentication
gh auth login

# Or use personal access token
# GitHub → Settings → Developer settings → Personal access tokens
```

---

## 📱 Update Your App Later

```bash
# Make changes to app.py

# Commit and push
git add .
git commit -m "Updated features"
git push

# Streamlit will automatically redeploy!
```

---

## 🆓 Cost Breakdown

- ✅ Streamlit Cloud: **FREE** (public apps)
- ✅ Groq API: **FREE** (with rate limits)
- ✅ GitHub: **FREE** (public repos)

**Total Cost: $0**

---

## 🎯 Next Steps

1. Customize the app title and styling
2. Add your custom domain (Streamlit Pro)
3. Share with friends!

Need help? Let me know! 🚀
