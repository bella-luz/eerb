# GitHub Push Instructions - Step by Step

## 🎯 GOAL: Push your code to GitHub so deployment can happen

**Estimated Time:** 10 minutes  
**Difficulty:** Easy

---

## STEP 1: Create GitHub Repository Online

### Go to GitHub.com

1. Open browser
2. Go to **https://github.com/new**
3. Sign in if needed

### Fill in the Form

Fill in these fields:

| Field | Value |
|-------|-------|
| **Repository name** | `eerb` |
| **Description** | `Energy Engineering Review Board - AI engineering review before you build` |
| **Visibility** | ☑️ **Public** (must be public for hackathon) |

### Click "Create Repository"

After clicking, you'll see a page with a URL like:
```
https://github.com/bella-luz/eerb.git
```

**COPY THIS URL** - you'll need it in a moment.

---

## STEP 2: Open PowerShell in Your Project Folder

### Navigate to Your Project

1. Open File Explorer
2. Go to: `C:\Users\dandy\Desktop\Iqra\AI training\Mid Hackathon`
3. Right-click in empty space
4. Click **"Open PowerShell here"** or **"Open in Terminal"**

### You should see:

```
PS C:\Users\dandy\Desktop\Iqra\AI training\Mid Hackathon>
```

---

## STEP 3: Connect Your Local Repo to GitHub

Type these commands **one at a time**. Press Enter after each.

### Command 1: Add Remote (connects to GitHub)

```powershell
git remote add origin https://github.com/bella-luz/eerb.git
```

**What it does:** Links your local folder to your GitHub repo

**Expected result:** No message (that's good)

### Command 2: Rename Branch to "main"

```powershell
git branch -M main
```

**What it does:** Renames the default branch to "main" (GitHub standard)

**Expected result:** No message

### Command 3: Push Everything to GitHub

```powershell
git push -u origin main
```

**What it does:** Uploads all your code to GitHub

**Expected result:** It will ask you to sign in...

---

## STEP 4: Authenticate with GitHub

### When PowerShell Asks to Authenticate

You'll see something like:
```
Please complete the authentication in your browser...
```

Two options appear:

### Option A: GitHub Web Login (Easiest)

Click the link that appears or a browser window opens automatically.

1. Sign in with your GitHub account
2. Authorize "Git Credential Manager"
3. Come back to PowerShell
4. It will continue automatically

### Option B: Personal Access Token (If Option A Doesn't Work)

If the browser login doesn't work:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "eerb-push"
4. Check: ☑️ `repo` (full control of private repositories)
5. Click "Generate token"
6. Copy the token (you'll only see it once!)
7. Go back to PowerShell
8. Paste the token when it asks for password

---

## STEP 5: Verify Success ✅

Type this command:
```powershell
git status
```

### You should see:

```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

### If you see this, SUCCESS! ✅

---

## STEP 6: Check GitHub Website

Open browser and go to:
```
https://github.com/bella-luz/eerb
```

You should see:
- ✅ All your Python files
- ✅ Folders (agents, calculations, utils, data, schemas)
- ✅ README.md
- ✅ requirements.txt

---

## ✅ DONE! Your Code is on GitHub!

Now you can:
1. Deploy to Streamlit Cloud (uses GitHub repo automatically)
2. Share the repo link: `https://github.com/bella-luz/eerb`

---

## 🆘 TROUBLESHOOTING

### "fatal: remote origin already exists"

**Solution:** The remote was already added. Skip command 1, continue with 2 and 3.

### "Authentication failed"

**Solution:** 
- Try Option A (web browser) first
- If that fails, use Option B (personal access token)
- Make sure you copied the token correctly (no extra spaces)

### "Could not resolve host"

**Solution:** Check your internet connection. Try again.

### "Permission denied (publickey)"

**Solution:** Use personal access token instead (Option B above)

### Changes still ask you to push

**Solution:** Run `git push -u origin main` again

---

## 📋 COMPLETE CHECKLIST

- [ ] Created repo at https://github.com/new
- [ ] Copied repo URL (https://github.com/bella-luz/eerb.git)
- [ ] Opened PowerShell in project folder
- [ ] Ran `git remote add origin ...`
- [ ] Ran `git branch -M main`
- [ ] Ran `git push -u origin main`
- [ ] Authenticated (web browser or token)
- [ ] Verified with `git status` (no uncommitted changes)
- [ ] Checked GitHub website - code is there!

✅ **All done? Move to next step: Deploy to Streamlit Cloud**

---

## 📞 NEED HELP?

If you get stuck:
1. Read the error message carefully
2. Check the troubleshooting section above
3. If still stuck, come back and I can help debug
