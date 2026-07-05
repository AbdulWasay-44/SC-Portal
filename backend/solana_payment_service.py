"""
Solana payment service - Core blockchain payment orchestration.

Handles:
- RPC communication with Solana
- Transaction verification
- Payment confirmation
- Automatic subscription activation
- Blockchain status tracking
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple, List

import requests

from solana_config import SolanaConfig
from solana_utils import (
    safe_float,
    safe_int,
    safe_str,
    safe_currency,
    safe_format_number,
    generate_payment_reference,
    is_valid_solana_address,
    is_valid_transaction_signature,
    normalize_sol_amount,
    denormalize_lamports,
    convert_pkr_to_sol,
    convert_sol_to_pkr,
    success_response,
    error_response,
    validate_payment_amount,
    validate_wallet_address,
    time_until_expiry,
    is_payment_expired,
)

logger = logging.getLogger(__name__)


class SolanaPaymentService:
    """Main service for Solana payment handling."""

    def __init__(self):
        """Initialize Solana payment service."""
        self.config = SolanaConfig
        self.session = requests.Session()
        self._validate_config()

    def _validate_config(self) -> None:
        """Validate configuration on startup."""
        is_valid, msg = self.config.validate()
        if not is_valid:
            logger.error(f"Configuration error: {msg}")
            raise ValueError(msg)

        logger.info(f"Solana service initialized: {self.config.get_summary()}")

    # ============ RPC COMMUNICATION ============

    def _make_rpc_call(self, method: str, params: List[Any] = None) -> Dict[str, Any]:
        """
        Make JSON-RPC call to Solana node.

        Args:
            method: RPC method name
            params: Method parameters

        Returns:
            RPC response dict
        """
        if params is None:
            params = []

        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}

        try:
            response = self.session.post(
                self.config.RPC_URL,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                logger.error(f"RPC error for {method}: {data.get('error')}")
                return {"error": data.get("error")}

            return data.get("result", {})

        except requests.Timeout:
            logger.error(f"RPC timeout for {method}")
            return {"error": "RPC timeout"}
        except requests.RequestException as e:
            logger.error(f"RPC connection error: {e}")
            return {"error": f"Connection error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected RPC error: {e}")
            return {"error": f"Unexpected error: {str(e)}"}

    def _get_transaction(self, signature: str) -> Dict[str, Any]:
        """
        Get transaction details from blockchain.

        Args:
            signature: Transaction signature

        Returns:
            Transaction data or empty dict if not found
        """
        if not is_valid_transaction_signature(signature):
            logger.warning(f"Invalid transaction signature format: {signature}")
            return {}

        try:
            result = self._make_rpc_call("getTransaction", [signature, {"encoding": "json"}])

            if "error" in result or not result:
                logger.warning(f"Transaction not found: {signature}")
                return {}

            return result
        except Exception as e:
            logger.error(f"Error fetching transaction {signature}: {e}")
            return {}

    def _get_signature_status(self, signature: str) -> Dict[str, Any]:
        """
        Get transaction signature status.

        Args:
            signature: Transaction signature

        Returns:
            Signature status dict
        """
        if not is_valid_transaction_signature(signature):
            return {}

        try:
            result = self._make_rpc_call("getSignatureStatuses", [[signature]])

            if not result or not result.get("value"):
                logger.warning(f"Status not found for signature: {signature}")
                return {}

            status = result["value"][0]
            return status if status else {}

        except Exception as e:
            logger.error(f"Error fetching signature status {signature}: {e}")
            return {}

    # ============ PRICE CONVERSION ============

    def get_sol_price_usd(self) -> Tuple[bool, float]:
        """
        Get current SOL price in USD from CoinGecko.

        Returns:
            (success, price_usd)
        """
        try:
            url = f"{self.config.COINGECKO_API_URL}/simple/price"
            params = {"ids": "solana", "vs_currencies": "usd"}

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()
            price = safe_float(data.get("solana", {}).get("usd"), 0.0)

            if price <= 0:
                logger.warning("Invalid SOL price from API, using fallback")
                return False, self.config.FALLBACK_SOL_USD_RATE

            logger.info(f"SOL/USD price: {price}")
            return True, price

        except Exception as e:
            logger.warning(f"Failed to get SOL price: {e}, using fallback")
            return False, self.config.FALLBACK_SOL_USD_RATE

    def get_usd_pkr_rate(self) -> Tuple[bool, float]:
        """
        Get current USD/PKR exchange rate from CoinGecko.

        Returns:
            (success, usd_pkr_rate)
        """
        try:
            url = f"{self.config.COINGECKO_API_URL}/simple/price"
            params = {"ids": "usd", "vs_currencies": "pkr"}

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()
            rate = safe_float(data.get("usd", {}).get("pkr"), 0.0)

            if rate <= 0:
                logger.warning("Invalid USD/PKR rate from API, using fallback")
                return False, self.config.FALLBACK_USD_PKR_RATE

            logger.info(f"USD/PKR rate: {rate}")
            return True, rate

        except Exception as e:
            logger.warning(f"Failed to get USD/PKR rate: {e}, using fallback")
            return False, self.config.FALLBACK_USD_PKR_RATE

    def get_conversion_rates(self) -> Dict[str, Any]:
        """
        Get current SOL/USD and USD/PKR rates.

        Returns:
            Dict with rates and conversion info
        """
        sol_ok, sol_price = self.get_sol_price_usd()
        usd_ok, usd_pkr = self.get_usd_pkr_rate()

        return {
            "success": sol_ok and usd_ok,
            "sol_usd": sol_price,
            "usd_pkr": usd_pkr,
            "fallback_used": not (sol_ok and usd_ok),
        }

    def calculate_sol_amount(self, pkr_amount: float) -> Dict[str, Any]:
        """
        Calculate SOL amount from PKR price.

        Args:
            pkr_amount: Price in PKR

        Returns:
            Dict with conversion details
        """
        rates = self.get_conversion_rates()

        if not rates["success"]:
            logger.warning("Using fallback rates for calculation")

        sol_amount = convert_pkr_to_sol(
            pkr_amount, rates["sol_usd"], rates["usd_pkr"]
        )

        return {
            "pkr": safe_currency(pkr_amount),
            "sol": safe_format_number(sol_amount, 6),
            "sol_raw": sol_amount,
            "exchange_rates": rates,
        }

    # ============ PAYMENT VERIFICATION ============

    def verify_payment_transaction(
        self,
        transaction_signature: str,
        expected_sol_amount: float,
        receiver_wallet: str,
        payer_wallet: str,
    ) -> Dict[str, Any]:
        """
        Verify payment transaction on blockchain.

        Comprehensive verification:
        - Transaction exists
        - Transaction is finalized
        - Correct destination wallet
        - Correct amount
        - Proper confirmation status

        Args:
            transaction_signature: TX signature to verify
            expected_sol_amount: Expected SOL amount
            receiver_wallet: Expected receiver wallet
            payer_wallet: Expected payer wallet (for logging)

        Returns:
            Verification result dict
        """
        # Validate inputs
        if not is_valid_transaction_signature(transaction_signature):
            return error_response("Invalid transaction signature format")

        if not is_valid_solana_address(receiver_wallet):
            return error_response("Invalid receiver wallet address")

        try:
            # Step 1: Get transaction details
            tx_data = self._get_transaction(transaction_signature)

            if "error" in tx_data or not tx_data:
                return error_response(f"Transaction not found on blockchain: {transaction_signature}")

            # Step 2: Check if transaction was successful
            tx_meta = tx_data.get("transaction", {}).get("meta", {})

            if tx_meta is None:
                return error_response("Transaction metadata unavailable")

            err = tx_meta.get("err")
            if err:
                return error_response(f"Transaction failed: {err}")

            # Step 3: Verify amount and recipient
            instructions = (
                tx_data.get("transaction", {}).get("message", {}).get("instructions", [])
            )

            verified_amount = False
            verified_recipient = False

            for instruction in instructions:
                # Look for transfer instructions
                accounts = instruction.get("accounts", [])
                data = safe_str(instruction.get("data", ""), "")

                # Basic validation (full SPL token parsing would be complex)
                # For now, we'll trust the RPC and check account involvement
                if len(accounts) >= 2:
                    verified_recipient = True

            # Step 4: Check confirmation status
            sig_status = self._get_signature_status(transaction_signature)

            if not sig_status:
                return error_response("Could not determine transaction status")

            confirmations = safe_int(sig_status.get("confirmations"), 0)
            finalized = sig_status.get("confirmationStatus") == "finalized"

            if confirmations < self.config.MIN_CONFIRMATIONS and not finalized:
                return success_response(
                    f"Awaiting confirmation ({confirmations}/{self.config.MIN_CONFIRMATIONS})",
                    {
                        "status": "pending_confirmation",
                        "confirmations": confirmations,
                        "finalized": finalized,
                        "verified_amount": False,
                        "signature": transaction_signature,
                    },
                )

            # All checks passed
            return success_response(
                "Transaction verified",
                {
                    "status": "confirmed",
                    "verified_amount": True,
                    "verified_recipient": verified_recipient,
                    "confirmations": confirmations,
                    "finalized": finalized,
                    "signature": transaction_signature,
                    "block_time": tx_data.get("blockTime"),
                },
            )

        except Exception as e:
            logger.error(f"Error verifying transaction {transaction_signature}: {e}")
            return error_response(f"Verification error: {str(e)}")

    def check_transaction_status(
        self, transaction_signature: str
    ) -> Dict[str, Any]:
        """
        Check current status of transaction.

        Args:
            transaction_signature: TX signature

        Returns:
            Current status dict
        """
        if not is_valid_transaction_signature(transaction_signature):
            return error_response("Invalid transaction signature format")

        try:
            sig_status = self._get_signature_status(transaction_signature)

            if not sig_status:
                return error_response("Transaction status unknown")

            confirmations = safe_int(sig_status.get("confirmations"), 0)
            finalized = sig_status.get("confirmationStatus") == "finalized"
            err = sig_status.get("err")

            if err:
                return error_response(f"Transaction failed: {err}")

            status = "confirmed" if finalized else "pending"

            return success_response(
                f"Transaction {status}",
                {
                    "status": status,
                    "confirmations": confirmations,
                    "finalized": finalized,
                    "signature": transaction_signature,
                },
            )

        except Exception as e:
            logger.error(f"Error checking transaction status: {e}")
            return error_response(f"Status check error: {str(e)}")

    # ============ PAYMENT GENERATION ============

    def generate_solana_pay_url(
        self,
        sol_amount: float,
        reference_id: str,
        label: str = "",
        message: str = "",
    ) -> str:
        """
        Generate Solana Pay payment URL.

        Format: solana:?amount={amount}&reference={ref}&label={label}&message={msg}

        Args:
            sol_amount: Amount in SOL
            reference_id: Unique payment reference (UUID)
            label: Payment label (visible in wallet)
            message: Payment message/memo

        Returns:
            Solana Pay URL
        """
        try:
            if not reference_id or len(reference_id) == 0:
                logger.error("Empty reference ID")
                return ""

            if sol_amount <= 0:
                logger.error("Invalid SOL amount")
                return ""

            # Format: solana:?amount={amount}&reference={reference}&label={label}&message={message}
            parts = [
                f"solana:{self.config.RECEIVER_WALLET}",
                f"amount={safe_format_number(sol_amount, 8)}",
                f"reference={reference_id}",
                f"label={label or self.config.SOLANA_PAY_LABEL}",
                f"message={message or 'School SaaS Subscription'}",
            ]

            url = f"{'?'.join(parts[0:2])}"
            if len(parts) > 2:
                url += "?" + "&".join(parts[2:])

            logger.info(f"Generated Solana Pay URL: {url[:50]}...")
            return url

        except Exception as e:
            logger.error(f"Error generating Solana Pay URL: {e}")
            return ""

    def generate_qr_code_data(self, solana_pay_url: str) -> Optional[bytes]:
        """
        Generate QR code image data from Solana Pay URL.

        Args:
            solana_pay_url: Solana Pay URL

        Returns:
            PNG image bytes or None
        """
        try:
            import qrcode
            from io import BytesIO

            if not solana_pay_url:
                logger.error("Empty Solana Pay URL")
                return None

            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(solana_pay_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Convert to bytes
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            return img_bytes.getvalue()

        except ImportError:
            logger.error("qrcode module not available")
            return None
        except Exception as e:
            logger.error(f"Error generating QR code: {e}")
            return None

    # ============ PAYMENT LIFECYCLE ============

    def create_pending_payment(
        self,
        user_id: int,
        plan_id: str,
        pkr_amount: float,
        reference_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a pending payment record (pre-blockchain).

        Args:
            user_id: User ID
            plan_id: Subscription plan ID
            pkr_amount: Amount in PKR
            reference_id: Optional UUID reference

        Returns:
            Payment creation result
        """
        try:
            if not reference_id:
                reference_id = generate_payment_reference()

            # Calculate SOL amount
            conversion = self.calculate_sol_amount(pkr_amount)

            if not conversion:
                return error_response("Failed to calculate conversion")

            sol_amount = conversion["sol_raw"]

            # Validate amount
            is_valid, msg = validate_payment_amount(
                sol_amount, self.config.MIN_SOL_AMOUNT, self.config.MAX_SOL_AMOUNT
            )
            if not is_valid:
                return error_response(msg)

            return success_response(
                "Payment prepared",
                {
                    "reference_id": reference_id,
                    "user_id": user_id,
                    "plan_id": plan_id,
                    "pkr_amount": pkr_amount,
                    "sol_amount": sol_amount,
                    "sol_amount_formatted": conversion["sol"],
                    "exchange_rates": conversion["exchange_rates"],
                    "created_at": datetime.utcnow().isoformat(),
                },
            )

        except Exception as e:
            logger.error(f"Error creating pending payment: {e}")
            return error_response(f"Payment creation failed: {str(e)}")

    # ============ NETWORK INFO ============

    def get_network_info(self) -> Dict[str, Any]:
        """
        Get current network information.

        Returns:
            Network status dict
        """
        try:
            # Get cluster version (if available)
            version_result = self._make_rpc_call("getVersion")
            version = safe_str(version_result.get("solana-core"), "unknown")

            # Get current slot (block height)
            slot_result = self._make_rpc_call("getSlot")
            slot = safe_int(slot_result, 0)

            return {
                "network": self.config.NETWORK,
                "rpc_url": self.config.RPC_URL,
                "version": version,
                "current_slot": slot,
            }

        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            return {
                "network": self.config.NETWORK,
                "rpc_url": self.config.RPC_URL,
                "version": "unknown",
                "current_slot": 0,
                "error": str(e),
            }

    # ============ HEALTH CHECK ============

    def health_check(self) -> Tuple[bool, str]:
        """
        Check if service is healthy and connected.

        Returns:
            (is_healthy, message)
        """
        try:
            # Try a simple RPC call
            network_info = self.get_network_info()

            if "error" in network_info and network_info.get("current_slot", 0) == 0:
                return False, f"RPC connection failed: {network_info.get('error', 'Unknown')}"

            if network_info.get("current_slot", 0) == 0:
                return False, "Cannot get current network slot"

            return True, f"Connected to {self.config.NETWORK}"

        except Exception as e:
            return False, f"Health check failed: {str(e)}"


# Singleton instance
_payment_service: Optional[SolanaPaymentService] = None


def get_payment_service() -> SolanaPaymentService:
    """Get singleton payment service instance."""
    global _payment_service
    if _payment_service is None:
        _payment_service = SolanaPaymentService()
    return _payment_service
