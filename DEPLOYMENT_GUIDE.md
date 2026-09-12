# EERB Deployment Guide

## Prerequisites

✅ GitHub account (bella-luz)  
✅ Python 3.10+ installed  
✅ Git installed  
✅ Streamlit Cloud account (connected to GitHub)  
✅ OpenAI API key (in `.env` locally)  

---

## Step 1: Create GitHub Repository

### Option A: Using GitHub CLI

```bash
# Install GitHub CLI (if not already installed)
# Windows: winget install gh
# Or download from: https://github.com/cli/cli

# Create repo
gh repo create eerb --public --source=. --remote=origin --push
```

### Option B: Manual GitHub Web Creation

1. Go to https://github.com/new
2. Repository name: `eerb`
3. Description: "Energy Engineering Review Board - AI engineering review before you build"
4. Public
5. Create repository

### Then Push Code:

```bash
cd "C:\Users\dandy\Desktop\Iqra\AI training\Mid Hackathon"
git remote add origin https://github.com/bella-luz/eerb.git
git branch -M main
git push -u origin main
```

---

## Step 2: Verify GitHub Push

```bash
git status
# Should show: "Your branch is up to date with 'origin/main'."

# View repo online
echo "https://github.com/bella-luz/eerb"
```

---

## Step 3: Deploy to Streamlit Cloud

### Setup (One-time)

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"

### Deploy

1. **GitHub repository:** bella-luz/eerb
2. **Branch:** main
3. **File path:** app.py
4. Click "Deploy"

### Add API Key Secret

Once app is deploying:

1. Click "⋮" (three dots, top-right) → Settings
2. → Secrets
3. Paste:
   ```
   OPENAI_API_KEY = sk-your-actual-key-here
   ```
4. Save

### Deployment Time

- Initial: 2-3 minutes
- App URL: `https://eerb.streamlit.app` (or similar)

---

## Step 4: Test Live Deployment

1. Open your Streamlit Cloud app link
2. Click "Demo Project"
3. Click "Run Engineering Review"
4. Verify:
   - ✅ App loads without errors
   - ✅ Demo data is populated
   - ✅ Charts render
   - ✅ Agents execute
   - ✅ Report downloads

---

## Troubleshooting

### Issue: `ModuleNotFoundError`

**Solution:** Imports are already fixed for Streamlit Cloud. If you see this:
1. Check that `sys.path.insert(0, ...)` is in app.py
2. Ensure all files are pushed to GitHub

### Issue: `OPENAI_API_KEY` not found

**Solution:** 
1. Go to Streamlit Cloud app → Settings → Secrets
2. Ensure `OPENAI_API_KEY = sk-...` is added
3. Restart the app (click ⋮ → Reboot)

### Issue: Slow response from LLM

**Note:** First run may be slow (LLM API latency). Subsequent runs are faster due to caching.

### Issue: Demo CSV files not found

**Solution:** Ensure `data/demo_load.csv` and `data/demo_pv.csv` are in GitHub repo.

---

## File Checklist for Deployment

```
eerb/ (GitHub root)
├── .env (LOCAL ONLY, not pushed)
├── .gitignore (✓ prevents .env from pushing)
├── .streamlit/config.toml
├── .streamlit/secrets.toml (STREAMLIT ONLY, set in cloud)
├── README.md
├── DEPLOYMENT_GUIDE.md
├── PRESENTATION_SLIDES.md
├── EERB_FINAL_MVP_PRD.md
├── requirements.txt
├── app.py
├── data/demo_load.csv
├── data/demo_pv.csv
├── agents/ (all files)
├── calculations/ (all files)
├── utils/ (all files)
└── schemas/ (all files)
```

---

## How to Make Changes & Redeploy

1. Make code changes locally
2. Test with `streamlit run app.py`
3. Commit:
   ```bash
   git add .
   git commit -m "Fix: description of change"
   git push
   ```
4. Streamlit Cloud auto-redeploys within 1-2 minutes

---

## Accessing Logs (Troubleshooting)

In Streamlit Cloud:
1. Click your app
2. Click "Logs" tab
3. View error messages

---

## Local Testing Before Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run app locally
streamlit run app.py

# Visit http://localhost:8501 in your browser
```

---

## Production Checklist

Before final submission:

- [ ] GitHub repo created and all files pushed
- [ ] Streamlit Cloud app deployed
- [ ] API key added to Streamlit Secrets (NOT in code)
- [ ] .gitignore prevents `.env` from being pushed
- [ ] Demo project runs successfully
- [ ] Charts render correctly
- [ ] Report downloads work
- [ ] No error messages in Streamlit Cloud logs

---

## Post-Deployment

### Share Deployment Link

GitHub repo: `https://github.com/bella-luz/eerb`

Live app: `https://eerb.streamlit.app` (or custom domain)

### Documentation Links for Submission

- **PRD:** EERB_FINAL_MVP_PRD.md (in repo)
- **README:** README.md (in repo)
- **Slides:** PRESENTATION_SLIDES.md (convert to Google Slides or PDF)
- **Code:** GitHub link
- **Live App:** Streamlit Cloud link

---

## Rollback (If Needed)

If something breaks:

1. Identify the bad commit:
   ```bash
   git log --oneline
   ```

2. Revert to previous version:
   ```bash
   git revert <commit-hash>
   git push
   ```

3. Streamlit Cloud auto-redeploys

---

**Status:** Ready for deployment! 🚀

Next step: Push to GitHub and deploy to Streamlit Cloud.
