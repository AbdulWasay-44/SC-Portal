# 🎓 Abdul School Management & AI Grading Platform

> **Enterprise-Level SaaS Platform** for AI-Powered School Management, Automated Grading, and Payment Processing

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)](https://streamlit.io/)
[![Solana](https://img.shields.io/badge/Blockchain-Solana-purple)](https://solana.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Components](#system-components)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Database](#database)
- [API Integration](#api-integration)
- [Security](#security)
- [Contributing](#contributing)

---

## 🎯 Overview

Abdul's School Management Platform is a **comprehensive, production-ready SaaS system** that combines:

- 🏫 **Complete School Management** - Students, teachers, classes, attendance, exams, assignments
- 🤖 **AI-Powered Grading** - Automated essay/assignment evaluation using OpenRouter API
- 💰 **Payment Processing** - Solana blockchain integration for secure, transparent payments
- 🎛️ **Enterprise Admin Panel** - 11-section command center for system governance
- 📊 **Advanced Analytics** - Real-time dashboards and comprehensive reporting
- 👥 **Multi-Role Access Control** - Students, Teachers, Admin, and Super Admin roles

**Status:** Production-Ready | **Version:** 1.0.0

---

## ✨ Key Features

### 🏫 School Portal (14+ Modules)
| Feature | Description |
|---------|-------------|
| 📚 **Student Management** | Create, edit, search students with profiles and performance tracking |
| 👨‍🏫 **Teacher Management** | Manage teachers, subjects, schedules, and assignments |
| 🏛️ **Class Management** | Organize classes, sections, and student grouping |
| 📝 **Attendance Tracking** | Real-time attendance marking with analytics |
| 📖 **Exams & Results** | Create exams, manage results, generate report cards |
| ✏️ **Assignments** | Create and track assignments with AI evaluation |
| 🤖 **AI Grading** | Automatic grading with detailed feedback using OpenRouter |
| 👀 **OCR Technology** | Extract text from handwritten & printed documents |
| 💵 **Fee Management** | Track student fees, generate receipts, payment reminders |
| 📊 **Reports & Analytics** | Student performance, attendance trends, revenue analysis |
| 📢 **Announcements** | School-wide broadcasts and notifications |
| 📚 **Library Management** | Book inventory and borrowing system |
| 🚌 **Transport & Hostel** | Manage transport routes and hostel accommodations |
| ⚙️ **System Settings** | Configure school details and system parameters |

### 🎛️ Master Admin Panel (11 Sections)
| Section | Features |
|---------|----------|
| 📊 **Global Overview** | 8 KPI cards, system health, real-time metrics |
| 📈 **Activity Monitor** | Real-time activity logs, user actions, system events |
| 👥 **User Access Control** | Suspend/unsuspend users, reset passwords, manage permissions |
| 🤖 **AI System Monitoring** | Grading accuracy, OCR success rate, model health |
| 💰 **Payment Governance** | Transaction verification, fraud detection, revenue analytics |
| 🔧 **Maintenance Control** | Database backups, cache management, service monitoring |
| 🔐 **Security Center** | Threat monitoring, access logs, incident tracking |
| 📉 **Advanced Analytics** | Traffic analysis, revenue trends, user behavior |
| 📢 **Broadcast Center** | Send announcements, notifications, system messages |
| 👑 **Role Management** | Define permissions for 5+ user roles |
| ⚙️ **System Settings** | Global configuration, email setup, theme settings |

### 💰 SaaS Hub & Payment System
| Feature | Details |
|---------|---------|
| 📱 **Subscription Plans** | Standard & Premium tiers with feature differentiation |
| 🔗 **Solana Integration** | Blockchain-based payment processing |
| 💳 **Multiple Currencies** | Support for PKR, USD, and other currencies |
| 📄 **Receipt Management** | Auto-generated digital receipts and proof of payment |
| 🔐 **Secure Wallets** | Encrypted wallet management and key storage |
| ✅ **Payment Verification** | Admin approval workflow for transaction verification |
| 🎓 **School Registration** | Multi-school support with isolated data |
| 📊 **Revenue Tracking** | Comprehensive payment analytics and reporting |

### 🔒 Security & Access Control
- ✅ Role-based access control (RBAC)
- ✅ Encrypted password storage
- ✅ Session management
- ✅ Audit trails for all operations
- ✅ API key protection in `.env`
- ✅ Solana keypair security
- ✅ Fraud detection algorithms

---

## 🏗️ System Components

### 1. **Frontend** - Streamlit UI
- Responsive web interface
- Real-time dashboards
- Interactive charts (Plotly)
- File upload handling
- Multi-tab navigation

### 2. **Backend Services**
- **Database Layer** - SQLite with 18+ tables
- **Grading Service** - OpenRouter AI integration
- **OCR Service** - EasyOCR text extraction
- **Payment Service** - Solana RPC communication
- **Analytics Engine** - Data aggregation and visualization
- **File Processor** - PDF, DOCX, image handling

### 3. **Data Layer**
- SQLite database for persistence
- 18+ normalized tables
- Relationship constraints
- Transaction support

### 4. **Payment Layer**
- Solana blockchain RPC calls
- Transaction verification
- Wallet management
- Payment confirmation

---

## 💻 Technology Stack

### Core Technologies
```
Backend:           Python 3.8+
Frontend:          Streamlit
Database:          SQLite3
Blockchain:        Solana (devnet/mainnet)
AI/ML:            OpenRouter API, EasyOCR
```

### Key Libraries
```
streamlit              # Web framework
pandas                 # Data manipulation
plotly                 # Interactive charts
PyPDF2                 # PDF processing
python-docx           # Word document handling
pillow                 # Image processing
pdfplumber            # PDF text extraction
easyocr               # Optical character recognition
openpyxl              # Excel export
google-cloud-vision   # Alternative OCR
requests              # HTTP client
solders               # Solana blockchain SDK
```

### Infrastructure
- Local development: Streamlit dev server
- Production: Streamlit Cloud or Docker
- Database: SQLite (local) or PostgreSQL (production)
- Blockchain: Solana devnet for testing, mainnet for production

---

## 🚀 Quick Start

### Minimum Requirements
- Python 3.8+
- 2GB RAM
- 500MB disk space
- Internet connection (for API calls)

### 30-Second Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd abdul-project

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 5. Seed sample data
python admin_data_seeder.py
python school_portal_data_seeder.py

# 6. Start application
streamlit run app.py
```

👉 **Detailed setup instructions in [setup.md](setup.md)**

---

## 📁 Project Structure

```
abdul-project/
│
├── 📄 Core Application
│   ├── app.py                          # Main entry point
│   ├── config.py                       # Configuration
│   ├── config.toml                     # Streamlit settings
│   ├── requirements.txt                # Dependencies
│   └── helpers.py                      # Utilities
│
├── 🎛️ Admin Panel
│   ├── master_admin_panel.py           # Admin dashboard (2100+ lines)
│   ├── admin_helpers.py                # Admin utilities (600+ lines)
│   └── admin_data_seeder.py            # Sample data generator
│
├── 🏫 School Portal
│   ├── school_portal.py                # Main school interface (2000+ lines)
│   ├── school_portal_helpers.py        # School utilities (600+ lines)
│   └── school_portal_data_seeder.py    # School sample data
│
├── 💰 SaaS & Payments
│   ├── school_saas_hub_ui.py          # SaaS UI module
│   ├── saas_database.py                # SaaS database layer
│   ├── saas_access_control.py          # Access control engine
│   ├── solana_payment_service.py       # Blockchain payments (500+ lines)
│   ├── solana_config.py                # Solana configuration
│   └── solana_utils.py                 # Solana utilities
│
├── 🤖 AI & Services
│   ├── grading_service.py              # AI grading engine
│   ├── ocr_service.py                  # Text extraction
│   ├── file_processor.py               # File handling
│   ├── analytics_service.py            # Analytics engine
│   └── excel_export.py                 # Excel reports
│
├── 💾 Database
│   ├── database.py                     # Main database layer (600+ lines)
│   └── abdul_project.db                # SQLite database (excluded from git)
│
├── 📚 Documentation
│   ├── README.md                       # This file
│   ├── setup.md                        # Installation guide
│   ├── MASTER_ADMIN_PANEL_README.md   # Admin panel docs (50+ pages)
│   ├── ADMIN_PANEL_QUICKSTART.md      # Admin quick start
│   ├── ADMIN_PANEL_ARCHITECTURE.md    # System architecture
│   ├── SCHOOL_PORTAL_README.md        # School portal docs
│   ├── SCHOOL_PORTAL_QUICKSTART.md    # School quick start
│   └── SCHOOL_PORTAL_ARCHITECTURE.md  # Technical guide
│
├── 📦 Configuration
│   ├── .env.example                    # Environment template
│   ├── .gitignore                      # Git ignore rules
│   └── .gitattributes                  # Git attributes
│
└── 📂 Directories (Git Ignored)
    ├── .venv/                          # Virtual environment
    ├── uploads/                        # User uploads
    ├── processed/                      # Generated files
    ├── results/                        # Export results
    └── logs/                           # Application logs
```

---

## 📖 Documentation

### 📋 Main Documentation
- **[README.md](README.md)** - Project overview (this file)
- **[setup.md](setup.md)** - Installation & deployment

### 🎛️ Admin Panel
- **[MASTER_ADMIN_PANEL_README.md](MASTER_ADMIN_PANEL_README.md)** - Complete feature guide (50+ pages)
- **[ADMIN_PANEL_QUICKSTART.md](ADMIN_PANEL_QUICKSTART.md)** - Quick start (5 minutes)
- **[ADMIN_PANEL_ARCHITECTURE.md](ADMIN_PANEL_ARCHITECTURE.md)** - Technical architecture
- **[ADMIN_PANEL_TESTING_CHECKLIST.md](ADMIN_PANEL_TESTING_CHECKLIST.md)** - Testing guide

### 🏫 School Portal
- **[SCHOOL_PORTAL_README.md](SCHOOL_PORTAL_README.md)** - Feature documentation
- **[SCHOOL_PORTAL_QUICKSTART.md](SCHOOL_PORTAL_QUICKSTART.md)** - Quick start (5 minutes)
- **[SCHOOL_PORTAL_ARCHITECTURE.md](SCHOOL_PORTAL_ARCHITECTURE.md)** - Technical design

---

## 💾 Installation

### Prerequisites
```bash
# Check Python version (3.8+)
python --version

# Check pip
pip --version
```

### Step-by-Step Setup

**1. Clone Repository**
```bash
git clone https://github.com/yourusername/abdul-project.git
cd abdul-project
```

**2. Create Virtual Environment**
```bash
python -m venv .venv

# Activate (Windows)
.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment**
```bash
# Copy template
cp .env.example .env

# Edit .env with your keys
# Required keys:
# - OPENROUTER_API_KEY
# - SOLANA_RECEIVER_WALLET
# - GOOGLE_APPLICATION_CREDENTIALS (optional, for Cloud Vision)
```

**5. Seed Database**
```bash
python admin_data_seeder.py
python school_portal_data_seeder.py
```

**6. Start Application**
```bash
streamlit run app.py
```

✅ **Application running at:** `http://localhost:8501`

---

## ⚙️ Configuration

### Environment Variables (.env)

```ini
# ── OpenRouter (AI Grading) ───────────────────────────────────
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_APP_NAME=school-saas-grading
OPENROUTER_SITE_URL=http://localhost:8501

# ── Solana (Blockchain Payments) ──────────────────────────────
SOLANA_NETWORK=devnet              # devnet for testing, mainnet-beta for production
SOLANA_RPC_URL=https://api.devnet.solana.com
SOLANA_RECEIVER_WALLET=YOUR_WALLET_ADDRESS_HERE
SOLANA_PAYMENT_TIMEOUT=900         # 15 minutes
SOLANA_CONFIRMATION_TIMEOUT=120    # 2 minutes
SOLANA_MIN_CONFIRMATIONS=3

# ── Google Cloud Vision (OCR) ────────────────────────────────
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# ── SOL/PKR Conversion ────────────────────────────────────────
FALLBACK_SOL_USD_RATE=142.50
```

### Streamlit Config (config.toml)
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

---

## 🎮 Usage

### For Students
1. **Register/Login** - Create account as student
2. **Submit Assignments** - Upload documents for grading
3. **View Feedback** - Get AI-generated grading feedback
4. **Track Performance** - View analytics and grade history
5. **Process Payments** - Pay subscription via Solana

### For Teachers
1. **Create Assignments** - Set grading criteria
2. **Set Exams** - Create and manage exams
3. **View Results** - AI-graded submissions
4. **Send Feedback** - Customize grading comments
5. **Export Reports** - Generate Excel report cards

### For School Admins
1. **Manage School** - Configure school details
2. **Student/Teacher Admin** - Manage users
3. **Approve Payments** - Verify payment receipts
4. **Generate Reports** - School-wide analytics
5. **System Settings** - Configure application

### For Master Admins
1. **System Monitoring** - KPI dashboards
2. **User Management** - Global access control
3. **Payment Governance** - Fraud detection, verification
4. **AI Monitoring** - Grading accuracy, OCR performance
5. **Security** - Activity logs, threat detection

---

## 🏛️ Architecture

### High-Level Architecture
```
┌──────────────────────────────────────────────────────────┐
│                   STREAMLIT FRONTEND                      │
│         (Multi-page: Welcome, Teachers, Students, Admin)  │
└────────────────────┬─────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    ┌────────┐  ┌──────────┐  ┌──────────┐
    │ School │  │ Master   │  │ SaaS Hub │
    │ Portal │  │ Admin    │  │ Payment  │
    │        │  │ Panel    │  │ System   │
    └────────┘  └──────────┘  └──────────┘
        │            │            │
        └────────────┼────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
    ┌────────────────┐    ┌──────────────────┐
    │ Business Logic │    │ AI Services      │
    │ & Helpers      │    │ - Grading        │
    │                │    │ - OCR            │
    │ - Validators   │    │ - Analytics      │
    │ - Formatters   │    │ - Export         │
    │ - Generators   │    └──────────────────┘
    └────────────────┘             │
        │                          │
        └──────────────┬───────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    ┌────────┐  ┌─────────┐  ┌─────────────┐
    │SQLite  │  │OpenRouter│  │Solana RPC   │
    │Database│  │API       │  │Blockchain   │
    └────────┘  └─────────┘  └─────────────┘
```

### Data Flow
```
User Upload → File Processor → OCR/Text Extraction → 
Grading Service (AI) → Results Storage → Analytics → 
Visualization Dashboard
```

---

## 💾 Database

### Schema Overview
18+ tables for:
- **Users** - Student, teacher, admin accounts
- **School Data** - Classes, subjects, exams
- **Academic** - Attendance, grades, assignments
- **Payments** - Transactions, subscriptions, receipts
- **Admin** - Activity logs, settings, backups

### Tables
| Table | Purpose |
|-------|---------|
| `users` | User authentication & profiles |
| `grading_sessions` | Grading submission batches |
| `grading_results` | AI grading output |
| `student_submissions` | Assignment submissions |
| `school_data` | School information |
| `saas_subscriptions` | Subscription records |
| `saas_payments` | Payment transactions |
| `activity_logs` | System audit trail |
| ... (11 more) | Various operational data |

---

## 🔌 API Integration

### OpenRouter (AI Grading)
```python
# Automatic integration via GradingService
# Supports: GPT-4, Claude, Llama models
# Features: JSON parsing, streaming, token limiting
```

### Solana (Blockchain Payments)
```python
# Via SolanaPaymentService
# Features: RPC calls, transaction verification,
# wallet management, payment confirmation
```

### EasyOCR (Text Extraction)
```python
# Via OCRService
# Supports: Handwritten & printed text
# Languages: English (extensible)
```

---

## 🔐 Security

### Access Control
- ✅ Role-based permissions (5 roles)
- ✅ Session management
- ✅ Encrypted passwords (SHA256)
- ✅ API key in environment only

### Data Protection
- ✅ Encrypted API credentials
- ✅ Solana keypair security
- ✅ No sensitive data in commits (.gitignore)
- ✅ Audit trails for all operations

### Best Practices
1. **Never commit .env files** - Use .env.example template
2. **Keep credentials secure** - Use environment variables
3. **Validate all inputs** - Prevent injection attacks
4. **Use HTTPS** - Enable in production
5. **Regular backups** - Automated database backups

---

## 🤝 Contributing

### Development Setup
```bash
# Fork & clone repository
git clone https://github.com/yourusername/abdul-project.git
cd abdul-project

# Create feature branch
git checkout -b feature/your-feature

# Install dev dependencies
pip install -r requirements.txt

# Make changes & test
# Commit & push
git push origin feature/your-feature

# Create pull request
```

### Code Standards
- ✅ Follow PEP 8
- ✅ Use type hints
- ✅ Document functions
- ✅ Test before committing
- ✅ Update documentation

---

## 📞 Support & Contact

- 📧 Email: support@abdul-project.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📚 Wiki: Project Wiki

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎉 Acknowledgments

- **Streamlit** - Web framework
- **OpenRouter** - AI API
- **Solana** - Blockchain integration
- **EasyOCR** - Text recognition
- **Plotly** - Visualizations

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Lines of Code | 15,000+ |
| Python Files | 20 |
| Database Tables | 18+ |
| Documentation Pages | 125+ |
| Features | 50+ |
| Supported Roles | 5 |

---

**Last Updated:** May 2026  
**Status:** ✅ Production Ready  
**Version:** 1.0.0
