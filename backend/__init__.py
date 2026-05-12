"""
Backend Module - Core services and database layer

This module contains all backend services including:
- Database layer (database.py, saas_database.py)
- AI Services (grading_service.py, ocr_service.py)
- Payment Services (solana_payment_service.py)
- Utilities and helpers
- Data seeders
"""

from .database import Database
from .saas_database import SaaSDatabase
from .grading_service import GradingService
from .ocr_service import OCRService
from .file_processor import FileProcessor
from .analytics_service import AnalyticsService
from .excel_export import ExcelExporter
from .saas_access_control import AccessControl
from .solana_payment_service import SolanaPaymentService

__all__ = [
    'Database',
    'SaaSDatabase',
    'GradingService',
    'OCRService',
    'FileProcessor',
    'AnalyticsService',
    'ExcelExporter',
    'AccessControl',
    'SolanaPaymentService',
]
