# 🚀 Installation & Deployment Guide

> Complete step-by-step instructions for setting up and deploying the Abdul School Management Platform

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Troubleshooting](#troubleshooting)
7. [Verification Checklist](#verification-checklist)

---

## 🖥️ System Requirements

### Minimum Requirements
```
Operating System:    Windows 10+, macOS 10.14+, or Ubuntu 18.04+
Python:              3.8 or higher
RAM:                 2 GB minimum (4 GB recommended)
Disk Space:          500 MB
Internet:            Required for API calls
```

### Recommended for Production
```
RAM:                 8 GB+
CPU:                 4+ cores
Disk Space:          2+ GB
Bandwidth:           Minimum 1 Mbps
```

### Verify Your System
```bash
# Check Python version
python --version
# Should show: Python 3.8.x or higher

# Check pip
pip --version
# Should show: pip 20.x or higher

# Check disk space
# Windows: dir C:\
# macOS/Linux: df -h
```

---

## 💻 Local Development Setup

### Step 1: Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ **Check "Add Python to PATH"**
4. Click "Install Now"

```bash
# Verify installation
python --version
```

#### macOS
```bash
# Using Homebrew (recommended)
brew install python3

# Verify
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify
python3 --version
```

---

### Step 2: Clone Repository

```bash
# Option A: Using Git (recommended)
git clone https://github.com/yourusername/abdul-project.git
cd abdul-project

# Option B: Download ZIP
# 1. Download from GitHub
# 2. Extract to folder
# 3. cd path/to/abdul-project
```

---

### Step 3: Create Virtual Environment

#### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv .venv

# Activate
.venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then run: .venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt)
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Verify:** You should see `(.venv)` at the start of your terminal prompt

---

### Step 4: Install Dependencies

```bash
# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Install all project dependencies
pip install -r requirements.txt

# Verify installation
pip list
# Should show: streamlit, pandas, plotly, etc.
```

### Requirements Summary
```
streamlit           # Web framework
pandas              # Data manipulation
plotly              # Interactive charts
PyPDF2              # PDF processing
python-docx         # Word documents
pillow              # Image processing
pdfplumber          # PDF extraction
easyocr             # Text recognition
openpyxl            # Excel export
google-cloud-vision # Cloud OCR (optional)
requests            # HTTP requests
solders             # Solana SDK
```

---

### Step 5: Configure Environment Variables

#### Create .env File
```bash
# Copy template
cp .env.example .env

# Edit .env with your values
# Use your preferred editor:
# - Windows: notepad .env
# - macOS/Linux: nano .env
```

#### Required Environment Variables

```ini
# ═══════════════════════════════════════════════════════════════
# CRITICAL: Must configure before first run
# ═══════════════════════════════════════════════════════════════

# 1. OPENROUTER API (for AI Grading)
OPENROUTER_API_KEY=your_openrouter_api_key_here
# Get from: https://openrouter.ai/keys
# Models: openai/gpt-4o-mini, claude-opus, llama-2, etc.

OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_APP_NAME=school-saas-grading
OPENROUTER_SITE_URL=http://localhost:8501


# 2. SOLANA (for Blockchain Payments)
SOLANA_NETWORK=devnet
# Options: devnet (testing) or mainnet-beta (production)

SOLANA_RPC_URL=https://api.devnet.solana.com
# Devnet: https://api.devnet.solana.com
# Mainnet: https://api.mainnet-beta.solana.com

SOLANA_RECEIVER_WALLET=YOUR_SOLANA_WALLET_ADDRESS
# Get wallet from: solflare.com or phantom.app

SOLANA_PAYMENT_TIMEOUT=900              # 15 minutes
SOLANA_CONFIRMATION_TIMEOUT=120         # 2 minutes
SOLANA_MIN_CONFIRMATIONS=3

# SOL/PKR Conversion rate (fallback if API down)
FALLBACK_SOL_USD_RATE=142.50


# 3. GOOGLE CLOUD VISION (Optional - for OCR)
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
# Leave empty to use EasyOCR instead (recommended)
```

#### Getting API Keys

**OpenRouter API Key:**
1. Visit https://openrouter.ai
2. Sign up (free tier available)
3. Go to Settings → API Keys
4. Copy key to OPENROUTER_API_KEY

**Solana Wallet:**
1. Install Phantom or Solflare wallet
2. Create new wallet
3. Switch to Devnet (for testing)
4. Copy public address to SOLANA_RECEIVER_WALLET
5. For mainnet: Switch to Mainnet, get real wallet

**Google Cloud Vision (Optional):**
1. Go to Google Cloud Console
2. Create project
3. Enable Vision API
4. Create service account
5. Download JSON key

---

### Step 6: Seed Database with Sample Data

```bash
# Seed admin panel data (25+ sample users, 50+ transactions, etc.)
python admin_data_seeder.py

# Should output:
# ✓ KPI data seeded
# ✓ Activity logs seeded
# ✓ Users seeded
# ✓ AI metrics seeded
# ✓ Payment transactions seeded
# ✓ Security alerts seeded
# ✓ Analytics data seeded
# ✅ Admin panel data seeded successfully!


# Seed school portal data (students, teachers, classes, etc.)
python school_portal_data_seeder.py

# Should output:
# ✓ Students seeded
# ✓ Teachers seeded
# ✓ Classes seeded
# ✓ Subjects seeded
# ✓ Attendance records seeded
# ✓ Exams seeded
# ✓ Assignments seeded
# ✓ Grades seeded
# ✅ All data seeded successfully!
```

**What's being seeded:**
- Admin user accounts
- Sample payment transactions
- Grading records
- School data (students, teachers, classes)
- Attendance records
- Exam results

---

### Step 7: Run Application

```bash
# Start Streamlit development server
streamlit run app.py

# Output should show:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
```

### First Launch Checklist
- [ ] See welcome page
- [ ] Check sidebar navigation
- [ ] Click "🎛️ Master Admin Panel"
- [ ] View sample KPI data
- [ ] Check activity logs
- [ ] View payment transactions

---

## 🌐 Production Deployment

### Option 1: Streamlit Cloud (Recommended for beginners)

#### Setup (5 minutes)
1. Push code to GitHub (public or private repo)
2. Go to https://streamlit.io/cloud
3. Click "Deploy an app"
4. Select your repository and branch
5. Streamlit automatically deploys!

#### Add Secrets
1. In Streamlit Cloud dashboard
2. Click "Settings" → "Secrets"
3. Add all .env variables:
```
OPENROUTER_API_KEY=your_key
SOLANA_RECEIVER_WALLET=your_wallet
SOLANA_NETWORK=devnet
...
```

#### Access
```
https://your-username-abdul-project.streamlit.app
```

---

### Option 2: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build & Run Docker
```bash
# Build image
docker build -t abdul-project .

# Run container
docker run -p 8501:8501 \
  -e OPENROUTER_API_KEY=your_key \
  -e SOLANA_RECEIVER_WALLET=your_wallet \
  abdul-project

# Access: http://localhost:8501
```

---

### Option 3: VPS Deployment (AWS/DigitalOcean/Heroku)

#### Deploy to Heroku
```bash
# 1. Create Heroku account
# 2. Install Heroku CLI

heroku login
heroku create abdul-project

# 3. Add buildpacks
heroku buildpacks:add heroku/python

# 4. Set environment variables
heroku config:set OPENROUTER_API_KEY=your_key
heroku config:set SOLANA_RECEIVER_WALLET=your_wallet
# ... add all other variables

# 5. Deploy
git push heroku main

# 6. View logs
heroku logs --tail

# Access: https://abdul-project.herokuapp.com
```

#### Deploy to AWS EC2
```bash
# 1. Launch Ubuntu EC2 instance
# 2. SSH into instance

ssh -i your-key.pem ubuntu@your-instance-ip

# 3. Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 4. Clone repository
git clone your-repo-url
cd abdul-project

# 5. Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install packages
pip install -r requirements.txt

# 7. Create .env file
nano .env
# Add all environment variables

# 8. Run with Supervisor (process manager)
sudo apt install supervisor

# Create config: /etc/supervisor/conf.d/abdul.conf
[program:abdul-project]
directory=/home/ubuntu/abdul-project
command=/home/ubuntu/abdul-project/venv/bin/streamlit run app.py
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/abdul.log

# Start service
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start abdul-project
```

---

### Option 4: Docker Compose (Multiple Services)

#### docker-compose.yml
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - SOLANA_RECEIVER_WALLET=${SOLANA_RECEIVER_WALLET}
      - SOLANA_NETWORK=devnet
    volumes:
      - ./uploads:/app/uploads
      - ./processed:/app/processed
      - ./results:/app/results
    restart: always
```

```bash
# Deploy
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop
docker-compose down
```

---

## ⚙️ Environment Configuration

### Configuration Files

#### config.py
```python
# API settings (load from environment)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

# File handling
UPLOAD_FOLDER = "uploads/"
PROCESSED_FOLDER = "processed/"
RESULTS_FOLDER = "results/"

# Streamlit settings
MAX_UPLOAD_SIZE_MB = 50
```

#### config.toml (Streamlit)
```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501

[browser]
gatherUsageStats = false
```

### .env.example (Template)
```bash
# Copy this to .env and fill in your values
cp .env.example .env
```

---

## 💾 Database Setup

### Automatic Setup
Database tables are created automatically on first run:

```python
# Runs automatically in database.py
database._initialize()  # Creates all tables

# Tables created:
# - users
# - grading_sessions
# - grading_results
# - student_submissions
# - school_data
# ... (18+ tables total)
```

### Manual Database Reset
```bash
# Delete existing database
rm abdul_project.db

# Seed fresh data
python admin_data_seeder.py
python school_portal_data_seeder.py
```

### Database Backup
```bash
# Backup database
cp abdul_project.db abdul_project.db.backup

# Backup to file
sqlite3 abdul_project.db ".dump" > backup.sql

# Restore from backup
cp abdul_project.db.backup abdul_project.db
```

---

## 🔧 Troubleshooting

### Issue 1: Python Not Found

**Error:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
```bash
# Windows: Check PATH environment variable
# 1. Control Panel → System Properties
# 2. Environment Variables
# 3. Add Python to PATH

# Restart terminal and try:
python --version
```

---

### Issue 2: Virtual Environment Not Activating

**Error:**
```
.venv\Scripts\Activate.ps1 cannot be loaded
```

**Solution (Windows PowerShell):**
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Now activate
.venv\Scripts\Activate.ps1

# Deactivate when done
deactivate
```

---

### Issue 3: Dependencies Installation Fails

**Error:**
```
ERROR: Failed building wheel for easyocr
```

**Solution:**
```bash
# Update pip
pip install --upgrade pip

# Install build tools (Windows)
pip install --upgrade setuptools wheel

# Try again
pip install -r requirements.txt

# If still fails, install pre-built wheels
pip install easyocr --prefer-binary
```

---

### Issue 4: API Key Not Working

**Error:**
```
OpenRouter API key not found in environment variables
```

**Solution:**
```bash
# Verify .env file exists
ls -la .env

# Check format
cat .env

# Verify variable is set
python -c "import os; print(os.getenv('OPENROUTER_API_KEY'))"

# Should print your API key (not blank)

# Restart Streamlit after editing .env
# Press Ctrl+C and run: streamlit run app.py
```

---

### Issue 5: Streamlit Port Already in Use

**Error:**
```
Error: Address already in use
```

**Solution:**
```bash
# Kill process using port 8501
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8501
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

---

### Issue 6: Database Lock Error

**Error:**
```
database is locked
```

**Solution:**
```bash
# Close all connections
# 1. Restart Streamlit: Ctrl+C
# 2. Wait 5 seconds
# 3. Run again: streamlit run app.py

# If persists, reset database:
rm abdul_project.db
python admin_data_seeder.py
```

---

### Issue 7: Solana Connection Failed

**Error:**
```
Failed to connect to Solana RPC
```

**Solution:**
```bash
# Verify RPC URL in .env
SOLANA_RPC_URL=https://api.devnet.solana.com

# Test connectivity
curl https://api.devnet.solana.com

# Check if devnet is working:
# Visit: https://status.solana.com

# Try mainnet (if production)
SOLANA_NETWORK=mainnet-beta
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
```

---

## ✅ Verification Checklist

### Pre-Launch Verification

#### 1. System Setup
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip list`)
- [ ] Disk space available (500 MB+)
- [ ] Internet connection working

#### 2. Configuration
- [ ] .env file created from .env.example
- [ ] OPENROUTER_API_KEY set
- [ ] SOLANA_RECEIVER_WALLET set
- [ ] SOLANA_NETWORK set to devnet (or mainnet)
- [ ] No sensitive data in git commits

#### 3. Database
- [ ] Database created (abdul_project.db)
- [ ] Tables created (18+)
- [ ] Sample data seeded
- [ ] No database lock errors

#### 4. API Keys
- [ ] OpenRouter key valid
- [ ] Solana wallet valid
- [ ] Google Cloud credentials (if using)
- [ ] API rate limits OK

#### 5. Application
- [ ] Streamlit runs without errors
- [ ] All pages load
- [ ] Sample data visible
- [ ] Navigation works
- [ ] Upload functionality works

### Quick Test Commands

```bash
# 1. Check Python
python --version

# 2. Check pip packages
pip list | grep streamlit

# 3. Check environment
python -c "import os; print(os.getenv('OPENROUTER_API_KEY'))"

# 4. Check database
python -c "from database import Database; db = Database(); print('Database OK')"

# 5. Start app
streamlit run app.py

# 6. Test in browser
# Open: http://localhost:8501
```

---

## 📚 Next Steps After Setup

1. **Read Documentation**
   - [README.md](README.md) - Project overview
   - [MASTER_ADMIN_PANEL_README.md](MASTER_ADMIN_PANEL_README.md) - Admin features
   - [SCHOOL_PORTAL_README.md](SCHOOL_PORTAL_README.md) - School features

2. **Explore Features**
   - Visit Master Admin Panel (sample data)
   - Check School Portal (student management)
   - Review SaaS Hub (payment system)

3. **Configure for Production**
   - Get OpenRouter API key
   - Create Solana mainnet wallet
   - Update .env with production values
   - Deploy to cloud platform

4. **Customize**
   - Update school logo/branding
   - Configure payment rates
   - Set up custom email templates
   - Modify grading criteria

---

## 🆘 Getting Help

### Resources
- 📖 [Full Documentation](README.md)
- 🎛️ [Admin Panel Guide](MASTER_ADMIN_PANEL_README.md)
- 🏫 [School Portal Guide](SCHOOL_PORTAL_README.md)
- 🐛 [GitHub Issues](https://github.com/yourusername/abdul-project/issues)

### Support Channels
- 💬 GitHub Discussions
- 📧 Email: support@abdul-project.com
- 🐛 Bug Reports: GitHub Issues

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | May 2026 | Initial production release |

---

**Last Updated:** May 2026  
**Status:** ✅ Production Ready
