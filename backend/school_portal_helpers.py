"""
SCHOOL PORTAL HELPERS
Advanced utilities for school management system.
"""

import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import json


# ==================== ID GENERATORS ====================

def generate_student_id(class_name: str, roll_number: int, year: str = None) -> str:
    """Generate unique student ID."""
    if year is None:
        year = datetime.now().strftime("%Y")
    return f"STU-{year}-{class_name}-{str(roll_number).zfill(3)}"


def generate_teacher_id(year: str = None) -> str:
    """Generate unique teacher ID."""
    if year is None:
        year = datetime.now().strftime("%Y")
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TCH-{year}-{random_suffix}"


def generate_class_id(class_name: str, section: str = "A") -> str:
    """Generate unique class ID."""
    return f"CLASS-{class_name}-{section}"


def generate_subject_id(subject_code: str, class_name: str) -> str:
    """Generate unique subject ID."""
    return f"SUB-{subject_code}-{class_name}"


def generate_exam_id(year: str = None) -> str:
    """Generate unique exam ID."""
    if year is None:
        year = datetime.now().strftime("%Y")
    random_suffix = ''.join(random.choices(string.digits, k=5))
    return f"EXAM-{year}-{random_suffix}"


def generate_assignment_id(year: str = None) -> str:
    """Generate unique assignment ID."""
    if year is None:
        year = datetime.now().strftime("%Y")
    random_suffix = ''.join(random.choices(string.digits, k=5))
    return f"ASS-{year}-{random_suffix}"


def generate_fee_id(student_id: str, year: str = None) -> str:
    """Generate unique fee ID."""
    if year is None:
        year = datetime.now().strftime("%Y")
    return f"FEE-{year}-{student_id}"


def generate_payment_id(year: str = None) -> str:
    """Generate unique payment ID."""
    if year is None:
        year = datetime.now().strftime("%Y")
    random_suffix = ''.join(random.choices(string.digits, k=6))
    return f"PAY-{year}-{random_suffix}"


def generate_transport_id() -> str:
    """Generate unique transport ID."""
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"TRN-{random_suffix}"


def generate_hostel_id() -> str:
    """Generate unique hostel ID."""
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"HST-{random_suffix}"


def generate_book_id() -> str:
    """Generate unique book ID."""
    random_suffix = ''.join(random.choices(string.digits, k=6))
    return f"BK-{random_suffix}"


def generate_receipt_number() -> str:
    """Generate receipt number."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices(string.digits, k=3))
    return f"RCP-{timestamp}-{random_suffix}"


# ==================== VALIDATORS ====================

def validate_email(email: str) -> bool:
    """Validate email format."""
    if not email:
        return False
    return "@" in email and "." in email.split("@")[1]


def validate_phone(phone: str) -> bool:
    """Validate phone number."""
    if not phone:
        return False
    return len(phone) >= 10 and phone.replace("-", "").replace(" ", "").isdigit()


def validate_roll_number(roll_number: int) -> bool:
    """Validate roll number."""
    return 1 <= roll_number <= 100


def validate_marks(marks: float, total_marks: float) -> bool:
    """Validate marks."""
    return 0 <= marks <= total_marks


def validate_percentage(percentage: float) -> bool:
    """Validate percentage."""
    return 0 <= percentage <= 100


# ==================== FORMATTERS ====================

def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"₹ {amount:,.2f}"


def format_date(date_str: str) -> str:
    """Format date string."""
    if not date_str:
        return "-"
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %b %Y")
    except:
        return date_str


def format_percentage(percentage: float) -> str:
    """Format percentage."""
    return f"{percentage:.1f}%"


def format_grade(percentage: float) -> str:
    """Convert percentage to grade."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def calculate_gpa(marks_list: List[float], total_marks: float = 100) -> float:
    """Calculate GPA from marks."""
    if not marks_list:
        return 0.0
    percentages = [min((marks / total_marks) * 100, 100) for marks in marks_list]
    return round(sum(percentages) / len(percentages) / 10, 2)


def calculate_percentage(obtained: float, total: float) -> float:
    """Calculate percentage."""
    if total == 0:
        return 0.0
    return round((obtained / total) * 100, 2)


# ==================== STATUS & COLOR MAPPING ====================

def get_status_color(status: str) -> str:
    """Get color for status."""
    status_colors = {
        "Active": "🟢",
        "Inactive": "🔴",
        "Pending": "🟡",
        "Approved": "✅",
        "Rejected": "❌",
        "Verified": "✔️",
        "Suspended": "⏸️",
        "Present": "✅",
        "Absent": "❌",
        "Leave": "📋",
        "Submitted": "✅",
        "Borrowed": "📕",
        "Returned": "✅",
        "Overdue": "⚠️",
        "Paid": "💚",
        "Unpaid": "❌",
        "Partial": "🟡"
    }
    return status_colors.get(status, "⚪")


def get_priority_color(priority: str) -> str:
    """Get color for priority."""
    priority_colors = {
        "Low": "🟢",
        "Medium": "🟡",
        "High": "🔴",
        "Critical": "🔴🔴"
    }
    return priority_colors.get(priority, "⚪")


def get_grade_color(grade: str) -> str:
    """Get emoji for grade."""
    grade_colors = {
        "A+": "🟢",
        "A": "🟢",
        "B": "🟡",
        "C": "🟠",
        "D": "🔴",
        "F": "🔴🔴"
    }
    return grade_colors.get(grade, "⚪")


# ==================== DATA CALCULATORS ====================

def calculate_attendance_percentage(present_days: int, total_days: int) -> float:
    """Calculate attendance percentage."""
    if total_days == 0:
        return 0.0
    return round((present_days / total_days) * 100, 2)


def calculate_late_fees(due_date: str, payment_date: str, daily_rate: float = 5.0) -> float:
    """Calculate late fees."""
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        payment = datetime.strptime(payment_date, "%Y-%m-%d")
        days_late = (payment - due).days
        if days_late > 0:
            return round(days_late * daily_rate, 2)
    except:
        pass
    return 0.0


def is_overdue(due_date: str) -> bool:
    """Check if due date is overdue."""
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        return datetime.now() > due
    except:
        return False


def days_until_due(due_date: str) -> int:
    """Get days until due date."""
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        delta = (due - datetime.now()).days
        return max(delta, 0)
    except:
        return 0


def calculate_class_average(marks_list: List[float]) -> float:
    """Calculate class average."""
    if not marks_list:
        return 0.0
    return round(sum(marks_list) / len(marks_list), 2)


def get_topper_student(students_data: List[Dict]) -> Dict:
    """Get topper student."""
    if not students_data:
        return {}
    return max(students_data, key=lambda x: x.get("percentage", 0))


def get_weak_students(students_data: List[Dict], threshold: float = 50) -> List[Dict]:
    """Get weak performing students."""
    return [s for s in students_data if s.get("percentage", 100) < threshold]


# ==================== ANALYTICS ====================

class AnalyticsCalculator:
    """Calculate analytics metrics."""
    
    @staticmethod
    def get_kpi_data(students: List[Dict], teachers: List[Dict], classes: List[Dict]) -> Dict:
        """Get KPI data."""
        return {
            "total_students": len(students),
            "total_teachers": len(teachers),
            "total_classes": len(classes),
            "active_students": len([s for s in students if s.get("status") == "Active"]),
            "active_teachers": len([t for t in teachers if t.get("status") == "Active"]),
            "average_class_size": round(len(students) / len(classes)) if classes else 0
        }
    
    @staticmethod
    def get_attendance_stats(attendance_records: List[Dict], student_id: str = None) -> Dict:
        """Calculate attendance statistics."""
        if student_id:
            records = [r for r in attendance_records if r.get("student_id") == student_id]
        else:
            records = attendance_records
        
        if not records:
            return {"present": 0, "absent": 0, "leave": 0, "percentage": 0}
        
        present = len([r for r in records if r.get("status") == "Present"])
        absent = len([r for r in records if r.get("status") == "Absent"])
        leave = len([r for r in records if r.get("status") == "Leave"])
        total = len(records)
        
        return {
            "present": present,
            "absent": absent,
            "leave": leave,
            "percentage": round((present / total) * 100, 2) if total > 0 else 0
        }
    
    @staticmethod
    def get_exam_statistics(exam_results: List[Dict]) -> Dict:
        """Calculate exam statistics."""
        if not exam_results:
            return {"average": 0, "highest": 0, "lowest": 0, "passed": 0, "failed": 0}
        
        marks = [r.get("obtained_marks", 0) for r in exam_results]
        total_marks = [r.get("total_marks", 100) for r in exam_results]
        percentages = [calculate_percentage(m, t) for m, t in zip(marks, total_marks)]
        passing_grade = [r.get("passing_marks", 40) for r in exam_results]
        
        passed = len([p for p, pm in zip(percentages, passing_grade) if p >= pm])
        failed = len(exam_results) - passed
        
        return {
            "average": round(sum(percentages) / len(percentages), 2) if percentages else 0,
            "highest": max(percentages) if percentages else 0,
            "lowest": min(percentages) if percentages else 0,
            "passed": passed,
            "failed": failed,
            "pass_percentage": round((passed / len(exam_results)) * 100, 2) if exam_results else 0
        }
    
    @staticmethod
    def get_fee_statistics(fees: List[Dict]) -> Dict:
        """Calculate fee statistics."""
        if not fees:
            return {"total": 0, "collected": 0, "pending": 0, "collection_rate": 0}
        
        total = sum([f.get("amount", 0) for f in fees])
        collected = sum([f.get("paid_amount", 0) for f in fees if f.get("payment_status") == "Paid"])
        pending = total - collected
        
        return {
            "total": total,
            "collected": collected,
            "pending": pending,
            "collection_rate": round((collected / total) * 100, 2) if total > 0 else 0
        }


# ==================== RANKING & PERFORMANCE ====================

def rank_students_by_performance(students_with_marks: List[Dict]) -> List[Tuple[int, Dict]]:
    """Rank students by their average marks."""
    sorted_students = sorted(
        students_with_marks,
        key=lambda x: x.get("average_marks", 0),
        reverse=True
    )
    return [(rank + 1, student) for rank, student in enumerate(sorted_students)]


def categorize_performance(percentage: float) -> str:
    """Categorize student performance."""
    if percentage >= 80:
        return "Excellent"
    elif percentage >= 60:
        return "Good"
    elif percentage >= 40:
        return "Average"
    else:
        return "Poor"


def get_performance_color(category: str) -> str:
    """Get color for performance category."""
    colors = {
        "Excellent": "🟢",
        "Good": "🟢",
        "Average": "🟡",
        "Poor": "🔴"
    }
    return colors.get(category, "⚪")


# ==================== RANDOM DATA GENERATORS ====================

def generate_random_attendance() -> str:
    """Generate random attendance status."""
    return random.choice(["Present", "Absent", "Leave"])


def generate_random_phone() -> str:
    """Generate random phone number."""
    return f"98{random.randint(00000000, 99999999)}"


def generate_random_marks(total_marks: float) -> float:
    """Generate random marks."""
    return round(random.uniform(0, total_marks), 2)


def generate_random_percentage() -> float:
    """Generate random percentage."""
    return round(random.uniform(0, 100), 2)


def generate_random_name(gender: str = "M") -> Tuple[str, str]:
    """Generate random name."""
    first_names_m = ["Aditya", "Arjun", "Akshay", "Amit", "Aman", "Anuj", "Ankur", "Ashok"]
    first_names_f = ["Aisha", "Amrita", "Anjali", "Archana", "Ananya", "Asha", "Avni", "Arya"]
    last_names = ["Singh", "Kumar", "Sharma", "Patel", "Gupta", "Verma", "Kapoor", "Malhotra"]
    
    first = random.choice(first_names_m if gender == "M" else first_names_f)
    last = random.choice(last_names)
    return first, last


def generate_random_date(days_back: int = 365) -> str:
    """Generate random date within last N days."""
    date = datetime.now() - timedelta(days=random.randint(0, days_back))
    return date.strftime("%Y-%m-%d")


def generate_random_time() -> str:
    """Generate random time."""
    hour = random.randint(8, 17)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"


# ==================== EXPORT HELPERS ====================

def prepare_student_report(student: Dict, attendance: Dict, results: Dict) -> Dict:
    """Prepare comprehensive student report."""
    return {
        "name": f"{student.get('first_name')} {student.get('last_name')}",
        "student_id": student.get("student_id"),
        "class": student.get("class"),
        "roll_number": student.get("roll_number"),
        "attendance": attendance,
        "exam_results": results,
        "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def prepare_class_report(class_data: Dict, students: List[Dict], statistics: Dict) -> Dict:
    """Prepare comprehensive class report."""
    return {
        "class_name": class_data.get("class_name"),
        "class_id": class_data.get("class_id"),
        "total_students": len(students),
        "statistics": statistics,
        "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# ==================== AI INTEGRATION HELPERS ====================

def prepare_ai_grading_input(assignment: Dict, submission: Dict) -> Dict:
    """Prepare data for AI grading."""
    return {
        "assignment_id": assignment.get("assignment_id"),
        "total_marks": assignment.get("total_marks"),
        "rubric": assignment.get("grading_rubric", "Standard rubric"),
        "submission_text": submission.get("text_content", ""),
        "student_id": submission.get("student_id")
    }


def parse_ai_grading_output(ai_output: Dict) -> Dict:
    """Parse AI grading output."""
    return {
        "marks_obtained": ai_output.get("score", 0),
        "feedback": ai_output.get("feedback", ""),
        "strengths": ai_output.get("strengths", []),
        "improvements": ai_output.get("improvements", []),
        "confidence_score": ai_output.get("confidence", 0.0)
    }


def calculate_ai_plagiarism_score(submission_text: str) -> float:
    """Simulate plagiarism detection."""
    # Placeholder for real plagiarism detection
    return round(random.uniform(0, 30), 2)


# ==================== NOTIFICATION HELPERS ====================

def generate_notification(title: str, message: str, priority: str = "Normal") -> Dict:
    """Generate notification."""
    return {
        "title": title,
        "message": message,
        "priority": priority,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read": False
    }


def get_notification_icon(notification_type: str) -> str:
    """Get icon for notification type."""
    icons = {
        "Assignment": "📝",
        "Exam": "📝",
        "Fee": "💰",
        "Attendance": "📋",
        "Result": "📊",
        "Alert": "⚠️",
        "Achievement": "🏆",
        "Transport": "🚌",
        "Hostel": "🏠"
    }
    return icons.get(notification_type, "📢")


# ==================== SEARCH & FILTER ====================

def search_students(students: List[Dict], query: str) -> List[Dict]:
    """Search students by name or ID."""
    query = query.lower()
    return [
        s for s in students
        if query in s.get("first_name", "").lower()
        or query in s.get("last_name", "").lower()
        or query in s.get("student_id", "").lower()
        or query in s.get("email", "").lower()
    ]


def filter_by_class(students: List[Dict], class_name: str) -> List[Dict]:
    """Filter students by class."""
    return [s for s in students if s.get("class") == class_name]


def filter_by_status(items: List[Dict], status: str) -> List[Dict]:
    """Filter items by status."""
    return [item for item in items if item.get("status") == status]


def filter_by_date_range(items: List[Dict], start_date: str, end_date: str) -> List[Dict]:
    """Filter items by date range."""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return [
            item for item in items
            if start <= datetime.strptime(item.get("created_at", ""), "%Y-%m-%d") <= end
        ]
    except:
        return items


# ==================== AUDIT & LOGGING ====================

def generate_audit_log(action: str, target: str, user_id: str, details: Dict = None) -> Dict:
    """Generate audit log entry."""
    return {
        "action": action,
        "target": target,
        "user_id": user_id,
        "details": details or {},
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": "127.0.0.1"
    }


# ==================== DASHBOARD HELPERS ====================

class DashboardHelper:
    """Helper for dashboard rendering."""
    
    @staticmethod
    def get_dashboard_summary(school_data: Dict) -> Dict:
        """Get dashboard summary."""
        return {
            "total_students": school_data.get("total_students", 0),
            "total_teachers": school_data.get("total_teachers", 0),
            "total_classes": school_data.get("total_classes", 0),
            "active_courses": school_data.get("active_courses", 0),
            "attendance_rate": school_data.get("avg_attendance", 0),
            "assignments_submitted": school_data.get("assignments_submitted", 0),
            "pending_fees": school_data.get("pending_fees", 0),
            "ai_requests": school_data.get("ai_requests", 0)
        }
    
    @staticmethod
    def get_recent_activities(activities: List[Dict], limit: int = 10) -> List[Dict]:
        """Get recent activities."""
        return activities[:limit]
    
    @staticmethod
    def get_alerts(alerts: List[Dict]) -> List[Dict]:
        """Get system alerts."""
        return sorted(alerts, key=lambda x: x.get("priority_level", 0), reverse=True)
