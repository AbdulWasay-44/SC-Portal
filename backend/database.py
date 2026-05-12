import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


DB_PATH = Path(__file__).resolve().parent / "abdul_project.db"


class Database:
    """SQLite-backed persistence for users and grading history."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = str(db_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS grading_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_username TEXT NOT NULL,
                    total_marks INTEGER NOT NULL,
                    custom_criteria_json TEXT NOT NULL,
                    additional_instructions TEXT,
                    detect_multiple_questions INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS grading_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    total_marks REAL NOT NULL,
                    awarded_marks REAL NOT NULL,
                    percentage REAL NOT NULL,
                    feedback TEXT,
                    criteria_breakdown_json TEXT NOT NULL,
                    criteria_explanations_json TEXT NOT NULL,
                    questions_json TEXT NOT NULL,
                    strengths_json TEXT NOT NULL,
                    areas_for_improvement_json TEXT NOT NULL,
                    grade_justification TEXT,
                    text_content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(session_id) REFERENCES grading_sessions(id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS student_submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_username TEXT NOT NULL,
                    title TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    submission_type TEXT NOT NULL,
                    deadline TEXT,
                    filename TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    extracted_text TEXT,
                    estimated_score REAL NOT NULL DEFAULT 0,
                    ai_feedback_json TEXT NOT NULL,
                    plagiarism_percentage REAL NOT NULL DEFAULT 0,
                    matched_source TEXT,
                    resubmission_allowed INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    category TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_username TEXT NOT NULL,
                    title TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    assessment_type TEXT NOT NULL,
                    submission_deadline TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    total_marks REAL NOT NULL,
                    questions_json TEXT NOT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS assessment_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id INTEGER NOT NULL,
                    student_username TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    submitted_at TEXT,
                    expires_at TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'started',
                    answers_json TEXT NOT NULL,
                    auto_score REAL NOT NULL DEFAULT 0,
                    total_marks REAL NOT NULL DEFAULT 0,
                    teacher_grade REAL,
                    ai_feedback TEXT,
                    FOREIGN KEY(assessment_id) REFERENCES assessments(id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS schools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    school_name TEXT NOT NULL,
                    school_code TEXT NOT NULL UNIQUE,
                    admin_username TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS school_memberships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    school_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    school_role TEXT NOT NULL,
                    approved INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(school_id, username),
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            # ============ ADMIN PANEL TABLES ============
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS payment_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT NOT NULL UNIQUE,
                    student_id TEXT NOT NULL,
                    student_name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Pending',
                    verified_by TEXT,
                    receipt_id TEXT,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    verified_date TIMESTAMP,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    username TEXT NOT NULL,
                    user_role TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    activity_description TEXT NOT NULL,
                    ip_address TEXT,
                    status TEXT NOT NULL DEFAULT 'Success',
                    details_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS system_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT NOT NULL UNIQUE,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'New',
                    resolved INTEGER NOT NULL DEFAULT 0,
                    assigned_to TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TIMESTAMP
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS ai_monitoring (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metric_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT NOT NULL DEFAULT 'Normal',
                    details_json TEXT,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS fraud_detection_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fraud_id TEXT NOT NULL UNIQUE,
                    fraud_type TEXT NOT NULL,
                    fraud_severity TEXT NOT NULL,
                    transaction_id TEXT,
                    student_id TEXT,
                    suspicious_pattern TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Investigating',
                    action_taken TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TIMESTAMP
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS admin_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_id TEXT NOT NULL UNIQUE,
                    admin_username TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    target_user TEXT,
                    target_resource TEXT,
                    action_description TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Completed',
                    details_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS admin_notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    notification_id TEXT NOT NULL UNIQUE,
                    admin_username TEXT NOT NULL,
                    notification_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    priority TEXT NOT NULL DEFAULT 'Normal',
                    is_read INTEGER NOT NULL DEFAULT 0,
                    action_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    read_at TIMESTAMP
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS security_incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    incident_id TEXT NOT NULL UNIQUE,
                    incident_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    user_id TEXT,
                    ip_address TEXT,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'New',
                    investigation_notes TEXT,
                    resolution TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TIMESTAMP
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS role_permissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_name TEXT NOT NULL UNIQUE,
                    permissions_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS system_backups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    backup_id TEXT NOT NULL UNIQUE,
                    backup_type TEXT NOT NULL,
                    backup_size_mb REAL NOT NULL,
                    backup_location TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Completed',
                    created_by TEXT NOT NULL,
                    backup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    restore_date TIMESTAMP
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS broadcasts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    broadcast_id TEXT NOT NULL UNIQUE,
                    broadcast_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    recipients_json TEXT NOT NULL,
                    channels_json TEXT NOT NULL,
                    sent_by TEXT NOT NULL,
                    scheduled_time TIMESTAMP,
                    sent_time TIMESTAMP,
                    status TEXT NOT NULL DEFAULT 'Sent',
                    delivery_count INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            
            # ============ SCHOOL PORTAL TABLES ============
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    roll_number INTEGER NOT NULL,
                    class TEXT NOT NULL,
                    section TEXT,
                    email TEXT,
                    phone TEXT,
                    parent_name TEXT,
                    parent_phone TEXT,
                    parent_email TEXT,
                    date_of_birth TEXT,
                    address TEXT,
                    admission_date TEXT,
                    photo_url TEXT,
                    status TEXT NOT NULL DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    subject_expertise TEXT,
                    experience_years INTEGER,
                    qualification TEXT,
                    address TEXT,
                    date_of_birth TEXT,
                    photo_url TEXT,
                    status TEXT NOT NULL DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    class_name TEXT NOT NULL,
                    class_teacher_id TEXT,
                    section TEXT,
                    total_students INTEGER DEFAULT 0,
                    academic_year TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    subject_name TEXT NOT NULL,
                    subject_code TEXT NOT NULL,
                    teacher_id TEXT,
                    class_id TEXT,
                    credits INTEGER DEFAULT 0,
                    status TEXT NOT NULL DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    school_id INTEGER NOT NULL,
                    student_id TEXT NOT NULL,
                    attendance_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    marked_by TEXT,
                    remarks TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(school_id, student_id, attendance_date),
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_exams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    exam_name TEXT NOT NULL,
                    exam_type TEXT NOT NULL,
                    class_id TEXT NOT NULL,
                    subject_id TEXT,
                    total_marks REAL NOT NULL,
                    exam_date TEXT,
                    duration_minutes INTEGER,
                    passing_marks REAL,
                    status TEXT NOT NULL DEFAULT 'Scheduled',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_exam_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    school_id INTEGER NOT NULL,
                    exam_id TEXT NOT NULL,
                    student_id TEXT NOT NULL,
                    obtained_marks REAL NOT NULL,
                    percentage REAL NOT NULL,
                    grade TEXT,
                    status TEXT NOT NULL DEFAULT 'Pending',
                    remarks TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assignment_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    class_id TEXT NOT NULL,
                    subject_id TEXT,
                    teacher_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    total_marks REAL,
                    deadline TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_assignment_submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    school_id INTEGER NOT NULL,
                    assignment_id TEXT NOT NULL,
                    student_id TEXT NOT NULL,
                    submission_date TEXT NOT NULL,
                    marks_obtained REAL,
                    ai_feedback TEXT,
                    plagiarism_score REAL DEFAULT 0,
                    status TEXT NOT NULL DEFAULT 'Submitted',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_fees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fee_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    student_id TEXT NOT NULL,
                    fee_name TEXT NOT NULL,
                    amount REAL NOT NULL,
                    due_date TEXT,
                    fine_amount REAL DEFAULT 0,
                    paid_amount REAL DEFAULT 0,
                    payment_status TEXT NOT NULL DEFAULT 'Pending',
                    payment_date TEXT,
                    receipt_number TEXT,
                    remarks TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payment_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    student_id TEXT NOT NULL,
                    fee_id TEXT,
                    amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    transaction_id TEXT,
                    verification_status TEXT NOT NULL DEFAULT 'Pending',
                    verified_by TEXT,
                    verified_date TEXT,
                    payment_date TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_ai_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ai_log_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    process_type TEXT NOT NULL,
                    input_data TEXT,
                    output_data TEXT,
                    confidence_score REAL,
                    processing_time_ms REAL,
                    status TEXT NOT NULL DEFAULT 'Success',
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_libraries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    author TEXT,
                    isbn TEXT,
                    category TEXT,
                    quantity INTEGER DEFAULT 1,
                    available_quantity INTEGER DEFAULT 1,
                    status TEXT NOT NULL DEFAULT 'Available',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_book_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    book_id TEXT NOT NULL,
                    student_id TEXT NOT NULL,
                    borrow_date TEXT NOT NULL,
                    return_date TEXT,
                    due_date TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Borrowed',
                    fine_amount REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_transports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transport_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    bus_number TEXT NOT NULL,
                    driver_name TEXT,
                    driver_phone TEXT,
                    route_name TEXT,
                    capacity INTEGER,
                    total_students INTEGER DEFAULT 0,
                    status TEXT NOT NULL DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_hostels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hostel_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    hostel_name TEXT NOT NULL,
                    hostel_type TEXT NOT NULL,
                    room_count INTEGER,
                    total_capacity INTEGER,
                    warden_name TEXT,
                    status TEXT NOT NULL DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_timetable (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timetable_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    class_id TEXT NOT NULL,
                    day_of_week TEXT NOT NULL,
                    period_number INTEGER NOT NULL,
                    subject_id TEXT,
                    teacher_id TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    room_number TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS portal_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analytics_id TEXT NOT NULL UNIQUE,
                    school_id INTEGER NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metric_date TEXT NOT NULL,
                    details_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(school_id) REFERENCES schools(id)
                )
                """
            )
            
            conn.commit()

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def register_user(self, role: str, username: str, password: str) -> bool:
        password_hash = self._hash_password(password)
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO users (role, username, password_hash) VALUES (?, ?, ?)",
                    (role, username, password_hash),
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, role: str, username: str, password: str) -> bool:
        password_hash = self._hash_password(password)
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id FROM users WHERE role = ? AND username = ? AND password_hash = ?",
                (role, username, password_hash),
            ).fetchone()
        return row is not None

    def create_grading_session(
        self,
        teacher_username: str,
        total_marks: int,
        custom_criteria: Dict[str, int],
        additional_instructions: str,
        detect_multiple_questions: bool,
    ) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO grading_sessions (
                    teacher_username,
                    total_marks,
                    custom_criteria_json,
                    additional_instructions,
                    detect_multiple_questions
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    teacher_username,
                    total_marks,
                    json.dumps(custom_criteria),
                    additional_instructions,
                    int(detect_multiple_questions),
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def save_grading_results(self, session_id: int, results: List[Dict[str, Any]]):
        with self._connect() as conn:
            conn.executemany(
                """
                INSERT INTO grading_results (
                    session_id,
                    filename,
                    file_type,
                    total_marks,
                    awarded_marks,
                    percentage,
                    feedback,
                    criteria_breakdown_json,
                    criteria_explanations_json,
                    questions_json,
                    strengths_json,
                    areas_for_improvement_json,
                    grade_justification,
                    text_content
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        session_id,
                        result["filename"],
                        result["file_type"],
                        result["total_marks"],
                        result["awarded_marks"],
                        result["percentage"],
                        result.get("feedback", ""),
                        json.dumps(result.get("criteria_breakdown", {})),
                        json.dumps(result.get("criteria_explanations", {})),
                        json.dumps(result.get("questions", [])),
                        json.dumps(result.get("strengths", [])),
                        json.dumps(result.get("areas_for_improvement", [])),
                        result.get("grade_justification", ""),
                        result.get("text_content", ""),
                    )
                    for result in results
                ],
            )
            conn.commit()

    def get_user_grading_history(self, teacher_username: str, limit: int = 10) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            sessions = conn.execute(
                """
                SELECT
                    gs.id,
                    gs.teacher_username,
                    gs.total_marks,
                    gs.custom_criteria_json,
                    gs.additional_instructions,
                    gs.detect_multiple_questions,
                    gs.created_at,
                    COUNT(gr.id) AS file_count,
                    AVG(gr.percentage) AS average_percentage
                FROM grading_sessions gs
                LEFT JOIN grading_results gr ON gr.session_id = gs.id
                WHERE gs.teacher_username = ?
                GROUP BY gs.id
                ORDER BY gs.created_at DESC
                LIMIT ?
                """,
                (teacher_username, limit),
            ).fetchall()

        return [
            {
                "id": row["id"],
                "teacher_username": row["teacher_username"],
                "total_marks": row["total_marks"],
                "custom_criteria": json.loads(row["custom_criteria_json"] or "{}"),
                "additional_instructions": row["additional_instructions"] or "",
                "detect_multiple_questions": bool(row["detect_multiple_questions"]),
                "created_at": row["created_at"],
                "file_count": row["file_count"] or 0,
                "average_percentage": row["average_percentage"] or 0,
            }
            for row in sessions
        ]

    def get_session_results(self, session_id: int) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM grading_results
                WHERE session_id = ?
                ORDER BY id ASC
                """,
                (session_id,),
            ).fetchall()

        return [self._deserialize_result_row(row) for row in rows]

    def get_user_role(self, username: str) -> Optional[str]:
        with self._connect() as conn:
            row = conn.execute("SELECT role FROM users WHERE username = ?", (username,)).fetchone()
        return row["role"] if row else None

    def get_user_profile(self, username: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT username, role, created_at FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        if not row:
            return None
        return {
            "username": row["username"],
            "role": row["role"],
            "created_at": row["created_at"],
        }

    def get_user_id(self, username: str) -> Optional[int]:
        """Return numeric user id for SaaS billing and access control."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        return int(row["id"]) if row else None

    def save_student_submission(
        self,
        student_username: str,
        title: str,
        subject: str,
        submission_type: str,
        deadline: str,
        filename: str,
        file_type: str,
        extracted_text: str,
        estimated_score: float,
        ai_feedback: Dict[str, Any],
        plagiarism_percentage: float,
        matched_source: str,
        resubmission_allowed: bool,
    ) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO student_submissions (
                    student_username,
                    title,
                    subject,
                    submission_type,
                    deadline,
                    filename,
                    file_type,
                    extracted_text,
                    estimated_score,
                    ai_feedback_json,
                    plagiarism_percentage,
                    matched_source,
                    resubmission_allowed
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student_username,
                    title,
                    subject,
                    submission_type,
                    deadline,
                    filename,
                    file_type,
                    extracted_text,
                    estimated_score,
                    json.dumps(ai_feedback),
                    plagiarism_percentage,
                    matched_source,
                    int(resubmission_allowed),
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def get_student_submissions(self, student_username: str, limit: int = 50) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM student_submissions
                WHERE student_username = ?
                ORDER BY created_at DESC, id DESC
                LIMIT ?
                """,
                (student_username, limit),
            ).fetchall()
        return [self._deserialize_student_submission(row) for row in rows]

    def get_submission_corpus(self, exclude_username: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            if exclude_username:
                rows = conn.execute(
                    """
                    SELECT id, student_username, title, extracted_text
                    FROM student_submissions
                    WHERE student_username != ? AND extracted_text IS NOT NULL AND TRIM(extracted_text) != ''
                    """,
                    (exclude_username,),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT id, student_username, title, extracted_text
                    FROM student_submissions
                    WHERE extracted_text IS NOT NULL AND TRIM(extracted_text) != ''
                    """
                ).fetchall()
        return [
            {
                "id": row["id"],
                "student_username": row["student_username"],
                "title": row["title"],
                "extracted_text": row["extracted_text"] or "",
            }
            for row in rows
        ]

    def create_notification(self, username: str, title: str, message: str, category: str):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO notifications (username, title, message, category)
                VALUES (?, ?, ?, ?)
                """,
                (username, title, message, category),
            )
            conn.commit()

    def get_notifications(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM notifications
                WHERE username = ?
                ORDER BY created_at DESC, id DESC
                LIMIT ?
                """,
                (username, limit),
            ).fetchall()
        return [
            {
                "title": row["title"],
                "message": row["message"],
                "category": row["category"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def create_assessment(
        self,
        teacher_username: str,
        title: str,
        subject: str,
        assessment_type: str,
        submission_deadline: str,
        duration_minutes: int,
        total_marks: float,
        questions: List[Dict[str, Any]],
    ) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO assessments (
                    teacher_username,
                    title,
                    subject,
                    assessment_type,
                    submission_deadline,
                    duration_minutes,
                    total_marks,
                    questions_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    teacher_username,
                    title,
                    subject,
                    assessment_type,
                    submission_deadline,
                    duration_minutes,
                    total_marks,
                    json.dumps(questions),
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def get_teacher_assessments(self, teacher_username: str, limit: int = 100) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM assessments
                WHERE teacher_username = ?
                ORDER BY created_at DESC, id DESC
                LIMIT ?
                """,
                (teacher_username, limit),
            ).fetchall()
        return [self._deserialize_assessment(row) for row in rows]

    def get_active_assessments(self, limit: int = 100) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM assessments
                WHERE is_active = 1
                ORDER BY created_at DESC, id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [self._deserialize_assessment(row) for row in rows]

    def get_assessment_by_id(self, assessment_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM assessments WHERE id = ?",
                (assessment_id,),
            ).fetchone()
        return self._deserialize_assessment(row) if row else None

    def get_attempt_by_student_and_assessment(self, student_username: str, assessment_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM assessment_attempts
                WHERE student_username = ? AND assessment_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (student_username, assessment_id),
            ).fetchone()
        return self._deserialize_attempt(row) if row else None

    def create_assessment_attempt(
        self,
        assessment_id: int,
        student_username: str,
        started_at: str,
        expires_at: str,
        total_marks: float,
    ) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO assessment_attempts (
                    assessment_id,
                    student_username,
                    started_at,
                    expires_at,
                    total_marks,
                    answers_json
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (assessment_id, student_username, started_at, expires_at, total_marks, json.dumps({})),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def submit_assessment_attempt(
        self,
        attempt_id: int,
        submitted_at: str,
        status: str,
        answers: Dict[str, Any],
        auto_score: float,
        total_marks: float,
    ):
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE assessment_attempts
                SET submitted_at = ?, status = ?, answers_json = ?, auto_score = ?, total_marks = ?
                WHERE id = ?
                """,
                (submitted_at, status, json.dumps(answers), auto_score, total_marks, attempt_id),
            )
            conn.commit()

    def save_teacher_quiz_grade(self, attempt_id: int, teacher_grade: float, ai_feedback: str):
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE assessment_attempts
                SET teacher_grade = ?, ai_feedback = ?, status = 'graded'
                WHERE id = ?
                """,
                (teacher_grade, ai_feedback, attempt_id),
            )
            conn.commit()

    def get_attempts_for_teacher(self, teacher_username: str, limit: int = 200) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT
                    aa.*,
                    a.title AS assessment_title,
                    a.subject AS assessment_subject,
                    a.assessment_type,
                    a.questions_json
                FROM assessment_attempts aa
                JOIN assessments a ON a.id = aa.assessment_id
                WHERE a.teacher_username = ?
                ORDER BY aa.id DESC
                LIMIT ?
                """,
                (teacher_username, limit),
            ).fetchall()
        return [self._deserialize_attempt(row) for row in rows]

    def create_school(self, school_name: str, school_code: str, admin_username: str) -> bool:
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO schools (school_name, school_code, admin_username)
                    VALUES (?, ?, ?)
                    """,
                    (school_name, school_code, admin_username),
                )
                school_id = int(cursor.lastrowid)
                conn.execute(
                    """
                    INSERT INTO school_memberships (school_id, username, school_role, approved)
                    VALUES (?, ?, ?, 1)
                    """,
                    (school_id, admin_username, "admin"),
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_school_by_code(self, school_code: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM schools WHERE school_code = ?",
                (school_code,),
            ).fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "school_name": row["school_name"],
            "school_code": row["school_code"],
            "admin_username": row["admin_username"],
            "created_at": row["created_at"],
        }

    def add_school_membership(self, school_code: str, username: str, school_role: str, approved: bool = False) -> bool:
        school = self.get_school_by_code(school_code)
        if not school:
            return False
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO school_memberships (school_id, username, school_role, approved)
                    VALUES (?, ?, ?, ?)
                    """,
                    (school["id"], username, school_role, int(approved)),
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_school_membership(self, school_code: str, username: str) -> Optional[Dict[str, Any]]:
        school = self.get_school_by_code(school_code)
        if not school:
            return None
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT sm.*, s.school_name, s.school_code
                FROM school_memberships sm
                JOIN schools s ON s.id = sm.school_id
                WHERE sm.school_id = ? AND sm.username = ?
                """,
                (school["id"], username),
            ).fetchone()
        if not row:
            return None
        return {
            "school_id": row["school_id"],
            "school_name": row["school_name"],
            "school_code": row["school_code"],
            "username": row["username"],
            "school_role": row["school_role"],
            "approved": bool(row["approved"]),
            "created_at": row["created_at"],
        }

    def approve_school_member(self, school_id: int, username: str):
        with self._connect() as conn:
            conn.execute(
                "UPDATE school_memberships SET approved = 1 WHERE school_id = ? AND username = ?",
                (school_id, username),
            )
            conn.commit()

    def get_school_members(self, school_id: int) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT username, school_role, approved, created_at
                FROM school_memberships
                WHERE school_id = ?
                ORDER BY created_at DESC
                """,
                (school_id,),
            ).fetchall()
        return [
            {
                "username": row["username"],
                "school_role": row["school_role"],
                "approved": bool(row["approved"]),
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def _deserialize_result_row(self, row: sqlite3.Row) -> Dict[str, Any]:
        return {
            "filename": row["filename"],
            "file_type": row["file_type"],
            "total_marks": row["total_marks"],
            "awarded_marks": row["awarded_marks"],
            "percentage": row["percentage"],
            "feedback": row["feedback"] or "",
            "criteria_breakdown": json.loads(row["criteria_breakdown_json"] or "{}"),
            "criteria_explanations": json.loads(row["criteria_explanations_json"] or "{}"),
            "questions": json.loads(row["questions_json"] or "[]"),
            "strengths": json.loads(row["strengths_json"] or "[]"),
            "areas_for_improvement": json.loads(row["areas_for_improvement_json"] or "[]"),
            "grade_justification": row["grade_justification"] or "",
            "text_content": row["text_content"] or "",
        }

    def _deserialize_student_submission(self, row: sqlite3.Row) -> Dict[str, Any]:
        return {
            "id": row["id"],
            "student_username": row["student_username"],
            "title": row["title"],
            "subject": row["subject"],
            "submission_type": row["submission_type"],
            "deadline": row["deadline"] or "",
            "filename": row["filename"],
            "file_type": row["file_type"],
            "extracted_text": row["extracted_text"] or "",
            "estimated_score": row["estimated_score"],
            "ai_feedback": json.loads(row["ai_feedback_json"] or "{}"),
            "plagiarism_percentage": row["plagiarism_percentage"],
            "matched_source": row["matched_source"] or "",
            "resubmission_allowed": bool(row["resubmission_allowed"]),
            "created_at": row["created_at"],
        }

    def _deserialize_assessment(self, row: sqlite3.Row) -> Dict[str, Any]:
        return {
            "id": row["id"],
            "teacher_username": row["teacher_username"],
            "title": row["title"],
            "subject": row["subject"],
            "assessment_type": row["assessment_type"],
            "submission_deadline": row["submission_deadline"],
            "duration_minutes": row["duration_minutes"],
            "total_marks": row["total_marks"],
            "questions": json.loads(row["questions_json"] or "[]"),
            "is_active": bool(row["is_active"]),
            "created_at": row["created_at"],
        }

    def _deserialize_attempt(self, row: sqlite3.Row) -> Dict[str, Any]:
        payload = {
            "id": row["id"],
            "assessment_id": row["assessment_id"],
            "student_username": row["student_username"],
            "started_at": row["started_at"],
            "submitted_at": row["submitted_at"] or "",
            "expires_at": row["expires_at"],
            "status": row["status"],
            "answers": json.loads(row["answers_json"] or "{}"),
            "auto_score": row["auto_score"],
            "total_marks": row["total_marks"],
            "teacher_grade": row["teacher_grade"],
            "ai_feedback": row["ai_feedback"] or "",
        }
        if "assessment_title" in row.keys():
            payload["assessment_title"] = row["assessment_title"]
        if "assessment_subject" in row.keys():
            payload["assessment_subject"] = row["assessment_subject"]
        if "assessment_type" in row.keys():
            payload["assessment_type"] = row["assessment_type"]
        if "questions_json" in row.keys():
            payload["questions"] = json.loads(row["questions_json"] or "[]")
        return payload
