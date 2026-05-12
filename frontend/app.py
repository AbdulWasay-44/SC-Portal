import time
from datetime import date, datetime, timedelta
from difflib import SequenceMatcher
from typing import Any, Dict, List

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Import from backend modules
import sys
from pathlib import Path

# Add backend and parent directory to path for imports
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analytics_service import AnalyticsService
from database import Database
from excel_export import ExcelExporter
from file_processor import FileProcessor
from grading_service import GradingService
from helpers import format_grade_display, validate_file_type, generate_profile_id
from ocr_service import OCRService
from master_admin_panel import render_master_admin_panel
from school_portal import render_school_portal
from school_saas_hub_ui import render_school_saas_hub
from saas_access_control import AccessControl


st.set_page_config(
    page_title="SC Portals",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def initialize_services():
    """Initialize reusable service objects."""
    return {
        "file_processor": FileProcessor(),
        "ocr_service": OCRService(),
        "grading_service": GradingService(),
        "excel_exporter": ExcelExporter(),
        "analytics_service": AnalyticsService(),
        "database": Database(),
    }


def initialize_session_state():
    """Create default session state values for navigation and auth."""
    defaults = {
        "current_page": "welcome",
        "is_logged_in": False,
        "user_role": None,
        "current_username": None,
        "user_id": None,
        "teacher_service_view": "grading",
        "school_code": None,
        "school_role": None,
        "school_admin_view": "Dashboard",
        "saas_selected_plan": None,
        "saas_pending_payment_id": None,
        "saas_hub_tab": None,
        "master_admin_username": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def navigate(page: str):
    """Switch visible page."""
    st.session_state.current_page = page


def handle_login(role: str, username: str, password: str, database: Database):
    """Log a user in if credentials match the database."""
    if not username or not password:
        st.warning(f"Enter both {role} username and password.")
        return
    if not database.authenticate_user(role, username, password):
        st.error(f"Invalid {role} credentials.")
        return

    st.session_state.is_logged_in = True
    st.session_state.user_role = role
    st.session_state.current_username = username
    st.session_state.user_id = database.get_user_id(username)
    navigate("teacher_service" if role == "teacher" else "student_service")
    st.success(f"{role.title()} logged in successfully.")


def handle_register(role: str, username: str, password: str, database: Database):
    """Register a user in the database."""
    if not username or not password:
        st.warning(f"Enter both {role} username and password to register.")
        return
    if not database.register_user(role, username, password):
        st.warning(f"{role.title()} username already exists.")
        return

    st.success(f"{role.title()} account created. You can log in now.")


def handle_school_admin_login(database: Database, school_code: str, username: str, password: str):
    """Authenticate a school admin directly from the school portal."""
    if not school_code or not username or not password:
        st.warning("Enter school code, admin username, and password.")
        return

    school = database.get_school_by_code(school_code)
    if not school:
        st.error("School code not found.")
        return

    membership = database.get_school_membership(school_code, username)
    if not membership or membership["school_role"] != "admin" or not membership["approved"]:
        st.error("This account does not have approved admin access for that school.")
        return

    if not database.authenticate_user("teacher", username, password):
        st.error("Invalid admin credentials.")
        return

    st.session_state.is_logged_in = True
    st.session_state.user_role = "teacher"
    st.session_state.current_username = username
    st.session_state.user_id = database.get_user_id(username)
    st.session_state.school_code = school_code
    st.session_state.school_role = "admin"
    navigate("school")
    st.success("School admin logged in successfully.")


def logout():
    """Reset auth state and return to welcome page."""
    st.session_state.is_logged_in = False
    st.session_state.user_role = None
    st.session_state.current_username = None
    st.session_state.user_id = None
    navigate("welcome")
    st.success("Logged out successfully.")


def render_sidebar():
    """Render a profile ID-based sidebar instead of traditional menu."""
    with st.sidebar:
        # ============ PROFILE CARD SECTION ============
        st.markdown("---")
        
        if st.session_state.is_logged_in:
            username = st.session_state.current_username
            profile_id = generate_profile_id(username)
            user_role = st.session_state.user_role.title() if st.session_state.user_role else "User"
            
            # Profile card with ID display
            st.markdown(
                f"""
                <div style="text-align: center; padding: 15px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 15px;">
                    <div style="font-size: 24px; font-weight: bold; color: #1f77b4;">👤 {profile_id}</div>
                    <div style="font-size: 12px; color: #666; margin-top: 8px;">Profile ID</div>
                    <div style="font-size: 13px; color: #333; margin-top: 5px; font-weight: 500;">{username}</div>
                    <div style="font-size: 11px; color: #888; margin-top: 3px;">{user_role}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Guest profile card
            st.markdown(
                """
                <div style="text-align: center; padding: 15px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 15px;">
                    <div style="font-size: 24px; font-weight: bold; color: #999;">👤 GUEST</div>
                    <div style="font-size: 12px; color: #666; margin-top: 8px;">Not Logged In</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        # ============ AUTHENTICATION SECTION ============
        st.markdown("### Authentication")
        login_label = "🚪 Logout" if st.session_state.is_logged_in else "🔐 Login"
        if st.button(login_label, use_container_width=True):
            if st.session_state.is_logged_in:
                logout()
            else:
                navigate("login")
        
        st.markdown("---")
        
        # ============ NAVIGATION SECTION ============
        st.markdown("### Navigation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👨‍🏫 Teacher", use_container_width=True, key="nav_teacher"):
                navigate("teacher_service")
            if st.button("🏫 School", use_container_width=True, key="nav_school"):
                navigate("school")
            if st.button("📚 History", use_container_width=True, key="nav_history"):
                navigate("history")
        
        with col2:
            if st.button("👨‍🎓 Student", use_container_width=True, key="nav_student"):
                navigate("student_service")
            if st.button("🏠 Welcome", use_container_width=True, key="nav_welcome"):
                navigate("welcome")
            if st.button("⚙️ Settings", use_container_width=True, key="nav_settings"):
                navigate("settings") if hasattr(st.session_state, 'settings') else st.info("Settings page coming soon")
        
        st.markdown("---")
        
        # ============ PORTAL ACCESS SECTION ============
        st.markdown("### Premium Access")
        
        if st.button("🎛️ Master Admin", use_container_width=True):
            navigate("master_admin")
        
        uid = st.session_state.get("user_id")
        if AccessControl.can_open_school_portal(uid):
            if st.button("🏫 School Portal", use_container_width=True):
                navigate("school_portal")
        else:
            st.info("🔒 School Portal unlocks after subscription + registration.", icon="ℹ️")
        
        st.markdown("---")
        
        # ============ STATUS SECTION ============
        st.markdown("### Status")
        if st.session_state.is_logged_in:
            st.success(f"✓ Logged in as **{st.session_state.current_username}**", icon="✅")
            st.caption(f"Role: {st.session_state.user_role.title()}")
        else:
            st.warning("Not logged in", icon="⚠️")
            st.caption("Login to access all features")


def render_welcome_page():
    """Landing page with project summary and usage guide."""
    st.title("SC Portals")
    st.subheader("Welcome")
    st.markdown(
        """
This website is designed to help teachers review assignments faster and more consistently.
It accepts PDF, DOCX, and image submissions, extracts readable text, grades the work with AI,
and then presents feedback, score summaries, analytics, and downloadable reports.

How to use the website:
- Teachers can open `Teacher Service` to upload assignment files and run grading.
- Students can open `Student Service` to access the student area.
- The `Login` page provides separate teacher and student login and registration cards.
- The left menu stays available for quick navigation between the welcome page, login, and services.
"""
    )

    st.info(
        "Use the menu in the upper-left sidebar to open Login, Teacher Service, or Student Service."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Teacher Workflow")
        st.write("Upload submissions, configure marks, grade automatically, review analytics, and export results.")
    with col2:
        st.markdown("### Student Workflow")
        st.write("Sign in from the login page, then open the student service area for student-facing access.")
    st.markdown("### School Organization Portal")
    st.write("Open `School` from the menu to access a school-managed site for approved teachers and students.")


def render_login_page(database: Database):
    """Render teacher/student login and registration cards."""
    st.title("Login Page")
    st.markdown("Use the cards below to register or log in as a teacher or a student.")

    teacher_col, student_col = st.columns(2)

    with teacher_col:
        st.markdown("### Teacher Login and Register")
        with st.container(border=True):
            teacher_login_username = st.text_input("Teacher Username", key="teacher_login_username")
            teacher_login_password = st.text_input(
                "Teacher Password", type="password", key="teacher_login_password"
            )
            login_col, register_col = st.columns(2)
            with login_col:
                if st.button("Teacher Login", use_container_width=True):
                    handle_login("teacher", teacher_login_username, teacher_login_password, database)
            with register_col:
                if st.button("Teacher Register", use_container_width=True):
                    handle_register("teacher", teacher_login_username, teacher_login_password, database)

    with student_col:
        st.markdown("### Student Login and Register")
        with st.container(border=True):
            student_login_username = st.text_input("Student Username", key="student_login_username")
            student_login_password = st.text_input(
                "Student Password", type="password", key="student_login_password"
            )
            login_col, register_col = st.columns(2)
            with login_col:
                if st.button("Student Login", use_container_width=True):
                    handle_login("student", student_login_username, student_login_password, database)
            with register_col:
                if st.button("Student Register", use_container_width=True):
                    handle_register("student", student_login_username, student_login_password, database)


def render_student_service_page():
    """Legacy placeholder removed; student service is rendered by the full portal."""
    st.write("")


def get_student_deadlines() -> List[Dict[str, str]]:
    """Static upcoming deadlines for the student portal."""
    today = date.today()
    return [
        {"title": "Machine Learning Quiz 1", "subject": "Machine Learning", "deadline": str(today + timedelta(days=2))},
        {"title": "Business Intelligence Assignment", "subject": "Business Intelligence", "deadline": str(today + timedelta(days=4))},
        {"title": "Database Project Draft", "subject": "Database Systems", "deadline": str(today + timedelta(days=7))},
    ]


def extract_text_for_uploaded_file(uploaded_file, services: Dict[str, Any]) -> str:
    """Extract text from any supported student upload."""
    file_type = validate_file_type(uploaded_file.name)
    if file_type in ["jpg", "jpeg", "png"]:
        return services["ocr_service"].extract_text_from_image(uploaded_file) or ""
    if file_type in ["pdf", "docx"]:
        return services["file_processor"].extract_text(uploaded_file, file_type) or ""
    return ""


def compute_plagiarism_details(database: Database, student_username: str, extracted_text: str) -> Dict[str, Any]:
    """Compare submission text against existing submissions using simple text similarity."""
    if not extracted_text.strip():
        return {"percentage": 0.0, "matched_source": "", "matched_excerpt": ""}

    best_ratio = 0.0
    matched_source = ""
    matched_excerpt = ""
    for record in database.get_submission_corpus(exclude_username=student_username):
        candidate_text = (record.get("extracted_text") or "").strip()
        if not candidate_text:
            continue
        ratio = SequenceMatcher(None, extracted_text[:4000], candidate_text[:4000]).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            matched_source = f"{record['title']} ({record['student_username']})"
            matched_excerpt = candidate_text[:220]

    return {
        "percentage": round(best_ratio * 100, 1),
        "matched_source": matched_source,
        "matched_excerpt": matched_excerpt,
    }


def build_study_recommendations(submissions: List[Dict[str, Any]]) -> List[str]:
    """Generate personalized recommendations from stored submission performance."""
    if not submissions:
        return [
            "Start by submitting your first assignment to unlock personalized study recommendations.",
            "Use the quiz portal to build a baseline of your current understanding.",
        ]

    subject_scores: Dict[str, List[float]] = {}
    weak_areas: List[str] = []
    for submission in submissions:
        subject_scores.setdefault(submission["subject"], []).append(submission["estimated_score"])
        weak_areas.extend(submission.get("ai_feedback", {}).get("weak_areas", []))

    recommendations = []
    sorted_subjects = sorted(
        ((subject, sum(scores) / len(scores)) for subject, scores in subject_scores.items()),
        key=lambda item: item[1],
    )
    if sorted_subjects:
        lowest_subject, lowest_score = sorted_subjects[0]
        recommendations.append(
            f"Focus revision on {lowest_subject}; your current estimated average there is {lowest_score:.1f}%."
        )
    if weak_areas:
        recommendations.append(f"Prioritize improvement in: {', '.join(sorted(set(weak_areas))[:3])}.")
    recommendations.append("Review feedback after every submission and turn the weakest point into a short practice task.")
    recommendations.append("Use the quiz portal weekly to track whether your revision is improving results.")
    return recommendations[:4]


def get_quiz_bank(subject: str) -> List[Dict[str, Any]]:
    """Return simple subject-wise quiz questions."""
    bank = {
        "Machine Learning": [
            {
                "question": "Which learning type uses labeled data?",
                "options": ["Unsupervised learning", "Supervised learning", "Reinforcement learning"],
                "answer": "Supervised learning",
            },
            {
                "question": "What is overfitting?",
                "options": ["Model ignores training data", "Model memorizes training data too closely", "Model has too few features"],
                "answer": "Model memorizes training data too closely",
            },
            {
                "question": "Which metric is common for classification?",
                "options": ["Accuracy", "Mean squared error only", "Throughput"],
                "answer": "Accuracy",
            },
        ],
        "Business Intelligence": [
            {
                "question": "What is the main goal of business intelligence?",
                "options": ["Decorating reports", "Supporting better decisions", "Replacing databases"],
                "answer": "Supporting better decisions",
            },
            {
                "question": "ETL stands for:",
                "options": ["Extract, Transform, Load", "Enter, Transfer, Link", "Execute, Track, Log"],
                "answer": "Extract, Transform, Load",
            },
            {
                "question": "A dashboard is mainly used for:",
                "options": ["Cooking recipes", "Visual performance monitoring", "File compression"],
                "answer": "Visual performance monitoring",
            },
        ],
        "Database Systems": [
            {
                "question": "A primary key is used to:",
                "options": ["Identify each row uniquely", "Store images only", "Delete all duplicates automatically"],
                "answer": "Identify each row uniquely",
            },
            {
                "question": "SQL is mainly used to:",
                "options": ["Paint graphics", "Query and manage data", "Compile Java"],
                "answer": "Query and manage data",
            },
            {
                "question": "Normalization helps reduce:",
                "options": ["Redundancy", "Internet speed", "Screen brightness"],
                "answer": "Redundancy",
            },
        ],
    }
    return bank.get(subject, bank["Business Intelligence"])


def current_timestamp() -> datetime:
    """Return the current local timestamp."""
    return datetime.now()


def format_datetime_local(value: datetime) -> str:
    """Format datetime values for storage and display."""
    return value.strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime_local(value: str) -> datetime:
    """Parse stored datetime strings."""
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def calculate_assessment_total_marks(questions: List[Dict[str, Any]]) -> float:
    """Sum question marks for an assessment."""
    return float(sum(float(question.get("marks", 0)) for question in questions))


def build_attempt_answer_text(assessment: Dict[str, Any], answers: Dict[str, Any]) -> str:
    """Create a text block for AI grading of quiz/test attempts."""
    parts = [f"Assessment: {assessment['title']}", f"Subject: {assessment['subject']}"]
    for index, question in enumerate(assessment.get("questions", []), start=1):
        question_key = str(index)
        student_answer = answers.get(question_key, "")
        expected_answer = question.get("correct_answer", "")
        parts.append(f"Question {index}: {question.get('question', '')}")
        parts.append(f"Expected Answer: {expected_answer}")
        parts.append(f"Student Answer: {student_answer}")
    return "\n".join(parts)


def render_assessment_creator(database: Database, teacher_username: str):
    """Render the dedicated quiz and test maker page for teachers."""
    st.header("Quiz and Test Maker")
    with st.form("assessment_creator_form"):
        maker_col1, maker_col2 = st.columns(2)
        with maker_col1:
            assessment_title = st.text_input("Assessment Title")
            assessment_subject = st.selectbox(
                "Assessment Subject",
                ["Machine Learning", "Business Intelligence", "Database Systems", "Software Engineering"],
                key="assessment_subject",
            )
            assessment_type = st.selectbox("Assessment Type", ["Quiz", "Test", "Paper"], key="assessment_type")
            question_count = st.number_input("Number of Questions", min_value=1, max_value=10, value=3)
        with maker_col2:
            submission_deadline = st.text_input(
                "Submission Deadline",
                value=(current_timestamp() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                help="Use format YYYY-MM-DD HH:MM:SS",
            )
            duration_minutes = st.number_input("Time Duration (minutes)", min_value=1, max_value=300, value=30)
            allow_publish = st.checkbox("Publish immediately", value=True)

        assessment_questions: List[Dict[str, Any]] = []
        for i in range(int(question_count)):
            st.markdown(f"**Question {i + 1}**")
            q_col1, q_col2, q_col3 = st.columns([4, 2, 1])
            with q_col1:
                question_text = st.text_input(f"Question Text {i + 1}", key=f"assessment_question_{i}")
            with q_col2:
                question_type = st.selectbox(
                    f"Type {i + 1}",
                    ["short_answer", "mcq"],
                    key=f"assessment_type_{i}",
                )
            with q_col3:
                marks = st.number_input(f"Marks {i + 1}", min_value=1, max_value=100, value=5, key=f"assessment_marks_{i}")

            options = []
            if question_type == "mcq":
                options = [
                    st.text_input(f"Option A {i + 1}", key=f"assessment_option_a_{i}"),
                    st.text_input(f"Option B {i + 1}", key=f"assessment_option_b_{i}"),
                    st.text_input(f"Option C {i + 1}", key=f"assessment_option_c_{i}"),
                    st.text_input(f"Option D {i + 1}", key=f"assessment_option_d_{i}"),
                ]
            correct_answer = st.text_input(f"Correct Answer / Marking Key {i + 1}", key=f"assessment_answer_{i}")
            assessment_questions.append(
                {
                    "question": question_text,
                    "question_type": question_type,
                    "marks": marks,
                    "options": [option for option in options if option],
                    "correct_answer": correct_answer,
                }
            )

        create_assessment = st.form_submit_button("Create Assessment", use_container_width=True)

    if create_assessment:
        if not (st.session_state.is_logged_in and st.session_state.user_role == "teacher"):
            st.error("Please log in as a teacher to create quizzes and tests.")
        elif not assessment_title:
            st.warning("Enter an assessment title.")
        else:
            try:
                parse_datetime_local(submission_deadline)
            except ValueError:
                st.error("Deadline must use the format YYYY-MM-DD HH:MM:SS.")
            else:
                cleaned_questions = [
                    question
                    for question in assessment_questions
                    if question.get("question") and question.get("correct_answer")
                ]
                if not cleaned_questions:
                    st.warning("Add at least one complete question with an answer key.")
                else:
                    assessment_id = database.create_assessment(
                        teacher_username=teacher_username,
                        title=assessment_title,
                        subject=assessment_subject,
                        assessment_type=assessment_type,
                        submission_deadline=submission_deadline,
                        duration_minutes=int(duration_minutes),
                        total_marks=calculate_assessment_total_marks(cleaned_questions),
                        questions=cleaned_questions,
                    )
                    if allow_publish:
                        database.create_notification(
                            teacher_username,
                            "Assessment created",
                            f"{assessment_title} is now available for students to attempt.",
                            "assessment",
                        )
                    st.success(f"Assessment created successfully with ID {assessment_id}.")


def score_assessment_attempt(assessment: Dict[str, Any], answers: Dict[str, Any]) -> float:
    """Compute an automatic score for teacher-made tests."""
    total = 0.0
    for index, question in enumerate(assessment.get("questions", []), start=1):
        marks = float(question.get("marks", 0))
        student_answer = str(answers.get(str(index), "")).strip()
        if question.get("question_type") == "mcq":
            if student_answer == str(question.get("correct_answer", "")).strip():
                total += marks
        else:
            correct_answer = str(question.get("correct_answer", "")).strip().lower()
            if correct_answer and correct_answer in student_answer.lower():
                total += marks
    return round(total, 2)


def inject_attempt_timeout_refresh(expires_at: datetime):
    """Refresh the app when the active quiz timer expires."""
    milliseconds = int(max((expires_at - current_timestamp()).total_seconds(), 0) * 1000)
    if milliseconds <= 0:
        return
    components.html(
        f"""
        <script>
        setTimeout(function() {{
            window.parent.location.reload();
        }}, {milliseconds});
        </script>
        """,
        height=0,
    )


def render_student_service_page(services: Dict[str, Any]):
    """Render the student portal with submissions, feedback, dashboard, and quizzes."""
    database: Database = services["database"]
    st.title("Student Service Portal")
    st.markdown("Welcome Student")

    if not (st.session_state.is_logged_in and st.session_state.user_role == "student"):
        st.warning("Log in as a student to store submissions, track performance, and receive alerts.")
        current_username = "guest_student"
    else:
        current_username = st.session_state.current_username
        st.success(f"Student session active: {current_username}")

    submissions = database.get_student_submissions(current_username, limit=100) if current_username else []
    notifications = database.get_notifications(current_username, limit=20) if current_username else []

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Submission Center",
            "AI Feedback & Suggestions",
            "Performance Dashboard",
            "Plagiarism & Recommendations",
            "Notifications & Alerts",
            "Quiz & Test Portal",
        ]
    )

    with tab1:
        st.subheader("Assignment Submission")
        deadline_df = pd.DataFrame(get_student_deadlines())
        st.write("Upcoming deadlines")
        st.dataframe(deadline_df, use_container_width=True)

        with st.form("student_submission_form"):
            col1, col2 = st.columns(2)
            with col1:
                submission_title = st.text_input("Title")
                submission_subject = st.selectbox(
                    "Subject",
                    ["Machine Learning", "Business Intelligence", "Database Systems", "Software Engineering"],
                )
                submission_type = st.selectbox("Submission Type", ["Assignment", "Quiz", "Project"])
            with col2:
                deadline_options = [item["deadline"] for item in get_student_deadlines()]
                selected_deadline = st.selectbox("Deadline", deadline_options)
                allow_resubmission = st.checkbox("Allow resubmission before deadline", value=True)
                uploaded_file = st.file_uploader(
                    "Upload file",
                    type=["pdf", "docx", "jpg", "jpeg", "png", "zip"],
                    help="Supported formats: PDF, DOCX, images, and ZIP archives.",
                )
            submit_student_work = st.form_submit_button("Submit Work", use_container_width=True)

        if submit_student_work:
            if not (st.session_state.is_logged_in and st.session_state.user_role == "student"):
                st.error("Please log in as a student before submitting work.")
            elif not submission_title or not uploaded_file:
                st.warning("Add a title and upload a file before submitting.")
            else:
                extracted_text = ""
                file_type = uploaded_file.name.split(".")[-1].lower()
                if file_type != "zip":
                    extracted_text = extract_text_for_uploaded_file(uploaded_file, services)

                if file_type == "zip":
                    ai_feedback = {
                        "estimated_score": 0,
                        "mistake_identification": ["ZIP submission stored successfully, but AI text analysis was skipped."],
                        "grammar_spelling_suggestions": [],
                        "conceptual_feedback": [],
                        "improvement_recommendations": ["Upload readable PDF, DOCX, or image files for AI feedback."],
                        "suggested_learning_resources": [],
                        "weak_areas": [],
                        "strong_areas": [],
                    }
                else:
                    ai_feedback = services["grading_service"].generate_student_feedback(
                        extracted_text or "Submission content was too limited for analysis.",
                        submission_subject,
                        submission_type,
                    )

                plagiarism_details = compute_plagiarism_details(database, current_username, extracted_text)
                database.save_student_submission(
                    student_username=current_username,
                    title=submission_title,
                    subject=submission_subject,
                    submission_type=submission_type,
                    deadline=selected_deadline,
                    filename=uploaded_file.name,
                    file_type=file_type,
                    extracted_text=extracted_text,
                    estimated_score=ai_feedback.get("estimated_score", 0),
                    ai_feedback=ai_feedback,
                    plagiarism_percentage=plagiarism_details["percentage"],
                    matched_source=plagiarism_details["matched_source"],
                    resubmission_allowed=allow_resubmission,
                )
                database.create_notification(
                    current_username,
                    "Submission received",
                    f"{submission_title} was submitted successfully.",
                    "submission",
                )
                database.create_notification(
                    current_username,
                    "AI feedback available",
                    f"Feedback for {submission_title} is ready to review.",
                    "feedback",
                )
                st.success("Submission saved successfully.")
                submissions = database.get_student_submissions(current_username, limit=100)

        if submissions:
            st.markdown("### Submission History")
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Title": item["title"],
                            "Subject": item["subject"],
                            "Type": item["submission_type"],
                            "Score": f"{item['estimated_score']:.1f}%",
                            "Deadline": item["deadline"],
                            "Submitted": item["created_at"],
                        }
                        for item in submissions
                    ]
                ),
                use_container_width=True,
            )

    with tab2:
        st.subheader("AI Feedback & Suggestions")
        if submissions:
            selected_submission_title = st.selectbox(
                "Choose a submission",
                options=[f"{item['title']} | {item['subject']} | {item['created_at']}" for item in submissions],
                key="student_feedback_selector",
            )
            selected_submission = submissions[
                [f"{item['title']} | {item['subject']} | {item['created_at']}" for item in submissions].index(
                    selected_submission_title
                )
            ]
            ai_feedback = selected_submission.get("ai_feedback", {})
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Estimated Score", f"{selected_submission['estimated_score']:.1f}%")
                st.write("**Mistake Identification**")
                for item in ai_feedback.get("mistake_identification", []):
                    st.write(f"- {item}")
                st.write("**Grammar/Spelling Suggestions**")
                for item in ai_feedback.get("grammar_spelling_suggestions", []):
                    st.write(f"- {item}")
                st.write("**Conceptual Feedback**")
                for item in ai_feedback.get("conceptual_feedback", []):
                    st.write(f"- {item}")
            with col2:
                st.write("**Improvement Recommendations**")
                for item in ai_feedback.get("improvement_recommendations", []):
                    st.write(f"- {item}")
                st.write("**Suggested Learning Resources**")
                for item in ai_feedback.get("suggested_learning_resources", []):
                    st.write(f"- {item}")
                st.info(
                    "Example insight: “Your answer lacks explanation of supervised learning concepts.”"
                )
        else:
            st.info("Submit work first to unlock AI feedback and suggestions.")

    with tab3:
        st.subheader("Performance Dashboard")
        if submissions:
            overall_average = sum(item["estimated_score"] for item in submissions) / len(submissions)
            subject_rows: Dict[str, List[float]] = {}
            strong_areas: List[str] = []
            weak_areas: List[str] = []
            for submission in submissions:
                subject_rows.setdefault(submission["subject"], []).append(submission["estimated_score"])
                strong_areas.extend(submission.get("ai_feedback", {}).get("strong_areas", []))
                weak_areas.extend(submission.get("ai_feedback", {}).get("weak_areas", []))

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Grades", f"{overall_average:.1f}%")
            with col2:
                best_subject = max(subject_rows.items(), key=lambda item: sum(item[1]) / len(item[1]))[0]
                st.metric("Strongest Subject", best_subject)
            with col3:
                weak_subject = min(subject_rows.items(), key=lambda item: sum(item[1]) / len(item[1]))[0]
                st.metric("Weakest Subject", weak_subject)

            subject_df = pd.DataFrame(
                [
                    {"Subject": subject, "Average Score": sum(scores) / len(scores)}
                    for subject, scores in subject_rows.items()
                ]
            )
            history_df = pd.DataFrame(
                [
                    {
                        "Submitted": item["created_at"],
                        "Title": item["title"],
                        "Subject": item["subject"],
                        "Score": item["estimated_score"],
                    }
                    for item in reversed(submissions)
                ]
            )

            st.write("**Subject-wise Performance**")
            st.bar_chart(subject_df.set_index("Subject"))
            st.write("**Progress Graph**")
            st.line_chart(history_df.set_index("Submitted")["Score"])
            st.write("**Assignment History**")
            st.dataframe(history_df, use_container_width=True)
            st.write("**Strong Areas**")
            st.write(", ".join(sorted(set(strong_areas))[:5]) if strong_areas else "No strong areas identified yet.")
            st.write("**Weak Areas**")
            st.write(", ".join(sorted(set(weak_areas))[:5]) if weak_areas else "No weak areas identified yet.")
        else:
            st.info("Your dashboard will appear after your first submission.")

    with tab4:
        st.subheader("Plagiarism Detection")
        if submissions:
            latest_submission = submissions[0]
            st.metric("Plagiarism Percentage", f"{latest_submission['plagiarism_percentage']:.1f}%")
            st.write(
                f"Matched Source: {latest_submission['matched_source'] or 'No strong duplication match found.'}"
            )
            if latest_submission["plagiarism_percentage"] >= 40:
                st.warning("Potential duplicated content detected. Review the submission carefully.")
            else:
                st.success("No major duplication signal detected.")

        st.subheader("AI Study Recommendations")
        for recommendation in build_study_recommendations(submissions):
            st.write(f"- {recommendation}")

    with tab5:
        st.subheader("Notifications & Alerts")
        for deadline in get_student_deadlines():
            st.info(f"Upcoming deadline: {deadline['title']} due on {deadline['deadline']}")
        if notifications:
            for notification in notifications:
                with st.expander(f"{notification['created_at']} | {notification['title']}"):
                    st.write(f"Category: {notification['category']}")
                    st.write(notification["message"])
        else:
            st.caption("No saved alerts yet.")

    with tab6:
        st.subheader("Quiz & Test Portal")
        if not (st.session_state.is_logged_in and st.session_state.user_role == "student"):
            st.warning("Please log in as a student to attempt teacher-created quizzes and tests.")
        else:
            active_assessments = database.get_active_assessments(limit=100)
            if active_assessments:
                for assessment in active_assessments:
                    deadline = parse_datetime_local(assessment["submission_deadline"])
                    attempt = database.get_attempt_by_student_and_assessment(current_username, assessment["id"])
                    with st.expander(
                        f"{assessment['title']} | {assessment['assessment_type']} | {assessment['subject']}"
                    ):
                        st.write(f"Teacher: {assessment['teacher_username']}")
                        st.write(f"Deadline: {assessment['submission_deadline']}")
                        st.write(f"Duration: {assessment['duration_minutes']} minutes")
                        st.write(f"Total Marks: {assessment['total_marks']}")

                        if current_timestamp() > deadline:
                            st.error("Submission deadline has passed. This assessment is closed.")
                            continue

                        if attempt and attempt["status"] in {"submitted", "graded"}:
                            final_grade = attempt["teacher_grade"] if attempt["teacher_grade"] is not None else attempt["auto_score"]
                            st.success(
                                f"You already attempted this assessment. Score: {final_grade}/{attempt['total_marks']}"
                            )
                            if attempt.get("ai_feedback"):
                                st.write(attempt["ai_feedback"])
                            continue

                        if attempt is None:
                            if st.button(f"Start {assessment['assessment_type']} {assessment['id']}", key=f"start_assessment_{assessment['id']}"):
                                started_at = current_timestamp()
                                expires_at = started_at + timedelta(minutes=int(assessment["duration_minutes"]))
                                database.create_assessment_attempt(
                                    assessment_id=assessment["id"],
                                    student_username=current_username,
                                    started_at=format_datetime_local(started_at),
                                    expires_at=format_datetime_local(expires_at),
                                    total_marks=assessment["total_marks"],
                                )
                                database.create_notification(
                                    current_username,
                                    "Assessment started",
                                    f"You started {assessment['title']}. Submit before the timer ends.",
                                    "assessment",
                                )
                                st.rerun()
                            continue

                        expires_at = parse_datetime_local(attempt["expires_at"])
                        remaining_seconds = int((expires_at - current_timestamp()).total_seconds())
                        inject_attempt_timeout_refresh(expires_at)

                        if remaining_seconds <= 0:
                            database.submit_assessment_attempt(
                                attempt_id=attempt["id"],
                                submitted_at=format_datetime_local(current_timestamp()),
                                status="timed_out",
                                answers=attempt.get("answers", {}),
                                auto_score=0,
                                total_marks=assessment["total_marks"],
                            )
                            database.create_notification(
                                current_username,
                                "Assessment closed",
                                f"The time for {assessment['title']} has expired.",
                                "assessment",
                            )
                            st.error("Time is over. This assessment is now closed and can no longer be attempted.")
                            st.rerun()

                        minutes_left = remaining_seconds // 60
                        seconds_left = remaining_seconds % 60
                        st.warning(f"Time Remaining: {minutes_left:02d}:{seconds_left:02d}")

                        with st.form(f"attempt_form_{assessment['id']}"):
                            answer_payload: Dict[str, Any] = {}
                            for idx, question in enumerate(assessment["questions"], start=1):
                                st.write(f"Q{idx}. {question['question']} ({question['marks']} marks)")
                                if question.get("question_type") == "mcq":
                                    answer_payload[str(idx)] = st.radio(
                                        f"Select answer for question {idx}",
                                        options=question.get("options", []),
                                        key=f"assessment_answer_{assessment['id']}_{idx}",
                                    )
                                else:
                                    answer_payload[str(idx)] = st.text_area(
                                        f"Write answer for question {idx}",
                                        key=f"assessment_answer_{assessment['id']}_{idx}",
                                    )
                            submit_attempt = st.form_submit_button("Submit Assessment", use_container_width=True)

                        if submit_attempt:
                            submission_time = current_timestamp()
                            if submission_time > expires_at:
                                database.submit_assessment_attempt(
                                    attempt_id=attempt["id"],
                                    submitted_at=format_datetime_local(submission_time),
                                    status="timed_out",
                                    answers=answer_payload,
                                    auto_score=0,
                                    total_marks=assessment["total_marks"],
                                )
                                st.error("Timer expired before submission could be accepted.")
                            else:
                                auto_score = score_assessment_attempt(assessment, answer_payload)
                                database.submit_assessment_attempt(
                                    attempt_id=attempt["id"],
                                    submitted_at=format_datetime_local(submission_time),
                                    status="submitted",
                                    answers=answer_payload,
                                    auto_score=auto_score,
                                    total_marks=assessment["total_marks"],
                                )
                                database.create_notification(
                                    current_username,
                                    "Assessment submitted",
                                    f"You submitted {assessment['title']} successfully.",
                                    "assessment",
                                )
                                database.create_notification(
                                    assessment["teacher_username"],
                                    "New assessment attempt",
                                    f"{current_username} submitted {assessment['title']} for grading.",
                                    "assessment",
                                )
                                st.success(
                                    f"Assessment submitted successfully. Auto score: {auto_score}/{assessment['total_marks']}"
                                )
                                st.rerun()
            else:
                st.info("No teacher-created quizzes or tests are available right now.")

            st.markdown("### Practice Quiz")
            quiz_subject = st.selectbox(
                "Choose subject for practice",
                ["Machine Learning", "Business Intelligence", "Database Systems"],
                key="quiz_subject_select",
            )
            questions = get_quiz_bank(quiz_subject)
            with st.form("quiz_form"):
                answers = []
                for idx, question in enumerate(questions, start=1):
                    answers.append(
                        st.radio(
                            f"Q{idx}. {question['question']}",
                            options=question["options"],
                            key=f"quiz_q_{quiz_subject}_{idx}",
                        )
                    )
                quiz_submit = st.form_submit_button("Submit Practice Quiz", use_container_width=True)

            if quiz_submit:
                score = 0
                for given_answer, question in zip(answers, questions):
                    if given_answer == question["answer"]:
                        score += 1
                percentage = (score / len(questions)) * 100 if questions else 0
                st.success(f"Instant Result: {score}/{len(questions)} ({percentage:.1f}%)")
                st.write("Practice quiz completed. Review mistakes and retry for stronger preparation.")


def render_history_page(services: Dict[str, Any]):
    """Render user-specific account and activity history."""
    database: Database = services["database"]
    st.title("History")

    if not (st.session_state.is_logged_in and st.session_state.current_username):
        st.warning("Log in first to view your personal history.")
        return

    username = st.session_state.current_username
    role = st.session_state.user_role
    profile = database.get_user_profile(username)

    st.subheader("User Credentials")
    if profile:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Username", profile["username"])
        with col2:
            st.metric("Role", profile["role"].title())
        with col3:
            st.metric("Registered On", profile["created_at"])
    else:
        st.info("No profile data found.")
        return

    if role == "teacher":
        st.subheader("Teacher Work History")
        sessions = database.get_user_grading_history(username, limit=50)
        assessments = database.get_teacher_assessments(username, limit=50)
        if not sessions:
            st.info("No teacher history found for this account yet.")
        else:
            history_df = pd.DataFrame(
                [
                    {
                        "Date": session["created_at"],
                        "Files": session["file_count"],
                        "Average Score": f"{session['average_percentage']:.1f}%",
                        "Total Marks": session["total_marks"],
                        "Multiple Questions": "Yes" if session["detect_multiple_questions"] else "No",
                    }
                    for session in sessions
                ]
            )
            st.dataframe(history_df, use_container_width=True)

            for session in sessions:
                with st.expander(
                    f"{session['created_at']} | {session['file_count']} files | Avg {session['average_percentage']:.1f}%"
                ):
                    if session["custom_criteria"]:
                        st.write(f"Criteria: {session['custom_criteria']}")
                    if session["additional_instructions"]:
                        st.write(f"Instructions: {session['additional_instructions']}")
                    session_results = database.get_session_results(session["id"])
                    if session_results:
                        st.write("Saved grading work:")
                        for item in session_results:
                            st.write(
                                f"- {item['filename']} | {item['awarded_marks']}/{item['total_marks']} "
                                f"({item['percentage']:.1f}%)"
                            )

        st.subheader("Created Quizzes and Tests")
        if assessments:
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Created": assessment["created_at"],
                            "Title": assessment["title"],
                            "Type": assessment["assessment_type"],
                            "Subject": assessment["subject"],
                            "Deadline": assessment["submission_deadline"],
                            "Duration": f"{assessment['duration_minutes']} min",
                            "Marks": assessment["total_marks"],
                        }
                        for assessment in assessments
                    ]
                ),
                use_container_width=True,
            )
        else:
            st.caption("No teacher-created assessments yet.")

    elif role == "student":
        st.subheader("Student Work History")
        submissions = database.get_student_submissions(username, limit=100)
        notifications = database.get_notifications(username, limit=50)
        active_assessments = database.get_active_assessments(limit=200)
        student_attempts = []
        for assessment in active_assessments:
            attempt = database.get_attempt_by_student_and_assessment(username, assessment["id"])
            if attempt:
                student_attempts.append({"assessment": assessment, "attempt": attempt})

        if submissions:
            submissions_df = pd.DataFrame(
                [
                    {
                        "Submitted": item["created_at"],
                        "Title": item["title"],
                        "Subject": item["subject"],
                        "Type": item["submission_type"],
                        "Score": f"{item['estimated_score']:.1f}%",
                        "Plagiarism": f"{item['plagiarism_percentage']:.1f}%",
                    }
                    for item in submissions
                ]
            )
            st.dataframe(submissions_df, use_container_width=True)

            for item in submissions:
                with st.expander(
                    f"{item['created_at']} | {item['title']} | {item['estimated_score']:.1f}%"
                ):
                    st.write(f"Subject: {item['subject']}")
                    st.write(f"Submission Type: {item['submission_type']}")
                    st.write(f"Deadline: {item['deadline']}")
                    st.write(f"File: {item['filename']}")
                    st.write(f"Plagiarism: {item['plagiarism_percentage']:.1f}%")
                    if item["matched_source"]:
                        st.write(f"Matched Source: {item['matched_source']}")
                    feedback = item.get("ai_feedback", {})
                    if feedback:
                        st.write("AI Feedback Summary:")
                        for line in feedback.get("improvement_recommendations", [])[:3]:
                            st.write(f"- {line}")
        else:
            st.info("No student submissions found for this account yet.")

        st.subheader("Attempted Quizzes and Tests")
        if student_attempts:
            st.dataframe(
                pd.DataFrame(
                    [
                        {
                            "Assessment": item["assessment"]["title"],
                            "Type": item["assessment"]["assessment_type"],
                            "Subject": item["assessment"]["subject"],
                            "Status": item["attempt"]["status"],
                            "Auto Score": f"{item['attempt']['auto_score']}/{item['attempt']['total_marks']}",
                            "Teacher Grade": item["attempt"]["teacher_grade"] if item["attempt"]["teacher_grade"] is not None else "-",
                        }
                        for item in student_attempts
                    ]
                ),
                use_container_width=True,
            )
        else:
            st.caption("No quiz or test attempts saved for this account yet.")

        st.subheader("Saved Alerts")
        if notifications:
            for notification in notifications:
                with st.expander(f"{notification['created_at']} | {notification['title']}"):
                    st.write(f"Category: {notification['category']}")
                    st.write(notification["message"])
        else:
            st.caption("No saved notifications for this account.")


def render_school_dashboard_section(database: Database, school: Dict[str, Any]):
    """Overview dashboard for the school portal."""
    members = database.get_school_members(school["id"])
    teacher_count = sum(1 for member in members if member["school_role"] == "teacher" and member["approved"])
    student_count = sum(1 for member in members if member["school_role"] == "student" and member["approved"])
    pending_members = sum(1 for member in members if not member["approved"])
    total_classes = 8

    st.subheader("Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Students", student_count)
    with c2:
        st.metric("Total Teachers", teacher_count)
    with c3:
        st.metric("Total Classes", total_classes)
    with c4:
        st.metric("Pending Approvals", pending_members)

    stats_df = pd.DataFrame(
        {
            "Category": ["Attendance", "Pending Fees", "Upcoming Exams", "Recent Activities"],
            "Value": [91, 14, 6, 12],
        }
    )
    st.bar_chart(stats_df.set_index("Category"))

    st.markdown("### Quick Summary")
    st.write("- Attendance summary: current monitored attendance is approximately 91%.")
    st.write("- Pending fees: 14 accounts need follow-up.")
    st.write("- Upcoming exams: 6 school-wide exams are planned.")
    st.write("- Notifications: school-wide alerts and announcements can be managed centrally.")


def render_school_admin_page(database: Database, school: Dict[str, Any]):
    """Render the admin-only school management portal."""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### School Admin")
        admin_sections = [
            "Dashboard",
            "Students",
            "Teachers",
            "Parents",
            "Classes",
            "Subjects",
            "Attendance",
            "Exams",
            "Assignments",
            "Fees",
            "Reports",
            "Notifications",
            "AI Analytics",
            "Settings",
            "Logout",
        ]
        selected_section = st.radio("Admin Sidebar", admin_sections, index=admin_sections.index(st.session_state.school_admin_view))
        st.session_state.school_admin_view = selected_section
        if selected_section == "Logout":
            st.session_state.school_code = None
            st.session_state.school_role = None
            st.session_state.school_admin_view = "Dashboard"
            navigate("welcome")
            st.rerun()

    section = st.session_state.school_admin_view
    members = database.get_school_members(school["id"])

    if section == "Dashboard":
        render_school_dashboard_section(database, school)
    elif section == "Students":
        st.subheader("Student Management")
        st.write("Admin can add, edit, delete, promote, suspend, or remove students from the school system.")
        student_rows = [member for member in members if member["school_role"] == "student"]
        st.dataframe(pd.DataFrame(student_rows), use_container_width=True)
    elif section == "Teachers":
        st.subheader("Teacher Management")
        st.write("Admin can assign subjects/classes, manage schedules, and monitor teacher attendance.")
        teacher_rows = [member for member in members if member["school_role"] == "teacher"]
        st.dataframe(pd.DataFrame(teacher_rows), use_container_width=True)
    elif section == "Parents":
        st.subheader("Parents")
        st.info("Parent access and family communication can be managed from this section.")
    elif section == "Classes":
        st.subheader("Class & Subject Management")
        st.write("Create classes and sections, assign teachers, and manage timetables.")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Class": "Grade 9-A", "Teacher": "teacher_demo", "Subjects": "Math, Science, English"},
                    {"Class": "Grade 10-B", "Teacher": "teacher_demo", "Subjects": "BI, CS, Statistics"},
                ]
            ),
            use_container_width=True,
        )
    elif section == "Subjects":
        st.subheader("Subjects")
        st.write("Allocate subjects, manage subject mapping, and review syllabus coverage.")
    elif section == "Attendance":
        st.subheader("Attendance Management")
        st.write("Monitor daily and monthly attendance, approve leave requests, and export records.")
        st.line_chart(pd.DataFrame({"Attendance %": [88, 90, 91, 89, 93]}, index=["Mon", "Tue", "Wed", "Thu", "Fri"]))
    elif section == "Exams":
        st.subheader("Examination & Grading System")
        st.write("Create exams, upload marks, publish results, and run AI-assisted grading analysis.")
    elif section == "Assignments":
        st.subheader("Assignment & Homework Management")
        st.write("Upload assignments, set deadlines, monitor submissions, and review grading status.")
    elif section == "Fees":
        st.subheader("Fee Management")
        st.write("Generate vouchers, track payments, manage scholarships/fines, and review financial reports.")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Category": "Pending Dues", "Count": 14},
                    {"Category": "Scholarships", "Count": 6},
                    {"Category": "Fines", "Count": 3},
                ]
            ),
            use_container_width=True,
        )
    elif section == "Reports":
        st.subheader("Reports Section")
        st.write("Generate student, attendance, fee, performance, and teacher reports in PDF, Excel, or CSV.")
    elif section == "Notifications":
        st.subheader("Notifications & Announcements")
        st.write("Send announcements, exam schedules, and emergency alerts to school users.")
        pending = [member for member in members if not member["approved"]]
        if pending:
            st.markdown("### Pending Access Requests")
            for member in pending:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{member['username']} requested {member['school_role']} access")
                with col2:
                    if st.button("Approve", key=f"approve_{member['username']}"):
                        database.approve_school_member(school["id"], member["username"])
                        st.success(f"Approved {member['username']}.")
                        st.rerun()
        else:
            st.caption("No pending approval requests.")
    elif section == "AI Analytics":
        st.subheader("AI Analytics Dashboard")
        st.write("AI can predict weak students, detect attendance issues, analyze trends, and recommend improvements.")
        st.area_chart(pd.DataFrame({"Performance Trend": [62, 66, 71, 69, 76, 82]}))
        st.info("AI Chat Assistant: quickly search records, answer system questions, and generate summaries.")
    elif section == "Settings":
        st.subheader("System Settings")
        st.write("Manage school information, academic year, password policies, themes/logo, email/SMS settings, and backups.")
        st.write("Backup & Database Management is included here for professional deployment workflows.")


def render_school_page(services: Dict[str, Any]):
    """SaaS school hub: subscription, payment proof, registration, portal access."""
    render_school_saas_hub(services)


def render_legacy_school_organization_page(services: Dict[str, Any]):
    """Classic join-by-code school organization UI."""
    database: Database = services["database"]
    st.title("School Organization Portal")
    st.markdown("Create or join a school-managed version of this system.")

    if not st.session_state.is_logged_in:
        st.subheader("School Admin Login")
        st.write("Log in here as the school admin to open the school-specific website.")

        with st.form("school_admin_login_form"):
            school_code = st.text_input("School Access Code")
            admin_username = st.text_input("Admin Username")
            admin_password = st.text_input("Admin Password", type="password")
            school_admin_login_submit = st.form_submit_button("Open School Website", use_container_width=True)

        if school_admin_login_submit:
            handle_school_admin_login(database, school_code, admin_username, admin_password)

        st.markdown("---")
        st.markdown("### Create School Organization")
        st.caption("Use this only when setting up a brand-new school portal.")
        with st.form("create_school_without_main_login"):
            new_admin_username = st.text_input("Teacher/Admin Username")
            new_admin_password = st.text_input("Teacher/Admin Password", type="password")
            school_name = st.text_input("School Name")
            new_school_code = st.text_input("New School Access Code")
            create_school_submit = st.form_submit_button("Create School Website", use_container_width=True)

        if create_school_submit:
            if not new_admin_username or not new_admin_password or not school_name or not new_school_code:
                st.warning("Fill in all fields to create a school website.")
            elif not database.authenticate_user("teacher", new_admin_username, new_admin_password):
                st.error("Admin account must be an existing teacher account with valid credentials.")
            elif database.create_school(school_name, new_school_code, new_admin_username):
                st.success("School website created. You can now log in through the school admin form above.")
            else:
                st.error("That school access code already exists or the school could not be created.")
        return

    current_username = st.session_state.current_username
    current_role = st.session_state.user_role

    if not st.session_state.school_code:
        st.subheader("School Access")
        left, right = st.columns(2)
        with left:
            st.markdown("### Create School Organization")
            if current_role == "teacher":
                with st.form("create_school_form"):
                    school_name = st.text_input("School Name")
                    school_code = st.text_input("School Access Code")
                    create_school_submit = st.form_submit_button("Create School", use_container_width=True)
                if create_school_submit:
                    if not school_name or not school_code:
                        st.warning("Enter both school name and school access code.")
                    elif database.create_school(school_name, school_code, current_username):
                        st.session_state.school_code = school_code
                        st.session_state.school_role = "admin"
                        st.success("School organization created successfully.")
                        st.rerun()
                    else:
                        st.error("That school access code already exists.")
            else:
                st.info("Only teachers can create a school organization and become school head/admin.")

        with right:
            st.markdown("### Join Existing School")
            with st.form("join_school_form"):
                join_school_code = st.text_input("School Access Code", key="join_school_code")
                school_role = st.selectbox("Join As", ["teacher", "student"], key="join_school_role")
                join_school_submit = st.form_submit_button("Request Access", use_container_width=True)
            if join_school_submit:
                if school_role != current_role:
                    st.warning(f"You are logged in as {current_role}. Join using the same account role.")
                elif not join_school_code:
                    st.warning("Enter a school access code.")
                else:
                    membership = database.get_school_membership(join_school_code, current_username)
                    if membership:
                        st.session_state.school_code = join_school_code
                        st.session_state.school_role = membership["school_role"] if membership["approved"] else "pending"
                        st.success("School access loaded.")
                        st.rerun()
                    elif database.add_school_membership(join_school_code, current_username, school_role, approved=False):
                        st.session_state.school_code = join_school_code
                        st.session_state.school_role = "pending"
                        st.success("Access request sent. Wait for school admin approval.")
                        st.rerun()
                    else:
                        st.error("School code not found or access request could not be created.")
        return

    school = database.get_school_by_code(st.session_state.school_code)
    if not school:
        st.session_state.school_code = None
        st.session_state.school_role = None
        st.error("School portal could not be loaded.")
        return

    membership = database.get_school_membership(st.session_state.school_code, current_username)
    st.success(f"School Site: {school['school_name']}")
    st.caption(f"School Code: {school['school_code']}")

    if not membership:
        st.error("You are not registered in this school portal.")
        return

    if not membership["approved"]:
        st.warning("Your school access is waiting for approval from the school head/admin.")
        return

    st.session_state.school_role = membership["school_role"]

    if membership["school_role"] == "admin":
        st.markdown("### Admin Button")
        render_school_admin_page(database, school)
    else:
        st.subheader("School Member Page")
        st.write(
            f"This school-specific site is accessible only to approved users allowed by the school head. "
            f"You are currently inside as a {membership['school_role']}."
        )
        st.write(
            "Teachers and students can use the regular Teacher Service and Student Service pages, "
            "while the school admin manages the full organization portal."
        )


def render_teacher_service_page(services: Dict[str, Any]):
    """Render the grading UI for teachers."""
    database: Database = services["database"]
    st.title("Teacher Grading Service")
    st.markdown("Upload assignments and exams to get automated grading with detailed feedback.")

    teacher_username = st.session_state.current_username if st.session_state.user_role == "teacher" else "guest_teacher"

    with st.sidebar:
        st.markdown("---")
        st.markdown("### Teacher Tools")
        if st.button("Grading Service", use_container_width=True):
            st.session_state.teacher_service_view = "grading"
        if st.button("Quiz and Test Maker", use_container_width=True):
            st.session_state.teacher_service_view = "assessment_maker"

        teacher_view = st.session_state.teacher_service_view

        if teacher_view == "grading":
            st.markdown("### Grading Configuration")

            total_marks = st.number_input(
                "Total Marks for Assignment",
                min_value=1,
                max_value=1000,
                value=100,
                help="Enter the total marks for this assignment",
            )

            st.subheader("Custom Grading Criteria")
            use_custom_criteria = st.checkbox(
                "Use Custom Grading Criteria",
                help="Define specific point allocation for different aspects",
                key="use_custom_criteria",
            )

            custom_criteria = {}
            if use_custom_criteria:
                st.write("Define your grading criteria:")
                num_criteria = st.number_input(
                    "Number of Criteria", min_value=1, max_value=10, value=3, key="num_criteria"
                )

                for i in range(int(num_criteria)):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        criterion_name = st.text_input(
                            f"Criterion {i + 1}",
                            value=f"Criterion {i + 1}",
                            key=f"criterion_name_{i}",
                        )
                    with col2:
                        criterion_marks = st.number_input(
                            "Marks",
                            min_value=0,
                            max_value=total_marks,
                            value=10,
                            key=f"criterion_marks_{i}",
                        )
                    if criterion_name:
                        custom_criteria[criterion_name] = criterion_marks

                if sum(custom_criteria.values()) > total_marks:
                    st.error(
                        f"Sum of criteria marks ({sum(custom_criteria.values())}) exceeds total marks ({total_marks})"
                    )

            additional_instructions = st.text_area(
                "Additional Grading Instructions",
                placeholder="Enter any specific instructions for grading...",
                help="Provide context about the assignment, what to look for, etc.",
            )

            detect_multiple_questions = st.checkbox(
                "Detect Multiple Questions",
                value=True,
                help="Attempt to identify and grade multiple questions within each file",
            )

            st.subheader("Export Options")
            export_to_excel = st.checkbox(
                "Export Results to Excel",
                value=True,
                help="Compile all results into an Excel file",
            )
            show_detailed_feedback = st.checkbox(
                "Show Detailed Feedback",
                value=True,
                help="Display comprehensive feedback for each submission",
            )
        else:
            total_marks = 100
            use_custom_criteria = False
            custom_criteria = {}
            additional_instructions = ""
            detect_multiple_questions = True
            export_to_excel = True
            show_detailed_feedback = True

    col1, col2 = st.columns([2, 1])
    with col1:
        if teacher_view == "assessment_maker":
            render_assessment_creator(database, teacher_username)
        else:
            st.header("Upload Assignment Files")
            uploaded_files = st.file_uploader(
                "Choose files to grade",
                type=["pdf", "docx", "jpg", "jpeg", "png"],
                accept_multiple_files=True,
                help="Supported formats: PDF, Word documents, and images (JPG, PNG)",
            )

            if uploaded_files:
                st.success(f"{len(uploaded_files)} file(s) uploaded successfully")
                with st.expander("Uploaded Files", expanded=True):
                    for file in uploaded_files:
                        file_type = validate_file_type(file.name)
                        file_type_display = file_type.upper() if file_type else "UNKNOWN"
                        st.write(f"- **{file.name}** ({file_type_display}) - {file.size:,} bytes")

    with col2:
        st.header("Teacher Access")
        if st.session_state.is_logged_in and st.session_state.user_role == "teacher":
            st.success(f"Teacher session active: {st.session_state.current_username}")
        else:
            st.warning("You are viewing teacher services without a teacher login.")

        if st.session_state.is_logged_in and st.session_state.user_role == "teacher":
            st.markdown("### Assessment Attempts")
            attempts = database.get_attempts_for_teacher(teacher_username, limit=20)
            if attempts:
                for attempt in attempts:
                    with st.expander(
                        f"{attempt.get('assessment_title', 'Assessment')} | {attempt['student_username']} | {attempt['status']}"
                    ):
                        st.write(f"Subject: {attempt.get('assessment_subject', '')}")
                        st.write(f"Started: {attempt['started_at']}")
                        st.write(f"Submitted: {attempt['submitted_at'] or 'Not submitted'}")
                        st.write(f"Auto Score: {attempt['auto_score']}/{attempt['total_marks']}")
                        if attempt.get("teacher_grade") is not None:
                            st.write(f"Teacher Grade: {attempt['teacher_grade']}/{attempt['total_marks']}")
                        for idx, question in enumerate(attempt.get("questions", []), start=1):
                            st.write(f"Q{idx}: {question.get('question', '')}")
                            st.write(f"Student Answer: {attempt.get('answers', {}).get(str(idx), 'No answer')}")
                        if st.button(f"AI Grade Attempt {attempt['id']}", key=f"ai_grade_attempt_{attempt['id']}"):
                            assessment = database.get_assessment_by_id(attempt["assessment_id"])
                            if assessment:
                                grading_text = build_attempt_answer_text(assessment, attempt.get("answers", {}))
                                ai_grade = services["grading_service"].grade_assignment(
                                    grading_text,
                                    int(assessment["total_marks"]),
                                    {},
                                    "Grade this assessment attempt by comparing student answers with the expected answers.",
                                    True,
                                )
                                database.save_teacher_quiz_grade(
                                    attempt["id"],
                                    ai_grade.get("total_score", 0),
                                    ai_grade.get("feedback", ""),
                                )
                                st.success("Attempt graded and saved.")
                                st.write(ai_grade.get("feedback", ""))
                        if attempt.get("ai_feedback"):
                            st.write("Saved AI Feedback:")
                            st.write(attempt["ai_feedback"])
            else:
                st.caption("No assessment attempts yet.")

            st.markdown("### Saved Grading History")
            history = database.get_user_grading_history(st.session_state.current_username, limit=5)
            if history:
                for session in history:
                    with st.expander(
                        f"{session['created_at']} | {session['file_count']} files | Avg {session['average_percentage']:.1f}%"
                    ):
                        st.write(f"Total marks: {session['total_marks']}")
                        st.write(
                            f"Detect multiple questions: {'Yes' if session['detect_multiple_questions'] else 'No'}"
                        )
                        if session["custom_criteria"]:
                            st.write(f"Criteria: {session['custom_criteria']}")
                        if session["additional_instructions"]:
                            st.write(f"Instructions: {session['additional_instructions']}")
                        saved_results = database.get_session_results(session["id"])
                        if saved_results:
                            st.write("Saved files:")
                            for saved_result in saved_results:
                                st.write(
                                    f"- {saved_result['filename']}: {saved_result['awarded_marks']}/"
                                    f"{saved_result['total_marks']} ({saved_result['percentage']:.1f}%)"
                                )
            else:
                st.caption("No saved grading history yet.")

    if teacher_view == "grading" and uploaded_files:
        st.header("Start Grading")
        if st.button("Grade All Assignments", type="primary", use_container_width=True):
            if use_custom_criteria and sum(custom_criteria.values()) > total_marks:
                st.error("Please fix the grading criteria configuration before proceeding.")
                return

            progress_bar = st.progress(0)
            status_text = st.empty()
            results_container = st.container()
            all_results = []

            try:
                for idx, uploaded_file in enumerate(uploaded_files):
                    progress = idx / len(uploaded_files)
                    progress_bar.progress(progress)
                    status_text.text(f"Processing {uploaded_file.name}...")

                    with st.spinner(f"Grading {uploaded_file.name}..."):
                        result = process_single_file(
                            uploaded_file,
                            services,
                            total_marks,
                            custom_criteria if use_custom_criteria else {},
                            additional_instructions,
                            detect_multiple_questions,
                        )
                        if result:
                            all_results.append(result)

                progress_bar.progress(1.0)
                status_text.text("All files processed successfully!")

                if all_results:
                    if st.session_state.is_logged_in and st.session_state.user_role == "teacher":
                        session_id = database.create_grading_session(
                            teacher_username=st.session_state.current_username,
                            total_marks=total_marks,
                            custom_criteria=custom_criteria if use_custom_criteria else {},
                            additional_instructions=additional_instructions,
                            detect_multiple_questions=detect_multiple_questions,
                        )
                        database.save_grading_results(session_id, all_results)

                    results_tab, analytics_tab = st.tabs(["Results", "Advanced Analytics"])

                    with results_tab:
                        display_results(all_results, show_detailed_feedback, results_container)
                        if export_to_excel:
                            excel_data = services["excel_exporter"].create_excel_report(all_results)
                            if excel_data:
                                st.download_button(
                                    label="Download Excel Report",
                                    data=excel_data,
                                    file_name=f"grading_report_{int(time.time())}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                )

                    with analytics_tab:
                        display_analytics(all_results, services["analytics_service"])

            except Exception as e:
                st.error(f"Error during processing: {str(e)}")
                st.exception(e)


def process_single_file(
    uploaded_file,
    services,
    total_marks,
    custom_criteria,
    additional_instructions,
    detect_multiple_questions,
) -> Dict[str, Any]:
    """Process a single uploaded file and return grading results."""
    file_type = validate_file_type(uploaded_file.name)

    try:
        if file_type in ["jpg", "jpeg", "png"]:
            text_content = services["ocr_service"].extract_text_from_image(uploaded_file)
        else:
            text_content = services["file_processor"].extract_text(uploaded_file, file_type)

        if not text_content or not text_content.strip():
            st.warning(f"No text content found in {uploaded_file.name}")
            return {
                "filename": uploaded_file.name,
                "file_type": file_type or "unknown",
                "total_marks": total_marks,
                "awarded_marks": 0,
                "percentage": 0,
                "feedback": "No text content could be extracted from this file.",
                "criteria_breakdown": {},
                "criteria_explanations": {},
                "questions": [],
                "strengths": [],
                "areas_for_improvement": [],
                "grade_justification": "",
                "text_content": "No content available",
            }

        grading_result = services["grading_service"].grade_assignment(
            text_content,
            total_marks,
            custom_criteria,
            additional_instructions,
            detect_multiple_questions,
        )

        return {
            "filename": uploaded_file.name,
            "file_type": file_type,
            "total_marks": total_marks,
            "awarded_marks": grading_result.get("total_score", 0),
            "percentage": grading_result.get("percentage", 0),
            "feedback": grading_result.get("feedback", ""),
            "criteria_breakdown": grading_result.get("criteria_scores", {}),
            "criteria_explanations": grading_result.get("criteria_explanations", {}),
            "questions": grading_result.get("questions", []),
            "strengths": grading_result.get("strengths", []),
            "areas_for_improvement": grading_result.get("areas_for_improvement", []),
            "grade_justification": grading_result.get("grade_justification", ""),
            "text_content": text_content[:500] + "..." if len(text_content) > 500 else text_content,
        }

    except Exception as e:
        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
        return {
            "filename": uploaded_file.name,
            "file_type": file_type or "unknown",
            "total_marks": total_marks,
            "awarded_marks": 0,
            "percentage": 0,
            "feedback": f"Error processing file: {str(e)}",
            "criteria_breakdown": {},
            "criteria_explanations": {},
            "questions": [],
            "strengths": [],
            "areas_for_improvement": [],
            "grade_justification": "",
            "text_content": "Error occurred during processing",
        }


def display_results(results: List[Dict], show_detailed_feedback: bool, container):
    """Display grading results in an organized format."""
    with container:
        st.header("Grading Results")
        total_files = len(results)
        avg_score = sum(r["percentage"] for r in results) / total_files if results else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Files Graded", total_files)
        with col2:
            st.metric("Average Score", f"{avg_score:.1f}%")
        with col3:
            highest_score = max(r["percentage"] for r in results) if results else 0
            st.metric("Highest Score", f"{highest_score:.1f}%")

        st.subheader("Summary Table")
        df = pd.DataFrame(
            [
                {
                    "File Name": result["filename"],
                    "Score": f"{result['awarded_marks']}/{result['total_marks']}",
                    "Percentage": f"{result['percentage']:.1f}%",
                    "Grade": format_grade_display(result["percentage"]),
                }
                for result in results
            ]
        )
        st.dataframe(df, use_container_width=True)

        st.subheader("Detailed Results")
        for result in results:
            with st.expander(
                f"{result['filename']} - {result['awarded_marks']}/{result['total_marks']} ({result['percentage']:.1f}%)"
            ):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.write("**Score Breakdown:**")
                    if result["criteria_breakdown"]:
                        for criterion, score in result["criteria_breakdown"].items():
                            explanation = result.get("criteria_explanations", {}).get(criterion, "")
                            st.write(f"- {criterion}: {score} marks")
                            if explanation:
                                st.write(f"  *{explanation}*")
                    else:
                        st.write(f"Total Score: {result['awarded_marks']}/{result['total_marks']}")

                with col2:
                    st.write("**File Information:**")
                    st.write(f"- File Type: {result['file_type'].upper()}")
                    st.write(f"- Grade: {format_grade_display(result['percentage'])}")

                if result["questions"] and len(result["questions"]) > 1:
                    st.write("**Questions Breakdown:**")
                    for i, question in enumerate(result["questions"], 1):
                        st.write(f"**Question {i}:** {question.get('score', 0)} marks")
                        if show_detailed_feedback and question.get("feedback"):
                            st.write(f"*Feedback:* {question['feedback']}")

                if show_detailed_feedback and result["feedback"]:
                    st.write("**Overall Feedback:**")
                    st.write(result["feedback"])

                st.write("**Extracted Text Preview:**")
                st.text_area(
                    "Text Content",
                    value=result["text_content"],
                    height=100,
                    disabled=True,
                    key=f"text_preview_{result['filename']}",
                )


def display_analytics(results: List[Dict], analytics_service: AnalyticsService):
    """Display advanced analytics with interactive visualizations."""
    analytics_service.load_results(results)
    st.header("Advanced Analytics Dashboard")

    st.subheader("1. Question Attempt Analysis")
    max_questions = analytics_service.get_max_questions()
    if max_questions > 0:
        selected_question = st.selectbox(
            "Select question number to analyze:",
            options=list(range(1, max_questions + 1)),
            key="question_selector",
        )
        attempt_data = analytics_service.analyze_question_attempts(selected_question)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Students Attempted", attempt_data["attempted_count"])
        with col2:
            st.metric("Total Students", attempt_data["total_students"])
        with col3:
            st.metric("Attempt Rate", f"{attempt_data['percentage']:.1f}%")

    st.subheader("2. Most Attempted Question")
    most_attempted = analytics_service.get_most_attempted_question()
    if most_attempted["question_number"] > 0:
        st.info(
            f"Question {most_attempted['question_number']} was attempted by "
            f"{most_attempted['attempts']} students ({most_attempted['percentage']:.1f}%)"
        )

    st.subheader("3. Average Questions Attempted")
    st.metric("Average Questions per Student", f"{analytics_service.get_average_questions_attempted():.1f}")

    st.subheader("4. Most Skipped Question")
    most_skipped = analytics_service.get_most_skipped_question()
    if most_skipped["question_number"] > 0:
        st.warning(
            f"Question {most_skipped['question_number']} was skipped by "
            f"{most_skipped['skipped_count']} students ({most_skipped['percentage']:.1f}%)"
        )

    st.subheader("5. Grade Distribution")
    col1, col2 = st.columns([2, 1])
    with col1:
        grade_chart = analytics_service.create_grade_distribution_chart()
        if grade_chart.data:
            st.plotly_chart(grade_chart, use_container_width=True)
    with col2:
        grade_dist = analytics_service.get_grade_distribution()
        st.write("**Grade Statistics:**")
        st.metric("Class Average", f"{grade_dist['average']:.1f}%")
        st.metric("Median Score", f"{grade_dist['median']:.1f}%")
        st.metric("Standard Deviation", f"{grade_dist['std_dev']:.1f}")

    st.subheader("6. Consistent Performers")
    consistent_students = analytics_service.get_consistent_performers()
    if consistent_students:
        st.write(f"{len(consistent_students)} students showed consistent performance:")
        for student in consistent_students[:5]:
            with st.expander(
                f"{student['filename']} - Avg: {student['average_score']:.1f}%, "
                f"Deviation: {student['std_deviation']:.1f}"
            ):
                scores_text = ", ".join(
                    [f"Q{i + 1}: {score:.1f}%" for i, score in enumerate(student["question_scores"])]
                )
                st.write(f"Question scores: {scores_text}")
    else:
        st.info("No students with consistent performance patterns found.")

    st.subheader("7. Inconsistent Performance")
    inconsistent_students = analytics_service.get_inconsistent_performers()
    if inconsistent_students:
        st.write(f"{len(inconsistent_students)} students showed inconsistent performance:")
        for student in inconsistent_students[:5]:
            with st.expander(
                f"{student['filename']} - Range: {student['score_range']:.1f}%, "
                f"Deviation: {student['std_deviation']:.1f}"
            ):
                scores_text = ", ".join(
                    [f"Q{i + 1}: {score:.1f}%" for i, score in enumerate(student["question_scores"])]
                )
                st.write(f"Question scores: {scores_text}")
                st.write(f"Lowest: {student['min_score']:.1f}%, Highest: {student['max_score']:.1f}%")
    else:
        st.info("No students with significant performance inconsistencies found.")

    st.subheader("8. Above Average Performance")
    above_avg_data = analytics_service.get_above_average_percentage()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Students Above Average", f"{above_avg_data['count']}/{above_avg_data['total']}")
    with col2:
        st.metric("Percentage Above Average", f"{above_avg_data['percentage']:.1f}%")
    with col3:
        st.metric("Class Average", f"{above_avg_data['class_average']:.1f}%")

    st.subheader("Interactive Visualizations")
    st.write("**Question Attempts vs Skipped**")
    attempts_chart = analytics_service.create_question_attempts_chart()
    if attempts_chart.data:
        st.plotly_chart(attempts_chart, use_container_width=True)

    st.write("**Performance Consistency Analysis**")
    consistency_chart = analytics_service.create_performance_consistency_chart()
    if consistency_chart.data:
        st.plotly_chart(consistency_chart, use_container_width=True)
        st.caption(
            "Students in the bottom-left are most consistent. Students in the top-right scored well but vary more."
        )


def main():
    initialize_session_state()
    services = initialize_services()
    render_sidebar()

    page = st.session_state.current_page
    if page == "welcome":
        render_welcome_page()
    elif page == "login":
        render_login_page(services["database"])
    elif page == "master_admin":
        render_master_admin_panel()
    elif page == "school_portal":
        uid = st.session_state.get("user_id")
        if not AccessControl.can_open_school_portal(uid):
            st.error("School Portal is locked. Complete **subscription payment verification** and **school registration** from the School hub.")
            if st.button("Open School hub", type="primary"):
                navigate("school")
                st.rerun()
        else:
            render_school_portal()
    elif page == "student_service":
        render_student_service_page(services)
    elif page == "school":
        render_school_page(services)
    elif page == "school_legacy":
        render_legacy_school_organization_page(services)
    elif page == "history":
        render_history_page(services)
    elif page == "teacher_service":
        render_teacher_service_page(services)
    else:
        render_welcome_page()


if __name__ == "__main__":
    main()
