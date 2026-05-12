
import os

# --------------------------
# API KEYS (replace with your keys or load securely)
# --------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "abdul-project-grading-app")
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "http://localhost:5000")

# --------------------------
# FILE HANDLING
# --------------------------
ALLOWED_FILE_EXTENSIONS = ['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg']

UPLOAD_FOLDER = "uploads/"
PROCESSED_FOLDER = "processed/"
RESULTS_FOLDER = "results/"

# --------------------------
# GRADING DEFAULTS
# --------------------------
DEFAULT_PASSING_MARK = 50  # Example default passing mark
DEFAULT_BIN_SIZE = 10      # For analytics bins

# --------------------------
# STREAMLIT SETTINGS
# --------------------------
MAX_UPLOAD_SIZE_MB = 50    # Max file size to upload (adjust as needed)

# --------------------------
# OTHER CONSTANTS
# --------------------------
LOG_FILE = "logs/app.log"

# Ensure folders exist at runtime
for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER, RESULTS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)
