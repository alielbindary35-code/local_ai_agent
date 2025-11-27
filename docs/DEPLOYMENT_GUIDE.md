# 🚀 Deployment Guide - Local AI Agent

Complete guide to deploy your Local AI Agent to GitHub, run auto-learning, and use Colab.

---

## 📋 Table of Contents

1. [GitHub Setup](#1-github-setup)
2. [Run Auto-Learner](#2-run-auto-learner)
3. [Colab Deployment](#3-colab-deployment)

---

## 1. GitHub Setup

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository settings:
   - **Name**: `local_ai_agent` (or your preferred name)
   - **Description**: "Self-learning Local AI Agent with Fast Learning and Colab Support"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

### Step 2: Connect Local Repo to GitHub

After creating the repository, GitHub will show you commands. Use these:

```powershell
# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/local_ai_agent.git

# Verify it was added
git remote -v

# Push to GitHub
git push -u origin master
```

**Note**: If your default branch is `main` instead of `master`, use:
```powershell
git push -u origin master:main
```

### Step 3: Verify Push

1. Refresh your GitHub repository page
2. You should see all your files there!

---

## 2. Run Auto-Learner

The auto-learner will systematically learn all tools from `data/essential_tools.json`.

### Prerequisites

Make sure you have:
- ✅ Python 3.8+ installed
- ✅ Virtual environment activated (if using one)
- ✅ Dependencies installed: `pip install -r requirements.txt`

### Run the Auto-Learner

```powershell
# From the project root directory
python src/tools/auto_learner.py
```

### What It Does

1. **Reads** `data/essential_tools.json` (67+ tools across 5 categories)
2. **Learns** each tool using FastLearning (web scraping, docs, GitHub)
3. **Saves** knowledge to `data/knowledge_base/`
4. **Tracks** progress in `data/learning_progress.json`

### Expected Output

```
🚀 Auto-Learner Initialized
📚 Total Tools: 67
✅ Already Learned: 0
🎓 To Learn: 67

[cyan]Learning Pandas (data_analysis)...
[cyan]Learning NumPy (data_analysis)...
...
✨ Auto-Learning Session Complete! ✨
📂 Knowledge stored in: C:\Users\engha\Music\New folder1\local_ai_agent\data\knowledge_base
```

### Time Estimate

- **Per tool**: ~5-10 seconds (with API rate limiting)
- **Total time**: ~6-11 minutes for all 67 tools
- **Progress**: Saved after each tool, so you can stop and resume anytime!

### Resume Learning

If interrupted, the auto-learner will skip already-learned tools automatically.

---

## 3. Colab Deployment

### Option A: Clone from GitHub (Recommended)

1. **Open Google Colab**: [colab.research.google.com](https://colab.research.google.com)
2. **Upload the notebook**:
   - Go to **File** → **Upload notebook**
   - Select `notebooks/Agent_On_Colab.ipynb`
3. **Update the clone command** in the setup cell:
   ```python
   # Replace YOUR_USERNAME with your GitHub username
   !git clone https://github.com/YOUR_USERNAME/local_ai_agent.git
   %cd local_ai_agent
   ```
4. **Run the cells** in order:
   - Cell 1: Setup Environment
   - Cell 2: Run Auto-Learner
   - Cell 3: Download Knowledge Base (optional)

### Option B: Upload Files Directly

1. **Upload project to Google Drive**:
   - Zip the project: `Compress-Archive -Path . -DestinationPath local_ai_agent.zip`
   - Upload to Google Drive
2. **Mount Drive in Colab**:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
3. **Extract and navigate**:
   ```python
   !unzip /content/drive/MyDrive/local_ai_agent.zip
   %cd local_ai_agent
   ```

### Colab Benefits

- ⚡ **Faster Learning**: Cloud GPUs for parallel processing
- 💾 **Free Storage**: Large knowledge base storage
- 🔄 **Easy Sharing**: Share notebooks with team
- 📊 **Visualization**: Built-in charts and graphs

### Download Results

After learning completes, use Cell 3 to download the knowledge base:
- Creates `knowledge_base.zip`
- Downloads automatically to your computer
- Extract and merge with local `data/knowledge_base/`

---

## 🔧 Troubleshooting

### GitHub Push Issues

**Error: "remote origin already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/local_ai_agent.git
```

**Error: "authentication failed"**
- Use Personal Access Token instead of password
- Generate token: GitHub → Settings → Developer settings → Personal access tokens
- Use token as password when prompted

### Auto-Learner Issues

**Error: "ModuleNotFoundError"**
```powershell
pip install -r requirements.txt
```

**Error: "Rate limit exceeded"**
- The script includes 1-second delays between requests
- If still hitting limits, increase delay in `auto_learner.py` (line 120)

### Colab Issues

**Error: "git clone failed"**
- Make sure repository is public, OR
- Use GitHub token: `!git clone https://TOKEN@github.com/YOUR_USERNAME/local_ai_agent.git`

**Error: "Module not found"**
- Make sure you ran the setup cell first
- Check that `%cd local_ai_agent` executed successfully

---

## 📊 Next Steps After Deployment

1. ✅ **Monitor Learning Progress**: Check `data/learning_progress.json`
2. ✅ **Test Knowledge Base**: Query the agent about learned tools
3. ✅ **Expand Tools List**: Add more tools to `data/essential_tools.json`
4. ✅ **Customize Topics**: Modify topics in `auto_learner.py` for specific needs
5. ✅ **Schedule Learning**: Set up cron job (Linux) or Task Scheduler (Windows) for periodic updates

---

## 📞 Support

If you encounter issues:
1. Check the logs in `data/logs_backup/`
2. Review `data/agent_log.txt`
3. Verify all dependencies: `pip list`

---

**Happy Learning! 🎓✨**

