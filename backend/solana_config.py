"""
Solana payment configuration and constants.

Centralized configuration for Solana blockchain integration.
Supports Devnet/Mainnet switching and environment variable overrides.
"""

import os
from typing import Optional


class SolanaConfig:
    """Solana blockchain configuration container."""

    # ============ NETWORK CONFIGURATION ============
    # Default: Devnet (safe testing). Change to 'mainnet-beta' for production.
    NETWORK: str = os.getenv("SOLANA_NETWORK", "devnet")

    # RPC URLs
    DEVNET_RPC_URL: str = "https://api.devnet.solana.com"
    MAINNET_RPC_URL: str = "https://api.mainnet-beta.solana.com"

    # Get active RPC URL from environment or use network default
    RPC_URL: str = os.getenv(
        "SOLANA_RPC_URL",
        DEVNET_RPC_URL if NETWORK == "devnet" else MAINNET_RPC_URL,
    )

    # ============ PAYMENT RECEIVER WALLET ============
    # Must be set in .env. Example: SOLANA_RECEIVER_WALLET=YOUR_WALLET_ADDRESS
    RECEIVER_WALLET: Optional[str] = os.getenv("SOLANA_RECEIVER_WALLET")

    # ============ PAYMENT CONFIGURATION ============
    # Payment request expiry time in seconds (default: 15 minutes)
    PAYMENT_TIMEOUT_SECONDS: int = int(os.getenv("SOLANA_PAYMENT_TIMEOUT", "900"))

    # Transaction confirmation timeout in seconds (default: 2 minutes)
    CONFIRMATION_TIMEOUT_SECONDS: int = int(
        os.getenv("SOLANA_CONFIRMATION_TIMEOUT", "120")
    )

    # Minimum confirmations required for payment to be considered final
    MIN_CONFIRMATIONS: int = int(os.getenv("SOLANA_MIN_CONFIRMATIONS", "3"))

    # ============ SOLANA PAY CONFIGURATION ============
    # Solana Pay label (appears in wallet)
    SOLANA_PAY_LABEL: str = "School SaaS"

    # ============ SOL/PKR CONVERSION ============
    # CoinGecko API for real-time SOL price
    COINGECKO_API_URL: str = "https://api.coingecko.com/api/v3"

    # Cache currency conversion for N seconds (default: 300 = 5 minutes)
    PRICE_CACHE_SECONDS: int = int(os.getenv("PRICE_CACHE_SECONDS", "300"))

    # Fallback SOL/USD rate if API fails (as of May 2026, example value)
    FALLBACK_SOL_USD_RATE: float = float(os.getenv("FALLBACK_SOL_USD_RATE", "142.50"))

    # Fallback USD/PKR rate if API fails
    FALLBACK_USD_PKR_RATE: float = float(os.getenv("FALLBACK_USD_PKR_RATE", "277.50"))

    # ============ SUBSCRIPTION PLANS ============
    # Plan definitions (will be stored in DB, but defaults provided here)
    DEFAULT_PLANS = {
        "standard": {
            "plan_name": "Standard",
            "price_pkr": 5000,  # PKR per month
            "description": "Monthly subscription with school portal access",
            "features": [
                "School portal access",
                "Up to 1,000 student records",
                "Basic analytics",
                "Email support",
                "Monthly renewal",
            ],
            "school_portal_access": True,
            "monthly_price_pkr": 5000,
        },
        "premium": {
            "plan_name": "Premium",
            "price_pkr": 10000,  # PKR per month
            "description": "Premium subscription with advanced features",
            "features": [
                "Everything in Standard",
                "Up to 5,000 student records",
                "Advanced analytics & reporting",
                "Priority support",
                "API access",
                "Monthly renewal",
            ],
            "school_portal_access": True,
            "monthly_price_pkr": 10000,
        },
    }

    # ============ SECURITY ============
    # Transaction replay prevention - unique nonce prefix
    TRANSACTION_NONCE_PREFIX: str = "SOL-SCHOOL-SAAS"

    # ============ VALIDATION ============
    # Min/Max SOL amounts for payments (prevent accidental overpayment)
    MIN_SOL_AMOUNT: float = float(os.getenv("MIN_SOL_AMOUNT", "0.01"))
    MAX_SOL_AMOUNT: float = float(os.getenv("MAX_SOL_AMOUNT", "100.0"))

    # ============ LOGGING ============
    # Enable detailed blockchain logging
    DEBUG_BLOCKCHAIN: bool = os.getenv("DEBUG_BLOCKCHAIN", "false").lower() == "true"

    @classmethod
    def validate(cls) -> tuple[bool, str]:
        """
        Validate critical configuration values.

        Returns:
            (is_valid, error_message)
        """
        if not cls.RECEIVER_WALLET:
            return False, "SOLANA_RECEIVER_WALLET not set in environment"

        if cls.NETWORK not in ["devnet", "mainnet-beta"]:
            return False, f"Invalid NETWORK: {cls.NETWORK}. Use 'devnet' or 'mainnet-beta'"

        if cls.MIN_CONFIRMATIONS < 1:
            return False, "MIN_CONFIRMATIONS must be >= 1"

        if cls.PAYMENT_TIMEOUT_SECONDS < 60:
            return False, "PAYMENT_TIMEOUT_SECONDS should be >= 60"

        return True, "Configuration valid"

    @classmethod
    def get_summary(cls) -> dict:
        """Get configuration summary for logging/debugging."""
        return {
            "network": cls.NETWORK,
            "rpc_url": cls.RPC_URL,
            "receiver_wallet": cls.RECEIVER_WALLET[:8] + "..." if cls.RECEIVER_WALLET else "NOT SET",
            "payment_timeout_seconds": cls.PAYMENT_TIMEOUT_SECONDS,
            "confirmation_timeout_seconds": cls.CONFIRMATION_TIMEOUT_SECONDS,
            "min_confirmations": cls.MIN_CONFIRMATIONS,
            "debug_mode": cls.DEBUG_BLOCKCHAIN,
        }
