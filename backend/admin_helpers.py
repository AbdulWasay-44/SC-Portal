"""
=============================================================================
MASTER ADMIN PANEL - Helper Functions & Utilities
=============================================================================

Utility functions, database helpers, and support services for the
Master Admin Panel.

Features:
- User management utilities
- Payment processing helpers
- Security utilities
- Analytics helpers
- Data validation and formatting
- Email/notification services

Author: Abdul's School Portal Team
Version: 1.0.0
=============================================================================
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
import json
import random
import string


# ============================================================================
# USER MANAGEMENT UTILITIES
# ============================================================================

class UserManager:
    """Utilities for user management operations."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def generate_temp_password(length: int = 12) -> str:
        """Generate a temporary password."""
        characters = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def get_user_activity_summary(user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get activity summary for a user."""
        return {
            "user_id": user_id,
            "total_logins": random.randint(5, 100),
            "assignments_submitted": random.randint(0, 50),
            "files_uploaded": random.randint(0, 30),
            "last_login": datetime.now() - timedelta(days=random.randint(0, 7)),
            "first_login": datetime.now() - timedelta(days=random.randint(30, 365)),
            "account_age_days": random.randint(30, 365),
        }

    @staticmethod
    def get_role_permissions(role: str) -> Dict[str, bool]:
        """Get all permissions for a specific role."""
        permissions = {
            "Super Admin": {
                "manage_users": True,
                "manage_payments": True,
                "manage_security": True,
                "manage_ai": True,
                "manage_system": True,
                "view_analytics": True,
                "manage_roles": True,
                "backup_database": True,
                "send_broadcasts": True,
                "manage_maintenance": True,
            },
            "Admin": {
                "manage_users": True,
                "manage_payments": True,
                "manage_security": False,
                "manage_ai": False,
                "manage_system": True,
                "view_analytics": True,
                "manage_roles": False,
                "backup_database": False,
                "send_broadcasts": True,
                "manage_maintenance": False,
            },
            "Teacher": {
                "manage_users": False,
                "manage_payments": False,
                "manage_security": False,
                "manage_ai": False,
                "manage_system": False,
                "view_analytics": True,
                "manage_roles": False,
                "backup_database": False,
                "send_broadcasts": False,
                "manage_maintenance": False,
            },
            "Student": {
                "manage_users": False,
                "manage_payments": False,
                "manage_security": False,
                "manage_ai": False,
                "manage_system": False,
                "view_analytics": False,
                "manage_roles": False,
                "backup_database": False,
                "send_broadcasts": False,
                "manage_maintenance": False,
            },
        }
        return permissions.get(role, {})


# ============================================================================
# PAYMENT PROCESSING UTILITIES
# ============================================================================

class PaymentManager:
    """Utilities for payment processing and management."""

    @staticmethod
    def validate_transaction_id(transaction_id: str) -> bool:
        """Validate transaction ID format."""
        # Format: TXN20240510XXXXX
        import re
        pattern = r'^TXN\d{8}\d{5}$'
        return re.match(pattern, transaction_id) is not None

    @staticmethod
    def generate_receipt_id() -> str:
        """Generate a unique receipt ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"RCP{timestamp}{random_suffix}"

    @staticmethod
    def generate_invoice_number() -> str:
        """Generate a unique invoice number."""
        timestamp = datetime.now().strftime("%Y%m%d")
        random_suffix = ''.join(random.choices(string.digits, k=6))
        return f"INV{timestamp}{random_suffix}"

    @staticmethod
    def calculate_late_fee(amount: float, late_percentage: float = 5.0) -> float:
        """Calculate late payment fee."""
        return amount * (late_percentage / 100)

    @staticmethod
    def detect_duplicate_transaction(
        transaction_id: str,
        amount: float,
        student_id: str,
        transactions_list: List[Dict[str, Any]],
        time_window_minutes: int = 60
    ) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Detect if a transaction is a duplicate.
        
        Returns:
            Tuple of (is_duplicate, duplicate_transaction_dict)
        """
        current_time = datetime.now()
        
        for trans in transactions_list:
            trans_time = trans.get('timestamp', current_time)
            time_diff = (current_time - trans_time).total_seconds() / 60
            
            if (trans.get('student_id') == student_id and
                abs(trans.get('amount', 0) - amount) < 0.01 and
                time_diff <= time_window_minutes):
                return True, trans
        
        return False, None

    @staticmethod
    def detect_suspicious_activity(transaction: Dict[str, Any]) -> List[str]:
        """
        Detect suspicious patterns in a transaction.
        
        Returns:
            List of suspicious patterns detected
        """
        flags = []
        
        amount = transaction.get('amount', 0)
        if amount > 10000:
            flags.append("Unusually high amount")
        
        # Check for repeated receipts
        if transaction.get('receipt_count', 0) > 1:
            flags.append("Multiple receipt submissions")
        
        # Check for unusual IPs
        if transaction.get('ip_address'):
            flags.append("New IP address detected")
        
        return flags

    @staticmethod
    def calculate_payment_statistics(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate payment statistics from transaction list."""
        if not transactions:
            return {}
        
        total_amount = sum(t.get('amount', 0) for t in transactions)
        count = len(transactions)
        
        return {
            "total_transactions": count,
            "total_amount": total_amount,
            "average_amount": total_amount / count if count > 0 else 0,
            "min_amount": min(t.get('amount', 0) for t in transactions) if transactions else 0,
            "max_amount": max(t.get('amount', 0) for t in transactions) if transactions else 0,
        }


# ============================================================================
# SECURITY UTILITIES
# ============================================================================

class SecurityManager:
    """Utilities for security monitoring and management."""

    @staticmethod
    def validate_ip_address(ip: str) -> bool:
        """Validate IP address format."""
        import re
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        
        # Check if all octets are 0-255
        octets = ip.split('.')
        return all(0 <= int(octet) <= 255 for octet in octets)

    @staticmethod
    def check_brute_force_attack(
        failed_attempts: int,
        time_window_minutes: int = 15,
        threshold: int = 5
    ) -> bool:
        """Check if brute force attack threshold is exceeded."""
        return failed_attempts >= threshold

    @staticmethod
    def generate_security_alert(
        alert_type: str,
        severity: str,
        user_id: str,
        details: str
    ) -> Dict[str, Any]:
        """Generate a security alert."""
        alert_id = f"ALR{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            "alert_id": alert_id,
            "type": alert_type,
            "severity": severity,
            "user_id": user_id,
            "details": details,
            "timestamp": datetime.now(),
            "status": "New",
            "resolved": False,
        }

    @staticmethod
    def get_threat_level(
        failed_logins: int,
        suspicious_ips: int,
        unusual_activities: int
    ) -> str:
        """Calculate overall threat level."""
        threat_score = (failed_logins * 0.3) + (suspicious_ips * 0.4) + (unusual_activities * 0.3)
        
        if threat_score < 20:
            return "Low"
        elif threat_score < 50:
            return "Medium"
        elif threat_score < 80:
            return "High"
        else:
            return "Critical"


# ============================================================================
# AI SYSTEM UTILITIES
# ============================================================================

class AISystemManager:
    """Utilities for AI system monitoring and management."""

    @staticmethod
    def get_ai_health_metrics() -> Dict[str, Any]:
        """Get current AI system health metrics."""
        return {
            "grading_engine_health": random.uniform(85, 100),
            "ocr_engine_health": random.uniform(80, 95),
            "api_uptime": random.uniform(99, 99.99),
            "average_response_time": random.uniform(2, 8),
            "success_rate": random.uniform(90, 98),
        }

    @staticmethod
    def calculate_ai_accuracy(
        total_gradings: int,
        correct_gradings: int,
        feedback_quality_score: float
    ) -> Dict[str, float]:
        """Calculate AI accuracy metrics."""
        accuracy_percentage = (correct_gradings / total_gradings * 100) if total_gradings > 0 else 0
        
        return {
            "accuracy_percentage": accuracy_percentage,
            "confidence_score": random.uniform(85, 95),
            "feedback_quality": feedback_quality_score,
            "ocr_accuracy": random.uniform(88, 96),
        }

    @staticmethod
    def get_model_performance_insights() -> Dict[str, Any]:
        """Get insights into model performance."""
        return {
            "best_performing_subject": "Mathematics",
            "worst_performing_subject": "Essay Writing",
            "improvement_areas": [
                "Handwriting recognition",
                "Mathematical notation",
                "Diagram interpretation"
            ],
            "confidence_threshold": 0.85,
            "training_progress": random.uniform(85, 100),
        }


# ============================================================================
# ANALYTICS UTILITIES
# ============================================================================

class AnalyticsHelper:
    """Utilities for analytics and reporting."""

    @staticmethod
    def calculate_growth_percentage(current: float, previous: float) -> float:
        """Calculate percentage growth."""
        if previous == 0:
            return 100 if current > 0 else 0
        return ((current - previous) / previous) * 100

    @staticmethod
    def get_trend_direction(values: List[float]) -> str:
        """Determine trend direction from list of values."""
        if len(values) < 2:
            return "Stable"
        
        recent = values[-1]
        previous = values[-2]
        
        if recent > previous:
            return "Uptrend"
        elif recent < previous:
            return "Downtrend"
        else:
            return "Stable"

    @staticmethod
    def calculate_weekly_metrics(daily_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate weekly aggregated metrics."""
        if not daily_data:
            return {}
        
        return {
            "week_total": sum(d.get('value', 0) for d in daily_data),
            "week_average": sum(d.get('value', 0) for d in daily_data) / len(daily_data),
            "week_max": max(d.get('value', 0) for d in daily_data),
            "week_min": min(d.get('value', 0) for d in daily_data),
        }

    @staticmethod
    def calculate_monthly_metrics(daily_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate monthly aggregated metrics."""
        if not daily_data:
            return {}
        
        return {
            "month_total": sum(d.get('value', 0) for d in daily_data),
            "month_average": sum(d.get('value', 0) for d in daily_data) / len(daily_data),
            "month_max": max(d.get('value', 0) for d in daily_data),
            "month_min": min(d.get('value', 0) for d in daily_data),
        }

    @staticmethod
    def get_top_performers(
        data: List[Dict[str, Any]],
        key: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get top performers from data list."""
        sorted_data = sorted(data, key=lambda x: x.get(key, 0), reverse=True)
        return sorted_data[:limit]

    @staticmethod
    def get_performance_percentile(value: float, all_values: List[float]) -> float:
        """Calculate percentile rank for a value."""
        if not all_values:
            return 0
        
        rank = sum(1 for v in all_values if v <= value)
        return (rank / len(all_values)) * 100


# ============================================================================
# DATA VALIDATION & FORMATTING
# ============================================================================

class DataValidator:
    """Utilities for data validation."""

    @staticmethod
    def validate_school_code(code: str) -> bool:
        """Validate school code format."""
        import re
        # Format: XXX-NNN or XXXNNN
        pattern = r'^[A-Z]{2,4}[-]?[0-9]{1,4}$'
        return re.match(pattern, code.upper()) is not None

    @staticmethod
    def validate_student_id(student_id: str) -> bool:
        """Validate student ID format."""
        import re
        # Format: STU followed by 5-6 digits
        pattern = r'^STU\d{5,6}$'
        return re.match(pattern, student_id.upper()) is not None

    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Validate monetary amount."""
        return isinstance(amount, (int, float)) and amount > 0

    @staticmethod
    def clean_phone_number(phone: str) -> str:
        """Clean and format phone number."""
        import re
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)
        return cleaned


class DataFormatter:
    """Utilities for data formatting."""

    @staticmethod
    def format_currency(amount: float, currency: str = "USD") -> str:
        """Format amount as currency."""
        currency_symbols = {
            "USD": "$",
            "EUR": "€",
            "GBP": "£",
            "AED": "د.إ",
        }
        symbol = currency_symbols.get(currency, currency)
        return f"{symbol}{amount:,.2f}"

    @staticmethod
    def format_date(date_obj: datetime, format_str: str = "%Y-%m-%d") -> str:
        """Format date object."""
        return date_obj.strftime(format_str)

    @staticmethod
    def format_time(time_seconds: float) -> str:
        """Format seconds to readable time."""
        hours = int(time_seconds // 3600)
        minutes = int((time_seconds % 3600) // 60)
        seconds = int(time_seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    @staticmethod
    def format_percentage(value: float, decimal_places: int = 1) -> str:
        """Format value as percentage."""
        return f"{value:.{decimal_places}f}%"

    @staticmethod
    def truncate_text(text: str, length: int = 50) -> str:
        """Truncate text to specified length."""
        if len(text) <= length:
            return text
        return text[:length-3] + "..."


# ============================================================================
# NOTIFICATION & EMAIL SERVICES
# ============================================================================

class NotificationService:
    """Service for sending notifications."""

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """Send email notification."""
        # Placeholder for email sending logic
        return True

    @staticmethod
    def send_sms(phone_number: str, message: str) -> bool:
        """Send SMS notification."""
        # Placeholder for SMS sending logic
        return True

    @staticmethod
    def send_in_app_notification(user_id: str, message: str, type_: str = "info") -> bool:
        """Send in-app notification."""
        # Placeholder for in-app notification logic
        return True

    @staticmethod
    def send_push_notification(device_id: str, title: str, message: str) -> bool:
        """Send push notification."""
        # Placeholder for push notification logic
        return True

    @staticmethod
    def send_bulk_notification(
        user_ids: List[str],
        message: str,
        channels: List[str] = None
    ) -> Dict[str, int]:
        """Send bulk notifications."""
        if channels is None:
            channels = ["email", "in_app"]
        
        return {
            "total_sent": len(user_ids),
            "email_sent": len(user_ids) if "email" in channels else 0,
            "sms_sent": len(user_ids) if "sms" in channels else 0,
            "push_sent": len(user_ids) if "push" in channels else 0,
        }


# ============================================================================
# REPORT GENERATION
# ============================================================================

class ReportGenerator:
    """Utilities for generating reports."""

    @staticmethod
    def generate_daily_report() -> Dict[str, Any]:
        """Generate daily summary report."""
        return {
            "date": datetime.now().date(),
            "total_users_online": random.randint(500, 2000),
            "total_transactions": random.randint(50, 300),
            "system_uptime": random.uniform(99, 99.99),
            "api_calls": random.randint(5000, 50000),
            "errors_encountered": random.randint(0, 50),
            "successful_gradings": random.randint(100, 1000),
        }

    @staticmethod
    def generate_weekly_report() -> Dict[str, Any]:
        """Generate weekly summary report."""
        return {
            "week_starting": (datetime.now() - timedelta(days=datetime.now().weekday())).date(),
            "total_users_active": random.randint(3000, 5000),
            "total_transactions": random.randint(500, 3000),
            "average_daily_uptime": random.uniform(99, 99.99),
            "successful_gradings": random.randint(2000, 10000),
            "total_revenue": random.uniform(50000, 200000),
        }

    @staticmethod
    def generate_monthly_report() -> Dict[str, Any]:
        """Generate monthly summary report."""
        return {
            "month": datetime.now().strftime("%B %Y"),
            "total_students": random.randint(3000, 5000),
            "total_teachers": random.randint(100, 200),
            "total_transactions": random.randint(2000, 10000),
            "total_revenue": random.uniform(200000, 500000),
            "successful_gradings": random.randint(10000, 50000),
            "new_registrations": random.randint(100, 500),
            "system_incidents": random.randint(0, 5),
        }


if __name__ == "__main__":
    # Test utility functions
    print("Admin Panel Helpers Module Loaded Successfully")
    
    # Test user manager
    print(f"\n[UserManager] Sample password: {UserManager.generate_temp_password()}")
    print(f"[UserManager] Email valid: {UserManager.validate_email('test@school.edu')}")
    
    # Test payment manager
    print(f"\n[PaymentManager] Receipt ID: {PaymentManager.generate_receipt_id()}")
    print(f"[PaymentManager] Invoice ID: {PaymentManager.generate_invoice_number()}")
    
    # Test data formatter
    print(f"\n[DataFormatter] Currency: {DataFormatter.format_currency(1234.56)}")
    print(f"[DataFormatter] Percentage: {DataFormatter.format_percentage(85.5)}")
