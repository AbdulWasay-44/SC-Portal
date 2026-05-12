"""
SaaS Access Control & Business Logic Module
Handles permission checking, subscription verification, and access rules
"""

import uuid
from typing import Dict, Optional, Tuple

import streamlit as st

from saas_database import SaaSDatabase

db = SaaSDatabase()


class AccessControl:
    """Backend access control and permission system."""

    # ============ SUBSCRIPTION CHECKS ============

    @staticmethod
    def has_active_subscription(user_id: int) -> bool:
        """
        Check if user has active, verified subscription.
        This is the PRIMARY gatekeeper function.
        """
        return db.has_active_subscription(user_id)

    @staticmethod
    def get_subscription_status(user_id: int) -> Dict:
        """Get detailed subscription status."""
        subscription = db.get_user_subscription(user_id)

        if not subscription:
            return {
                "has_subscription": False,
                "is_active": False,
                "status": "No subscription",
                "plan": None,
            }

        return {
            "has_subscription": True,
            "is_active": bool(subscription["is_active"]),
            "status": subscription["payment_status"],
            "plan": subscription["plan_name"],
            "plan_tier": subscription["plan_tier"],
            "expiry_date": subscription["expiry_date"],
            "renewal_date": subscription["renewal_date"],
        }

    # ============ SCHOOL CHECKS ============

    @staticmethod
    def has_registered_school(user_id: int) -> bool:
        """
        Check if user has registered school.
        Can ONLY register after paying for subscription.
        """
        return db.has_registered_school(user_id)

    @staticmethod
    def get_school_info(user_id: int) -> Optional[Dict]:
        """Get user's school information."""
        return db.get_user_school(user_id)

    # ============ ACCESS REQUIREMENT FUNCTIONS ============
    # These are the backend protection functions

    @staticmethod
    def _subscription_block_reason(user_id: int) -> str:
        db.expire_stale_pending_payments()
        db.deactivate_expired_subscriptions()
        subscription = db.get_latest_subscription_row(user_id)
        if not subscription:
            return "No subscription — choose Standard or Premium to unlock the School Portal"
        status = subscription.get("payment_status") or ""
        if status == "Pending":
            return "Payment submitted — awaiting admin verification"
        if status in ("Rejected", "Refunded"):
            return f"Billing status: {status}. Please start a new checkout."
        if status == "Expired":
            return "Subscription expired — renew to restore access"
        if status == "Suspended":
            return "Subscription suspended — contact support"
        return "Subscription does not include School Portal access on this plan"

    @staticmethod
    def require_subscription(user_id: int) -> Tuple[bool, str]:
        """Active paid (or trial) SaaS plan that includes School Portal."""
        db.expire_stale_pending_payments()
        db.deactivate_expired_subscriptions()
        if db.has_active_school_saas_subscription(user_id):
            return (True, "Subscription verified")
        return (False, AccessControl._subscription_block_reason(user_id))

    @staticmethod
    def require_registered_school(user_id: int) -> Tuple[bool, str]:
        """School profile must exist (use after subscription check)."""
        if not AccessControl.has_registered_school(user_id):
            return (False, "No registered school profile")
        return (True, "School profile found")

    @staticmethod
    def require_school_registration(user_id: int) -> Tuple[bool, str]:
        """Alias: full portal gate — verified subscription + registered school."""
        return AccessControl.require_school_access(user_id)

    @staticmethod
    def require_school_access(user_id: int) -> Tuple[bool, str]:
        """Backend gate for School Portal UI and APIs."""
        ok, msg = AccessControl.require_subscription(user_id)
        if not ok:
            return (False, msg)
        ok2, msg2 = AccessControl.require_registered_school(user_id)
        if not ok2:
            return (False, msg2)
        return (True, "Full school access granted")

    @staticmethod
    def can_register_school_profile(user_id: int) -> bool:
        """Eligible to show school registration form (paid, no profile yet)."""
        db.expire_stale_pending_payments()
        db.deactivate_expired_subscriptions()
        return db.has_active_school_saas_subscription(user_id) and not db.has_registered_school(user_id)

    @staticmethod
    def can_open_school_portal(user_id: Optional[int]) -> bool:
        if user_id is None:
            return False
        ok, _ = AccessControl.require_school_access(user_id)
        return ok

    # ============ STREAMLIT UI PROTECTION ============

    @staticmethod
    def check_and_enforce_school_access(user_id: int) -> bool:
        """
        Check subscription and school access for Streamlit pages.
        If not allowed, shows error and returns False.
        """
        is_allowed, message = AccessControl.require_school_access(user_id)

        if not is_allowed:
            st.error(f"❌ Access Denied: {message}")

            # Show next steps
            if not AccessControl.has_active_subscription(user_id):
                st.info("💳 Please subscribe to access School Portal")
            elif not AccessControl.has_registered_school(user_id):
                st.info("🏫 Please register your school first")

            return False

        return True

    @staticmethod
    def check_and_enforce_subscription(user_id: int) -> bool:
        """Check subscription for Streamlit pages."""
        is_allowed, message = AccessControl.require_subscription(user_id)

        if not is_allowed:
            st.error(f"❌ {message}")
            st.info("💳 Please subscribe to continue")
            return False

        return True

    # ============ PLAN FEATURE CHECKS ============

    @staticmethod
    def has_school_portal_access(user_id: int) -> bool:
        """Check if plan includes school portal access."""
        subscription = db.get_user_subscription(user_id)
        if not subscription:
            return False

        plan = db.get_plan_by_plan_name(subscription["plan_name"])
        if not plan:
            return False

        return bool(plan["school_portal_access"])

    @staticmethod
    def has_ai_grading_access(user_id: int) -> bool:
        """Check if plan includes AI grading access."""
        subscription = db.get_user_subscription(user_id)
        if not subscription:
            return False

        plan = db.get_plan_by_plan_name(subscription["plan_name"])
        if not plan:
            return False

        return bool(plan["ai_grading_access"])

    @staticmethod
    def has_advanced_analytics(user_id: int) -> bool:
        """Check if plan includes advanced analytics."""
        subscription = db.get_user_subscription(user_id)
        if not subscription:
            return False

        plan = db.get_plan_by_plan_name(subscription["plan_name"])
        if not plan:
            return False

        return bool(plan["advanced_analytics"])

    # ============ PAYMENT OPERATIONS ============

    @staticmethod
    def initiate_payment(
        user_id: int, username: str, plan_id: str, payment_method: str
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Initiate a payment for subscription.
        Returns: (success, message, payment_data)
        """
        try:
            # Get plan details
            plan = db.get_subscription_plan(plan_id)
            if not plan:
                return (False, "Plan not found", None)

            # Generate IDs
            subscription_id = f"SUB-{uuid.uuid4().hex[:12].upper()}"
            payment_id = f"PAY-{uuid.uuid4().hex[:12].upper()}"

            # Create subscription
            success = db.create_subscription(
                subscription_id=subscription_id,
                user_id=user_id,
                username=username,
                plan_name=plan["plan_name"],
                plan_tier=plan["plan_tier"],
                amount=plan["price"],
                currency="PKR",
                plan_id=plan["plan_id"],
                trial_days=0,
            )

            if not success:
                return (False, "Failed to create subscription", None)

            # Create payment record
            success = db.create_payment(
                payment_id=payment_id,
                subscription_id=subscription_id,
                user_id=user_id,
                username=username,
                amount=plan["price"],
                payment_method=payment_method,
                currency="PKR",
            )

            if not success:
                return (False, "Failed to create payment", None)

            payment_data = {
                "payment_id": payment_id,
                "subscription_id": subscription_id,
                "amount": plan["price"],
                "plan_name": plan["plan_name"],
                "payment_method": payment_method,
            }

            return (True, "Payment initiated successfully", payment_data)

        except Exception as e:
            return (False, f"Error: {str(e)}", None)

    # ============ SCHOOL REGISTRATION ============

    @staticmethod
    def register_school(
        user_id: int,
        owner_username: str,
        school_data: Dict,
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Register a school for user.
        Can ONLY be called if user has active subscription.
        Returns: (success, message, school_id)
        """
        try:
            if not db.has_active_school_saas_subscription(user_id):
                return (False, "Active verified subscription required before school registration", None)

            if db.has_registered_school(user_id):
                return (False, "A school is already registered to this account", None)

            school_id = f"SCH-{uuid.uuid4().hex[:12].upper()}"

            subscription = db.get_active_school_subscription(user_id)
            if not subscription:
                return (False, "No qualifying subscription record found", None)

            success = db.register_school(
                school_id=school_id,
                owner_user_id=user_id,
                owner_username=owner_username,
                school_name=school_data.get("school_name", ""),
                principal_name=school_data.get("principal_name", ""),
                school_email=school_data.get("school_email", ""),
                school_phone=school_data.get("school_phone", ""),
                school_address=school_data.get("school_address", ""),
                city=school_data.get("city", ""),
                country=school_data.get("country", "Pakistan"),
                school_type=school_data.get("school_type", ""),
                subscription_id=subscription["subscription_id"],
                registration_number=school_data.get("registration_number", ""),
                website=school_data.get("website", ""),
                total_students=int(school_data.get("total_students") or 0),
                school_logo_path=school_data.get("school_logo_path"),
            )

            if not success:
                return (False, "Failed to register school", None)

            return (True, "School registered successfully", school_id)

        except Exception as e:
            return (False, f"Error: {str(e)}", None)

    # ============ MASTER ADMIN FUNCTIONS ============

    @staticmethod
    def admin_verify_payment(
        payment_id: str,
        admin_username: str,
        transaction_id: str = None,
        verification_notes: str = "",
    ) -> Tuple[bool, str]:
        """
        Admin function to verify a payment.
        Backend protected - admin role required in actual implementation.
        """
        try:
            success = db.verify_payment(
                payment_id=payment_id,
                verified_by=admin_username,
                transaction_id=transaction_id,
                verification_notes=verification_notes,
            )

            if success:
                # Log activity
                db.log_activity(
                    log_id=f"LOG-{uuid.uuid4().hex[:12].upper()}",
                    user_id=0,  # Admin user
                    username=admin_username,
                    activity_type="Payment Verification",
                    activity_description=f"Payment {payment_id} verified",
                    resource_type="Payment",
                    resource_id=payment_id,
                    status="Success",
                )

            return (success, "Payment verified" if success else "Failed to verify")

        except Exception as e:
            return (False, f"Error: {str(e)}")

    @staticmethod
    def admin_reject_payment(
        payment_id: str, admin_username: str, reason: str = ""
    ) -> Tuple[bool, str]:
        """Admin function to reject a payment."""
        try:
            success = db.reject_payment(
                payment_id=payment_id, verified_by=admin_username, reason=reason
            )

            if success:
                db.log_activity(
                    log_id=f"LOG-{uuid.uuid4().hex[:12].upper()}",
                    user_id=0,
                    username=admin_username,
                    activity_type="Payment Rejection",
                    activity_description=f"Payment {payment_id} rejected: {reason}",
                    resource_type="Payment",
                    resource_id=payment_id,
                    status="Success",
                )

            return (success, "Payment rejected" if success else "Failed to reject")

        except Exception as e:
            return (False, f"Error: {str(e)}")

    @staticmethod
    def admin_verify_school(
        school_id: str, admin_username: str
    ) -> Tuple[bool, str]:
        """Admin function to verify a school registration."""
        try:
            success = db.verify_school(school_id, admin_username)

            if success:
                db.log_activity(
                    log_id=f"LOG-{uuid.uuid4().hex[:12].upper()}",
                    user_id=0,
                    username=admin_username,
                    activity_type="School Verification",
                    activity_description=f"School {school_id} verified",
                    resource_type="School",
                    resource_id=school_id,
                    status="Success",
                )

            return (success, "School verified" if success else "Failed to verify")

        except Exception as e:
            return (False, f"Error: {str(e)}")

    @staticmethod
    def admin_suspend_subscription(
        subscription_id: str, admin_username: str, reason: str = ""
    ) -> Tuple[bool, str]:
        """Admin function to suspend a subscription."""
        try:
            ok = db.suspend_subscription(subscription_id, reason)
            if ok:
                db.log_activity(
                    log_id=f"LOG-{uuid.uuid4().hex[:12].upper()}",
                    user_id=0,
                    username=admin_username,
                    activity_type="Subscription Suspension",
                    activity_description=f"Subscription {subscription_id} suspended: {reason}",
                    resource_type="Subscription",
                    resource_id=subscription_id,
                    status="Success",
                )
            return (ok, "Subscription suspended" if ok else "Unable to suspend")

        except Exception as e:
            return (False, f"Error: {str(e)}")

    # ============ UTILITY FUNCTIONS ============

    @staticmethod
    def get_user_status_summary(user_id: int) -> Dict:
        """Get complete user status summary for dashboard."""
        subscription = db.get_user_subscription(user_id)
        school = db.get_user_school(user_id)

        return {
            "has_subscription": subscription is not None,
            "subscription_status": subscription["payment_status"]
            if subscription
            else None,
            "subscription_plan": subscription["plan_name"] if subscription else None,
            "subscription_active": bool(subscription["is_active"])
            if subscription
            else False,
            "has_school": school is not None,
            "school_name": school["school_name"] if school else None,
            "school_verified": (
                school["verification_status"] == "Verified" if school else False
            ),
            "can_access_portal": AccessControl.can_open_school_portal(user_id),
        }
