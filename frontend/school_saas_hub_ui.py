"""
School Access Hub — subscription, payment proof, school registration (Streamlit).
All gates delegate to AccessControl / SaaSDatabase (not UI-only).
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# Add backend to path for imports
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from database import Database
from saas_access_control import AccessControl
from saas_database import SaaSDatabase

saas_db = SaaSDatabase()
RECEIPT_DIR = Path(__file__).resolve().parent.parent / "uploads" / "receipts"
RECEIPT_DIR.mkdir(parents=True, exist_ok=True)


def _inject_saas_css() -> None:
    st.markdown(
        """
        <style>
        .saas-hero {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #312e81 100%);
            color: #f8fafc;
            padding: 2rem 1.5rem;
            border-radius: 16px;
            margin-bottom: 1.5rem;
        }
        .plan-card {
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.25rem;
            height: 100%;
            background: #fff;
            box-shadow: 0 4px 20px rgba(15,23,42,0.06);
        }
        
        /* Premium Plan Card */
        .plan-card-premium {
            border: 2px solid #f59e0b;
            border-radius: 14px;
            padding: 1.5rem;
            height: 100%;
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
            box-shadow: 0 8px 32px rgba(245, 158, 11, 0.15);
            position: relative;
        }
        
        .plan-card-premium::before {
            content: "⭐ MOST POPULAR";
            position: absolute;
            top: -12px;
            left: 20px;
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        }
        
        /* Standard Plan Card */
        .plan-card-standard {
            border: 2px solid #3b82f6;
            border-radius: 14px;
            padding: 1.5rem;
            height: 100%;
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1);
        }
        
        .plan-name {
            font-size: 28px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 12px;
        }
        
        .plan-price {
            font-size: 48px;
            font-weight: 800;
            background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 4px;
        }
        
        .plan-price-currency {
            font-size: 24px;
            margin-right: -8px;
        }
        
        .plan-period {
            font-size: 14px;
            color: #6b7280;
            font-weight: 500;
            margin-bottom: 20px;
        }
        
        .plan-features {
            margin: 24px 0;
        }
        
        .plan-feature-item {
            display: flex;
            align-items: center;
            margin: 12px 0;
            font-size: 14px;
            color: #374151;
            line-height: 1.5;
        }
        
        .plan-feature-check {
            color: #10b981;
            font-weight: 800;
            margin-right: 10px;
            font-size: 16px;
        }
        
        .btn-premium {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        }
        
        .btn-premium:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
        }
        
        .btn-standard {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .btn-standard:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
        }
        
        .checkout-header {
            display: flex;
            align-items: center;
            margin-bottom: 24px;
        }
        
        .checkout-title {
            font-size: 24px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 0;
        }
        
        .checkout-divider {
            flex: 1;
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, #e5e7eb 50%, transparent 100%);
            margin: 0 16px;
        }
        
        .step-indicator {
            display: flex;
            justify-content: space-between;
            margin: 24px 0;
            gap: 16px;
        }
        
        .step {
            flex: 1;
            text-align: center;
            padding: 12px;
            background: #f9fafb;
            border-radius: 8px;
            border-left: 4px solid #d1d5db;
            font-size: 12px;
            font-weight: 600;
            color: #6b7280;
        }
        
        .step.active {
            background: #dbeafe;
            border-left-color: #3b82f6;
            color: #1e40af;
        }
        
        .checkout-card {
            border-left: 4px solid #3b82f6;
            background: #f0f9ff;
            padding: 20px;
            border-radius: 8px;
            margin: 16px 0;
        }
        
        .payment-summary {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid #e2e8f0;
        }
        
        .summary-row {
            display: flex;
            justify-content: space-between;
            margin: 12px 0;
            font-size: 14px;
            color: #374151;
        }
        
        .summary-row.total {
            font-size: 18px;
            font-weight: 700;
            color: #1f2937;
            border-top: 1px solid #e5e7eb;
            padding-top: 12px;
            margin-top: 12px;
        }
        
        div[data-testid="stMetricValue"] { font-size: 1.6rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_school_saas_hub(services: Dict[str, Any]) -> None:
    """Main hub when user clicks **School Registration** in the sidebar."""
    _inject_saas_css()
    database: Database = services["database"]

    st.markdown('<div class="saas-hero"><h2>School & Organization</h2>'
                  '<p>Enterprise SaaS access — subscribe, verify payment, register your school, then open the portal.</p></div>',
                  unsafe_allow_html=True)

    tab_saas, tab_legacy = st.tabs(["☁️ School Registration (SaaS)", "🏫 Legacy School Join / Admin Login"])

    with tab_saas:
        if not st.session_state.get("is_logged_in"):
            st.warning("Please log in from the **Login** page to manage subscription and school registration.")
            return

        if st.session_state.get("user_role") != "teacher":
            st.info(
                "School subscription and registration are available to **teacher accounts** "
                "(organization owners). Student accounts use the features granted by your school."
            )
            return

        user_id = st.session_state.get("user_id")
        username = st.session_state.get("current_username")
        if user_id is None and username:
            user_id = database.get_user_id(username)
            st.session_state.user_id = user_id
        if not user_id or not username:
            st.error("Session is missing user id — please log out and log in again.")
            return

        saas_db.expire_stale_pending_payments()
        saas_db.deactivate_expired_subscriptions()

        summary = AccessControl.get_user_status_summary(user_id)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("SaaS plan", summary.get("subscription_plan") or "—")
        with c2:
            st.metric("Billing", summary.get("subscription_status") or "—")
        with c3:
            st.metric("School profile", "Yes" if summary.get("has_school") else "No")
        with c4:
            st.metric("Portal", "Unlocked" if summary.get("can_access_portal") else "Locked")

        st.divider()

        if summary.get("can_access_portal"):
            _render_portal_unlocked(username, user_id, database)
            return

        if not saas_db.has_active_school_saas_subscription(user_id):
            _render_subscription_and_payment(user_id, username)
            st.divider()
            st.caption("After an administrator verifies your payment, return here to complete school registration.")
            return

        if AccessControl.can_register_school_profile(user_id):
            _render_school_registration_form(user_id, username, database)
            return

        st.error("Unexpected access state. Please contact support.")

    with tab_legacy:
        _render_legacy_school_tools(database)


def _render_legacy_school_tools(database: Database) -> None:
    """
    Legacy flows, now accessible from the School Registration hub.
    Keep SaaS rule: subscription must be active before *creating* a new school organization.
    """
    st.subheader("Legacy school access")
    st.caption("Admin login by school code, and join-by-code membership workflows.")

    # 1) School Admin login (works without being logged into the main app)
    with st.container(border=True):
        st.markdown("### School Admin Login (legacy)")
        with st.form("legacy_school_admin_login_form"):
            school_code = st.text_input("School Access Code", key="legacy_school_code")
            admin_username = st.text_input("Admin Username", key="legacy_admin_username")
            admin_password = st.text_input("Admin Password", type="password", key="legacy_admin_password")
            submit = st.form_submit_button("Open School Website", use_container_width=True)

        if submit:
            if not school_code or not admin_username or not admin_password:
                st.warning("Enter school code, admin username, and password.")
            else:
                school = database.get_school_by_code(school_code)
                if not school:
                    st.error("School code not found.")
                else:
                    membership = database.get_school_membership(school_code, admin_username)
                    if not membership or membership["school_role"] != "admin" or not membership["approved"]:
                        st.error("This account does not have approved admin access for that school.")
                    elif not database.authenticate_user("teacher", admin_username, admin_password):
                        st.error("Invalid admin credentials.")
                    else:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "teacher"
                        st.session_state.current_username = admin_username
                        st.session_state.user_id = database.get_user_id(admin_username)
                        st.session_state.school_code = school_code
                        st.session_state.school_role = "admin"
                        st.session_state.current_page = "school_legacy"
                        st.success("School admin logged in successfully.")
                        st.rerun()

    st.divider()

    # 2) Join/create (requires main login)
    if not st.session_state.get("is_logged_in") or not st.session_state.get("current_username"):
        st.info("Log in from the main **Login** page to request membership or create a school organization.")
        return

    current_username = st.session_state.current_username
    current_role = st.session_state.user_role
    user_id = st.session_state.get("user_id") or database.get_user_id(current_username)
    if user_id:
        st.session_state.user_id = user_id

    left, right = st.columns(2)
    with left:
        st.markdown("### Create School Organization (legacy)")
        st.caption("Creation is gated by SaaS subscription (first subscribe → then create).")
        if current_role == "teacher":
            with st.form("legacy_create_school_form"):
                school_name = st.text_input("School Name", key="legacy_create_school_name")
                school_code = st.text_input("School Access Code", key="legacy_create_school_code")
                create_school_submit = st.form_submit_button("Create School", use_container_width=True)

            if create_school_submit:
                ok, msg = AccessControl.require_subscription(int(user_id or 0))
                if not ok:
                    st.error(f"Subscription required to create a school: {msg}")
                elif not school_name or not school_code:
                    st.warning("Enter both school name and school access code.")
                elif database.create_school(school_name, school_code, current_username):
                    st.success("School organization created successfully.")
                else:
                    st.error("That school access code already exists.")
        else:
            st.info("Only teachers can create a school organization.")

    with right:
        st.markdown("### Join Existing School (legacy)")
        with st.form("legacy_join_school_form"):
            join_school_code = st.text_input("School Access Code", key="legacy_join_school_code")
            school_role = st.selectbox("Join As", ["teacher", "student"], key="legacy_join_school_role")
            join_school_submit = st.form_submit_button("Request Access", use_container_width=True)
        if join_school_submit:
            if school_role != current_role:
                st.warning(f"You are logged in as {current_role}. Join using the same account role.")
            elif not join_school_code:
                st.warning("Enter a school access code.")
            else:
                membership = database.get_school_membership(join_school_code, current_username)
                if membership:
                    st.success("School access loaded. (If pending, wait for admin approval.)")
                elif database.add_school_membership(join_school_code, current_username, school_role, approved=False):
                    st.success("Access request sent. Wait for school admin approval.")
                else:
                    st.error("School code not found or access request could not be created.")


def _render_portal_unlocked(username: str, user_id: int, database: Database) -> None:
    st.success("Your organization has an **active subscription** and a **registered school profile**.")
    school = saas_db.get_user_school(user_id)
    if school:
        st.write(
            f"**{school['school_name']}** · {school.get('city', '')}, {school.get('country', '')} · "
            f"Code `{school['school_id']}`"
        )
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Open School Portal", type="primary", use_container_width=True):
            st.session_state.current_page = "school_portal"
            st.rerun()
    with col2:
        if st.button("Legacy school join (code)", use_container_width=True):
            st.session_state.current_page = "school"
            st.rerun()
    with col3:
        if st.button("Subscription & invoices", use_container_width=True):
            st.session_state.saas_hub_tab = "billing"
            st.rerun()

    if st.session_state.get("saas_hub_tab") == "billing":
        _render_billing_tab(user_id)


def _render_billing_tab(user_id: int) -> None:
    st.subheader("Billing history")
    rows = saas_db.list_user_payments(user_id)
    if not rows:
        st.caption("No payments yet.")
        return
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _render_subscription_and_payment(user_id: int, username: str) -> None:
    """Render modern subscription plan selection and payment checkout interface."""
    
    # ============ PLAN SELECTION SECTION ============
    st.markdown(
        """
        <div style="margin-bottom: 32px;">
            <h2 style="font-size: 32px; font-weight: 700; color: #1f2937; margin-bottom: 8px;">
                Choose Your Subscription Plan
            </h2>
            <p style="font-size: 16px; color: #6b7280; margin: 0;">
                Select the plan that best fits your school's needs. All plans include core features with full support.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    plans = saas_db.get_subscription_plans()
    paid = [p for p in plans if float(p.get("price") or 0) > 0 and int(p.get("school_portal_access") or 0) == 1]
    if not paid:
        st.error("No paid plans configured.")
        return

    chosen_plan_id = st.session_state.get("saas_selected_plan")
    
    # Determine which plan is Premium and which is Standard
    # (Usually based on price or plan_name)
    plan_order = sorted(paid, key=lambda p: float(p.get("price") or 0))
    standard_plan = plan_order[0] if len(plan_order) > 0 else paid[0]
    premium_plan = plan_order[-1] if len(plan_order) > 1 else None
    
    cols = st.columns(len(paid)) if len(paid) > 1 else [st.container()]
    
    for col, plan in zip(cols, paid):
        feats = []
        try:
            import json as _json
            feats = _json.loads(plan.get("features_json") or "[]")
        except Exception:
            feats = []
        
        is_premium = premium_plan and plan["plan_id"] == premium_plan["plan_id"]
        is_selected = plan["plan_id"] == chosen_plan_id
        card_class = "plan-card-premium" if is_premium else "plan-card-standard"
        
        with col:
            # Add extra padding to premium card to account for badge
            if is_premium:
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            
            with st.container(border=False):
                st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                
                # Plan name
                st.markdown(
                    f'<div class="plan-name">{plan["plan_name"]}</div>',
                    unsafe_allow_html=True,
                )
                
                # Price display
                st.markdown(
                    f'''
                    <div style="margin-bottom: 8px;">
                        <div class="plan-price">
                            <span class="plan-price-currency">PKR</span> {float(plan.get("price") or 0):,.0f}
                        </div>
                    </div>
                    <div class="plan-period">per month, billed monthly</div>
                    ''',
                    unsafe_allow_html=True,
                )
                
                # Features list with checkmarks
                st.markdown('<div class="plan-features">', unsafe_allow_html=True)
                for f in feats[:5]:
                    st.markdown(
                        f'<div class="plan-feature-item"><span class="plan-feature-check">✅</span>{f}</div>',
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Selection button
                button_class = "btn-premium" if is_premium else "btn-standard"
                button_text = "✓ Selected" if is_selected else f"Select Plan"
                button_html = f'''
                <button class="{button_class}" onclick="document.forms[0].submit();" style="opacity: {'1' if is_selected else '0.95'};">
                    {button_text}
                </button>
                '''
                
                if st.button(
                    button_text,
                    key=f"pick_{plan['plan_id']}",
                    use_container_width=True,
                ):
                    st.session_state.saas_selected_plan = plan["plan_id"]
                    st.toast(f"✅ Selected {plan['plan_name']}")
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)
    
    # ============ CHECKOUT SECTION ============
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px;">
            <h2 style="font-size: 28px; font-weight: 700; color: #1f2937; margin: 0;">
                Complete Your Payment
            </h2>
            <div style="flex: 1; height: 2px; background: linear-gradient(90deg, transparent 0%, #e5e7eb 50%, transparent 100%);"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Step indicator
    st.markdown(
        """
        <div class="step-indicator">
            <div class="step active">
                <div style="font-size: 20px; margin-bottom: 4px;">✓</div>
                <div>Step 1: Choose Plan</div>
            </div>
            <div class="step active">
                <div style="font-size: 20px; margin-bottom: 4px;">2</div>
                <div>Step 2: Payment</div>
            </div>
            <div class="step">
                <div style="font-size: 20px; margin-bottom: 4px;">3</div>
                <div>Step 3: Access Portal</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    chosen_plan_id = st.session_state.get("saas_selected_plan")
    if not chosen_plan_id:
        st.markdown(
            """
            <div class="checkout-card">
                <div style="color: #1e40af; font-weight: 600; margin-bottom: 8px;">ℹ️ Select a plan to continue</div>
                <div style="color: #64748b; font-size: 14px;">
                    Choose either <strong>Standard</strong> or <strong>Premium</strong> from the plans above to proceed with payment setup.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    plan = saas_db.get_subscription_plan(chosen_plan_id)
    if not plan:
        st.error("Invalid plan selection.")
        return
    
    # Payment summary card
    st.markdown(
        f"""
        <div class="payment-summary">
            <div class="summary-row">
                <span>Plan</span>
                <strong>{plan['plan_name']}</strong>
            </div>
            <div class="summary-row">
                <span>Monthly price</span>
                <strong>PKR {float(plan.get("price") or 0):,.0f}</strong>
            </div>
            <div class="summary-row">
                <span>Billing cycle</span>
                <strong>Monthly renewal</strong>
            </div>
            <div class="summary-row total">
                <span>Total due today</span>
                <span>PKR {float(plan.get("price") or 0):,.0f}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Payment method selection
    st.markdown(
        '<div style="margin-top: 24px; padding-top: 24px; border-top: 1px solid #e5e7eb;"><h3 style="font-size: 18px; font-weight: 600; color: #1f2937; margin-bottom: 16px;">Payment Method</h3></div>',
        unsafe_allow_html=True,
    )
    
    pm = st.selectbox(
        "Select your preferred payment channel",
        ["JazzCash", "EasyPaisa", "Bank Transfer", "Stripe (demo)", "PayPal (demo)"],
        key="saas_pm",
    )
    
    st.markdown(
        f"""
        <div style="background: #f0f9ff; border-left: 4px solid #3b82f6; padding: 16px; border-radius: 6px; margin-top: 12px;">
            <div style="font-size: 13px; color: #1e40af; line-height: 1.6;">
                💳 <strong>Send payment</strong> using <strong>{pm}</strong>, then submit your transaction reference and receipt below for verification.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Generate payment request
    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)
    if st.button("💳 Generate Payment Request", type="primary", key="saas_init_pay", use_container_width=True):
        ok, msg, data = AccessControl.initiate_payment(user_id, username, chosen_plan_id, pm)
        if ok and data:
            st.session_state.saas_pending_payment_id = data["payment_id"]
            st.session_state.saas_pending_subscription_id = data["subscription_id"]
            st.success(msg)
            st.toast("💳 Payment record created", icon="✅")
        else:
            st.error(msg or "Could not start payment")

    # Payment proof submission
    pending_pid = st.session_state.get("saas_pending_payment_id")
    if pending_pid:
        st.markdown("<div style='margin-top: 32px; padding-top: 32px; border-top: 2px solid #e5e7eb;'></div>", unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div style="margin-bottom: 24px;">
                <h3 style="font-size: 18px; font-weight: 700; color: #1f2937; margin-bottom: 8px;">
                    ✅ Submit Payment Proof
                </h3>
                <div style="background: #dbeafe; border-left: 4px solid #0284c7; padding: 12px; border-radius: 6px;">
                    <div style="font-size: 13px; color: #0c4a6e; font-weight: 600; margin-bottom: 4px;">Payment ID: {pending_pid}</div>
                    <div style="font-size: 12px; color: #164e63;">Submit your transaction reference and receipt for verification</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<label style="font-weight: 600; color: #1f2937; font-size: 14px;">Transaction / Reference ID *</label>', unsafe_allow_html=True)
            txn = st.text_input("", placeholder="e.g., TXN123456789", key="saas_txn", label_visibility="collapsed")
        
        with col2:
            st.markdown('<label style="font-weight: 600; color: #1f2937; font-size: 14px;">Receipt Screenshot (optional)</label>', unsafe_allow_html=True)
            receipt = st.file_uploader("", type=["png", "jpg", "jpeg", "pdf"], key="saas_receipt", label_visibility="collapsed")

        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        if st.button("📸 Submit Proof for Verification", type="primary", key="saas_submit_proof", use_container_width=True):
            if not txn.strip():
                st.warning("⚠️ Transaction ID is required.")
            else:
                path = None
                fname = None
                if receipt is not None:
                    fname = f"{pending_pid}_{receipt.name}"
                    path = str(RECEIPT_DIR / fname)
                    with open(path, "wb") as f:
                        f.write(receipt.getbuffer())
                    saas_db.update_payment_receipt(pending_pid, path)
                saas_db.submit_payment_proof(pending_pid, txn.strip(), path, fname)

                dup = saas_db.count_duplicate_transaction_ids(txn.strip(), pending_pid)
                if dup > 0:
                    saas_db.insert_fraud_alert(
                        alert_id=f"FR-{uuid.uuid4().hex[:10].upper()}",
                        fraud_type="duplicate_transaction_id",
                        severity="Medium",
                        pattern="Transaction ID reused across multiple payment records",
                        confidence=min(0.5 + 0.2 * dup, 0.99),
                        user_id=user_id,
                        username=username,
                        payment_id=pending_pid,
                        details={"matches": dup},
                    )
                    st.toast("⚠️ Fraud monitor: duplicate reference flagged for admin review", icon="🚨")

                st.markdown(
                    """
                    <div style="background: #dcfce7; border-left: 4px solid #22c55e; padding: 16px; border-radius: 8px; margin-top: 16px;">
                        <div style="color: #166534; font-weight: 700; margin-bottom: 4px;">✅ Proof Submitted Successfully</div>
                        <div style="color: #365314; font-size: 13px; line-height: 1.6;">
                            Your payment proof has been submitted. Our <strong>Master Admin</strong> will verify your payment and activate your subscription within 24-48 hours.<br><br>
                            <strong>What to expect next:</strong> You'll receive an email confirmation once your subscription is active.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.session_state.saas_pending_payment_id = None
                st.balloons()

    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.divider()
    
    # Platform stats
    rev = saas_db.get_revenue_summary()
    if rev:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; background: #f8fafc; border-radius: 8px; margin-top: 24px;">
                <div style="font-size: 12px; color: #6b7280; margin-bottom: 8px;">Platform Payment Records</div>
                <div style="display: flex; justify-content: center; gap: 32px; flex-wrap: wrap;">
                    <div>
                        <div style="font-size: 24px; font-weight: 700; color: #1f2937;">{rev.get('cnt', 0)}</div>
                        <div style="font-size: 12px; color: #6b7280;">Total Payments</div>
                    </div>
                    <div>
                        <div style="font-size: 24px; font-weight: 700; color: #059669;">PKR {rev.get('verified_total', 0):,.0f}</div>
                        <div style="font-size: 12px; color: #6b7280;">Verified Volume</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_school_registration_form(user_id: int, username: str, database: Database) -> None:
    st.subheader("Register your school")
    st.success("Subscription is **active**. Complete the profile below to unlock the School Portal.")

    with st.form("saas_school_reg"):
        c1, c2 = st.columns(2)
        with c1:
            school_name = st.text_input("School name *")
            principal_name = st.text_input("Principal name *")
            school_email = st.text_input("School email *")
            school_phone = st.text_input("School phone *")
            logo = st.file_uploader("School logo (optional)", type=["png", "jpg", "jpeg"])
        with c2:
            school_address = st.text_area("Address *")
            city = st.text_input("City *")
            country = st.text_input("Country *", value="Pakistan")
            school_type = st.selectbox(
                "School type *",
                ["Public", "Private", "International", "Charter", "Online", "Other"],
            )
            total_students = st.number_input("Total students (estimate) *", min_value=0, value=100)
            registration_number = st.text_input("Official registration / license number")

        submitted = st.form_submit_button("Create school profile", type="primary", use_container_width=True)

    if not submitted:
        return

    required = [school_name, principal_name, school_email, school_phone, school_address, city, country]
    if not all(required):
        st.warning("Please fill all required fields (*).")
        return

    logo_path = None
    if logo is not None:
        lid = f"LOGO-{uuid.uuid4().hex[:8]}"
        ext = os.path.splitext(logo.name)[1]
        dest = RECEIPT_DIR / f"{lid}{ext}"
        with open(dest, "wb") as f:
            f.write(logo.getbuffer())
        logo_path = str(dest)

    data = {
        "school_name": school_name.strip(),
        "principal_name": principal_name.strip(),
        "school_email": school_email.strip(),
        "school_phone": school_phone.strip(),
        "school_address": school_address.strip(),
        "city": city.strip(),
        "country": country.strip(),
        "school_type": school_type,
        "total_students": int(total_students),
        "registration_number": registration_number.strip(),
        "school_logo_path": logo_path,
    }
    ok, msg, sid = AccessControl.register_school(user_id, username, data)
    if not ok:
        st.error(msg)
        return

    st.success(f"{msg} School ID: `{sid}`")
    _sync_legacy_school(database, username, school_name.strip(), sid)
    st.toast("School Portal is now available from the sidebar", icon="🏫")
    st.balloons()
    st.rerun()


def _sync_legacy_school(database: Database, admin_username: str, school_name: str, saas_school_id: str) -> None:
    """Create a matching row in the classic `schools` table for existing join-code flows."""
    code = f"ORG-{saas_school_id.replace('SCH-', '')[:10].upper()}"
    try:
        if database.get_school_by_code(code):
            return
        database.create_school(school_name, code, admin_username)
    except Exception:
        pass


def render_saas_master_admin_tab() -> None:
    """Embedded in Master Admin — real SaaS payment verification."""
    st.subheader("☁️ SaaS subscription payments")
    saas_db.expire_stale_pending_payments()
    saas_db.deactivate_expired_subscriptions()

    pending = saas_db.get_pending_payments()
    st.metric("Pending SaaS proofs", len(pending))
    if not pending:
        st.success("No pending SaaS payment proofs.")
    else:
        for p in pending:
            with st.expander(
                f"{p['payment_id']} · {p['username']} · Pak Rs. {p['amount']:,.0f} · {p['payment_method']}"
            ):
                st.write(f"Subscription: `{p['subscription_id']}`")
                st.write(f"Transaction ID: `{p.get('transaction_id') or '—'}`")
                st.write(f"Receipt: `{p.get('receipt_path') or '—'}`")
                admin_u = st.session_state.get("master_admin_username") or "master_admin"
                txn_fix = st.text_input("Confirm / adjust transaction ID", value=p.get("transaction_id") or "", key=f"adm_txn_{p['payment_id']}")
                notes = st.text_area("Verification notes", key=f"adm_notes_{p['payment_id']}")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("Verify & activate", key=f"v_{p['payment_id']}"):
                        ok, msg = AccessControl.admin_verify_payment(
                            p["payment_id"], admin_u, txn_fix or None, notes
                        )
                        st.success(msg) if ok else st.error(msg)
                        st.rerun()
                with c2:
                    if st.button("Reject", key=f"r_{p['payment_id']}"):
                        ok, msg = AccessControl.admin_reject_payment(p["payment_id"], admin_u, notes or "Rejected")
                        st.warning(msg)
                        st.rerun()
                with c3:
                    if st.button("Mark refunded", key=f"ref_{p['payment_id']}"):
                        saas_db.mark_payment_refunded(p["payment_id"], admin_u, notes)
                        st.info("Marked as refunded")
                        st.rerun()

    st.divider()
    st.subheader("Revenue (verified)")
    rev = saas_db.get_revenue_summary()
    if rev:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("All payments (count)", int(rev.get("cnt") or 0))
        with c2:
            st.metric("Verified (Pak Rs.)", f"{float(rev.get('verified_total') or 0):,.0f}")
        with c3:
            st.metric("Pending queue", int(rev.get("pending_cnt") or 0))

    pay_rows = []
    try:
        with saas_db._connect() as conn:
            cur = conn.execute(
                "SELECT payment_date, amount, status FROM saas_payments ORDER BY payment_date DESC LIMIT 200"
            )
            pay_rows = [dict(r) for r in cur.fetchall()]
    except Exception:
        pass
    if pay_rows:
        df = pd.DataFrame(pay_rows)
        agg = df.groupby("status", as_index=False)["amount"].sum()
        fig = px.bar(agg, x="status", y="amount", title="Recorded amounts by status", color="status")
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Fraud queue (recent)")
    try:
        with saas_db._connect() as conn:
            cur = conn.execute(
                "SELECT * FROM saas_fraud_alerts ORDER BY created_at DESC LIMIT 15"
            )
            fraud = [dict(r) for r in cur.fetchall()]
        if fraud:
            st.dataframe(pd.DataFrame(fraud), use_container_width=True, hide_index=True)
        else:
            st.caption("No fraud alerts logged.")
    except Exception:
        st.caption("Fraud table unavailable.")
