# 📁 Project Structure Guide

## Clean Architecture: Backend/Frontend Separation

Your project now has a clean, professional structure separating concerns:

```
abdul-project/
│
├── 📂 backend/                    # All backend services & logic
│   ├── __init__.py
│   ├── database.py               # Main database layer
│   ├── saas_database.py          # SaaS subscription database
│   ├── config.py                 # Configuration & constants
│   │
│   ├── 🤖 AI & Services
│   ├── grading_service.py        # AI grading engine
│   ├── ocr_service.py            # Text extraction
│   ├── file_processor.py         # File handling
│   ├── analytics_service.py      # Analytics engine
│   ├── excel_export.py           # Excel reporting
│   │
│   ├── 💰 Payment Services
│   ├── solana_payment_service.py # Blockchain payments
│   ├── solana_config.py          # Solana configuration
│   ├── solana_utils.py           # Solana utilities
│   ├── saas_access_control.py    # Access control engine
│   │
│   ├── 🛠️ Utilities & Helpers
│   ├── helpers.py                # General utilities
│   ├── admin_helpers.py          # Admin utilities
│   ├── school_portal_helpers.py  # School utilities
│   │
│   └── 🌱 Data Seeders
│       ├── admin_data_seeder.py           # Admin sample data
│       └── school_portal_data_seeder.py   # School sample data
│
├── 📂 frontend/                   # All Streamlit UI components
│   ├── __init__.py
│   ├── app.py                    # Main Streamlit app (entry point)
│   ├── master_admin_panel.py     # Admin dashboard (2100+ lines)
│   ├── school_portal.py          # School portal (2000+ lines)
│   └── school_saas_hub_ui.py    # SaaS subscription UI
│
├── 📂 legacy_pages/               # Legacy admin features
│   ├── __init__.py
│   └── admin_payment_verification.py
│
├── 📂 uploads/                    # User uploads (git ignored)
│   └── receipts/
│
├── 📂 processed/                  # Processed files (git ignored)
├── 📂 results/                    # Export results (git ignored)
├── 📂 logs/                       # Application logs (git ignored)
├── 📂 .venv/                      # Virtual environment (git ignored)
│
├── 📚 Documentation
│   ├── README.md
│   ├── setup.md
│   ├── MASTER_ADMIN_PANEL_README.md
│   ├── ADMIN_PANEL_QUICKSTART.md
│   ├── ADMIN_PANEL_ARCHITECTURE.md
│   ├── ADMIN_PANEL_TESTING_CHECKLIST.md
│   ├── SCHOOL_PORTAL_README.md
│   ├── SCHOOL_PORTAL_QUICKSTART.md
│   ├── SCHOOL_PORTAL_ARCHITECTURE.md
│   ├── SCHOOL_PORTAL_DELIVERY_SUMMARY.md
│   ├── DELIVERY_SUMMARY.md
│   └── PROJECT_STRUCTURE.md (this file)
│
├── ⚙️ Configuration
│   ├── config.toml
│   ├── .env.example
│   ├── .gitignore
│   ├── .gitattributes
│   ├── requirements.txt
│   └── LICENSE
│
└── 📦 Database (git ignored)
    └── abdul_project.db

```

## 🎯 Architecture Overview

### Backend (`backend/`)
**Purpose:** All business logic, services, and data persistence

| Module | Purpose | Files |
|--------|---------|-------|
| **Database** | Data persistence layer | database.py, saas_database.py |
| **AI Services** | Machine learning & NLP | grading_service.py, ocr_service.py |
| **File Processing** | Document handling | file_processor.py, analytics_service.py, excel_export.py |
| **Payments** | Blockchain integration | solana_payment_service.py, solana_config.py, solana_utils.py |
| **Access Control** | Permissions & authentication | saas_access_control.py |
| **Utilities** | Helper functions | helpers.py, admin_helpers.py, school_portal_helpers.py |
| **Data Seeding** | Sample data generation | admin_data_seeder.py, school_portal_data_seeder.py |

### Frontend (`frontend/`)
**Purpose:** All user-facing Streamlit UI components

| Module | Purpose | Lines |
|--------|---------|-------|
| **app.py** | Main entry point & navigation | 400+ |
| **master_admin_panel.py** | Admin dashboard with 11 sections | 2100+ |
| **school_portal.py** | School management interface | 2000+ |
| **school_saas_hub_ui.py** | SaaS subscription & payment UI | 800+ |

---

## 🚀 How to Run

### From Root Directory
```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows

# Run the frontend app (automatically imports backend)
streamlit run frontend/app.py
```

### Directory Structure Benefits

✅ **Separation of Concerns**
- Backend logic separate from UI
- Easy to maintain and update
- Clear dependency flow

✅ **Scalability**
- Add new services to backend
- Create new frontend pages easily
- Decouple logic from presentation

✅ **Testing**
- Test backend services independently
- Test frontend components separately
- Easy to mock dependencies

✅ **Deployment**
- Deploy backend and frontend separately
- Easier to containerize
- Better for microservices architecture

---

## 📦 Import Paths

### In Frontend Files
```python
# Automatically resolves to backend/ modules
from database import Database
from grading_service import GradingService
from analytics_service import AnalyticsService
# ... etc

# Local imports within frontend
from master_admin_panel import render_master_admin_panel
from school_portal import render_school_portal
```

### Path Resolution
All frontend files have automatic path setup:
```python
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(Path(__file__).resolve().parent))
```

This allows clean imports without worrying about relative paths.

---

## 🔄 File Organization Tips

### Adding New Backend Service
1. Create file in `backend/`
2. Add import to `backend/__init__.py`
3. Use in frontend: `from my_service import MyService`

### Adding New Frontend Page
1. Create file in `frontend/`
2. Import in `frontend/app.py`
3. Add navigation option

### Adding New Utility
1. Add to appropriate backend helper (helpers.py, admin_helpers.py, etc.)
2. Use via: `from helpers import my_function`

---

## 🛠️ Maintenance

### Update Imports When Moving Files
All imports automatically resolve through the path setup in each file.

### Database Path Reference
Database uses relative path from config:
```python
DB_PATH = Path(__file__).resolve().parent.parent / "abdul_project.db"
```
✅ Works correctly from both root and backend directories

### Configuration Access
Config is imported from backend:
```python
from config import OPENROUTER_API_KEY, UPLOAD_FOLDER
```

---

## ✅ Migration Completed

- ✅ Created `/backend` directory with 17 backend files
- ✅ Created `/frontend` directory with 4 UI files
- ✅ Created `__init__.py` in both directories
- ✅ Updated all imports in frontend files
- ✅ Path resolution configured automatically
- ✅ All services accessible from frontend
- ✅ Database paths adjusted to work from root

---

## 🎓 Running the Application

```bash
# Navigate to project root
cd "d:\zip of FYP\abdul project"

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies (if needed)
pip install -r requirements.txt

# Seed database
python backend/admin_data_seeder.py
python backend/school_portal_data_seeder.py

# Run frontend
streamlit run frontend/app.py

# Visit: http://localhost:8501
```

---

## 📝 Next Steps

1. **Test the Application**
   - Run `streamlit run frontend/app.py`
   - Navigate through all pages
   - Verify all services work

2. **Git Commit**
   ```bash
   git add -A
   git commit -m "Refactor: Organize code into backend/frontend structure"
   git push origin main
   ```

3. **Update Documentation**
   - Update internal references if needed
   - Update deployment guides
   - Update onboarding docs

4. **Consider Further Optimization**
   - Create subdirectories in backend (services/, models/, utils/)
   - Add type hints across all modules
   - Add comprehensive error handling
   - Add logging throughout

---

**Last Updated:** May 2026  
**Status:** ✅ Structure Complete
