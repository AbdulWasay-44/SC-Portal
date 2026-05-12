"""
Solana utilities and safe formatting helpers.

Provides defensive programming utilities to prevent NoneType crashes
and ensures robust error handling throughout the application.
"""

import logging
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Optional, Dict, List, Tuple
import uuid

logger = logging.getLogger(__name__)


# ============ SAFE FORMATTING UTILITIES ============


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert any value to float.

    Args:
        value: Value to convert
        default: Default if conversion fails

    Returns:
        Float value or default
    """
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        logger.warning(f"Failed to convert {value} to float, using default {default}")
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert any value to integer.

    Args:
        value: Value to convert
        default: Default if conversion fails

    Returns:
        Integer value or default
    """
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        logger.warning(f"Failed to convert {value} to int, using default {default}")
        return default


def safe_str(value: Any, default: str = "") -> str:
    """
    Safely convert any value to string.

    Args:
        value: Value to convert
        default: Default if conversion fails

    Returns:
        String value or default
    """
    if value is None:
        return default
    try:
        return str(value)
    except Exception:
        logger.warning(f"Failed to convert {value} to string, using default {default}")
        return default


def safe_currency(value: Any, decimals: int = 0, prefix: str = "PKR ") -> str:
    """
    Safely format currency value with thousands separator.

    Prevents: TypeError: unsupported format string passed to NoneType.__format__

    Args:
        value: Currency amount
        decimals: Decimal places (default 0)
        prefix: Currency prefix (default "PKR ")

    Returns:
        Formatted currency string
    """
    num = safe_float(value, 0.0)
    try:
        if decimals == 0:
            return f"{prefix}{num:,.0f}"
        else:
            return f"{prefix}{num:,.{decimals}f}"
    except Exception as e:
        logger.error(f"Currency formatting error: {e}")
        return f"{prefix}0"


def safe_percentage(value: Any, decimals: int = 1) -> str:
    """
    Safely format percentage value.

    Args:
        value: Percentage value
        decimals: Decimal places

    Returns:
        Formatted percentage string
    """
    num = safe_float(value, 0.0)
    try:
        return f"{num:.{decimals}f}%"
    except Exception:
        return "0%"


def safe_format_number(value: Any, decimals: int = 2) -> str:
    """
    Safely format a number with comma separators.

    Args:
        value: Number to format
        decimals: Decimal places

    Returns:
        Formatted number string
    """
    num = safe_float(value, 0.0)
    try:
        if decimals == 0:
            return f"{num:,.0f}"
        else:
            return f"{num:,.{decimals}f}"
    except Exception:
        return "0"


def safe_date(value: Any, format_str: str = "%Y-%m-%d") -> str:
    """
    Safely format datetime value.

    Args:
        value: DateTime value (datetime object or string)
        format_str: Format string

    Returns:
        Formatted date string
    """
    if value is None:
        return "N/A"

    try:
        if isinstance(value, datetime):
            return value.strftime(format_str)
        elif isinstance(value, str):
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt.strftime(format_str)
        else:
            return "Invalid date"
    except Exception as e:
        logger.warning(f"Date formatting error: {e}")
        return "Invalid date"


def safe_get_nested(data: Dict, keys: List[str], default: Any = None) -> Any:
    """
    Safely get nested dictionary values.

    Args:
        data: Dictionary to search
        keys: List of keys in path (e.g., ["user", "profile", "name"])
        default: Default value if path not found

    Returns:
        Value at path or default
    """
    if not isinstance(data, dict):
        return default

    result = data
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
        else:
            return default

    return result if result is not None else default


# ============ SOLANA-SPECIFIC UTILITIES ============


def generate_payment_reference() -> str:
    """
    Generate unique payment reference UUID.

    Returns:
        Unique reference string (UUID format)
    """
    return str(uuid.uuid4())


def is_valid_solana_address(address: str) -> bool:
    """
    Validate Solana address format (base58 encoding, 44 characters).

    Args:
        address: Solana public key address

    Returns:
        True if valid format
    """
    if not isinstance(address, str):
        return False

    # Solana addresses are 44 characters long in base58 encoding
    if len(address) != 44:
        return False

    # Check if all characters are valid base58
    base58_alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return all(c in base58_alphabet for c in address)


def is_valid_transaction_signature(signature: str) -> bool:
    """
    Validate Solana transaction signature format.

    Args:
        signature: Transaction signature (88 characters base58)

    Returns:
        True if valid format
    """
    if not isinstance(signature, str):
        return False

    # Solana signatures are 88 characters in base58 encoding
    if len(signature) != 88:
        return False

    base58_alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    return all(c in base58_alphabet for c in signature)


def normalize_sol_amount(amount: float, decimals: int = 8) -> int:
    """
    Convert SOL amount to lamports (smallest unit).

    Args:
        amount: SOL amount (decimal)
        decimals: SOL decimal places (default 8)

    Returns:
        Amount in lamports (integer)
    """
    try:
        decimal_amount = Decimal(str(amount))
        lamports = decimal_amount * Decimal(10 ** decimals)
        return int(lamports.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    except Exception as e:
        logger.error(f"Error normalizing SOL amount {amount}: {e}")
        return 0


def denormalize_lamports(lamports: int, decimals: int = 8) -> float:
    """
    Convert lamports back to SOL.

    Args:
        lamports: Amount in lamports (integer)
        decimals: SOL decimal places (default 8)

    Returns:
        Amount in SOL (float)
    """
    try:
        return float(lamports) / (10 ** decimals)
    except Exception as e:
        logger.error(f"Error denormalizing lamports {lamports}: {e}")
        return 0.0


def round_sol_amount(amount: float, decimals: int = 6) -> float:
    """
    Round SOL amount to reasonable precision.

    Args:
        amount: SOL amount
        decimals: Decimal places to round to (default 6)

    Returns:
        Rounded SOL amount
    """
    try:
        return round(amount, decimals)
    except Exception:
        return 0.0


# ============ PRICE CONVERSION ============


def convert_pkr_to_sol(
    pkr_amount: float, sol_price_usd: float, usd_pkr_rate: float
) -> float:
    """
    Convert PKR amount to SOL.

    Formula: PKR -> USD -> SOL
    - USD = PKR / USD_PKR_RATE
    - SOL = USD / SOL_USD_PRICE

    Args:
        pkr_amount: Amount in PKR
        sol_price_usd: SOL price in USD
        usd_pkr_rate: USD/PKR exchange rate

    Returns:
        Amount in SOL
    """
    try:
        if sol_price_usd <= 0 or usd_pkr_rate <= 0:
            raise ValueError("Invalid exchange rates")

        usd_amount = pkr_amount / usd_pkr_rate
        sol_amount = usd_amount / sol_price_usd
        return round_sol_amount(sol_amount)
    except Exception as e:
        logger.error(f"PKR to SOL conversion error: {e}")
        return 0.0


def convert_sol_to_pkr(
    sol_amount: float, sol_price_usd: float, usd_pkr_rate: float
) -> float:
    """
    Convert SOL amount to PKR.

    Formula: SOL -> USD -> PKR
    - USD = SOL * SOL_USD_PRICE
    - PKR = USD * USD_PKR_RATE

    Args:
        sol_amount: Amount in SOL
        sol_price_usd: SOL price in USD
        usd_pkr_rate: USD/PKR exchange rate

    Returns:
        Amount in PKR
    """
    try:
        if sol_price_usd <= 0 or usd_pkr_rate <= 0:
            raise ValueError("Invalid exchange rates")

        usd_amount = sol_amount * sol_price_usd
        pkr_amount = usd_amount * usd_pkr_rate
        return round(pkr_amount, 2)
    except Exception as e:
        logger.error(f"SOL to PKR conversion error: {e}")
        return 0.0


# ============ TIME UTILITIES ============


def get_payment_expiry_time(timeout_seconds: int) -> datetime:
    """
    Calculate payment expiry datetime.

    Args:
        timeout_seconds: Timeout in seconds

    Returns:
        Expiry datetime
    """
    try:
        return datetime.utcnow() + timedelta(seconds=timeout_seconds)
    except Exception as e:
        logger.error(f"Error calculating expiry time: {e}")
        return datetime.utcnow() + timedelta(seconds=900)


def is_payment_expired(expiry_time: Optional[datetime]) -> bool:
    """
    Check if payment has expired.

    Args:
        expiry_time: Expiry datetime

    Returns:
        True if expired
    """
    if expiry_time is None:
        return True

    try:
        return datetime.utcnow() > expiry_time
    except Exception:
        return True


def time_until_expiry(expiry_time: Optional[datetime]) -> int:
    """
    Get seconds until payment expires.

    Args:
        expiry_time: Expiry datetime

    Returns:
        Seconds remaining (0 if expired)
    """
    if expiry_time is None:
        return 0

    try:
        remaining = expiry_time - datetime.utcnow()
        seconds = int(remaining.total_seconds())
        return max(0, seconds)
    except Exception:
        return 0


# ============ STRUCTURED RESPONSES ============


def success_response(message: str = "", data: Any = None) -> Dict[str, Any]:
    """
    Create standardized success response.

    Args:
        message: Response message
        data: Response data

    Returns:
        Structured response dict
    """
    return {"success": True, "message": message, "data": data}


def error_response(message: str = "Unknown error", data: Any = None) -> Dict[str, Any]:
    """
    Create standardized error response.

    Args:
        message: Error message
        data: Additional error data

    Returns:
        Structured response dict
    """
    return {"success": False, "message": message, "data": data}


# ============ VALIDATION ============


def validate_payment_amount(sol_amount: float, min_sol: float, max_sol: float) -> Tuple[bool, str]:
    """
    Validate payment amount is within acceptable range.

    Args:
        sol_amount: Amount in SOL
        min_sol: Minimum acceptable SOL
        max_sol: Maximum acceptable SOL

    Returns:
        (is_valid, error_message)
    """
    if sol_amount <= 0:
        return False, "Payment amount must be greater than 0"

    if sol_amount < min_sol:
        return False, f"Minimum payment is {safe_format_number(min_sol, 4)} SOL"

    if sol_amount > max_sol:
        return False, f"Maximum payment is {safe_format_number(max_sol, 4)} SOL"

    return True, ""


def validate_wallet_address(wallet: str) -> Tuple[bool, str]:
    """
    Validate wallet address format.

    Args:
        wallet: Wallet address

    Returns:
        (is_valid, error_message)
    """
    if not wallet:
        return False, "Wallet address cannot be empty"

    if not is_valid_solana_address(wallet):
        return False, "Invalid Solana wallet address format"

    return True, ""
