# ⚡ Quick Start Guide - Complete Deployment

This guide will help you complete all three deployment tasks in under 10 minutes!

---

## 🎯 Three Simple Steps

### Step 1: Push to GitHub (5 minutes)

**Option A: Use the Helper Script (Easiest)**
```powershell
.\setup_github.ps1
```
The script will guide you through:
- Adding your GitHub username
- Configuring the remote
- Pushing your code

**Option B: Manual Setup**
1. Create a new repository on GitHub: https://github.com/new
   - Name: `local_ai_agent`
   - **DO NOT** initialize with README, .gitignore, or license
2. Run these commands (replace `YOUR_USERNAME`):
```powershell
git remote add origin https://github.com/YOUR_USERNAME/local_ai_agent.git
git push -u origin master
```

**If your GitHub default branch is `main`:**
```powershell
git push -u origin master:main
```

---

### Step 2: Run Auto-Learning (6-11 minutes)

**Option A: Use the Helper Script (Recommended)**
```powershell
.\run_auto_learning.ps1
```
The script will:
- Check dependencies
- Show progress
- Run the auto-learner

**Option B: Direct Command**
```powershell
python src/tools/auto_learner.py
```

**What happens:**
- Learns 67+ tools from `data/essential_tools.json`
- Saves knowledge to `data/knowledge_base/`
- Tracks progress in `data/learning_progress.json`
- Can be stopped and resumed anytime!

**Expected Output:**
```
🚀 Auto-Learner Initialized
📚 Total Tools: 67
✅ Already Learned: 0
🎓 To Learn: 67

[cyan]Learning Pandas (data_analysis)...
[cyan]Learning NumPy (data_analysis)...
...
✨ Auto-Learning Session Complete! ✨
```

---

### Step 3: Deploy to Colab (3 minutes)

1. **Open Google Colab**: https://colab.research.google.com

2. **Upload the notebook**:
   - File → Upload notebook
   - Select `notebooks/Agent_On_Colab.ipynb`

3. **Update GitHub URL** in Cell 1:
   ```python
   # Replace YOUR_USERNAME with your GitHub username
   !git clone https://github.com/YOUR_USERNAME/local_ai_agent.git
   %cd local_ai_agent
   ```

4. **Run all cells** in order:
   - Cell 1: Setup Environment
   - Cell 2: Run Auto-Learner
   - Cell 3: Download Knowledge Base (optional)

5. **Download results** (optional):
   - Run Cell 3 to download `knowledge_base.zip`
   - Extract and merge with local `data/knowledge_base/`

---

## 📊 What You'll Get

After completing all steps:

✅ **GitHub Repository**: Your code is backed up and shareable  
✅ **Knowledge Base**: 67+ tools learned and stored locally  
✅ **Colab Ready**: Cloud deployment for faster learning  
✅ **Progress Tracking**: Resume learning anytime  

---

## 🔧 Troubleshooting

### GitHub Issues

**"remote origin already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/local_ai_agent.git
```

**"authentication failed"**
- Use Personal Access Token (not password)
- Generate: GitHub → Settings → Developer settings → Personal access tokens

### Auto-Learning Issues

**"ModuleNotFoundError"**
```powershell
pip install -r requirements.txt
```

**Rate limiting**
- The script includes delays, but if issues persist, increase delay in `auto_learner.py` line 120

### Colab Issues

**"git clone failed"**
- Make sure repo is public, OR
- Use token: `!git clone https://TOKEN@github.com/YOUR_USERNAME/local_ai_agent.git`

---

## 📚 Next Steps

1. **Monitor Progress**: Check `data/learning_progress.json`
2. **Test Knowledge**: Query your agent about learned tools
3. **Expand Tools**: Add more to `data/essential_tools.json`
4. **Schedule Updates**: Set up periodic learning (cron/Task Scheduler)

---

## 📞 Need Help?

- See `DEPLOYMENT_GUIDE.md` for detailed instructions
- Check logs in `data/logs_backup/`
- Review `data/agent_log.txt`

---

**Ready? Let's go! 🚀**

Start with Step 1, then Step 2, then Step 3. Each step is independent, so you can do them in any order or separately.

