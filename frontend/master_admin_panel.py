"""
=============================================================================
MASTER ADMIN PANEL - Enterprise-Level Dashboard
=============================================================================

A comprehensive command center for governing and controlling the entire
AI-powered School Portal and AI Grading System.

Features:
- Global System Overview with KPIs
- Website Activity Monitoring
- User Access Control
- AI System Monitoring
- Smart Payment Governance System
- Website Maintenance Control
- Security Center
- Advanced Analytics
- Broadcast Center
- Role & Permission Management
- System Settings

Author: Abdul's School Portal Team
Version: 1.0.0
=============================================================================
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from school_saas_hub_ui import render_saas_master_admin_tab
from legacy_pages.admin_payment_verification import render_admin_payment_dashboard_embedded
from typing import Dict, List, Any, Optional
import random
from enum import Enum


# ============================================================================
# ENUM DEFINITIONS
# ============================================================================

class PaymentStatus(Enum):
    """Payment status enumeration."""
    PENDING = "Pending"
    VERIFIED = "Verified"
    REJECTED = "Rejected"
    REFUNDED = "Refunded"
    PARTIAL_PAID = "Partial Paid"


class UserRole(Enum):
    """User role enumeration."""
    SUPER_ADMIN = "Super Admin"
    ADMIN = "Admin"
    TEACHER = "Teacher"
    STUDENT = "Student"
    PARENT = "Parent"


class ActivityType(Enum):
    """Activity type enumeration."""
    LOGIN = "Login"
    LOGOUT = "Logout"
    FILE_UPLOAD = "File Upload"
    GRADING = "Grading"
    ASSIGNMENT_SUBMIT = "Assignment Submit"
    EXAM_SUBMIT = "Exam Submit"
    PAYMENT = "Payment"
    SETTINGS_CHANGE = "Settings Change"


# ============================================================================
# DATA MODELS & SAMPLE DATA GENERATORS
# ============================================================================

class SampleDataGenerator:
    """Generate realistic sample data for the admin panel."""

    @staticmethod
    def generate_kpi_data() -> Dict[str, Any]:
        """Generate KPI statistics."""
        return {
            "total_students": 4250,
            "total_teachers": 142,
            "active_users": 1847,
            "assignments_submitted": 12456,
            "ai_grading_requests": 8934,
            "total_revenue": 284500,
            "pending_payments": 45200,
            "system_health": 98.5,
        }

    @staticmethod
    def generate_activity_logs(count: int = 15) -> pd.DataFrame:
        """Generate recent activity logs."""
        activities = []
        for i in range(count):
            timestamp = datetime.now() - timedelta(minutes=random.randint(1, 1440))
            activity_type = random.choice(list(ActivityType))
            
            activities.append({
                "timestamp": timestamp,
                "user": f"user_{random.randint(1000, 9999)}",
                "role": random.choice(["Student", "Teacher", "Admin"]),
                "activity": activity_type.value,
                "status": random.choice(["Success", "Pending", "Failed"]),
                "details": f"Activity {i+1} details",
            })
        
        df = pd.DataFrame(activities)
        df = df.sort_values("timestamp", ascending=False)
        return df

    @staticmethod
    def generate_users_data(count: int = 20) -> pd.DataFrame:
        """Generate user list for management."""
        users = []
        roles = ["Student", "Teacher", "Admin"]
        statuses = ["Active", "Inactive", "Suspended", "Pending"]
        
        for i in range(count):
            users.append({
                "user_id": f"USR{1000+i}",
                "name": f"User {i+1}",
                "email": f"user{i+1}@school.edu",
                "role": random.choice(roles),
                "status": random.choice(statuses),
                "last_login": datetime.now() - timedelta(days=random.randint(0, 30)),
                "join_date": datetime.now() - timedelta(days=random.randint(30, 365)),
            })
        
        return pd.DataFrame(users)

    @staticmethod
    def generate_ai_metrics() -> Dict[str, Any]:
        """Generate AI system metrics."""
        return {
            "grading_accuracy": 94.7,
            "ocr_success_rate": 91.2,
            "failed_requests": 156,
            "avg_grading_time": 4.3,  # seconds
            "avg_confidence_score": 88.5,
            "total_processed": 8934,
        }

    @staticmethod
    def generate_payment_transactions(count: int = 20) -> pd.DataFrame:
        """Generate payment transaction data."""
        transactions = []
        methods = ["Credit Card", "Debit Card", "Bank Transfer", "Online Wallet"]
        statuses = [
            PaymentStatus.PENDING.value,
            PaymentStatus.VERIFIED.value,
            PaymentStatus.REJECTED.value,
            PaymentStatus.REFUNDED.value,
            PaymentStatus.PARTIAL_PAID.value,
        ]
        
        for i in range(count):
            amount = random.uniform(500, 5000)
            transactions.append({
                "transaction_id": f"TXN{datetime.now().strftime('%Y%m%d')}{1000+i}",
                "student_id": f"STU{1000+i}",
                "student_name": f"Student {i+1}",
                "amount": amount,
                "method": random.choice(methods),
                "status": random.choice(statuses),
                "date": datetime.now() - timedelta(days=random.randint(0, 60)),
                "verified_by": "admin_001" if random.random() > 0.3 else None,
            })
        
        df = pd.DataFrame(transactions)
        return df.sort_values("date", ascending=False)

    @staticmethod
    def generate_security_alerts(count: int = 10) -> pd.DataFrame:
        """Generate security alerts."""
        alerts = []
        alert_types = [
            "Failed Login Attempt",
            "Multiple Device Login",
            "Unusual Activity",
            "IP Address Change",
            "Permission Violation",
            "File Download Attempt",
        ]
        
        for i in range(count):
            alerts.append({
                "alert_id": f"ALR{1000+i}",
                "type": random.choice(alert_types),
                "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                "user": f"user_{random.randint(1000, 9999)}",
                "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "timestamp": datetime.now() - timedelta(hours=random.randint(1, 72)),
                "status": random.choice(["New", "Investigating", "Resolved"]),
            })
        
        return pd.DataFrame(alerts)

    @staticmethod
    def generate_analytics_data() -> Dict[str, pd.DataFrame]:
        """Generate analytics data for charts."""
        days = 30
        dates = [datetime.now() - timedelta(days=x) for x in range(days)]
        
        return {
            "daily_traffic": pd.DataFrame({
                "date": dates,
                "students": [random.randint(200, 800) for _ in range(days)],
                "teachers": [random.randint(30, 150) for _ in range(days)],
                "admins": [random.randint(5, 25) for _ in range(days)],
            }),
            "revenue_data": pd.DataFrame({
                "date": dates,
                "amount": [random.uniform(5000, 25000) for _ in range(days)],
            }),
            "ai_usage": pd.DataFrame({
                "date": dates,
                "grading_requests": [random.randint(100, 500) for _ in range(days)],
                "ocr_requests": [random.randint(50, 300) for _ in range(days)],
            }),
        }


# ============================================================================
# UTILITY FUNCTIONS & HELPERS
# ============================================================================

def initialize_admin_session_state():
    """Initialize session state variables for admin panel."""
    defaults = {
        "admin_current_tab": "Overview",
        "admin_payment_filter": "All",
        "admin_user_search": "",
        "admin_show_maintenance_warning": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"${amount:,.2f}"


def get_trend_indicator(current: float, previous: float) -> tuple:
    """Get trend indicator and percentage change."""
    if previous == 0:
        change_pct = 100 if current > 0 else 0
        trend = "📈" if current > 0 else "📉"
    else:
        change_pct = ((current - previous) / previous) * 100
        trend = "📈" if change_pct > 0 else "📉" if change_pct < 0 else "➡️"
    
    return trend, abs(change_pct)


def get_status_badge_color(status: str) -> str:
    """Get color for status badge."""
    status_colors = {
        "Active": "🟢",
        "Inactive": "🔵",
        "Suspended": "🔴",
        "Pending": "🟡",
        "Verified": "🟢",
        "Rejected": "🔴",
        "Refunded": "🔵",
        "Success": "🟢",
        "Failed": "🔴",
    }
    return status_colors.get(status, "⚪")


def display_metric_card(title: str, value: Any, subtitle: str = "", 
                       trend: Optional[str] = None, trend_pct: float = 0):
    """Display a professional metric card."""
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"### {title}")
            st.markdown(f"## {value}")
            if subtitle:
                st.caption(subtitle)
        
        with col2:
            if trend:
                st.markdown(f"### {trend}")
                if trend_pct > 0:
                    st.caption(f"+{trend_pct:.1f}%")
                elif trend_pct < 0:
                    st.caption(f"{trend_pct:.1f}%")


# ============================================================================
# PAGE SECTIONS - 1. GLOBAL SYSTEM OVERVIEW
# ============================================================================

def render_global_overview():
    """Render the global system overview with KPI cards."""
    st.header("🎯 Global System Overview")
    
    data = SampleDataGenerator.generate_kpi_data()
    
    # Row 1: Key Statistics
    st.subheader("Key Performance Indicators")
    cols = st.columns(4)
    
    with cols[0]:
        display_metric_card(
            "Total Students",
            f"{data['total_students']:,}",
            "Registered accounts",
            "📈", 5.2
        )
    
    with cols[1]:
        display_metric_card(
            "Total Teachers",
            f"{data['total_teachers']}",
            "Active instructors",
            "📈", 2.1
        )
    
    with cols[2]:
        display_metric_card(
            "Active Users",
            f"{data['active_users']:,}",
            "Online now",
            "📈", 8.3
        )
    
    with cols[3]:
        display_metric_card(
            "System Health",
            f"{data['system_health']:.1f}%",
            "Status: Excellent",
            "🟢", 0
        )
    
    # Row 2: More Statistics
    cols = st.columns(4)
    
    with cols[0]:
        display_metric_card(
            "Assignments",
            f"{data['assignments_submitted']:,}",
            "This semester",
            "📈", 12.5
        )
    
    with cols[1]:
        display_metric_card(
            "AI Gradings",
            f"{data['ai_grading_requests']:,}",
            "Processed",
            "📈", 15.3
        )
    
    with cols[2]:
        display_metric_card(
            "Total Revenue",
            format_currency(data['total_revenue']),
            "Current session",
            "📈", 22.1
        )
    
    with cols[3]:
        display_metric_card(
            "Pending Payments",
            format_currency(data['pending_payments']),
            "Outstanding",
            "📉", -8.5
        )


# ============================================================================
# PAGE SECTIONS - 2. WEBSITE ACTIVITY MONITOR
# ============================================================================

def render_activity_monitor():
    """Render the website activity monitoring section."""
    st.header("📊 Website Activity Monitor")
    
    # Activity statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Today's Logins", 342, "+15")
    with col2:
        st.metric("Active Sessions", 187, "-8")
    with col3:
        st.metric("Files Uploaded", 89, "+23")
    with col4:
        st.metric("Exams Submitted", 56, "+5")
    
    st.divider()
    
    # Activity logs table
    st.subheader("Recent Activity Logs")
    activity_logs = SampleDataGenerator.generate_activity_logs(20)
    
    # Format for display
    display_logs = activity_logs.copy()
    display_logs["timestamp"] = display_logs["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
    display_logs["status_badge"] = display_logs["status"].apply(get_status_badge_color)
    display_logs["display"] = (
        display_logs["status_badge"] + " " + 
        display_logs["user"] + " - " + 
        display_logs["activity"] + " (" + 
        display_logs["role"] + ")"
    )
    
    st.dataframe(
        display_logs[["timestamp", "display", "status"]],
        hide_index=True,
        use_container_width=True,
        column_config={
            "timestamp": st.column_config.TextColumn("Time"),
            "display": st.column_config.TextColumn("Activity"),
            "status": st.column_config.TextColumn("Status"),
        }
    )


# ============================================================================
# PAGE SECTIONS - 3. USER ACCESS CONTROL
# ============================================================================

def render_user_access_control():
    """Render user access control and management section."""
    st.header("👥 User Access Control")
    
    # Filter options
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        search_term = st.text_input("🔍 Search users by name/email", placeholder="Enter name or email...")
    with col2:
        role_filter = st.selectbox("Filter by role", ["All", "Student", "Teacher", "Admin"])
    with col3:
        status_filter = st.selectbox("Filter by status", ["All", "Active", "Inactive", "Suspended", "Pending"])
    
    st.divider()
    
    # Generate user data
    users_df = SampleDataGenerator.generate_users_data(25)
    
    # Apply filters
    if search_term:
        users_df = users_df[
            users_df["name"].str.contains(search_term, case=False, na=False) |
            users_df["email"].str.contains(search_term, case=False, na=False)
        ]
    
    if role_filter != "All":
        users_df = users_df[users_df["role"] == role_filter]
    
    if status_filter != "All":
        users_df = users_df[users_df["status"] == status_filter]
    
    st.subheader(f"Users Found: {len(users_df)}")
    
    # Display users with action buttons
    for idx, user in users_df.iterrows():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 1.5, 1.5, 1.5, 1.5])
        
        with col1:
            st.write(f"**{user['name']}**")
            st.caption(user['email'])
        
        with col2:
            st.write(f"🏷️ {user['role']}")
            st.caption(f"ID: {user['user_id']}")
        
        with col3:
            status_badge = get_status_badge_color(user['status'])
            st.write(f"{status_badge} {user['status']}")
            st.caption(f"Joined: {user['join_date'].strftime('%Y-%m-%d')}")
        
        with col4:
            if st.button("👁️ View", key=f"view_{user['user_id']}", use_container_width=True):
                st.toast(f"Viewing {user['name']}'s details...")
        
        with col5:
            if st.button("🔑 Reset PW", key=f"reset_{user['user_id']}", use_container_width=True):
                st.toast(f"Password reset link sent to {user['email']}")
        
        with col6:
            if user['status'] != 'Suspended':
                if st.button("⛔ Suspend", key=f"suspend_{user['user_id']}", use_container_width=True):
                    st.toast(f"❌ {user['name']} suspended")
            else:
                if st.button("✅ Unsuspend", key=f"unsuspend_{user['user_id']}", use_container_width=True):
                    st.toast(f"✅ {user['name']} unsuspended")
        
        with col7:
            if st.button("🗑️ Delete", key=f"delete_{user['user_id']}", use_container_width=True):
                st.warning(f"⚠️ Are you sure? This will delete {user['name']}")


# ============================================================================
# PAGE SECTIONS - 4. AI SYSTEM MONITORING
# ============================================================================

def render_ai_monitoring():
    """Render AI system monitoring section."""
    st.header("🤖 AI System Monitoring")
    
    metrics = SampleDataGenerator.generate_ai_metrics()
    
    # Performance metrics
    st.subheader("AI Performance Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Grading Accuracy", f"{metrics['grading_accuracy']:.1f}%", "+2.3%")
    with col2:
        st.metric("OCR Success Rate", f"{metrics['ocr_success_rate']:.1f}%", "+1.8%")
    with col3:
        st.metric("Failed Requests", metrics['failed_requests'], "-12")
    with col4:
        st.metric("Avg Time", f"{metrics['avg_grading_time']:.1f}s", "-0.3s")
    with col5:
        st.metric("Confidence Score", f"{metrics['avg_confidence_score']:.1f}%", "+3.2%")
    
    st.divider()
    
    # Progress bars for health indicators
    st.subheader("System Health Indicators")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Grading Engine Health**")
        st.progress(metrics['grading_accuracy'] / 100)
        
        st.write("**OCR Engine Health**")
        st.progress(metrics['ocr_success_rate'] / 100)
    
    with col2:
        st.write("**API Uptime**")
        st.progress(0.987)
        
        st.write("**Model Performance**")
        st.progress(metrics['avg_confidence_score'] / 100)
    
    st.divider()
    
    # AI Actions
    st.subheader("AI System Controls")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Retrain AI Model", use_container_width=True):
            st.info("🔄 AI Model retraining initiated...")
            st.toast("Model retraining started. This may take 2-3 hours.")
    
    with col2:
        if st.button("🔍 Validate AI Output", use_container_width=True):
            st.info("🔍 Running validation tests...")
            st.toast("AI validation completed. 94.7% accuracy confirmed.")
    
    with col3:
        if st.button("📊 View AI Logs", use_container_width=True):
            st.info("📊 Fetching recent AI logs...")
    
    with col4:
        if st.button("⚙️ Configure AI Settings", use_container_width=True):
            st.info("⚙️ Opening AI configuration panel...")


# ============================================================================
# PAGE SECTIONS - 5. PAYMENT GOVERNANCE SYSTEM (MOST IMPORTANT)
# ============================================================================

def render_payment_governance():
    """Render the comprehensive Smart Payment Governance System."""
    st.header("💰 Smart Payment Governance System")
    
    # Create tabs for different payment sections
    payment_tabs = st.tabs([
        "💳 Transactions",
        "📋 Fee Monitoring",
        "📊 Financial Analytics",
        "🎓 Scholarships & Discounts",
        "🔐 Fraud Detection",
        "📄 Receipts & Invoices"
    ])
    
    # ===== TAB 1: PAYMENT VERIFICATION =====
    with payment_tabs[0]:
        st.subheader("Payment Transaction Management")
        
        # Transaction filters
        col1, col2, col3 = st.columns(3)
        with col1:
            trans_status_filter = st.multiselect(
                "Filter by status",
                [s.value for s in PaymentStatus],
                default=[PaymentStatus.PENDING.value]
            )
        with col2:
            trans_method_filter = st.selectbox(
                "Payment method",
                ["All", "Credit Card", "Debit Card", "Bank Transfer", "Online Wallet"]
            )
        with col3:
            trans_date_range = st.date_input(
                "Date range",
                value=(datetime.now() - timedelta(days=30), datetime.now())
            )
        
        # Generate and filter transactions
        transactions_df = SampleDataGenerator.generate_payment_transactions(30)
        
        # Apply filters
        transactions_df = transactions_df[
            transactions_df["status"].isin(trans_status_filter)
        ]
        
        if trans_method_filter != "All":
            transactions_df = transactions_df[transactions_df["method"] == trans_method_filter]
        
        st.subheader(f"Total Transactions: {len(transactions_df)}")
        
        # Display transaction table
        display_trans = transactions_df.copy()
        display_trans["amount"] = display_trans["amount"].apply(format_currency)
        display_trans["date"] = display_trans["date"].dt.strftime("%Y-%m-%d %H:%M")
        display_trans["status_badge"] = display_trans["status"].apply(get_status_badge_color)
        
        st.dataframe(
            display_trans[["transaction_id", "student_name", "amount", "method", "status_badge", "date"]],
            hide_index=True,
            use_container_width=True,
            column_config={
                "transaction_id": st.column_config.TextColumn("Transaction ID", width=120),
                "student_name": st.column_config.TextColumn("Student"),
                "amount": st.column_config.TextColumn("Amount", width=100),
                "method": st.column_config.TextColumn("Method"),
                "status_badge": st.column_config.TextColumn("Status", width=80),
                "date": st.column_config.TextColumn("Date", width=140),
            }
        )
        
        # Transaction action section
        st.divider()
        st.subheader("Verify Pending Transactions")
        
        pending_trans = transactions_df[transactions_df["status"] == PaymentStatus.PENDING.value].head(5)
        if not pending_trans.empty:
            for idx, trans in pending_trans.iterrows():
                with st.container(border=True):
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 1.5, 1.5, 1])
                    
                    with col1:
                        st.write(f"**{trans['transaction_id']}**")
                        st.caption(trans['student_name'])
                    
                    with col2:
                        st.write(f"Amount: {format_currency(trans['amount'])}")
                        st.caption(f"Method: {trans['method']}")
                    
                    with col3:
                        if st.button("✅ Approve", key=f"approve_{trans['transaction_id']}", use_container_width=True):
                            st.success(f"✅ Transaction {trans['transaction_id']} approved!")
                            st.toast("Payment verified successfully")
                    
                    with col4:
                        if st.button("❌ Reject", key=f"reject_{trans['transaction_id']}", use_container_width=True):
                            st.error(f"❌ Transaction {trans['transaction_id']} rejected!")
                            st.toast("Payment rejected")
                    
                    with col5:
                        if st.button("🔍 View", key=f"view_trans_{trans['transaction_id']}", use_container_width=True):
                            st.info(f"Viewing details for {trans['transaction_id']}")
        else:
            st.success("✅ All transactions verified!")
    
    # ===== TAB 2: FEE MONITORING =====
    with payment_tabs[1]:
        st.subheader("Fee Monitoring & Student Dues")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Pending Dues", "$45,200", "-$2,100")
        with col2:
            st.metric("Overdue Students", 67, "+5")
        with col3:
            st.metric("Partial Paid", 123, "-8")
        with col4:
            st.metric("Fully Paid", 3450, "+45")
        
        st.divider()
        
        # Fee status breakdown
        st.subheader("Student Fee Status")
        fee_status_data = {
            "Status": ["Fully Paid", "Partially Paid", "Pending", "Overdue"],
            "Count": [3450, 123, 687, 67],
            "Amount": [
                1_725_000,
                150_000,
                200_000,
                45_200
            ]
        }
        
        fee_df = pd.DataFrame(fee_status_data)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(
                fee_df,
                values="Count",
                names="Status",
                title="Student Distribution by Fee Status",
                color_discrete_map={
                    "Fully Paid": "#00CC96",
                    "Partially Paid": "#FFA15A",
                    "Pending": "#AB63FA",
                    "Overdue": "#EF553B"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                fee_df,
                x="Status",
                y="Amount",
                title="Amount Outstanding by Status",
                color="Status",
                color_discrete_map={
                    "Fully Paid": "#00CC96",
                    "Partially Paid": "#FFA15A",
                    "Pending": "#AB63FA",
                    "Overdue": "#EF553B"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Overdue students list
        st.subheader("⚠️ Overdue Students")
        overdue_data = {
            "student_id": [f"STU{1000+i}" for i in range(10)],
            "name": [f"Student {i+1}" for i in range(10)],
            "due_amount": [random.uniform(500, 5000) for _ in range(10)],
            "days_overdue": [random.randint(5, 120) for _ in range(10)],
        }
        
        overdue_df = pd.DataFrame(overdue_data)
        overdue_df = overdue_df.sort_values("days_overdue", ascending=False)
        
        for idx, student in overdue_df.iterrows():
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                
                with col1:
                    st.write(f"**{student['name']}**")
                    st.caption(student['student_id'])
                
                with col2:
                    st.write(f"Due: {format_currency(student['due_amount'])}")
                    severity = "🔴 Critical" if student['days_overdue'] > 90 else "🟠 Warning"
                    st.caption(f"{severity}")
                
                with col3:
                    st.write(f"Overdue: {student['days_overdue']} days")
                
                with col4:
                    if st.button("📧 Send Reminder", key=f"remind_{student['student_id']}", use_container_width=True):
                        st.toast(f"Reminder sent to {student['name']}")
    
    # ===== TAB 3: FINANCIAL ANALYTICS =====
    with payment_tabs[2]:
        st.subheader("Financial Analytics & Trends")
        
        analytics_data = SampleDataGenerator.generate_analytics_data()
        
        # Revenue chart
        revenue_df = analytics_data['revenue_data'].sort_values('date')
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=revenue_df['date'],
            y=revenue_df['amount'],
            mode='lines+markers',
            name='Daily Revenue',
            line=dict(color='#00CC96', width=3),
            fill='tozeroy',
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
        ))
        fig.update_layout(
            title="Daily Revenue Trend",
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Payment method distribution
        col1, col2 = st.columns(2)
        
        with col1:
            payment_methods = {
                "Credit Card": 45,
                "Debit Card": 25,
                "Bank Transfer": 20,
                "Online Wallet": 10
            }
            fig = px.pie(
                values=list(payment_methods.values()),
                names=list(payment_methods.keys()),
                title="Payment Methods Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Paid vs Unpaid chart
            fee_status = {"Paid": 3450, "Unpaid": 877}
            colors = ["#00CC96", "#EF553B"]
            fig = px.bar(
                x=list(fee_status.keys()),
                y=list(fee_status.values()),
                title="Paid vs Unpaid Fees",
                color=list(fee_status.keys()),
                color_discrete_map={"Paid": colors[0], "Unpaid": colors[1]},
                labels={"x": "Fee Status", "y": "Student Count"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ===== TAB 4: SCHOLARSHIPS & DISCOUNTS =====
    with payment_tabs[3]:
        st.subheader("Scholarship & Discount Management")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Scholarships", 234, "+12")
        with col2:
            st.metric("Active Discounts", 456, "+23")
        with col3:
            st.metric("Total Savings", "$125,400", "+$8,200")
        
        st.divider()
        
        # Scholarship/Discount requests
        st.subheader("📋 Pending Approvals")
        
        approval_data = {
            "type": ["Scholarship", "Discount", "Scholarship", "Discount", "Scholarship"],
            "student": ["Student A", "Student B", "Student C", "Student D", "Student E"],
            "amount": [2500, 500, 3000, 750, 2000],
            "reason": [
                "Merit-based",
                "Financial hardship",
                "Athletics",
                "Financial hardship",
                "Need-based"
            ]
        }
        
        approval_df = pd.DataFrame(approval_data)
        
        for idx, item in approval_df.iterrows():
            with st.container(border=True):
                col1, col2, col3, col4, col5 = st.columns([1.5, 2, 2, 1.5, 1.5])
                
                with col1:
                    badge = "🎓" if item['type'] == "Scholarship" else "💰"
                    st.write(f"{badge} {item['type']}")
                
                with col2:
                    st.write(f"**{item['student']}**")
                    st.caption(item['reason'])
                
                with col3:
                    st.write(f"Amount: {format_currency(item['amount'])}")
                
                with col4:
                    if st.button("✅ Approve", key=f"approve_scholarship_{idx}", use_container_width=True):
                        st.success(f"✅ Approved: {format_currency(item['amount'])}")
                
                with col5:
                    if st.button("❌ Reject", key=f"reject_scholarship_{idx}", use_container_width=True):
                        st.error(f"❌ Rejected")
    
    # ===== TAB 5: FRAUD DETECTION =====
    with payment_tabs[4]:
        st.subheader("🔐 AI Fraud Detection System")
        
        st.info(
            "🤖 Advanced fraud detection using machine learning to identify suspicious patterns, "
            "duplicate transactions, and potential fraudulent activities."
        )
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Fraud Alerts Today", 3, "+1")
        with col2:
            st.metric("Flagged Transactions", 8, "=")
        with col3:
            st.metric("Suspicious IPs", 5, "+2")
        with col4:
            st.metric("System Accuracy", "96.8%", "+0.5%")
        
        st.divider()
        
        # Fraud detection results
        st.subheader("🚨 Recent Fraud Alerts")
        
        fraud_data = {
            "alert_id": ["FRD001", "FRD002", "FRD003", "FRD004", "FRD005"],
            "type": [
                "Duplicate Transaction",
                "Unusual IP Address",
                "Multiple Failed Attempts",
                "Repeated Receipt",
                "High Amount Transaction"
            ],
            "severity": ["🔴 High", "🟠 Medium", "🔴 High", "🟠 Medium", "🟡 Low"],
            "details": [
                "Transaction TXN001 appears twice",
                "Login from new IP: 203.45.67.89",
                "5 failed attempts in 2 minutes",
                "Receipt ID RCP089 submitted 3 times",
                "$4,500 transaction from student account"
            ],
            "status": ["New", "Investigating", "New", "Resolved", "Investigating"]
        }
        
        fraud_df = pd.DataFrame(fraud_data)
        
        for idx, alert in fraud_df.iterrows():
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([1.5, 3, 1.5, 2])
                
                with col1:
                    st.write(f"**{alert['alert_id']}**")
                    st.write(alert['severity'])
                
                with col2:
                    st.write(f"**{alert['type']}**")
                    st.caption(alert['details'])
                
                with col3:
                    status_badge = "🔴" if alert['status'] == "New" else "🟡" if alert['status'] == "Investigating" else "🟢"
                    st.write(f"{status_badge} {alert['status']}")
                
                with col4:
                    if alert['status'] != 'Resolved':
                        if st.button("🔍 Investigate", key=f"investigate_{alert['alert_id']}", use_container_width=True):
                            st.toast(f"Investigating {alert['alert_id']}...")
    
    # ===== TAB 6: RECEIPTS & INVOICES =====
    with payment_tabs[5]:
        st.subheader("📄 Receipt & Invoice Management")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Receipts Issued", 3847, "+120")
        with col2:
            st.metric("Pending Invoices", 234, "-15")
        
        st.divider()
        
        st.subheader("Generate Receipt/Invoice")
        
        col1, col2 = st.columns(2)
        with col1:
            receipt_student = st.selectbox(
                "Select student",
                [f"Student {i}" for i in range(1, 11)],
                key="receipt_student"
            )
            receipt_amount = st.number_input("Amount ($)", min_value=0.0, step=100.0)
        
        with col2:
            receipt_type = st.selectbox("Receipt Type", ["Payment Receipt", "Invoice", "Fee Statement"])
            receipt_date = st.date_input("Date")
        
        if st.button("🖨️ Generate & Download Receipt", use_container_width=True):
            st.success(f"✅ Receipt generated for {receipt_student}")
            st.toast("Receipt downloaded successfully")
            
            # Show preview
            with st.expander("📋 Receipt Preview"):
                st.write(f"**Receipt ID:** RCP{datetime.now().strftime('%Y%m%d%H%M%S')}")
                st.write(f"**Student:** {receipt_student}")
                st.write(f"**Amount:** {format_currency(receipt_amount)}")
                st.write(f"**Date:** {receipt_date}")
                st.write(f"**Type:** {receipt_type}")


# ============================================================================
# PAGE SECTIONS - 6. WEBSITE MAINTENANCE
# ============================================================================

def render_maintenance_control():
    """Render website maintenance control section."""
    st.header("🔧 Website Maintenance Control")
    
    # Maintenance status
    st.subheader("Current System Status")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("System Uptime", "99.87%", "📈")
    with col2:
        st.metric("Database Status", "✅ Healthy", "🟢")
    with col3:
        st.metric("API Health", "✅ Operational", "🟢")
    with col4:
        st.metric("Last Backup", "2 hours ago", "⏰")
    
    st.divider()
    
    # Maintenance tools
    st.subheader("Maintenance Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.write("### 🛠️ System Maintenance")
            
            if st.checkbox("Enable Maintenance Mode"):
                st.warning("⚠️ Website will be inaccessible to users during maintenance")
                if st.button("🔴 Enable Now", use_container_width=True):
                    st.error("🛑 Maintenance mode ENABLED. Website is now in maintenance.")
                    st.toast("Maintenance mode activated")
            
            if st.button("💾 Backup Database", use_container_width=True):
                st.info("💾 Creating database backup...")
                st.toast("Database backup completed successfully")
            
            if st.button("🔄 Restore Database", use_container_width=True):
                st.warning("⚠️ This will restore the database to a previous state")
                st.toast("Database restoration initiated")
            
            if st.button("🚀 Clear Cache", use_container_width=True):
                st.info("🧹 Cache cleared successfully")
                st.toast("Cache cleared")
    
    with col2:
        with st.container(border=True):
            st.write("### 🤖 AI Services")
            
            if st.button("🔄 Restart AI Grading Service", use_container_width=True):
                st.info("🔄 AI Grading Service restarting...")
                st.toast("AI Grading Service restarted")
            
            if st.button("🔄 Restart OCR Service", use_container_width=True):
                st.info("🔄 OCR Service restarting...")
                st.toast("OCR Service restarted")
            
            if st.button("🧹 Clear Upload Files", use_container_width=True):
                st.warning("⚠️ This will delete all uploaded files")
                st.error("❌ Upload directory cleared")
                st.toast("Uploaded files cleared")
            
            if st.button("📊 Optimize Database", use_container_width=True):
                st.info("🔧 Database optimization in progress...")
                st.toast("Database optimized")


# ============================================================================
# PAGE SECTIONS - 7. SECURITY CENTER
# ============================================================================

def render_security_center():
    """Render security monitoring and management section."""
    st.header("🔐 Security Center")
    
    # Security metrics
    st.subheader("Security Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Failed Login Attempts", 23, "+5")
    with col2:
        st.metric("Blocked IPs", 12, "+2")
    with col3:
        st.metric("Active Sessions", 187, "-8")
    with col4:
        st.metric("Security Score", "94/100", "⬆️")
    
    st.divider()
    
    # Security alerts
    st.subheader("🚨 Security Alerts")
    alerts = SampleDataGenerator.generate_security_alerts(10)
    
    for idx, alert in alerts.iterrows():
        severity_color = {
            "Low": "🟢",
            "Medium": "🟡",
            "High": "🟠",
            "Critical": "🔴"
        }
        
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
            
            with col1:
                st.write(f"**{alert['alert_id']}**")
                st.write(f"{severity_color[alert['severity']]} {alert['severity']}")
            
            with col2:
                st.write(f"**{alert['type']}**")
                st.caption(f"IP: {alert['ip_address']}")
            
            with col3:
                st.write(f"User: {alert['user']}")
                st.caption(alert['timestamp'].strftime("%Y-%m-%d %H:%M"))
            
            with col4:
                status_badge = "🆕" if alert['status'] == "New" else "🔍" if alert['status'] == "Investigating" else "✅"
                st.write(f"{status_badge} {alert['status']}")
                
                if alert['status'] != 'Resolved':
                    if st.button("Mark Resolved", key=f"resolve_{alert['alert_id']}", use_container_width=True):
                        st.success(f"✅ {alert['alert_id']} marked as resolved")
    
    st.divider()
    
    # Security actions
    st.subheader("Security Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔒 Force Re-authentication", use_container_width=True):
            st.warning("⚠️ All users will be required to re-authenticate")
            st.toast("Force re-authentication initiated")
    
    with col2:
        if st.button("⛔ Block IP Address", use_container_width=True):
            ip_to_block = st.text_input("Enter IP address to block")
            if ip_to_block:
                st.error(f"🚫 IP {ip_to_block} has been blocked")
    
    with col3:
        if st.button("🔑 Reset Admin Passwords", use_container_width=True):
            st.warning("⚠️ This will reset all admin passwords")
            st.toast("Admin password reset initiated")


# ============================================================================
# PAGE SECTIONS - 8. ADVANCED ANALYTICS
# ============================================================================

def render_advanced_analytics():
    """Render advanced analytics and reporting."""
    st.header("📊 Advanced Analytics & Reporting")
    
    analytics_data = SampleDataGenerator.generate_analytics_data()
    
    st.subheader("Daily Traffic Analysis")
    traffic_df = analytics_data['daily_traffic'].sort_values('date')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=traffic_df['date'], y=traffic_df['students'],
        mode='lines', name='Students', line=dict(color='#00CC96', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=traffic_df['date'], y=traffic_df['teachers'],
        mode='lines', name='Teachers', line=dict(color='#AB63FA', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=traffic_df['date'], y=traffic_df['admins'],
        mode='lines', name='Admins', line=dict(color='#EF553B', width=2)
    ))
    fig.update_layout(
        title="User Traffic Over Time",
        xaxis_title="Date",
        yaxis_title="Number of Users",
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("AI Usage Trends")
        ai_df = analytics_data['ai_usage'].sort_values('date')
        
        fig = px.bar(
            ai_df,
            x='date',
            y=['grading_requests', 'ocr_requests'],
            title='AI Service Requests',
            labels={'date': 'Date', 'value': 'Number of Requests'},
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue Growth")
        revenue_df = analytics_data['revenue_data'].sort_values('date')
        
        # Calculate cumulative revenue
        revenue_df['cumulative'] = revenue_df['amount'].cumsum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=revenue_df['date'],
            y=revenue_df['cumulative'],
            mode='lines+markers',
            name='Cumulative Revenue',
            fill='tozeroy',
            line=dict(color='#00CC96', width=3)
        ))
        fig.update_layout(
            title="Cumulative Revenue",
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# PAGE SECTIONS - 9. BROADCAST CENTER
# ============================================================================

def render_broadcast_center():
    """Render the broadcast and notification system."""
    st.header("📢 Broadcast Center")
    
    st.subheader("Send Announcements & Alerts")
    
    # Broadcast form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        broadcast_type = st.selectbox(
            "Announcement Type",
            ["General Announcement", "Emergency Alert", "Exam Reminder", "Maintenance Notice"]
        )
    
    with col2:
        schedule_option = st.selectbox(
            "Send",
            ["Now", "Schedule Later"]
        )
    
    # Message composition
    st.subheader("Compose Message")
    broadcast_title = st.text_input("Title", placeholder="Enter announcement title...")
    broadcast_message = st.text_area(
        "Message",
        placeholder="Enter your message here...",
        height=200
    )
    
    # Recipient selection
    st.subheader("Select Recipients")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        send_to_students = st.checkbox("Students", value=True)
    with col2:
        send_to_teachers = st.checkbox("Teachers", value=True)
    with col3:
        send_to_admins = st.checkbox("Admins")
    
    # Send options
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        send_email = st.checkbox("📧 Email", value=True)
    with col2:
        send_in_app = st.checkbox("🔔 In-App", value=True)
    with col3:
        send_sms = st.checkbox("📱 SMS")
    with col4:
        send_push = st.checkbox("📲 Push", value=True)
    
    st.divider()
    
    # Preview and send
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👁️ Preview Message", use_container_width=True):
            with st.container(border=True):
                st.write(f"### {broadcast_title}")
                st.write(broadcast_message)
                st.caption(f"Type: {broadcast_type} | Recipients: Students, Teachers" + (", Admins" if send_to_admins else ""))
    
    with col2:
        if st.button("🚀 Send Broadcast", use_container_width=True):
            st.success(f"✅ Broadcast sent to {['Students', 'Teachers'] + (['Admins'] if send_to_admins else [])}")
            st.toast(f"Message delivered to users via {', '.join(['Email' if send_email else '', 'In-App' if send_in_app else '', 'SMS' if send_sms else '', 'Push' if send_push else '']).strip(', ')}")
    
    st.divider()
    
    # Recent broadcasts
    st.subheader("Recent Broadcasts")
    
    recent_broadcasts = [
        {"title": "Important: Server Maintenance", "type": "Maintenance Notice", "recipients": "All", "sent": datetime.now() - timedelta(hours=2)},
        {"title": "Final Exam Schedule Released", "type": "Exam Reminder", "recipients": "Students", "sent": datetime.now() - timedelta(days=1)},
        {"title": "New Feature Available", "type": "General Announcement", "recipients": "All", "sent": datetime.now() - timedelta(days=2)},
    ]
    
    for broadcast in recent_broadcasts:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                st.write(f"**{broadcast['title']}**")
                st.caption(f"Type: {broadcast['type']}")
            
            with col2:
                st.write(f"Recipients: {broadcast['recipients']}")
            
            with col3:
                st.write(f"Sent: {broadcast['sent'].strftime('%Y-%m-%d %H:%M')}")


# ============================================================================
# PAGE SECTIONS - 10. ROLE & PERMISSION MANAGEMENT
# ============================================================================

def render_role_permissions():
    """Render role and permission management interface."""
    st.header("👑 Role & Permission Management")
    
    st.subheader("User Roles")
    
    # Role management tabs
    role_tabs = st.tabs(["Super Admin", "Admin", "Teacher", "Student", "Parent"])
    
    for idx, (tab, role) in enumerate(zip(role_tabs, [
        "Super Admin", "Admin", "Teacher", "Student", "Parent"
    ])):
        with tab:
            st.write(f"### {role} Permissions")
            
            # Define permissions based on role
            if role == "Super Admin":
                permissions = {
                    "User Management": True,
                    "Payment Governance": True,
                    "Security": True,
                    "Analytics": True,
                    "System Settings": True,
                    "AI Management": True,
                    "Maintenance": True,
                    "Broadcast": True,
                }
            elif role == "Admin":
                permissions = {
                    "User Management": True,
                    "Payment Governance": True,
                    "Security": False,
                    "Analytics": True,
                    "System Settings": True,
                    "AI Management": False,
                    "Maintenance": False,
                    "Broadcast": True,
                }
            elif role == "Teacher":
                permissions = {
                    "Grade Students": True,
                    "Upload Materials": True,
                    "View Analytics": True,
                    "Create Assignments": True,
                    "View Payment Status": False,
                    "Manage Users": False,
                }
            else:
                permissions = {
                    "Submit Assignments": True,
                    "View Grades": True,
                    "Download Materials": True,
                    "View Payments": True,
                    "Manage Account": True,
                }
            
            # Display permissions as checkboxes
            cols = st.columns(2)
            col_idx = 0
            
            for perm, enabled in permissions.items():
                with cols[col_idx % 2]:
                    new_state = st.checkbox(perm, value=enabled, key=f"{role}_{perm}")
                col_idx += 1
            
            if st.button(f"💾 Save {role} Permissions", use_container_width=True):
                st.success(f"✅ {role} permissions updated successfully")
    
    st.divider()
    
    # User role assignment
    st.subheader("Assign User Roles")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        user_to_assign = st.selectbox("Select user", [f"User {i}" for i in range(1, 11)])
    
    with col2:
        new_role = st.selectbox("Assign role", ["Student", "Teacher", "Admin", "Super Admin"])
    
    with col3:
        if st.button("✅ Assign", use_container_width=True):
            st.success(f"✅ {user_to_assign} assigned as {new_role}")
            st.toast(f"Role assignment completed")


# ============================================================================
# PAGE SECTIONS - 11. SYSTEM SETTINGS
# ============================================================================

def render_system_settings():
    """Render system-wide settings and configuration."""
    st.header("⚙️ System Settings")
    
    settings_tabs = st.tabs([
        "🏫 School Info",
        "🎨 Theme",
        "📧 Email",
        "🔔 Notifications",
        "🤖 AI Settings",
        "💳 Payment Settings"
    ])
    
    # Tab 1: School Information
    with settings_tabs[0]:
        st.subheader("School Information")
        
        school_name = st.text_input("School Name", value="Premier International School")
        school_code = st.text_input("School Code", value="PIS-001")
        principal_name = st.text_input("Principal Name", value="Dr. Ahmad Khan")
        email = st.text_input("Email", value="principal@school.edu")
        phone = st.text_input("Phone", value="+1-555-123-4567")
        address = st.text_area("Address", value="123 Education Street, City, Country")
        
        if st.button("💾 Save School Information", use_container_width=True):
            st.success("✅ School information updated")
    
    # Tab 2: Theme Customization
    with settings_tabs[1]:
        st.subheader("Theme Customization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            primary_color = st.color_picker("Primary Color", "#1f77d2")
            secondary_color = st.color_picker("Secondary Color", "#ff7f0e")
        
        with col2:
            accent_color = st.color_picker("Accent Color", "#2ca02c")
            theme_mode = st.selectbox("Theme Mode", ["Light", "Dark", "Auto"])
        
        if st.button("💾 Save Theme Settings", use_container_width=True):
            st.success("✅ Theme settings updated")
    
    # Tab 3: Email Settings
    with settings_tabs[2]:
        st.subheader("Email Configuration")
        
        smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
        smtp_port = st.number_input("SMTP Port", value=587)
        email_address = st.text_input("Email Address", value="noreply@school.edu")
        email_password = st.text_input("Email Password", type="password")
        
        if st.button("🧪 Test Email Connection", use_container_width=True):
            st.success("✅ Email connection successful")
        
        if st.button("💾 Save Email Settings", use_container_width=True):
            st.success("✅ Email settings updated")
    
    # Tab 4: Notification Settings
    with settings_tabs[3]:
        st.subheader("Notification Preferences")
        
        st.write("**Email Notifications**")
        email_new_assignment = st.checkbox("New Assignment", value=True)
        email_grade_posted = st.checkbox("Grade Posted", value=True)
        email_payment_reminder = st.checkbox("Payment Reminder", value=True)
        
        st.write("**In-App Notifications**")
        inapp_messages = st.checkbox("Messages", value=True)
        inapp_updates = st.checkbox("System Updates", value=True)
        inapp_alerts = st.checkbox("Security Alerts", value=True)
        
        if st.button("💾 Save Notification Settings", use_container_width=True):
            st.success("✅ Notification settings updated")
    
    # Tab 5: AI Settings
    with settings_tabs[4]:
        st.subheader("AI Grading Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ai_model = st.selectbox("AI Model", ["GPT-4", "Claude-3", "Gemini Pro"])
            grading_strictness = st.slider("Grading Strictness", 0, 100, 75)
        
        with col2:
            feedback_detail = st.slider("Feedback Detail Level", 1, 10, 7)
            enable_ocr = st.checkbox("Enable OCR for images", value=True)
        
        if st.button("💾 Save AI Settings", use_container_width=True):
            st.success("✅ AI settings updated")
    
    # Tab 6: Payment Settings
    with settings_tabs[5]:
        st.subheader("Payment Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "AED"])
            payment_gateway = st.selectbox("Payment Gateway", ["Stripe", "PayPal", "2Checkout"])
        
        with col2:
            late_payment_fee = st.number_input("Late Payment Fee (%)", value=5.0, step=0.5)
            enable_installments = st.checkbox("Enable Installments", value=True)
        
        if st.button("💾 Save Payment Settings", use_container_width=True):
            st.success("✅ Payment settings updated")


# ============================================================================
# MAIN MASTER ADMIN PANEL FUNCTION
# ============================================================================

def render_master_admin_panel():
    """Main function to render the complete Master Admin Panel."""
    
    # Initialize session state
    initialize_admin_session_state()
    
    # Custom CSS for professional styling
    st.markdown("""
        <style>
        /* Professional styling */
        .stMetric {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        
        .stContainer {
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; border-bottom: 3px solid #1f77d2;">
        <h1>🎛️ MASTER ADMIN PANEL</h1>
        <p style="font-size: 16px; color: #666;">
            Enterprise Command Center for AI-Powered School Portal & Grading System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main navigation tabs
    main_tabs = st.tabs([
        "📊 Overview",
        "📈 Activity",
        "👥 Users",
        "🤖 AI System",
        "💰 Payments",
        "🔧 Maintenance",
        "🔐 Security",
        "📉 Analytics",
        "📢 Broadcast",
        "👑 Roles",
        "⚙️ Settings",
        "☁️ SaaS Billing",
        "✅ Admin Verify (Legacy)",
    ])
    
    with main_tabs[0]:
        render_global_overview()
    
    with main_tabs[1]:
        render_activity_monitor()
    
    with main_tabs[2]:
        render_user_access_control()
    
    with main_tabs[3]:
        render_ai_monitoring()
    
    with main_tabs[4]:
        render_payment_governance()
    
    with main_tabs[5]:
        render_maintenance_control()
    
    with main_tabs[6]:
        render_security_center()
    
    with main_tabs[7]:
        render_advanced_analytics()
    
    with main_tabs[8]:
        render_broadcast_center()
    
    with main_tabs[9]:
        render_role_permissions()
    
    with main_tabs[10]:
        render_system_settings()

    with main_tabs[11]:
        st.header("☁️ SaaS subscriptions & school billing")
        st.caption("Verify manual payments (JazzCash, EasyPaisa, bank transfer, demo gateways) to activate subscriptions.")
        auditor = st.text_input(
            "Auditor / admin display name (for audit trail)",
            value=st.session_state.get("master_admin_username") or "master_admin",
            key="master_admin_auditor_name",
        )
        st.session_state.master_admin_username = auditor
        render_saas_master_admin_tab()

    with main_tabs[12]:
        st.header("✅ Admin Payment Verification (embedded)")
        st.caption("This is the existing verification dashboard embedded inside Master Admin.")
        render_admin_payment_dashboard_embedded()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 20px; border-top: 1px solid #ddd; margin-top: 40px; color: #999;">
        <small>
            Master Admin Panel v1.0.0 | Last Updated: 2024 | 
            © Premier International School AI Portal
        </small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_master_admin_panel()
