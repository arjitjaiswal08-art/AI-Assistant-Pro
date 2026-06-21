# ✅ Deployment Checklist

Print this out and check off each step!

## Before You Start
- [ ] Have a GitHub account
- [ ] Have Git installed on your Mac
- [ ] Terminal app is open

---

## Part 1: Get API Key (5 min)

- [ ] Go to https://console.groq.com/
- [ ] Sign up or login
- [ ] Click "API Keys"
- [ ] Create new API key
- [ ] Copy and save the key

**Your API Key:** `gsk_________________________________`

---

## Part 2: Prepare Files (5 min)

Run in Terminal:

- [ ] `cd /Users/arjitjaiswal/Downloads/local-ai-chatbot-main`
- [ ] `cp app_cloud.py app.py`
- [ ] `cp requirements_cloud.txt requirements.txt`
- [ ] `mkdir -p .streamlit`
- [ ] Edit `.streamlit/secrets.toml` and add your API key

---

## Part 3: GitHub Setup (5 min)

- [ ] `git init`
- [ ] `git add .`
- [ ] `git commit -m "Initial commit"`
- [ ] Go to https://github.com/new
- [ ] Create repo named: `ai-assistant-pro`
- [ ] Make it Public
- [ ] Copy the remote URL
- [ ] `git remote add origin https://github.com/YOUR-USERNAME/ai-assistant-pro.git`
- [ ] `git push -u origin main`

**Your Repo URL:** `https://github.com/_______________/ai-assistant-pro`

---

## Part 4: Deploy to Streamlit (5 min)

- [ ] Go to https://share.streamlit.io/
- [ ] Click "New app"
- [ ] Connect GitHub
- [ ] Select your repo: `ai-assistant-pro`
- [ ] Branch: `main`
- [ ] File: `app.py`
- [ ] Click "Advanced settings"
- [ ] Add secret: `GROQ_API_KEY = "your-key"`
- [ ] Click "Deploy"
- [ ] Wait 3-5 minutes

**Your App URL:** `https://_______________________.streamlit.app`

---

## Part 5: Test It! (2 min)

- [ ] Open your app URL
- [ ] Send a test message
- [ ] Upload a PDF (optional)
- [ ] Check the watermark appears
- [ ] Try the chat history feature

---

## 🎉 Success!

Your AI Assistant Pro is now live on the internet!

Share your URL: `_________________________________`

---

## 📝 Notes

Write down any issues you encounter:

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| Can't push to GitHub | Run: `gh auth login` |
| Module not found | Check `requirements.txt` |
| API key error | Add to Streamlit secrets |
| Deployment failed | Check the logs in Streamlit |

---

**Deployment Date:** _______________

**Time Taken:** _______________

**Status:** ⭕ Not Started  |  🟡 In Progress  |  ✅ Complete
