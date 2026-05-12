"""
SaaS Subscription & Payment System Database Module
Handles subscriptions, payments, schools, and access control
"""

import json
import sqlite3
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DB_PATH = Path(__file__).resolve().parent / "abdul_project.db"


class SaaSDatabase:
    """Database operations for SaaS subscription and payment system."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = str(db_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        """Create database connection."""
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self):
        """Create SaaS tables if they don't exist."""
        with self._connect() as conn:
            # ============ SUBSCRIPTIONS TABLE ============
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saas_subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subscription_id TEXT NOT NULL UNIQUE,
                    user_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    plan_name TEXT NOT NULL,
                    plan_tier TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT NOT NULL DEFAULT 'PKR',
                    billing_cycle TEXT NOT NULL DEFAULT 'monthly',
                    start_date TIMESTAMP NOT NULL,
                    expiry_date TIMESTAMP NOT NULL,
                    renewal_date TIMESTAMP,
                    payment_status TEXT NOT NULL DEFAULT 'Pending',
                    is_active INTEGER NOT NULL DEFAULT 1,
                    auto_renew INTEGER NOT NULL DEFAULT 1,
                    cancellation_date TIMESTAMP,
                    cancellation_reason TEXT,
                    stripe_subscription_id TEXT,
                    payment_method TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
                """
            )

            # ============ PAYMENTS TABLE ============
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saas_payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payment_id TEXT NOT NULL UNIQUE,
                    subscription_id TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT NOT NULL DEFAULT 'PKR',
                    payment_method TEXT NOT NULL,
                    transaction_id TEXT,
                    receipt_path TEXT,
                    receipt_filename TEXT,
                    status TEXT NOT NULL DEFAULT 'Pending',
                    verified_by TEXT,
                    verification_notes TEXT,
                    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    verified_date TIMESTAMP,
                    expiry_date TIMESTAMP,
                    is_expired INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(subscription_id) REFERENCES saas_subscriptions(subscription_id)
                )
                """
            )

            # ============ SCHOOLS TABLE (SaaS) ============
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saas_schools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    school_id TEXT NOT NULL UNIQUE,
                    owner_user_id INTEGER NOT NULL,
                    owner_username TEXT NOT NULL,
                    school_name TEXT NOT NULL,
                    school_logo_path TEXT,
                    principal_name TEXT NOT NULL,
                    school_email TEXT NOT NULL,
                    school_phone TEXT NOT NULL,
                    school_address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT,
                    country TEXT NOT NULL DEFAULT 'Pakistan',
                    postal_code TEXT,
                    school_type TEXT NOT NULL,
                    total_students INTEGER DEFAULT 0,
                    registration_number TEXT,
                    website TEXT,
                    subscription_status TEXT NOT NULL DEFAULT 'Active',
                    subscription_id TEXT NOT NULL,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    verification_status TEXT NOT NULL DEFAULT 'Pending',
                    verified_by TEXT,
                    verified_date TIMESTAMP,
                    status TEXT NOT NULL DEFAULT 'Active',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(owner_user_id) REFERENCES users(id),
                    FOREIGN KEY(subscription_id) REFERENCES saas_subscriptions(subscription_id)
                )
                """
            )

            # ============ INVOICES TABLE ============
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saas_invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_id TEXT NOT NULL UNIQUE,
                    payment_id TEXT NOT NULL,
                    subscription_id TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    school_id TEXT,
                    invoice_number TEXT NOT NULL,
                    amount REAL NOT NULL,
                    currency TEXT NOT NULL DEFAULT 'PKR',
                    invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    due_date TIMESTAMP,
                    payment_date TIMESTAMP,
                    status TEXT NOT NULL DEFAULT 'Draft',
                    invoice_pdf_path TEXT,
                    description TEXT,
                    line_items_json TEXT,
                    tax_amount REAL DEFAULT 0,
                    discount_amount REAL DEFAULT 0,
                    total_amount REAL NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(payment_id) REFERENCES saas_payments(payment_id),
                    FOREIGN KEY(subscription_id) REFERENCES saas_subscriptions(subscription_id)
                )
                """
            )

            # ============ PAYMENT LOGS TABLE ============
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saas_payment_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    log_id TEXT NOT NULL UNIQUE,
                    payment_id TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    amount REAL,
                    payment_method TEXT,
                    transaction_id TEXT,
                    error_message TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    metadata_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(payment_id) REFERENCES saas_payments(payment_id)
                )
                """
            )

            # ============ ACTIVITY LOGS TABLE (SaaS) ============
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saas_activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    log_id TEXT NOT NULL UNIQUE,
                    user_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    activity_description TEXT NOT NULL,
                    resource_type TEXT,
                    resource_id TEXT,
                    ip_address TEXT,
                    status TEXT NOT NULL DEFAULT 'Success',
                    details_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
                """
            )

            # ============ SUBSCRIPTION HISTORY TABLE ============
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saas_subscription_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    history_id TEXT NOT NULL UNIQUE,
                    subscription_id TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    action TEXT NOT NULL,
                    plan_name TEXT,
                    old_plan_name TEXT,
                    amount REAL,
                    status_before TEXT,
                    status_after TEXT,
                    reason TEXT,
                    details_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(subscription_id) REFERENCES saas_subscriptions(subscription_id)
                )
                """
            )

            # ============ SUBSCRIPTION PLANS TABLE ============
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saas_subscription_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plan_id TEXT NOT NULL UNIQUE,
                    plan_name TEXT NOT NULL,
                    plan_tier TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price REAL NOT NULL,
                    currency TEXT NOT NULL DEFAULT 'PKR',
                    billing_cycle TEXT NOT NULL DEFAULT 'monthly',
                    features_json TEXT NOT NULL,
                    max_students INTEGER,
                    max_teachers INTEGER,
                    max_classes INTEGER,
                    school_portal_access INTEGER NOT NULL DEFAULT 1,
                    ai_grading_access INTEGER NOT NULL DEFAULT 0,
                    advanced_analytics INTEGER NOT NULL DEFAULT 0,
                    support_level TEXT NOT NULL DEFAULT 'Basic',
                    is_active INTEGER NOT NULL DEFAULT 1,
                    trial_days INTEGER DEFAULT 0,
                    display_order INTEGER DEFAULT 0,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # ============ FRAUD DETECTION TABLE ============
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saas_fraud_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_id TEXT NOT NULL UNIQUE,
                    payment_id TEXT,
                    user_id INTEGER,
                    username TEXT,
                    fraud_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    suspicious_pattern TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    details_json TEXT,
                    status TEXT NOT NULL DEFAULT 'Investigating',
                    assigned_to TEXT,
                    action_taken TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
                """
            )

            # ============ REVENUE ANALYTICS TABLE ============
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saas_revenue_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    analytics_id TEXT NOT NULL UNIQUE,
                    period_date TIMESTAMP NOT NULL,
                    total_revenue REAL NOT NULL,
                    subscription_revenue REAL NOT NULL,
                    payment_count INTEGER NOT NULL,
                    verified_count INTEGER NOT NULL,
                    pending_count INTEGER NOT NULL,
                    failed_count INTEGER NOT NULL,
                    active_subscriptions INTEGER NOT NULL,
                    new_subscriptions INTEGER NOT NULL,
                    cancelled_subscriptions INTEGER NOT NULL,
                    avg_revenue_per_user REAL NOT NULL,
                    churn_rate REAL NOT NULL,
                    revenue_growth REAL,
                    details_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            self._migrate_schema(conn)
            self._seed_subscription_plans(conn)
            conn.commit()

    def _table_columns(self, conn: sqlite3.Connection, table: str) -> List[str]:
        cur = conn.execute(f"PRAGMA table_info({table})")
        return [row[1] for row in cur.fetchall()]

    def _migrate_schema(self, conn: sqlite3.Connection) -> None:
        """Lightweight SQLite migrations for SaaS columns."""
        subs_cols = self._table_columns(conn, "saas_subscriptions")
        if "plan_id" not in subs_cols:
            conn.execute("ALTER TABLE saas_subscriptions ADD COLUMN plan_id TEXT")
        if "trial_end" not in subs_cols:
            conn.execute("ALTER TABLE saas_subscriptions ADD COLUMN trial_end TIMESTAMP")
        if "is_trial" not in subs_cols:
            conn.execute("ALTER TABLE saas_subscriptions ADD COLUMN is_trial INTEGER NOT NULL DEFAULT 0")

        # ============ BLOCKCHAIN PAYMENT EXTENSIONS ============
        payment_cols = self._table_columns(conn, "saas_payments")

        # Add Solana blockchain columns to saas_payments table
        if "blockchain_network" not in payment_cols:
            conn.execute(
                "ALTER TABLE saas_payments ADD COLUMN blockchain_network TEXT DEFAULT 'devnet'"
            )
        if "wallet_address" not in payment_cols:
            conn.execute(
                "ALTER TABLE saas_payments ADD COLUMN wallet_address TEXT"
            )
        if "transaction_signature" not in payment_cols:
            conn.execute(
                "ALTER TABLE saas_payments ADD COLUMN transaction_signature TEXT"
            )
        if "reference_id" not in payment_cols:
            conn.execute(
                "ALTER TABLE saas_payments ADD COLUMN reference_id TEXT"
            )
        if "sol_amount" not in payment_cols:
            conn.execute(
                "ALTER TABLE saas_payments ADD COLUMN sol_amount REAL"
            )
        if "exchange_rate" not in payment_cols:
            conn.execute(
                "ALTER TABLE saas_payments ADD COLUMN exchange_rate TEXT"  # JSON: {sol_usd, usd_pkr}
            )
        if "blockchain_verified" not in payment_cols:
            conn.execute(
                "ALTER TABLE saas_payments ADD COLUMN blockchain_verified INTEGER DEFAULT 0"
            )
        if "confirmation_count" not in payment_cols:
            conn.execute(
                "ALTER TABLE saas_payments ADD COLUMN confirmation_count INTEGER DEFAULT 0"
            )
        if "verification_response" not in payment_cols:
            conn.execute(
                "ALTER TABLE saas_payments ADD COLUMN verification_response TEXT"  # JSON response
            )
        if "payment_method_type" not in payment_cols:
            conn.execute(
                "ALTER TABLE saas_payments ADD COLUMN payment_method_type TEXT DEFAULT 'manual'"
            )

        # Create Solana blockchain transaction log table
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS solana_blockchain_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_id TEXT NOT NULL UNIQUE,
                payment_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                reference_id TEXT,
                transaction_signature TEXT UNIQUE,
                wallet_address TEXT,
                blockchain_network TEXT DEFAULT 'devnet',
                amount_sol REAL,
                verification_timestamp TIMESTAMP,
                verification_status TEXT DEFAULT 'pending',
                confirmation_count INTEGER DEFAULT 0,
                block_time TIMESTAMP,
                rpc_response_json TEXT,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(payment_id) REFERENCES saas_payments(payment_id)
            )
            """
        )

        # Create index for faster blockchain lookups
        try:
            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_solana_tx_signature ON solana_blockchain_log(transaction_signature)"
            )
        except Exception:
            pass

        try:
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_solana_ref_id ON saas_payments(reference_id) WHERE reference_id IS NOT NULL"
            )
        except Exception:
            pass

        try:
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_solana_wallet ON saas_payments(wallet_address) WHERE wallet_address IS NOT NULL"
            )
        except Exception:
            pass

    def _seed_subscription_plans(self, conn: sqlite3.Connection) -> None:
        """Default FREE / STANDARD / PREMIUM plans (idempotent)."""
        plans = [
            {
                "plan_id": "plan_free",
                "plan_name": "Free",
                "plan_tier": "free",
                "description": "Core grading tools for individuals. No organization school portal.",
                "price": 0.0,
                "features": ["Teacher & student accounts", "Basic AI grading", "No School Portal"],
                "max_students": 50,
                "max_teachers": 5,
                "max_classes": 5,
                "school_portal_access": 0,
                "ai_grading_access": 1,
                "advanced_analytics": 0,
                "support_level": "Community",
                "trial_days": 0,
                "display_order": 1,
            },
            {
                "plan_id": "plan_standard",
                "plan_name": "Standard",
                "plan_tier": "standard",
                "description": "Full School Portal, monthly billing, and collaboration.",
                "price": 4999.0,
                "features": [
                    "Everything in Free",
                    "School Portal access",
                    "School registration",
                    "Monthly billing",
                    "Standard support",
                ],
                "max_students": 5000,
                "max_teachers": 200,
                "max_classes": 200,
                "school_portal_access": 1,
                "ai_grading_access": 1,
                "advanced_analytics": 0,
                "support_level": "Standard",
                "trial_days": 7,
                "display_order": 2,
            },
            {
                "plan_id": "plan_premium",
                "plan_name": "Premium",
                "plan_tier": "premium",
                "description": "Enterprise AI analytics, insights, and priority support.",
                "price": 9999.0,
                "features": [
                    "Everything in Standard",
                    "Advanced AI analytics",
                    "Finance & fraud dashboards",
                    "Priority support",
                ],
                "max_students": 20000,
                "max_teachers": 500,
                "max_classes": 500,
                "school_portal_access": 1,
                "ai_grading_access": 1,
                "advanced_analytics": 1,
                "support_level": "Premium",
                "trial_days": 14,
                "display_order": 3,
            },
        ]
        for p in plans:
            conn.execute(
                """
                INSERT OR IGNORE INTO saas_subscription_plans (
                    plan_id, plan_name, plan_tier, description, price,
                    features_json, billing_cycle, max_students, max_teachers,
                    max_classes, school_portal_access, ai_grading_access,
                    advanced_analytics, support_level, trial_days, display_order
                ) VALUES (?, ?, ?, ?, ?, ?, 'monthly', ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    p["plan_id"],
                    p["plan_name"],
                    p["plan_tier"],
                    p["description"],
                    p["price"],
                    json.dumps(p["features"]),
                    p["max_students"],
                    p["max_teachers"],
                    p["max_classes"],
                    p["school_portal_access"],
                    p["ai_grading_access"],
                    p["advanced_analytics"],
                    p["support_level"],
                    p["trial_days"],
                    p["display_order"],
                ),
            )

    # ============ SUBSCRIPTION OPERATIONS ============

    def create_subscription(
        self,
        subscription_id: str,
        user_id: int,
        username: str,
        plan_name: str,
        plan_tier: str,
        amount: float,
        currency: str = "PKR",
        plan_id: Optional[str] = None,
        trial_days: int = 0,
    ) -> bool:
        """Create a new subscription record (inactive until payment verified)."""
        try:
            with self._connect() as conn:
                start_date = datetime.now()
                expiry_date = start_date + timedelta(days=30)
                trial_end = None
                is_trial = 0
                if trial_days and trial_days > 0:
                    trial_end = start_date + timedelta(days=trial_days)
                    expiry_date = trial_end
                    is_trial = 1

                conn.execute(
                    """
                    INSERT INTO saas_subscriptions (
                        subscription_id, user_id, username, plan_name, plan_tier, plan_id,
                        amount, currency, start_date, expiry_date, trial_end, is_trial,
                        payment_status, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        subscription_id,
                        user_id,
                        username,
                        plan_name,
                        plan_tier,
                        plan_id,
                        amount,
                        currency,
                        start_date,
                        expiry_date,
                        trial_end.isoformat() if trial_end else None,
                        is_trial,
                        "Trial" if is_trial else "Pending",
                        1 if is_trial else 0,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error creating subscription: {e}")
            return False

    def verify_subscription(
        self,
        subscription_id: str,
        payment_status: str = "Verified",
        billing_days: int = 30,
    ) -> bool:
        """Verify and activate a subscription with a fresh billing window."""
        try:
            with self._connect() as conn:
                now = datetime.now()
                expiry = now + timedelta(days=billing_days)
                conn.execute(
                    """
                    UPDATE saas_subscriptions
                    SET payment_status = ?, is_active = 1, is_trial = 0, trial_end = NULL,
                        start_date = ?, expiry_date = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE subscription_id = ?
                    """,
                    (payment_status, now, expiry, subscription_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error verifying subscription: {e}")
            return False

    def get_subscription(self, subscription_id: str) -> Optional[Dict]:
        """Get subscription details."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT * FROM saas_subscriptions WHERE subscription_id = ?",
                    (subscription_id,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting subscription: {e}")
            return None

    def get_user_subscription(self, user_id: int) -> Optional[Dict]:
        """Prefer the latest active subscription row for this user."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM saas_subscriptions
                    WHERE user_id = ? AND is_active = 1
                    ORDER BY updated_at DESC, created_at DESC LIMIT 1
                    """,
                    (user_id,),
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                cursor = conn.execute(
                    """
                    SELECT * FROM saas_subscriptions
                    WHERE user_id = ?
                    ORDER BY created_at DESC LIMIT 1
                    """,
                    (user_id,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting user subscription: {e}")
            return None

    def get_latest_subscription_row(self, user_id: int) -> Optional[Dict]:
        """Latest subscription regardless of active flag (for status UI)."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM saas_subscriptions
                    WHERE user_id = ?
                    ORDER BY created_at DESC LIMIT 1
                    """,
                    (user_id,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting latest subscription: {e}")
            return None

    def has_active_subscription(self, user_id: int) -> bool:
        """True when user has verified (or trial) access with a plan that includes School Portal."""
        return self.has_active_school_saas_subscription(user_id)

    def has_active_school_saas_subscription(self, user_id: int) -> bool:
        """
        Paid / trial access that unlocks school registration & portal.
        Requires plan.school_portal_access = 1 and non-expired window.
        """
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT s.id
                    FROM saas_subscriptions s
                    JOIN saas_subscription_plans p ON p.plan_name = s.plan_name
                    WHERE s.user_id = ?
                      AND s.is_active = 1
                      AND p.school_portal_access = 1
                      AND datetime(s.expiry_date) > datetime('now')
                      AND s.payment_status IN ('Verified', 'Trial')
                    ORDER BY s.created_at DESC
                    LIMIT 1
                    """,
                    (user_id,),
                )
                return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error checking school SaaS subscription: {e}")
            return False

    # ============ PAYMENT OPERATIONS ============

    def create_payment(
        self,
        payment_id: str,
        subscription_id: str,
        user_id: int,
        username: str,
        amount: float,
        payment_method: str,
        currency: str = "PKR",
    ) -> bool:
        """Create a new payment record."""
        try:
            with self._connect() as conn:
                expiry_date = datetime.now() + timedelta(hours=24)
                conn.execute(
                    """
                    INSERT INTO saas_payments (
                        payment_id, subscription_id, user_id, username, amount,
                        currency, payment_method, status, expiry_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        payment_id,
                        subscription_id,
                        user_id,
                        username,
                        amount,
                        currency,
                        payment_method,
                        "Pending",
                        expiry_date,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error creating payment: {e}")
            return False

    def verify_payment(
        self,
        payment_id: str,
        verified_by: str,
        verification_notes: str = "",
        transaction_id: Optional[str] = None,
    ) -> bool:
        """Verify a payment, activate subscription, invoice, and history."""
        try:
            payment = self.get_payment(payment_id)
            if not payment:
                return False
            tid = transaction_id or payment.get("transaction_id")
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE saas_payments
                    SET status = 'Verified', verified_by = ?, verification_notes = ?,
                        transaction_id = COALESCE(?, transaction_id),
                        verified_date = CURRENT_TIMESTAMP,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE payment_id = ?
                    """,
                    (verified_by, verification_notes, tid, payment_id),
                )
                conn.execute(
                    """
                    UPDATE saas_subscriptions
                    SET payment_status = 'Verified', is_active = 1, is_trial = 0,
                        start_date = ?, expiry_date = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE subscription_id = ?
                    """,
                    (
                        datetime.now(),
                        datetime.now() + timedelta(days=30),
                        payment["subscription_id"],
                    ),
                )
                conn.commit()

            self._append_subscription_history(
                payment["subscription_id"],
                payment["user_id"],
                payment["username"],
                "payment_verified",
                {"payment_id": payment_id, "verified_by": verified_by},
            )
            self._create_invoice_for_payment(payment_id)
            return True
        except Exception as e:
            print(f"Error verifying payment: {e}")
            return False

    def reject_payment(
        self, payment_id: str, verified_by: str, reason: str = ""
    ) -> bool:
        """Reject a payment and deactivate the linked subscription."""
        try:
            payment = self.get_payment(payment_id)
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE saas_payments
                    SET status = 'Rejected', verified_by = ?, verification_notes = ?,
                        verified_date = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                    WHERE payment_id = ?
                    """,
                    (verified_by, reason, payment_id),
                )
                if payment:
                    conn.execute(
                        """
                        UPDATE saas_subscriptions
                        SET is_active = 0, payment_status = 'Rejected',
                            updated_at = CURRENT_TIMESTAMP
                        WHERE subscription_id = ?
                        """,
                        (payment["subscription_id"],),
                    )
                conn.commit()
            if payment:
                self._append_subscription_history(
                    payment["subscription_id"],
                    payment["user_id"],
                    payment["username"],
                    "payment_rejected",
                    {"payment_id": payment_id, "reason": reason},
                )
            return True
        except Exception as e:
            print(f"Error rejecting payment: {e}")
            return False

    def mark_payment_refunded(self, payment_id: str, admin_username: str, notes: str = "") -> bool:
        try:
            payment = self.get_payment(payment_id)
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE saas_payments
                    SET status = 'Refunded', verified_by = ?, verification_notes = ?,
                        verified_date = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                    WHERE payment_id = ?
                    """,
                    (admin_username, notes, payment_id),
                )
                if payment:
                    conn.execute(
                        """
                        UPDATE saas_subscriptions
                        SET is_active = 0, payment_status = 'Refunded',
                            updated_at = CURRENT_TIMESTAMP
                        WHERE subscription_id = ?
                        """,
                        (payment["subscription_id"],),
                    )
                conn.commit()
            return True
        except Exception as e:
            print(f"Error refunding payment: {e}")
            return False

    def expire_stale_pending_payments(self) -> int:
        """Mark pending payments past expiry_date as Expired (returns count)."""
        try:
            with self._connect() as conn:
                cur = conn.execute(
                    """
                    UPDATE saas_payments
                    SET status = 'Expired', updated_at = CURRENT_TIMESTAMP
                    WHERE status = 'Pending' AND datetime(expiry_date) < datetime('now')
                    """
                )
                conn.commit()
                return int(cur.rowcount or 0)
        except Exception as e:
            print(f"Error expiring payments: {e}")
            return 0

    def deactivate_expired_subscriptions(self) -> int:
        """Deactivate subscriptions past expiry_date."""
        try:
            with self._connect() as conn:
                cur = conn.execute(
                    """
                    UPDATE saas_subscriptions
                    SET is_active = 0, payment_status = 'Expired', updated_at = CURRENT_TIMESTAMP
                    WHERE is_active = 1
                      AND datetime(expiry_date) < datetime('now')
                      AND payment_status IN ('Verified', 'Trial')
                    """
                )
                conn.commit()
                return int(cur.rowcount or 0)
        except Exception as e:
            print(f"Error expiring subscriptions: {e}")
            return 0

    def submit_payment_proof(
        self,
        payment_id: str,
        transaction_id: str,
        receipt_path: Optional[str] = None,
        receipt_filename: Optional[str] = None,
    ) -> bool:
        """Attach proof and transaction id while awaiting admin verification."""
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE saas_payments
                    SET transaction_id = ?, receipt_path = COALESCE(?, receipt_path),
                        receipt_filename = COALESCE(?, receipt_filename),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE payment_id = ?
                    """,
                    (transaction_id, receipt_path, receipt_filename, payment_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving payment proof: {e}")
            return False

    def suspend_subscription(self, subscription_id: str, reason: str = "") -> bool:
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE saas_subscriptions
                    SET is_active = 0, payment_status = 'Suspended', notes = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE subscription_id = ?
                    """,
                    (reason, subscription_id),
                )
                conn.commit()
            return True
        except Exception as e:
            print(f"Error suspending subscription: {e}")
            return False

    def deactivate_school(self, school_id: str, reason: str = "") -> bool:
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE saas_schools
                    SET status = 'Suspended', notes = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE school_id = ?
                    """,
                    (reason, school_id),
                )
                conn.commit()
            return True
        except Exception as e:
            print(f"Error deactivating school: {e}")
            return False

    def get_plan_by_plan_name(self, plan_name: str) -> Optional[Dict]:
        try:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT * FROM saas_subscription_plans WHERE plan_name = ?",
                    (plan_name,),
                ).fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error loading plan: {e}")
            return None

    def get_plan_by_plan_id(self, plan_id: str) -> Optional[Dict]:
        return self.get_subscription_plan(plan_id)

    def list_user_payments(self, user_id: int, limit: int = 50) -> List[Dict]:
        try:
            with self._connect() as conn:
                cur = conn.execute(
                    """
                    SELECT * FROM saas_payments
                    WHERE user_id = ?
                    ORDER BY payment_date DESC
                    LIMIT ?
                    """,
                    (user_id, limit),
                )
                return [dict(r) for r in cur.fetchall()]
        except Exception as e:
            print(f"Error listing payments: {e}")
            return []

    def get_revenue_summary(self) -> Dict[str, Any]:
        """Aggregate verified revenue for dashboards."""
        try:
            with self._connect() as conn:
                row = conn.execute(
                    """
                    SELECT
                        COUNT(*) AS cnt,
                        COALESCE(SUM(amount), 0) AS total,
                        SUM(CASE WHEN status = 'Verified' THEN amount ELSE 0 END) AS verified_total,
                        SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) AS pending_cnt
                    FROM saas_payments
                    """
                ).fetchone()
                return dict(row) if row else {}
        except Exception as e:
            print(f"Error revenue summary: {e}")
            return {}

    def count_duplicate_transaction_ids(self, transaction_id: str, exclude_payment_id: str) -> int:
        if not transaction_id:
            return 0
        try:
            with self._connect() as conn:
                cur = conn.execute(
                    """
                    SELECT COUNT(*) FROM saas_payments
                    WHERE transaction_id = ? AND payment_id != ?
                    """,
                    (transaction_id, exclude_payment_id),
                )
                return int(cur.fetchone()[0])
        except Exception as e:
            print(f"Error duplicate txn check: {e}")
            return 0

    def insert_fraud_alert(
        self,
        alert_id: str,
        fraud_type: str,
        severity: str,
        pattern: str,
        confidence: float,
        user_id: Optional[int],
        username: Optional[str],
        payment_id: Optional[str],
        details: Optional[Dict] = None,
    ) -> bool:
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO saas_fraud_alerts (
                        alert_id, payment_id, user_id, username, fraud_type,
                        severity, suspicious_pattern, confidence_score, details_json, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Investigating')
                    """,
                    (
                        alert_id,
                        payment_id,
                        user_id,
                        username,
                        fraud_type,
                        severity,
                        pattern,
                        confidence,
                        json.dumps(details or {}),
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error fraud alert: {e}")
            return False

    def _append_subscription_history(
        self,
        subscription_id: str,
        user_id: int,
        username: str,
        action: str,
        details: Optional[Dict],
    ) -> None:
        hid = f"HIST-{uuid.uuid4().hex[:16].upper()}"
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO saas_subscription_history (
                        history_id, subscription_id, user_id, username, action,
                        details_json
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (hid, subscription_id, user_id, username, action, json.dumps(details or {})),
                )
                conn.commit()
        except Exception as e:
            print(f"Error subscription history: {e}")

    def _create_invoice_for_payment(self, payment_id: str) -> Optional[str]:
        payment = self.get_payment(payment_id)
        if not payment:
            return None
        try:
            with self._connect() as conn:
                exists = conn.execute(
                    "SELECT 1 FROM saas_invoices WHERE payment_id = ? LIMIT 1",
                    (payment_id,),
                ).fetchone()
                if exists:
                    return None
        except Exception:
            pass
        invoice_id = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        inv_no = f"INV-{payment_id[-8:]}"
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO saas_invoices (
                        invoice_id, payment_id, subscription_id, user_id, username,
                        invoice_number, amount, currency, total_amount, status,
                        description, payment_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Paid', ?, CURRENT_TIMESTAMP)
                    """,
                    (
                        invoice_id,
                        payment_id,
                        payment["subscription_id"],
                        payment["user_id"],
                        payment["username"],
                        inv_no,
                        payment["amount"],
                        payment["currency"],
                        payment["amount"],
                        f"Subscription payment {payment_id}",
                    ),
                )
                conn.commit()
            return invoice_id
        except Exception as e:
            print(f"Error creating invoice: {e}")
            return None

    def get_payment(self, payment_id: str) -> Optional[Dict]:
        """Get payment details."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT * FROM saas_payments WHERE payment_id = ?", (payment_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting payment: {e}")
            return None

    def get_pending_payments(self) -> List[Dict]:
        """Get all pending payments."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM saas_payments
                    WHERE status = 'Pending' AND is_expired = 0
                    ORDER BY payment_date DESC
                    """
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting pending payments: {e}")
            return []

    def update_payment_receipt(self, payment_id: str, receipt_path: str) -> bool:
        """Update payment receipt path."""
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE saas_payments
                    SET receipt_path = ?, receipt_filename = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE payment_id = ?
                    """,
                    (receipt_path, receipt_path.split("/")[-1], payment_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating payment receipt: {e}")
            return False

    # ============ SCHOOL OPERATIONS ============

    def register_school(
        self,
        school_id: str,
        owner_user_id: int,
        owner_username: str,
        school_name: str,
        principal_name: str,
        school_email: str,
        school_phone: str,
        school_address: str,
        city: str,
        country: str,
        school_type: str,
        subscription_id: str,
        registration_number: str = "",
        website: str = "",
        total_students: int = 0,
        school_logo_path: Optional[str] = None,
    ) -> bool:
        """Register a new school (owner must have active paid SaaS plan)."""
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO saas_schools (
                        school_id, owner_user_id, owner_username, school_name,
                        school_logo_path, principal_name, school_email, school_phone, school_address,
                        city, country, school_type, subscription_id, registration_number,
                        website, total_students, verification_status, subscription_status, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Verified', 'Active', 'Active')
                    """,
                    (
                        school_id,
                        owner_user_id,
                        owner_username,
                        school_name,
                        school_logo_path,
                        principal_name,
                        school_email,
                        school_phone,
                        school_address,
                        city,
                        country,
                        school_type,
                        subscription_id,
                        registration_number,
                        website,
                        total_students,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error registering school: {e}")
            return False

    def get_school(self, school_id: str) -> Optional[Dict]:
        """Get school details."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT * FROM saas_schools WHERE school_id = ?", (school_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting school: {e}")
            return None

    def get_user_school(self, user_id: int) -> Optional[Dict]:
        """Get user's registered school."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM saas_schools
                    WHERE owner_user_id = ? AND status = 'Active'
                    ORDER BY registration_date DESC LIMIT 1
                    """,
                    (user_id,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting user school: {e}")
            return None

    def get_active_school_subscription(self, user_id: int) -> Optional[Dict]:
        """Return the subscription row that currently unlocks school SaaS features."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT s.*
                    FROM saas_subscriptions s
                    JOIN saas_subscription_plans p ON p.plan_name = s.plan_name
                    WHERE s.user_id = ?
                      AND s.is_active = 1
                      AND p.school_portal_access = 1
                      AND datetime(s.expiry_date) > datetime('now')
                      AND s.payment_status IN ('Verified', 'Trial')
                    ORDER BY s.created_at DESC
                    LIMIT 1
                    """,
                    (user_id,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error get_active_school_subscription: {e}")
            return None

    def has_registered_school(self, user_id: int) -> bool:
        """Check if user has registered school."""
        return self.get_user_school(user_id) is not None

    def verify_school(self, school_id: str, verified_by: str) -> bool:
        """Verify a school registration."""
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    UPDATE saas_schools
                    SET verification_status = 'Verified', verified_by = ?,
                        verified_date = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                    WHERE school_id = ?
                    """,
                    (verified_by, school_id),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error verifying school: {e}")
            return False

    # ============ SUBSCRIPTION PLANS ============

    def create_subscription_plan(
        self,
        plan_id: str,
        plan_name: str,
        plan_tier: str,
        description: str,
        price: float,
        features: Dict,
        billing_cycle: str = "monthly",
        max_students: int = None,
        max_teachers: int = None,
        max_classes: int = None,
        school_portal_access: bool = True,
        ai_grading_access: bool = False,
        advanced_analytics: bool = False,
        support_level: str = "Basic",
        trial_days: int = 0,
    ) -> bool:
        """Create a subscription plan."""
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO saas_subscription_plans (
                        plan_id, plan_name, plan_tier, description, price,
                        features_json, billing_cycle, max_students, max_teachers,
                        max_classes, school_portal_access, ai_grading_access,
                        advanced_analytics, support_level, trial_days
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        plan_id,
                        plan_name,
                        plan_tier,
                        description,
                        price,
                        json.dumps(features),
                        billing_cycle,
                        max_students,
                        max_teachers,
                        max_classes,
                        1 if school_portal_access else 0,
                        1 if ai_grading_access else 0,
                        1 if advanced_analytics else 0,
                        support_level,
                        trial_days,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error creating subscription plan: {e}")
            return False

    def get_subscription_plans(self) -> List[Dict]:
        """Get all active subscription plans."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM saas_subscription_plans
                    WHERE is_active = 1
                    ORDER BY display_order, price
                    """
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting subscription plans: {e}")
            return []

    def get_subscription_plan(self, plan_id: str) -> Optional[Dict]:
        """Get specific subscription plan."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT * FROM saas_subscription_plans WHERE plan_id = ?",
                    (plan_id,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting subscription plan: {e}")
            return None

    # ============ REVENUE ANALYTICS ============

    def get_revenue_analytics(self, period_date: str = None) -> Optional[Dict]:
        """Get revenue analytics for a period."""
        try:
            with self._connect() as conn:
                if period_date:
                    cursor = conn.execute(
                        "SELECT * FROM saas_revenue_analytics WHERE period_date = ?",
                        (period_date,),
                    )
                else:
                    cursor = conn.execute(
                        """
                        SELECT * FROM saas_revenue_analytics
                        ORDER BY period_date DESC LIMIT 1
                        """
                    )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting revenue analytics: {e}")
            return None

    def update_revenue_analytics(self) -> bool:
        """Update daily revenue analytics."""
        try:
            with self._connect() as conn:
                # Calculate today's metrics
                today = datetime.now().strftime("%Y-%m-%d")

                # Get payment metrics
                cursor = conn.execute(
                    """
                    SELECT
                        SUM(amount) as total_revenue,
                        COUNT(*) as payment_count,
                        SUM(CASE WHEN status = 'Verified' THEN 1 ELSE 0 END) as verified_count,
                        SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending_count,
                        SUM(CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END) as failed_count
                    FROM saas_payments
                    WHERE DATE(payment_date) = ?
                    """,
                    (today,),
                )
                payment_data = dict(cursor.fetchone())

                # Get subscription metrics
                cursor = conn.execute(
                    """
                    SELECT
                        COUNT(*) as active_subscriptions,
                        COUNT(CASE WHEN DATE(start_date) = ? THEN 1 END) as new_subscriptions,
                        COUNT(CASE WHEN DATE(cancellation_date) = ? THEN 1 END) as cancelled_subscriptions
                    FROM saas_subscriptions
                    WHERE is_active = 1
                    """,
                    (today, today),
                )
                subscription_data = dict(cursor.fetchone())

                # Insert analytics record
                analytics_id = f"ANA-{datetime.now().timestamp()}"
                conn.execute(
                    """
                    INSERT INTO saas_revenue_analytics (
                        analytics_id, period_date, total_revenue, subscription_revenue,
                        payment_count, verified_count, pending_count, failed_count,
                        active_subscriptions, new_subscriptions, cancelled_subscriptions,
                        avg_revenue_per_user, churn_rate
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        analytics_id,
                        today,
                        payment_data.get("total_revenue") or 0,
                        payment_data.get("total_revenue") or 0,
                        payment_data.get("payment_count") or 0,
                        payment_data.get("verified_count") or 0,
                        payment_data.get("pending_count") or 0,
                        payment_data.get("failed_count") or 0,
                        subscription_data.get("active_subscriptions") or 0,
                        subscription_data.get("new_subscriptions") or 0,
                        subscription_data.get("cancelled_subscriptions") or 0,
                        0,
                        0,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating revenue analytics: {e}")
            return False

    # ============ ACTIVITY LOGGING ============

    def log_activity(
        self,
        log_id: str,
        user_id: int,
        username: str,
        activity_type: str,
        activity_description: str,
        resource_type: str = None,
        resource_id: str = None,
        status: str = "Success",
        details: Dict = None,
    ) -> bool:
        """Log user activity."""
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO saas_activity_logs (
                        log_id, user_id, username, activity_type, activity_description,
                        resource_type, resource_id, status, details_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        log_id,
                        user_id,
                        username,
                        activity_type,
                        activity_description,
                        resource_type,
                        resource_id,
                        status,
                        json.dumps(details) if details else None,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False

    # ============ BLOCKCHAIN PAYMENT METHODS (SOLANA) ============

    def create_blockchain_payment_entry(
        self,
        payment_id: str,
        reference_id: str,
        wallet_address: str,
        sol_amount: float,
        exchange_rate_json: str,
        blockchain_network: str = "devnet",
    ) -> bool:
        """Create blockchain payment entry (called when user initiates Solana pay)."""
        try:
            with self._connect() as conn:
                # Update saas_payments with blockchain fields
                conn.execute(
                    """
                    UPDATE saas_payments
                    SET reference_id = ?, wallet_address = ?, sol_amount = ?,
                        exchange_rate = ?, blockchain_network = ?,
                        payment_method_type = 'blockchain',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE payment_id = ?
                    """,
                    (
                        reference_id,
                        wallet_address,
                        sol_amount,
                        exchange_rate_json,
                        blockchain_network,
                        payment_id,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error creating blockchain payment entry: {e}")
            return False

    def record_blockchain_transaction(
        self,
        log_id: str,
        payment_id: str,
        user_id: int,
        username: str,
        reference_id: str,
        transaction_signature: str,
        wallet_address: str,
        amount_sol: float,
        blockchain_network: str = "devnet",
        rpc_response: Optional[Dict] = None,
    ) -> bool:
        """Record blockchain transaction in solana_blockchain_log."""
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO solana_blockchain_log (
                        log_id, payment_id, user_id, username, reference_id,
                        transaction_signature, wallet_address, blockchain_network,
                        amount_sol, verification_status, rpc_response_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
                    """,
                    (
                        log_id,
                        payment_id,
                        user_id,
                        username,
                        reference_id,
                        transaction_signature,
                        wallet_address,
                        blockchain_network,
                        amount_sol,
                        json.dumps(rpc_response or {}),
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error recording blockchain transaction: {e}")
            return False

    def update_blockchain_verification(
        self,
        payment_id: str,
        transaction_signature: str,
        confirmation_count: int,
        verification_status: str = "verified",
        verification_response: Optional[Dict] = None,
    ) -> bool:
        """Update blockchain verification status in both tables."""
        try:
            with self._connect() as conn:
                # Update saas_payments
                conn.execute(
                    """
                    UPDATE saas_payments
                    SET transaction_signature = ?, blockchain_verified = 1,
                        confirmation_count = ?, verification_response = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE payment_id = ?
                    """,
                    (
                        transaction_signature,
                        confirmation_count,
                        json.dumps(verification_response or {}),
                        payment_id,
                    ),
                )

                # Update solana_blockchain_log
                conn.execute(
                    """
                    UPDATE solana_blockchain_log
                    SET verification_status = ?, confirmation_count = ?,
                        verification_timestamp = CURRENT_TIMESTAMP,
                        rpc_response_json = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE transaction_signature = ?
                    """,
                    (
                        verification_status,
                        confirmation_count,
                        json.dumps(verification_response or {}),
                        transaction_signature,
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating blockchain verification: {e}")
            return False

    def get_blockchain_payment_by_reference(
        self, reference_id: str
    ) -> Optional[Dict]:
        """Get payment record by reference_id (Solana payment reference)."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT * FROM saas_payments WHERE reference_id = ?",
                    (reference_id,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting blockchain payment by reference: {e}")
            return None

    def get_blockchain_transaction_log(
        self, transaction_signature: str
    ) -> Optional[Dict]:
        """Get blockchain transaction log by signature."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT * FROM solana_blockchain_log WHERE transaction_signature = ?",
                    (transaction_signature,),
                )
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error getting blockchain transaction log: {e}")
            return None

    def get_pending_blockchain_verifications(
        self, limit: int = 50
    ) -> List[Dict]:
        """Get all pending blockchain verifications (not yet confirmed on-chain)."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM solana_blockchain_log
                    WHERE verification_status = 'pending'
                    ORDER BY created_at ASC
                    LIMIT ?
                    """,
                    (limit,),
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting pending blockchain verifications: {e}")
            return []

    def mark_blockchain_payment_verified(
        self,
        payment_id: str,
        verified_by: str = "blockchain_auto",
        verification_notes: str = "",
    ) -> bool:
        """Mark blockchain payment as verified (after on-chain confirmation)."""
        try:
            payment = self.get_payment(payment_id)
            if not payment:
                return False

            with self._connect() as conn:
                # Update saas_payments
                conn.execute(
                    """
                    UPDATE saas_payments
                    SET status = 'Verified', verified_by = ?,
                        verification_notes = ?, verified_date = CURRENT_TIMESTAMP,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE payment_id = ?
                    """,
                    (
                        verified_by,
                        f"Blockchain verified: {verification_notes}",
                        payment_id,
                    ),
                )

                # Verify the subscription
                conn.execute(
                    """
                    UPDATE saas_subscriptions
                    SET payment_status = 'Verified', is_active = 1, is_trial = 0,
                        start_date = ?, expiry_date = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE subscription_id = ?
                    """,
                    (
                        datetime.now(),
                        datetime.now() + timedelta(days=30),
                        payment["subscription_id"],
                    ),
                )
                conn.commit()

            # Log subscription history
            self._append_subscription_history(
                payment["subscription_id"],
                payment["user_id"],
                payment["username"],
                "blockchain_payment_verified",
                {
                    "payment_id": payment_id,
                    "verified_by": verified_by,
                },
            )
            return True
        except Exception as e:
            print(f"Error marking blockchain payment verified: {e}")
            return False

    def record_blockchain_verification_error(
        self,
        log_id: str,
        payment_id: str,
        transaction_signature: str,
        error_message: str,
        blockchain_network: str = "devnet",
    ) -> bool:
        """Record blockchain verification error."""
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO solana_blockchain_log (
                        log_id, payment_id, transaction_signature, blockchain_network,
                        verification_status, error_message, updated_at
                    ) VALUES (?, ?, ?, ?, 'error', ?, CURRENT_TIMESTAMP)
                    """,
                    (log_id, payment_id, transaction_signature, blockchain_network, error_message),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"Error recording blockchain verification error: {e}")
            return False

    def get_user_blockchain_transactions(
        self, user_id: int, limit: int = 50
    ) -> List[Dict]:
        """Get all blockchain transactions for a user."""
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    """
                    SELECT * FROM solana_blockchain_log
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                    """,
                    (user_id, limit),
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting user blockchain transactions: {e}")
            return []

    def get_blockchain_payment_summary(self) -> Dict[str, Any]:
        """Get aggregate blockchain payment summary."""
        try:
            with self._connect() as conn:
                row = conn.execute(
                    """
                    SELECT
                        COUNT(*) AS total_blockchain_payments,
                        COUNT(CASE WHEN blockchain_verified = 1 THEN 1 END) AS verified_count,
                        COUNT(CASE WHEN blockchain_verified = 0 THEN 1 END) AS pending_count,
                        COALESCE(SUM(sol_amount), 0) AS total_sol_volume,
                        COALESCE(SUM(amount), 0) AS total_pkr_volume
                    FROM saas_payments
                    WHERE payment_method_type = 'blockchain'
                    """
                ).fetchone()
                return dict(row) if row else {}
        except Exception as e:
            print(f"Error getting blockchain payment summary: {e}")
            return {}
