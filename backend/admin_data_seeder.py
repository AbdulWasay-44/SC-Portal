"""
=============================================================================
ADMIN PANEL - Database Seeding & Sample Data Generation
=============================================================================

This module provides functions to seed the admin panel database with
realistic sample data for testing and demonstration purposes.

Usage:
    python admin_data_seeder.py
    OR
    from admin_data_seeder import seed_admin_database
    seed_admin_database()

Author: Abdul's School Portal Team
Version: 1.0.0
=============================================================================
"""

import sqlite3
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any


DB_PATH = Path(__file__).resolve().parent / "abdul_project.db"


def get_connection(db_path: str = str(DB_PATH)) -> sqlite3.Connection:
    """Get database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def seed_payment_transactions(count: int = 50) -> None:
    """Seed payment transactions table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    payment_methods = ["Credit Card", "Debit Card", "Bank Transfer", "Online Wallet"]
    statuses = ["Pending", "Verified", "Rejected", "Refunded", "Partial Paid"]
    
    transactions = []
    for i in range(count):
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d')}{1000+i}"
        student_id = f"STU{1000+i}"
        student_name = f"Student {i+1}"
        amount = random.uniform(500, 5000)
        method = random.choice(payment_methods)
        status = random.choice(statuses)
        verified_by = "admin_001" if random.random() > 0.4 else None
        receipt_id = f"RCP{datetime.now().strftime('%Y%m%d%H%M%S')}{1000+i}" if status == "Verified" else None
        
        transactions.append((
            transaction_id, student_id, student_name, amount, method, status,
            verified_by, receipt_id, datetime.now() - timedelta(days=random.randint(0, 60))
        ))
    
    cursor.executemany(
        """
        INSERT INTO payment_transactions 
        (transaction_id, student_id, student_name, amount, payment_method, status, 
         verified_by, receipt_id, transaction_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        transactions
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} payment transactions")


def seed_activity_logs(count: int = 100) -> None:
    """Seed activity logs table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    activity_types = [
        "Login", "Logout", "File Upload", "Grading", 
        "Assignment Submit", "Exam Submit", "Payment", "Settings Change"
    ]
    roles = ["Student", "Teacher", "Admin"]
    statuses = ["Success", "Pending", "Failed"]
    
    logs = []
    for i in range(count):
        user_id = f"USR{1000+i}"
        username = f"user_{1000+i}"
        role = random.choice(roles)
        activity_type = random.choice(activity_types)
        status = random.choice(statuses)
        
        logs.append((
            user_id, username, role, activity_type,
            f"{activity_type} activity", f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            status, None, datetime.now() - timedelta(hours=random.randint(1, 720))
        ))
    
    cursor.executemany(
        """
        INSERT INTO activity_logs 
        (user_id, username, user_role, activity_type, activity_description, ip_address, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        logs
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} activity logs")


def seed_system_alerts(count: int = 20) -> None:
    """Seed system alerts table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    alert_types = [
        "High CPU Usage",
        "Database Error",
        "Failed Payment",
        "Security Breach Attempt",
        "Service Down",
        "Storage Limit",
        "API Rate Limit"
    ]
    severities = ["Low", "Medium", "High", "Critical"]
    statuses = ["New", "Investigating", "Resolved"]
    
    alerts = []
    for i in range(count):
        alert_id = f"ALR{datetime.now().strftime('%Y%m%d')}{1000+i}"
        alert_type = random.choice(alert_types)
        severity = random.choice(severities)
        status = random.choice(statuses)
        
        alerts.append((
            alert_id, alert_type, severity,
            f"Alert: {alert_type}",
            f"Details for {alert_type}",
            status, 0, "admin_001" if status != "New" else None,
            datetime.now() - timedelta(hours=random.randint(1, 168))
        ))
    
    cursor.executemany(
        """
        INSERT INTO system_alerts 
        (alert_id, alert_type, severity, title, description, status, resolved, assigned_to, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        alerts
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} system alerts")


def seed_ai_monitoring(count: int = 30) -> None:
    """Seed AI monitoring metrics."""
    conn = get_connection()
    cursor = conn.cursor()
    
    metrics = [
        ("Grading Accuracy", 85, 100),
        ("OCR Success Rate", 75, 100),
        ("Average Response Time", 1, 10),
        ("API Uptime", 95, 100),
        ("Model Confidence", 60, 100),
    ]
    statuses = ["Normal", "Warning", "Critical"]
    
    records = []
    for i in range(count):
        metric_name, min_val, max_val = random.choice(metrics)
        value = random.uniform(min_val, max_val)
        status = random.choice(statuses)
        
        records.append((
            metric_name, value, status, None,
            datetime.now() - timedelta(hours=random.randint(0, 72))
        ))
    
    cursor.executemany(
        """
        INSERT INTO ai_monitoring 
        (metric_name, metric_value, status, details_json, recorded_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        records
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} AI monitoring records")


def seed_fraud_detection_logs(count: int = 15) -> None:
    """Seed fraud detection logs."""
    conn = get_connection()
    cursor = conn.cursor()
    
    fraud_types = [
        "Duplicate Transaction",
        "Suspicious IP",
        "Multiple Failed Attempts",
        "Repeated Receipt",
        "Unusual Amount"
    ]
    severities = ["Low", "Medium", "High"]
    statuses = ["Investigating", "Resolved", "False Alarm"]
    
    records = []
    for i in range(count):
        fraud_id = f"FRD{datetime.now().strftime('%Y%m%d')}{1000+i}"
        fraud_type = random.choice(fraud_types)
        severity = random.choice(severities)
        status = random.choice(statuses)
        confidence = random.uniform(0.5, 1.0)
        
        records.append((
            fraud_id, fraud_type, severity,
            f"TXN{datetime.now().strftime('%Y%m%d')}{random.randint(1000, 9999)}",
            f"STU{random.randint(1000, 9999)}",
            f"Pattern: {fraud_type}",
            confidence,
            status,
            f"Action: {status}",
            datetime.now() - timedelta(days=random.randint(0, 30))
        ))
    
    cursor.executemany(
        """
        INSERT INTO fraud_detection_logs 
        (fraud_id, fraud_type, fraud_severity, transaction_id, student_id, 
         suspicious_pattern, confidence_score, status, action_taken, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        records
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} fraud detection logs")


def seed_admin_actions(count: int = 40) -> None:
    """Seed admin actions log."""
    conn = get_connection()
    cursor = conn.cursor()
    
    action_types = [
        "User Suspension",
        "Password Reset",
        "Payment Verification",
        "System Restart",
        "Backup Created",
        "Permission Change",
        "Database Optimization"
    ]
    statuses = ["Completed", "In Progress", "Failed"]
    
    records = []
    for i in range(count):
        action_id = f"ACT{datetime.now().strftime('%Y%m%d')}{1000+i}"
        action_type = random.choice(action_types)
        status = random.choice(statuses)
        
        records.append((
            action_id, "admin_001", action_type,
            f"USR{random.randint(1000, 9999)}" if "User" in action_type else None,
            None,
            f"Action: {action_type}",
            status,
            None,
            datetime.now() - timedelta(hours=random.randint(1, 168))
        ))
    
    cursor.executemany(
        """
        INSERT INTO admin_actions 
        (action_id, admin_username, action_type, target_user, target_resource, 
         action_description, status, details_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        records
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} admin actions")


def seed_security_incidents(count: int = 25) -> None:
    """Seed security incidents."""
    conn = get_connection()
    cursor = conn.cursor()
    
    incident_types = [
        "Failed Login Attempt",
        "Suspicious IP Access",
        "Multiple Device Login",
        "Permission Violation",
        "Unusual Activity Pattern"
    ]
    severities = ["Low", "Medium", "High", "Critical"]
    statuses = ["New", "Investigating", "Resolved"]
    
    records = []
    for i in range(count):
        incident_id = f"INC{datetime.now().strftime('%Y%m%d')}{1000+i}"
        incident_type = random.choice(incident_types)
        severity = random.choice(severities)
        status = random.choice(statuses)
        
        records.append((
            incident_id, incident_type, severity,
            f"USR{random.randint(1000, 9999)}",
            f"203.45.{random.randint(1, 255)}.{random.randint(1, 255)}",
            f"Security incident: {incident_type}",
            status,
            f"Investigation notes for {incident_type}",
            f"Resolution for {incident_type}" if status == "Resolved" else None,
            datetime.now() - timedelta(days=random.randint(0, 60))
        ))
    
    cursor.executemany(
        """
        INSERT INTO security_incidents 
        (incident_id, incident_type, severity, user_id, ip_address, description, 
         status, investigation_notes, resolution, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        records
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} security incidents")


def seed_role_permissions() -> None:
    """Seed default role permissions."""
    conn = get_connection()
    cursor = conn.cursor()
    
    roles_permissions = {
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
            "grade_students": True,
            "upload_materials": True,
            "view_analytics": True,
            "create_assignments": True,
        },
        "Student": {
            "submit_assignments": True,
            "view_grades": True,
            "download_materials": True,
        },
    }
    
    for role, permissions in roles_permissions.items():
        cursor.execute(
            """
            INSERT OR IGNORE INTO role_permissions 
            (role_name, permissions_json)
            VALUES (?, ?)
            """,
            (role, json.dumps(permissions))
        )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded role permissions for {len(roles_permissions)} roles")


def seed_broadcasts(count: int = 10) -> None:
    """Seed broadcast messages."""
    conn = get_connection()
    cursor = conn.cursor()
    
    broadcast_types = [
        "General Announcement",
        "Emergency Alert",
        "Exam Reminder",
        "Maintenance Notice"
    ]
    
    records = []
    for i in range(count):
        broadcast_id = f"BRD{datetime.now().strftime('%Y%m%d')}{1000+i}"
        broadcast_type = random.choice(broadcast_types)
        recipients = json.dumps(["Students", "Teachers"])
        channels = json.dumps(["Email", "InApp", "Push"])
        
        records.append((
            broadcast_id, broadcast_type,
            f"Title {i+1}",
            f"Message content {i+1}",
            recipients, channels, "admin_001",
            None, datetime.now() - timedelta(days=random.randint(0, 30)),
            "Sent", random.randint(100, 500)
        ))
    
    cursor.executemany(
        """
        INSERT INTO broadcasts 
        (broadcast_id, broadcast_type, title, message, recipients_json, channels_json, 
         sent_by, scheduled_time, sent_time, status, delivery_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        records
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} broadcast messages")


def seed_system_backups(count: int = 12) -> None:
    """Seed system backups records."""
    conn = get_connection()
    cursor = conn.cursor()
    
    backup_types = ["Full", "Incremental", "Differential"]
    statuses = ["Completed", "Failed"]
    
    records = []
    for i in range(count):
        backup_id = f"BKP{datetime.now().strftime('%Y%m%d')}{1000+i}"
        backup_type = random.choice(backup_types)
        
        records.append((
            backup_id, backup_type,
            random.uniform(100, 5000),
            f"/backups/backup_{i}.zip",
            random.choice(statuses),
            "admin_001",
            datetime.now() - timedelta(days=random.randint(1, 60))
        ))
    
    cursor.executemany(
        """
        INSERT INTO system_backups 
        (backup_id, backup_type, backup_size_mb, backup_location, status, created_by, backup_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        records
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} system backup records")


def seed_admin_notifications(count: int = 30) -> None:
    """Seed admin notifications."""
    conn = get_connection()
    cursor = conn.cursor()
    
    notification_types = [
        "Payment Alert",
        "System Alert",
        "Security Alert",
        "User Activity",
        "AI Alert"
    ]
    priorities = ["Low", "Normal", "High", "Critical"]
    
    records = []
    for i in range(count):
        notification_id = f"NTF{datetime.now().strftime('%Y%m%d%H%M%S')}{1000+i}"
        notif_type = random.choice(notification_types)
        priority = random.choice(priorities)
        is_read = 1 if random.random() > 0.3 else 0
        
        records.append((
            notification_id, "admin_001", notif_type,
            f"Notification {i+1}",
            f"Details for notification {i+1}",
            priority, is_read, None,
            datetime.now() - timedelta(hours=random.randint(0, 72))
        ))
    
    cursor.executemany(
        """
        INSERT INTO admin_notifications 
        (notification_id, admin_username, notification_type, title, message, priority, is_read, action_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        records
    )
    
    conn.commit()
    conn.close()
    print(f"✅ Seeded {count} admin notifications")


def seed_admin_database() -> None:
    """
    Seed all admin panel tables with sample data.
    Run this function once to populate the database.
    """
    print("\n" + "="*70)
    print("ADMIN PANEL DATABASE SEEDING")
    print("="*70 + "\n")
    
    try:
        seed_payment_transactions(50)
        seed_activity_logs(100)
        seed_system_alerts(20)
        seed_ai_monitoring(30)
        seed_fraud_detection_logs(15)
        seed_admin_actions(40)
        seed_security_incidents(25)
        seed_role_permissions()
        seed_broadcasts(10)
        seed_system_backups(12)
        seed_admin_notifications(30)
        
        print("\n" + "="*70)
        print("✅ DATABASE SEEDING COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR during seeding: {str(e)}")
        print("Make sure the database tables have been created first.\n")


if __name__ == "__main__":
    seed_admin_database()
