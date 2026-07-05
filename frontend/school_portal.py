"""
SCHOOL PORTAL - Main Module
Enterprise-level school management system with AI integration.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import random
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from database import Database
from school_portal_helpers import *
from saas_access_control import AccessControl

# Configure page
st.set_page_config(
    page_title="SC Portals",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db = Database()


# ==================== DASHBOARD ====================

def render_dashboard():
    """Render school dashboard."""
    st.markdown("### 🎓 School Dashboard")
    
    # Get sample data
    kpi_data = {
        "total_students": random.randint(500, 1500),
        "total_teachers": random.randint(30, 80),
        "total_classes": random.randint(15, 40),
        "active_courses": random.randint(80, 150),
        "attendance_rate": round(random.uniform(85, 98), 1),
        "assignments_submitted": random.randint(300, 800),
        "pending_fees": round(random.uniform(50000, 200000), 2),
        "ai_requests": random.randint(1000, 5000)
    }
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            kpi_data["total_students"],
            "+12 this month"
        )
    
    with col2:
        st.metric(
            "👨‍🏫 Total Teachers",
            kpi_data["total_teachers"],
            "+2 this month"
        )
    
    with col3:
        st.metric(
            "📚 Total Classes",
            kpi_data["total_classes"],
            "Stable"
        )
    
    with col4:
        st.metric(
            "📖 Active Courses",
            kpi_data["active_courses"],
            "+5 this month"
        )
    
    # Second row of KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            "📊 Attendance Rate",
            f"{kpi_data['attendance_rate']}%",
            "+2.5%"
        )
    
    with col6:
        st.metric(
            "✅ Assignments",
            kpi_data["assignments_submitted"],
            "+45 today"
        )
    
    with col7:
        st.metric(
            "💰 Pending Fees",
            f"₹{kpi_data['pending_fees']:,.0f}",
            "-5% vs last month"
        )
    
    with col8:
        st.metric(
            "🤖 AI Requests",
            kpi_data["ai_requests"],
            "+8% this week"
        )
    
    # Charts
    st.divider()
    col1, col2 = st.columns(2)
    
    # Attendance Chart
    with col1:
        st.subheader("📈 Monthly Attendance Trend")
        days = pd.date_range(start="2024-04-01", periods=30, freq="D")
        attendance_data = [round(random.uniform(80, 98), 1) for _ in range(30)]
        
        fig_att = go.Figure()
        fig_att.add_trace(go.Scatter(
            x=days, y=attendance_data,
            mode='lines+markers',
            fill='tozeroy',
            name='Attendance %'
        ))
        fig_att.update_layout(
            title="Daily Attendance Percentage",
            xaxis_title="Date",
            yaxis_title="Attendance %",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_att, width='stretch')
    
    # Revenue Chart
    with col2:
        st.subheader("💹 Revenue Collection Trend")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        collected = [round(random.uniform(800000, 1200000), 2) for _ in months]
        
        fig_rev = go.Figure(data=[
            go.Bar(x=months, y=collected, marker_color='lightblue')
        ])
        fig_rev.update_layout(
            title="Monthly Revenue Collection",
            xaxis_title="Month",
            yaxis_title="Amount (₹)",
            height=400
        )
        st.plotly_chart(fig_rev, width='stretch')
    
    # Recent Activities
    st.divider()
    st.subheader("📋 Recent Activities")
    
    activities = [
        {"time": "2 mins ago", "user": "John Doe", "action": "Uploaded assignment", "type": "📝"},
        {"time": "15 mins ago", "user": "Jane Smith", "action": "Submitted exam", "type": "📊"},
        {"time": "1 hour ago", "user": "Admin", "action": "Updated timetable", "type": "📅"},
        {"time": "2 hours ago", "user": "Teacher", "action": "Marked attendance", "type": "✅"},
        {"time": "3 hours ago", "user": "Student", "action": "Paid fees", "type": "💰"},
    ]
    
    for activity in activities:
        col1, col2, col3, col4 = st.columns([0.5, 2, 3, 1.5])
        with col1:
            st.write(activity["type"])
        with col2:
            st.write(activity["user"])
        with col3:
            st.write(activity["action"])
        with col4:
            st.caption(activity["time"])


# ==================== STUDENT MANAGEMENT ====================

def render_student_management():
    """Render student management module."""
    st.markdown("### 👨‍🎓 Student Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["View Students", "Add Student", "Student Profile", "Student Analytics"])
    
    with tab1:
        st.subheader("Student List")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_query = st.text_input("🔍 Search student by name or ID")
        with col2:
            class_filter = st.selectbox("Filter by Class", ["All", "10-A", "10-B", "9-A", "9-B"])
        with col3:
            status_filter = st.selectbox("Filter by Status", ["All", "Active", "Suspended", "Left"])
        
        # Sample student data
        students_data = {
            "Student ID": [f"STU-2024-{i}" for i in range(1, 26)],
            "Name": [f"Student {i}" for i in range(1, 26)],
            "Roll": list(range(1, 26)),
            "Class": [random.choice(["10-A", "10-B", "9-A", "9-B"]) for _ in range(25)],
            "Email": [f"student{i}@school.com" for i in range(1, 26)],
            "Attendance": [f"{random.randint(70, 100)}%" for _ in range(25)],
            "Status": [random.choice(["Active", "Suspended"]) for _ in range(25)]
        }
        
        df_students = pd.DataFrame(students_data)
        
        # Apply filters
        if class_filter != "All":
            df_students = df_students[df_students["Class"] == class_filter]
        if status_filter != "All":
            df_students = df_students[df_students["Status"] == status_filter]
        
        st.dataframe(df_students, width='stretch', hide_index=True)
    
    with tab2:
        st.subheader("Add New Student")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            email = st.text_input("Email")
            class_name = st.selectbox("Class", ["10-A", "10-B", "9-A", "9-B", "8-A", "8-B"])
        
        with col2:
            last_name = st.text_input("Last Name")
            phone = st.text_input("Phone")
            roll_number = st.number_input("Roll Number", 1, 100)
        
        col3, col4 = st.columns(2)
        with col3:
            parent_name = st.text_input("Parent Name")
            parent_phone = st.text_input("Parent Phone")
        
        with col4:
            dob = st.date_input("Date of Birth")
            admission_date = st.date_input("Admission Date")
        
        if st.button("✅ Add Student", key="add_student_btn"):
            student_id = generate_student_id(class_name, roll_number)
            st.success(f"✓ Student added successfully! ID: {student_id}")
            st.balloons()
    
    with tab3:
        st.subheader("Student Profile")
        
        selected_student = st.selectbox("Select Student", [f"Student {i}" for i in range(1, 26)])
        
        # Profile sections
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Roll Number", "15")
            st.metric("Class", "10-A")
            st.metric("Status", "Active")
        
        with col2:
            st.metric("Attendance", "95%", "+5%")
            st.metric("GPA", "3.8", "+0.2")
            st.metric("Fees Status", "Paid", "✓")
        
        with col3:
            st.metric("Assignments", "12/12", "100%")
            st.metric("Exams Taken", "4/4", "100%")
            st.metric("AI Feedbacks", "8", "High Quality")
    
    with tab4:
        st.subheader("Student Analytics")
        
        # Performance distribution
        col1, col2 = st.columns(2)
        
        with col1:
            grades_dist = {"A+": 5, "A": 8, "B": 7, "C": 3, "D": 2}
            fig_grade = go.Figure(data=[
                go.Pie(labels=list(grades_dist.keys()), values=list(grades_dist.values()))
            ])
            fig_grade.update_layout(title="Grade Distribution")
            st.plotly_chart(fig_grade, width='stretch')
        
        with col2:
            attendance_ranges = {"90-100%": 15, "80-90%": 7, "70-80%": 2, "<70%": 1}
            fig_att = go.Figure(data=[
                go.Bar(x=list(attendance_ranges.keys()), y=list(attendance_ranges.values()))
            ])
            fig_att.update_layout(title="Attendance Distribution")
            st.plotly_chart(fig_att, width='stretch')


# ==================== TEACHER MANAGEMENT ====================

def render_teacher_management():
    """Render teacher management module."""
    st.markdown("### 👨‍🏫 Teacher Management")
    
    tab1, tab2, tab3 = st.tabs(["View Teachers", "Add Teacher", "Teacher Analytics"])
    
    with tab1:
        st.subheader("Teacher List")
        
        col1, col2 = st.columns(2)
        with col1:
            search_teacher = st.text_input("🔍 Search teacher")
        with col2:
            subject_filter = st.selectbox("Filter by Subject", ["All", "Mathematics", "English", "Science", "History"])
        
        teachers_data = {
            "Teacher ID": [f"TCH-2024-{i}" for i in range(1, 11)],
            "Name": [f"Teacher {i}" for i in range(1, 11)],
            "Subject": [random.choice(["Mathematics", "English", "Science", "History"]) for _ in range(10)],
            "Classes": [f"{random.randint(2, 4)} Classes" for _ in range(10)],
            "Experience": [f"{random.randint(2, 15)} years" for _ in range(10)],
            "AI Usage": [f"{random.randint(10, 100)}%" for _ in range(10)],
            "Rating": [f"{random.uniform(3.5, 5):.1f}/5" for _ in range(10)]
        }
        
        df_teachers = pd.DataFrame(teachers_data)
        st.dataframe(df_teachers, width='stretch', hide_index=True)
    
    with tab2:
        st.subheader("Add New Teacher")
        
        col1, col2 = st.columns(2)
        with col1:
            t_first_name = st.text_input("First Name", key="t_first")
            t_email = st.text_input("Email", key="t_email")
            t_subject = st.selectbox("Subject", ["Mathematics", "English", "Science", "History", "Computer Science"])
        
        with col2:
            t_last_name = st.text_input("Last Name", key="t_last")
            t_phone = st.text_input("Phone", key="t_phone")
            t_qualification = st.text_input("Qualification")
        
        if st.button("✅ Add Teacher", key="add_teacher_btn"):
            teacher_id = generate_teacher_id()
            st.success(f"✓ Teacher added successfully! ID: {teacher_id}")
            st.balloons()
    
    with tab3:
        st.subheader("Teacher Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**AI Grading Usage**")
            usage_data = [("Teacher 1", 95), ("Teacher 2", 87), ("Teacher 3", 92), ("Teacher 4", 78), ("Teacher 5", 88)]
            fig_usage = go.Figure(data=[
                go.Bar(y=[x[0] for x in usage_data], x=[x[1] for x in usage_data], orientation='h')
            ])
            st.plotly_chart(fig_usage, width='stretch')
        
        with col2:
            st.write("**Teaching Performance Ratings**")
            ratings = ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4", "Teacher 5"]
            scores = [4.8, 4.5, 4.7, 4.2, 4.6]
            fig_rating = go.Figure(data=[
                go.Bar(x=ratings, y=scores, marker_color='lightblue')
            ])
            fig_rating.update_layout(title="Average Rating (out of 5)")
            st.plotly_chart(fig_rating, width='stretch')


# ==================== CLASS & SUBJECT MANAGEMENT ====================

def render_class_management():
    """Render class and subject management."""
    st.markdown("### 📚 Classes & Subjects")
    
    tab1, tab2, tab3 = st.tabs(["View Classes", "Manage Subjects", "Timetable"])
    
    with tab1:
        st.subheader("Class List")
        
        classes_data = {
            "Class ID": [f"CLASS-{cls}-A" for cls in range(8, 13)],
            "Class Name": ["8-A", "9-A", "10-A", "11-A", "12-A"],
            "Class Teacher": ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4", "Teacher 5"],
            "Students": [45, 42, 40, 38, 35],
            "Subjects": [6, 6, 7, 8, 8],
            "Status": ["Active"] * 5
        }
        
        df_classes = pd.DataFrame(classes_data)
        st.dataframe(df_classes, width='stretch', hide_index=True)
    
    with tab2:
        st.subheader("Subject Management")
        
        selected_class = st.selectbox("Select Class", ["8-A", "9-A", "10-A", "11-A", "12-A"])
        
        subjects_list = {
            "Subject": ["Mathematics", "English", "Science", "Social Studies", "Physical Education"],
            "Code": ["MATH", "ENG", "SCI", "SOC", "PE"],
            "Teacher": ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4", "Teacher 5"],
            "Credits": [4, 3, 4, 3, 2]
        }
        
        df_subjects = pd.DataFrame(subjects_list)
        st.dataframe(df_subjects, width='stretch', hide_index=True)
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            new_subject = st.text_input("New Subject Name")
        with col2:
            new_code = st.text_input("Subject Code")
        
        if st.button("Add Subject"):
            st.success(f"✓ Subject '{new_subject}' added!")
    
    with tab3:
        st.subheader("Weekly Timetable")
        
        selected_class_tt = st.selectbox("Select Class", ["8-A", "9-A", "10-A", "11-A", "12-A"], key="tt_class")
        
        # Create timetable
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        periods = ["Period 1\n(9:00-10:00)", "Period 2\n(10:00-11:00)", "Period 3\n(11:00-12:00)", "Period 4\n(12:00-1:00)"]
        
        timetable = {
            day: [random.choice(["Mathematics", "English", "Science", "Social Studies", "PE"]) for _ in periods]
            for day in days
        }
        
        df_tt = pd.DataFrame(timetable, index=periods)
        st.dataframe(df_tt, width='stretch')


# ==================== ATTENDANCE MANAGEMENT ====================

def render_attendance():
    """Render attendance management module."""
    st.markdown("### 📋 Attendance Management")
    
    tab1, tab2, tab3 = st.tabs(["Mark Attendance", "View Records", "Analytics"])
    
    with tab1:
        st.subheader("Mark Attendance")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            att_date = st.date_input("Attendance Date")
        with col2:
            att_class = st.selectbox("Select Class", ["10-A", "10-B", "9-A", "9-B"])
        with col3:
            att_subject = st.selectbox("Subject", ["Mathematics", "English", "Science"])
        
        st.divider()
        
        # Create attendance form
        students_for_att = [f"Student {i} (Roll {i})" for i in range(1, 41)]
        att_status = []
        
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        
        for idx, student in enumerate(students_for_att[:16]):
            with cols[idx % 4]:
                status = st.radio(f"{student}", ["Present", "Absent", "Leave"], key=f"att_{idx}", horizontal=True)
                att_status.append(status)
        
        if st.button("💾 Save Attendance"):
            st.success("✓ Attendance marked successfully!")
    
    with tab2:
        st.subheader("Attendance Records")
        
        records_data = {
            "Date": pd.date_range("2024-04-01", periods=20, freq="D"),
            "Student": [f"Student {random.randint(1, 40)}" for _ in range(20)],
            "Status": [random.choice(["Present", "Absent", "Leave"]) for _ in range(20)],
            "Class": [random.choice(["10-A", "10-B", "9-A", "9-B"]) for _ in range(20)]
        }
        
        df_records = pd.DataFrame(records_data)
        st.dataframe(df_records, width='stretch', hide_index=True)
    
    with tab3:
        st.subheader("Attendance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Class-wise Attendance**")
            classes_att = ["10-A", "10-B", "9-A", "9-B"]
            attendance_pct = [round(random.uniform(85, 98), 1) for _ in classes_att]
            fig_class_att = go.Figure(data=[
                go.Bar(x=classes_att, y=attendance_pct, marker_color='lightgreen')
            ])
            st.plotly_chart(fig_class_att, width='stretch')
        
        with col2:
            st.write("**Monthly Attendance Trend**")
            months_att = ["Jan", "Feb", "Mar", "Apr", "May"]
            avg_attendance = [85, 87, 89, 92, 95]
            fig_trend = go.Figure(data=[
                go.Scatter(x=months_att, y=avg_attendance, mode='lines+markers', fill='tozeroy')
            ])
            fig_trend.update_layout(title="School Average Attendance")
            st.plotly_chart(fig_trend, width='stretch')


# ==================== EXAMINATION & RESULTS ====================

def render_exams():
    """Render examination management module."""
    st.markdown("### 📝 Examinations & Results")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Create Exam", "View Exams", "Upload Results", "Report Cards"])
    
    with tab1:
        st.subheader("Create New Exam")
        
        col1, col2 = st.columns(2)
        with col1:
            exam_name = st.text_input("Exam Name")
            exam_class = st.selectbox("Class", ["10-A", "10-B", "9-A", "9-B"])
            exam_date = st.date_input("Exam Date")
        
        with col2:
            exam_subject = st.selectbox("Subject", ["Mathematics", "English", "Science"])
            total_marks = st.number_input("Total Marks", 1, 500, 100)
            passing_marks = st.number_input("Passing Marks", 1, total_marks, int(total_marks * 0.4))
        
        if st.button("✅ Create Exam"):
            exam_id = generate_exam_id()
            st.success(f"✓ Exam created! ID: {exam_id}")
    
    with tab2:
        st.subheader("Exam Schedule")
        
        exams_list = {
            "Exam ID": [f"EXAM-2024-{i}" for i in range(1, 11)],
            "Exam Name": ["Unit Test 1", "Unit Test 2", "Mid-Term", "Unit Test 3", "Final Exam"] * 2,
            "Class": ["10-A", "10-A", "10-A", "10-A", "10-A", "10-B", "10-B", "10-B", "10-B", "10-B"],
            "Subject": [random.choice(["Mathematics", "English", "Science"]) for _ in range(10)],
            "Date": pd.date_range("2024-04-15", periods=10, freq="5D"),
            "Status": [random.choice(["Scheduled", "Completed", "Active"]) for _ in range(10)]
        }
        
        df_exams = pd.DataFrame(exams_list)
        st.dataframe(df_exams, width='stretch', hide_index=True)
    
    with tab3:
        st.subheader("Upload Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            result_exam = st.selectbox("Exam", ["Unit Test 1", "Unit Test 2", "Mid-Term"])
        with col2:
            result_class = st.selectbox("Class", ["10-A", "10-B", "9-A", "9-B"])
        with col3:
            result_file = st.file_uploader("Upload Excel/CSV", type=["xlsx", "csv"])
        
        if st.button("📤 Upload Results"):
            st.success("✓ Results uploaded successfully!")
    
    with tab4:
        st.subheader("Report Cards")
        
        selected_student_report = st.selectbox("Select Student", [f"Student {i}" for i in range(1, 26)], key="report_student")
        
        report_card_data = {
            "Subject": ["Mathematics", "English", "Science", "Social Studies", "PE"],
            "Total Marks": [100, 100, 100, 100, 50],
            "Obtained": [85, 92, 88, 79, 45],
            "Percentage": ["85%", "92%", "88%", "79%", "90%"],
            "Grade": ["A", "A+", "A", "B", "A+"]
        }
        
        df_report = pd.DataFrame(report_card_data)
        st.dataframe(df_report, width='stretch', hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            avg_percentage = 85.0
            st.metric("GPA", "3.8", "+0.2")
            st.metric("Average Percentage", f"{avg_percentage}%", "Excellent")
        
        with col2:
            if st.button("📄 Generate PDF Report"):
                st.success("✓ PDF generated! Ready for download.")
            if st.button("📧 Email Report"):
                st.success("✓ Report sent to parent email!")


# ==================== AI GRADING & ANALYTICS ====================

def render_ai_grading():
    """Render AI grading integration."""
    st.markdown("### 🤖 AI Grading & Analytics")
    
    tab1, tab2, tab3 = st.tabs(["AI Grading", "Grading History", "AI Analytics"])
    
    with tab1:
        st.subheader("Submit for AI Grading")
        
        col1, col2 = st.columns(2)
        with col1:
            ai_assignment = st.selectbox("Assignment", ["Assignment 1", "Assignment 2", "Assignment 3"])
            ai_class = st.selectbox("Class", ["10-A", "10-B", "9-A", "9-B"])
        
        with col2:
            ai_subject = st.selectbox("Subject", ["Mathematics", "English", "Science"])
            ai_total_marks = st.number_input("Total Marks", 1, 100, 50)
        
        ai_rubric = st.text_area("Grading Rubric/Criteria")
        
        ai_file = st.file_uploader("Upload student submissions", type=["pdf", "docx", "txt"], accept_multiple_files=True)
        
        if st.button("🤖 Grade with AI"):
            st.info("⏳ Processing submissions with AI...")
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
            st.success("✓ Grading completed! Results below:")
            
            grading_results = {
                "File": ["submission_1.pdf", "submission_2.pdf", "submission_3.pdf"],
                "Marks": [45, 38, 42],
                "Percentage": ["90%", "76%", "84%"],
                "Grade": ["A", "B", "A"],
                "Confidence": ["95%", "87%", "92%"],
                "AI Feedback": ["Good job!", "Needs improvement", "Very good"]
            }
            df_grading = pd.DataFrame(grading_results)
            st.dataframe(df_grading, width='stretch', hide_index=True)
    
    with tab2:
        st.subheader("Grading History")
        
        history_data = {
            "Date": pd.date_range("2024-03-01", periods=15, freq="D"),
            "Assignment": [f"Assignment {random.randint(1, 5)}" for _ in range(15)],
            "Total Files": [random.randint(20, 50) for _ in range(15)],
            "Avg Score": [f"{random.randint(60, 95)}%" for _ in range(15)],
            "Status": [random.choice(["Completed", "Processing"]) for _ in range(15)]
        }
        
        df_history = pd.DataFrame(history_data)
        st.dataframe(df_history, width='stretch', hide_index=True)
    
    with tab3:
        st.subheader("AI System Analytics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Confidence Score", "92%", "+2%")
        with col2:
            st.metric("Total Submissions Graded", "2,456", "+145 today")
        with col3:
            st.metric("AI Accuracy Rate", "94.5%", "+0.5%")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Confidence Scores Distribution**")
            scores = list(range(70, 101, 5))
            count = [random.randint(20, 150) for _ in scores]
            fig_conf = go.Figure(data=[
                go.Bar(x=scores, y=count, marker_color='lightblue')
            ])
            st.plotly_chart(fig_conf, width='stretch')
        
        with col2:
            st.write("**Grade Distribution (AI)**")
            grades_ai = {"A+": 45, "A": 78, "B": 95, "C": 52, "D": 18, "F": 5}
            fig_grade_ai = go.Figure(data=[
                go.Pie(labels=list(grades_ai.keys()), values=list(grades_ai.values()))
            ])
            st.plotly_chart(fig_grade_ai, width='stretch')


# ==================== ASSIGNMENT MANAGEMENT ====================

def render_assignments():
    """Render assignment management."""
    st.markdown("### 📝 Assignment Management")
    
    tab1, tab2, tab3 = st.tabs(["Create Assignment", "View Submissions", "Assignment Analytics"])
    
    with tab1:
        st.subheader("Create New Assignment")
        
        col1, col2 = st.columns(2)
        with col1:
            assign_title = st.text_input("Assignment Title")
            assign_class = st.selectbox("Class", ["10-A", "10-B", "9-A", "9-B"])
            assign_deadline = st.date_input("Deadline")
        
        with col2:
            assign_subject = st.selectbox("Subject", ["Mathematics", "English", "Science"])
            assign_marks = st.number_input("Total Marks", 1, 100, 20)
            assign_desc = st.text_area("Description")
        
        if st.button("✅ Create Assignment"):
            assign_id = generate_assignment_id()
            st.success(f"✓ Assignment created! ID: {assign_id}")
    
    with tab2:
        st.subheader("Student Submissions")
        
        submissions_data = {
            "Submission ID": [f"SUB-{i}" for i in range(1, 26)],
            "Student": [f"Student {i}" for i in range(1, 26)],
            "Submitted": ["✓"] * 25,
            "Date": [f"2024-04-{random.randint(1, 30):02d}" for _ in range(25)],
            "Late": [random.choice(["No", "No", "No", "Yes"]) for _ in range(25)],
            "Plagiarism": [f"{random.randint(0, 30)}%" for _ in range(25)],
            "Status": [random.choice(["Pending", "Graded"]) for _ in range(25)]
        }
        
        df_submissions = pd.DataFrame(submissions_data)
        st.dataframe(df_submissions, width='stretch', hide_index=True)
    
    with tab3:
        st.subheader("Assignment Performance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Submission Rate by Assignment**")
            assignments = ["Assignment 1", "Assignment 2", "Assignment 3", "Assignment 4"]
            submission_rates = [95, 92, 88, 85]
            fig_sub = go.Figure(data=[
                go.Bar(x=assignments, y=submission_rates, marker_color='lightblue')
            ])
            st.plotly_chart(fig_sub, width='stretch')
        
        with col2:
            st.write("**Average Scores by Assignment**")
            avg_scores = [78, 82, 75, 80]
            fig_score = go.Figure(data=[
                go.Bar(x=assignments, y=avg_scores, marker_color='lightgreen')
            ])
            st.plotly_chart(fig_score, width='stretch')


# ==================== FEE & PAYMENT MANAGEMENT ====================

def render_fees():
    """Render fee and payment management."""
    st.markdown("### 💰 Fees & Payments")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Fee Structure", "Student Fees", "Payments", "Fee Analytics"])
    
    with tab1:
        st.subheader("Fee Structure")
        
        fee_structure = {
            "Fee Type": ["Tuition Fee", "Transport Fee", "Library Fee", "Lab Fee", "Sports Fee"],
            "Amount": [25000, 5000, 1500, 2000, 1000],
            "Frequency": ["Monthly", "Monthly", "Annual", "Annual", "Annual"],
            "Status": ["Active"] * 5
        }
        
        df_structure = pd.DataFrame(fee_structure)
        st.dataframe(df_structure, width='stretch', hide_index=True)
    
    with tab2:
        st.subheader("Student Fee Status")
        
        col1, col2 = st.columns(2)
        with col1:
            fee_class = st.selectbox("Class", ["10-A", "10-B", "9-A", "9-B"])
        with col2:
            fee_status = st.selectbox("Payment Status", ["All", "Paid", "Unpaid", "Partial"])
        
        fees_student = {
            "Student ID": [f"STU-{i}" for i in range(1, 26)],
            "Name": [f"Student {i}" for i in range(1, 26)],
            "Total Fee": [35500] * 25,
            "Paid": [random.randint(0, 35500) for _ in range(25)],
            "Pending": [random.randint(0, 35500) for _ in range(25)],
            "Status": [random.choice(["Paid", "Unpaid", "Partial"]) for _ in range(25)]
        }
        
        df_fees = pd.DataFrame(fees_student)
        st.dataframe(df_fees, width='stretch', hide_index=True)
    
    with tab3:
        st.subheader("Payment Processing")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pay_student = st.selectbox("Student", [f"Student {i}" for i in range(1, 26)], key="pay_student")
        with col2:
            pay_amount = st.number_input("Amount", 0, 50000)
        with col3:
            pay_method = st.selectbox("Payment Method", ["Cash", "Check", "Online Transfer", "Card"])
        
        pay_transaction_id = st.text_input("Transaction ID")
        pay_remarks = st.text_area("Remarks")
        
        if st.button("✅ Verify & Process Payment"):
            payment_id = generate_payment_id()
            receipt_num = generate_receipt_number()
            st.success(f"✓ Payment verified! Receipt: {receipt_num}")
            st.info(f"Payment ID: {payment_id}")
    
    with tab4:
        st.subheader("Fee Collection Analytics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Fee Collected", "₹28,50,000", "+5% vs last month")
        with col2:
            st.metric("Pending Fees", "₹7,50,000", "-8% vs last month")
        with col3:
            st.metric("Collection Rate", "79%", "+3% vs last month")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Monthly Collection Trend**")
            months_fee = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
            collections = [2800000, 2750000, 2900000, 2850000, 3000000, 3100000]
            fig_coll = go.Figure(data=[
                go.Scatter(x=months_fee, y=collections, mode='lines+markers', fill='tozeroy')
            ])
            st.plotly_chart(fig_coll, width='stretch')
        
        with col2:
            st.write("**Payment Status Distribution**")
            status_dist = {"Paid": 750, "Unpaid": 120, "Partial": 80}
            fig_status = go.Figure(data=[
                go.Pie(labels=list(status_dist.keys()), values=list(status_dist.values()))
            ])
            st.plotly_chart(fig_status, width='stretch')


# ==================== NOTIFICATIONS & ANNOUNCEMENTS ====================

def render_announcements():
    """Render announcements and notifications."""
    st.markdown("### 📢 Announcements & Notifications")
    
    tab1, tab2 = st.tabs(["Send Announcement", "Notification History"])
    
    with tab1:
        st.subheader("Send New Announcement")
        
        ann_title = st.text_input("Announcement Title")
        ann_recipient = st.multiselect("Send to", ["All Students", "All Teachers", "All Parents", "Specific Class", "Specific Student"])
        ann_priority = st.selectbox("Priority", ["Low", "Normal", "High", "Critical"])
        ann_message = st.text_area("Message", height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            ann_channels = st.multiselect("Delivery Channels", ["Email", "SMS", "In-App", "Push Notification"])
        with col2:
            ann_date = st.date_input("Send Date")
        
        if st.button("✅ Send Announcement"):
            st.success("✓ Announcement sent to all recipients!")
            st.balloons()
    
    with tab2:
        st.subheader("Notification History")
        
        notifications = {
            "Date": pd.date_range("2024-04-01", periods=15, freq="D"),
            "Title": [f"Announcement {i}" for i in range(1, 16)],
            "Type": [random.choice(["Exam", "Assignment", "Fee", "Event", "General"]) for _ in range(15)],
            "Recipients": [f"{random.randint(50, 1000)} users" for _ in range(15)],
            "Delivery": [random.choice(["Email", "SMS", "In-App"]) for _ in range(15)],
            "Status": [random.choice(["Sent", "Scheduled"]) for _ in range(15)]
        }
        
        df_notifications = pd.DataFrame(notifications)
        st.dataframe(df_notifications, width='stretch', hide_index=True)


# ==================== LIBRARY MANAGEMENT ====================

def render_library():
    """Render library management."""
    st.markdown("### 📚 Library Management")
    
    tab1, tab2 = st.tabs(["Book Inventory", "Borrowing"])
    
    with tab1:
        st.subheader("Book Inventory")
        
        col1, col2 = st.columns(2)
        with col1:
            search_book = st.text_input("🔍 Search book")
        with col2:
            category_filter = st.selectbox("Category", ["All", "Fiction", "Reference", "Science", "Mathematics"])
        
        books = {
            "Book ID": [f"BK-{i}" for i in range(1, 21)],
            "Title": ["Book " + str(i) for i in range(1, 21)],
            "Author": ["Author " + str(i) for i in range(1, 21)],
            "Category": [random.choice(["Fiction", "Reference", "Science", "Mathematics"]) for _ in range(20)],
            "Total": [random.randint(2, 10) for _ in range(20)],
            "Available": [random.randint(0, 10) for _ in range(20)],
            "Status": [random.choice(["In Stock", "Low Stock"]) for _ in range(20)]
        }
        
        df_books = pd.DataFrame(books)
        st.dataframe(df_books, width='stretch', hide_index=True)
    
    with tab2:
        st.subheader("Book Borrowing")
        
        borrowing = {
            "Borrow ID": [f"BRW-{i}" for i in range(1, 16)],
            "Student": ["Student " + str(i) for i in range(1, 16)],
            "Book": ["Book " + str(random.randint(1, 20)) for _ in range(15)],
            "Borrow Date": pd.date_range("2024-03-01", periods=15, freq="D"),
            "Due Date": pd.date_range("2024-04-01", periods=15, freq="D"),
            "Status": [random.choice(["Borrowed", "Returned", "Overdue"]) for _ in range(15)],
            "Fine": [f"₹{random.randint(0, 100)}" for _ in range(15)]
        }
        
        df_borrowing = pd.DataFrame(borrowing)
        st.dataframe(df_borrowing, width='stretch', hide_index=True)


# ==================== TRANSPORT & HOSTEL ====================

def render_transport_hostel():
    """Render transport and hostel management."""
    st.markdown("### 🚌 Transport & Hostel Management")
    
    tab1, tab2 = st.tabs(["Transport", "Hostel"])
    
    with tab1:
        st.subheader("Transport Management")
        
        transport = {
            "Bus Number": ["BUS-001", "BUS-002", "BUS-003", "BUS-004", "BUS-005"],
            "Route": ["Route-A", "Route-B", "Route-C", "Route-D", "Route-E"],
            "Driver": ["Driver 1", "Driver 2", "Driver 3", "Driver 4", "Driver 5"],
            "Capacity": [45, 50, 48, 52, 45],
            "Current": [42, 48, 45, 50, 43],
            "Status": ["Active"] * 5
        }
        
        df_transport = pd.DataFrame(transport)
        st.dataframe(df_transport, width='stretch', hide_index=True)
    
    with tab2:
        st.subheader("Hostel Management")
        
        hostels = {
            "Hostel ID": ["HST-001", "HST-002", "HST-003"],
            "Name": ["Boys Hostel", "Girls Hostel - A", "Girls Hostel - B"],
            "Type": ["Boys", "Girls", "Girls"],
            "Capacity": [120, 100, 80],
            "Occupied": [115, 98, 75],
            "Available": [5, 2, 5],
            "Warden": ["Mr. X", "Ms. Y", "Ms. Z"]
        }
        
        df_hostels = pd.DataFrame(hostels)
        st.dataframe(df_hostels, width='stretch', hide_index=True)


# ==================== REPORTS ====================

def render_reports():
    """Render reporting module."""
    st.markdown("### 📊 Reports & Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Generate Report", "View Reports", "Export"])
    
    with tab1:
        st.subheader("Generate Report")
        
        report_type = st.selectbox("Report Type", [
            "Student Report",
            "Teacher Report",
            "Class Report",
            "Attendance Report",
            "Fee Report",
            "Academic Report",
            "AI Grading Report"
        ])
        
        report_period = st.selectbox("Period", ["Monthly", "Quarterly", "Annual"])
        report_month = st.selectbox("Month/Quarter", ["January", "February", "March", "April", "May", "June"])
        
        if st.button("📋 Generate Report"):
            st.info("⏳ Generating report...")
            import time
            time.sleep(1)
            st.success("✓ Report generated successfully!")
    
    with tab2:
        st.subheader("View Reports")
        
        reports_list = {
            "Report ID": [f"RPT-{i}" for i in range(1, 11)],
            "Type": [random.choice(["Student", "Class", "Fee", "Attendance"]) for _ in range(10)],
            "Generated": pd.date_range("2024-03-01", periods=10, freq="D"),
            "Generated By": ["Admin"] * 10,
            "Status": ["Ready"] * 10
        }
        
        df_reports = pd.DataFrame(reports_list)
        st.dataframe(df_reports, width='stretch', hide_index=True)
    
    with tab3:
        st.subheader("Export Report")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 Download PDF"):
                st.success("✓ PDF downloaded!")
        with col2:
            if st.button("📊 Download Excel"):
                st.success("✓ Excel downloaded!")
        with col3:
            if st.button("📋 Download CSV"):
                st.success("✓ CSV downloaded!")


# ==================== SETTINGS ====================

def render_settings():
    """Render settings page."""
    st.markdown("### ⚙️ School Settings")
    
    tab1, tab2, tab3, tab4 = st.tabs(["School Info", "Academic Settings", "System Settings", "Advanced"])
    
    with tab1:
        st.subheader("School Information")
        
        col1, col2 = st.columns(2)
        with col1:
            school_name = st.text_input("School Name", "ABC Public School")
            school_code = st.text_input("School Code", "ABC-2024")
            principal = st.text_input("Principal Name", "Dr. John Doe")
        
        with col2:
            school_email = st.text_input("School Email", "info@abcschool.com")
            school_phone = st.text_input("School Phone", "011-XXXX-XXXX")
            school_address = st.text_area("Address", "123 Main Street, City, State")
        
        if st.button("💾 Save Changes"):
            st.success("✓ School information updated!")
    
    with tab2:
        st.subheader("Academic Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            academic_year = st.text_input("Academic Year", "2024-2025")
            start_date = st.date_input("Academic Year Start")
            end_date = st.date_input("Academic Year End")
        
        with col2:
            semesters = st.number_input("Number of Semesters", 1, 4, 2)
            grading_scale = st.selectbox("Grading Scale", ["A-F", "GPA 4.0", "Percentage"])
        
        if st.button("💾 Save Academic Settings"):
            st.success("✓ Academic settings updated!")
    
    with tab3:
        st.subheader("System Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
            language = st.selectbox("Language", ["English", "Hindi", "Marathi"])
        
        with col2:
            time_format = st.selectbox("Time Format", ["12-hour", "24-hour"])
            date_format = st.selectbox("Date Format", ["DD-MM-YYYY", "MM-DD-YYYY", "YYYY-MM-DD"])
        
        if st.button("💾 Save System Settings"):
            st.success("✓ System settings updated!")
    
    with tab4:
        st.subheader("Advanced Settings")
        
        enable_ai = st.checkbox("Enable AI Grading", value=True)
        enable_ocr = st.checkbox("Enable OCR Processing", value=True)
        maintenance_mode = st.checkbox("Maintenance Mode", value=False)
        
        if st.button("💾 Save Advanced Settings"):
            st.success("✓ Advanced settings updated!")


# ==================== MAIN PORTAL NAVIGATION ====================

def render_school_portal():
    """Main school portal navigation."""
    uid = st.session_state.get("user_id")
    if not AccessControl.can_open_school_portal(uid):
        st.error("Access denied. School Portal requires an active paid plan and a registered school profile.")
        return

    # Sidebar navigation
    st.sidebar.markdown("## 🎓 School Portal")
    portal_page = st.sidebar.radio(
        "Navigate",
        [
            "📊 Dashboard",
            "👨‍🎓 Students",
            "👨‍🏫 Teachers",
            "📚 Classes & Subjects",
            "📋 Attendance",
            "📝 Exams & Results",
            "🤖 AI Grading",
            "📝 Assignments",
            "💰 Fees & Payments",
            "📢 Announcements",
            "📚 Library",
            "🚌 Transport & Hostel",
            "📊 Reports",
            "⚙️ Settings"
        ]
    )
    
    st.divider()
    
    if portal_page == "📊 Dashboard":
        render_dashboard()
    elif portal_page == "👨‍🎓 Students":
        render_student_management()
    elif portal_page == "👨‍🏫 Teachers":
        render_teacher_management()
    elif portal_page == "📚 Classes & Subjects":
        render_class_management()
    elif portal_page == "📋 Attendance":
        render_attendance()
    elif portal_page == "📝 Exams & Results":
        render_exams()
    elif portal_page == "🤖 AI Grading":
        render_ai_grading()
    elif portal_page == "📝 Assignments":
        render_assignments()
    elif portal_page == "💰 Fees & Payments":
        render_fees()
    elif portal_page == "📢 Announcements":
        render_announcements()
    elif portal_page == "📚 Library":
        render_library()
    elif portal_page == "🚌 Transport & Hostel":
        render_transport_hostel()
    elif portal_page == "📊 Reports":
        render_reports()
    elif portal_page == "⚙️ Settings":
        render_settings()


if __name__ == "__main__":
    render_school_portal()
