"""
Legacy Admin - Payment Verification Dashboard
Moved from `pages/` so it doesn't show as a separate Streamlit page.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
from saas_database import SaaSDatabase
from saas_access_control import AccessControl

db = SaaSDatabase()


def render_admin_payment_dashboard_embedded():
    """
    Render the admin payment dashboard inside another page (no set_page_config).
    Use this when embedding in `master_admin_panel.py`.
    """
    # Admin authentication check
    if not is_admin():
        st.error("❌ Access Denied: Admin access required")
        return

    admin_username = st.session_state.get("username") or st.session_state.get("current_username") or "admin"

    st.header("🔒 Admin Payment Verification")
    st.caption("Verify/reject payments, manage subscriptions, and review revenue analytics.")
    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "💰 Pending Payments",
            "✅ Verified Payments",
            "🏫 School Registrations",
            "📊 Revenue Analytics",
            "📋 Activity Logs",
        ]
    )

    with tab1:
        render_pending_payments_tab(admin_username)
    with tab2:
        render_verified_payments_tab()
    with tab3:
        render_school_registrations_tab(admin_username)
    with tab4:
        render_revenue_analytics_tab()
    with tab5:
        render_activity_logs_tab()


def render_admin_payment_dashboard():
    """Standalone legacy page (kept for backward compatibility)."""
    st.set_page_config(page_title="🔒 Admin - Payment Verification", layout="wide")
    st.title("🔒 Master Admin - Payment Verification Dashboard")
    render_admin_payment_dashboard_embedded()


def is_admin() -> bool:
    """Check if current user is admin."""
    if "user_id" not in st.session_state:
        return False

    username_raw = st.session_state.get("username") or st.session_state.get("current_username") or ""
    role_raw = st.session_state.get("user_role")
    username = str(username_raw).lower()
    role = str(role_raw or "").lower()

    return "admin" in username or "master" in role or role == "admin"


def render_pending_payments_tab(admin_username: str):
    """Display and manage pending payments."""
    st.subheader("💰 Pending Payment Verification")

    pending_payments = db.get_pending_payments()
    if not pending_payments:
        st.info("✅ No pending payments")
        return

    col1, col2, col3, col4 = st.columns(4)
    total_pending = len(pending_payments)
    total_amount = sum(p["amount"] for p in pending_payments)

    with col1:
        st.metric("Pending Payments", total_pending)
    with col2:
        st.metric("Total Amount", f"Pak Rs. {total_amount:,.2f}")
    with col3:
        st.metric("Avg Amount", f"Pak Rs. {total_amount / total_pending:,.2f}" if total_pending else "Pak Rs. 0")
    with col4:
        st.metric("Oldest Payment", pending_payments[-1]["payment_date"][:10] if pending_payments else "-")

    st.markdown("---")

    df = pd.DataFrame(pending_payments)
    df_display = df[
        [
            "payment_id",
            "user_id",
            "username",
            "amount",
            "payment_method",
            "transaction_id",
            "receipt_path",
            "payment_date",
        ]
    ].copy()
    df_display["amount"] = df_display["amount"].apply(lambda x: f"Pak Rs. {float(x):,.2f}")

    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("🔍 Verify / Reject Payment")

    selected_payment_id = st.selectbox(
        "Select payment to verify/reject",
        options=[p["payment_id"] for p in pending_payments],
        key="admin_selected_payment",
    )

    if not selected_payment_id:
        return

    payment = db.get_payment(selected_payment_id)
    if not payment:
        st.error("Payment not found")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.write("### Payment Details")
        st.write(f"**Payment ID:** {payment['payment_id']}")
        st.write(f"**User:** {payment['username']} (ID: {payment['user_id']})")
        st.write(f"**Amount:** Pak Rs. {payment['amount']:,.2f}")
        st.write(f"**Method:** {payment['payment_method']}")
        st.write(f"**Transaction ID:** {payment.get('transaction_id') or '-'}")
        st.write(f"**Submitted:** {str(payment.get('payment_date', ''))[:16]}")
        if payment.get("receipt_path"):
            st.write(f"**Receipt:** `{payment['receipt_path']}`")
    with col2:
        st.write("### Admin Action")
        transaction_id = st.text_input(
            "Confirm transaction ID (optional)",
            value=payment.get("transaction_id") or "",
            key="admin_confirm_transaction_id",
        )
        notes = st.text_area("Verification notes", key="admin_verification_notes")

        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("✅ Verify Payment", type="primary", use_container_width=True):
                success = db.verify_payment(
                    payment_id=selected_payment_id,
                    verified_by=admin_username,
                    verification_notes=notes,
                    transaction_id=transaction_id or None,
                )
                if success:
                    st.success("✅ Payment verified and subscription activated")
                    st.toast("Subscription activated", icon="✅")
                    st.rerun()
                else:
                    st.error("❌ Failed to verify payment")

        with action_col2:
            if st.button("❌ Reject Payment", use_container_width=True):
                success = db.reject_payment(
                    payment_id=selected_payment_id,
                    verified_by=admin_username,
                    reason=notes or "Rejected by admin",
                )
                if success:
                    st.warning("Payment rejected")
                    st.rerun()
                else:
                    st.error("❌ Failed to reject payment")


def render_verified_payments_tab():
    """Display verified payments."""
    st.subheader("✅ Verified Payments")
    try:
        with db._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM saas_payments WHERE status = 'Verified' ORDER BY verified_date DESC LIMIT 200"
            ).fetchall()
        payments = [dict(r) for r in rows]
    except Exception:
        payments = []
    if not payments:
        st.info("No verified payments yet.")
        return
    df = pd.DataFrame(payments)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_school_registrations_tab(admin_username: str):
    """Display school registrations."""
    st.subheader("🏫 School Registrations")
    try:
        with db._connect() as conn:
            rows = conn.execute("SELECT * FROM saas_schools ORDER BY registration_date DESC LIMIT 200").fetchall()
        schools = [dict(r) for r in rows]
    except Exception:
        schools = []
    if not schools:
        st.info("No schools registered yet.")
        return
    st.dataframe(pd.DataFrame(schools), use_container_width=True, hide_index=True)


def render_revenue_analytics_tab():
    st.subheader("📊 Revenue Analytics")
    rev = db.get_revenue_summary()
    if not rev:
        st.info("No revenue data yet.")
        return
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Payments (count)", int(rev.get("cnt") or 0))
    with c2:
        st.metric("Verified volume", f"Pak Rs. {float(rev.get('verified_total') or 0):,.0f}")
    with c3:
        st.metric("Pending queue", int(rev.get("pending_cnt") or 0))


def render_activity_logs_tab():
    st.subheader("📋 Activity Logs")
    try:
        with db._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM saas_activity_logs ORDER BY created_at DESC LIMIT 200"
            ).fetchall()
        logs = [dict(r) for r in rows]
    except Exception:
        logs = []
    if not logs:
        st.info("No activity logs yet.")
        return
    st.dataframe(pd.DataFrame(logs), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    render_admin_payment_dashboard()

