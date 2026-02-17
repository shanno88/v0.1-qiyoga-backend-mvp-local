import re
from typing import Optional, Dict, Any
from datetime import datetime


def extract_rent_amount(text: str) -> Optional[str]:
    rent_patterns = [
        # Labeled forms with explicit labels (highest priority)
        r"Base\s+Rent:\s*\$?\s*[\d,]+\.?\d*\s*(?:USD)?(?:\s*(?:per\s+)?(?:month|mo|monthly))?",
        r"Monthly\s+Base\s+Rent:\s*[\d,]+\.?\d*\s*(?:USD)?\s*(?:per\s+)?(?:month|mo|monthly)?",
        r"Monthly\s+Rent:\s*\$?\s*[\d,]+\.?\d*\s*(?:per\s+)?(?:month|mo|monthly)?",
        r"Rent:\s*\$?\s*[\d,]+\.?\d*\s*(?:per\s+)?(?:month|mo|monthly)?",
        r"Rent\s+Amount:\s*\$?\s*[\d,]+\.?\d*\s*(?:per\s+)?(?:month|mo|monthly)?",
        r"\$\s*[\d,]+\.?\d*\s*(?:per\s+)?(?:month|mo|monthly)",
        r"[\d,]+\.?\d*\s*(?:per\s+)?(?:month|mo|monthly)",
        r"\$\s*[\d,]+\.?\d*\s*/\s*(?:month|mo)",
        # Descriptive sentences
        r"(?:The\s+)?(?:monthly|Monthly)\s+rent\s+(?:shall\s+be|is|will\s+be)\s*\$?\s*[\d,]+\.?\d*",
        r"(?:Rent|rent)\s+(?:shall\s+be|is|will\s+be)\s*\$?\s*[\d,]+\.?\d*\s*(?:per\s+)?(?:month|mo)",
    ]
    for pattern in rent_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            return match.group().strip()
    return None


def extract_lease_term(text: str) -> Optional[str]:
    term_patterns = [
        # Labeled forms with explicit labels (highest priority)
        r"Lease\s+Term:\s*(?:a\s+)?(?:term\s+of\s+)?(\d+)\s*(?:-|\s+to\s+-)\s*(\d+)\s*(?:month|months)",
        r"Lease\s+Term:\s*(?:a\s+)?(?:term\s+of\s+)?(\d+)\s*(?:month|months|year|years)",
        r"Term:\s*(?:a\s+)?(?:term\s+of\s+)?(\d+)\s*(?:month|months|year|years)",
        r"Lease\s+Period:\s*(?:a\s+)?(?:period\s+of\s+)?(\d+)\s*(?:month|months|year|years)",
        # Descriptive sentences
        r"(?:This\s+)?(?:lease|Lease)\s+is\s+(?:for\s+a\s+)?(?:term\s+of\s+)?(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)\s*\(\s*\d+\s*\)\s*(?:month|months|year|years)",
        r"for\s+(?:a\s+)?(?:period\s+of\s+)?(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)\s*\(\s*\d+\s*\)\s*(?:month|months)",
        r"for\s+(?:a\s+)?(?:period\s+of\s+)?(\d+)\s*(?:month|months|year|years)",
        r"(?:for|during|during\s+the\s+term\s+of)\s+(\d+)\s*(?:month|months|year|years)",
        # Numeric forms
        r"(\d+)\s*(?:-|\s+to\s+-)\s*(\d+)\s*(?:month|months)",
        r"(\d+)\s*(?:month|months|year|years)\s+(?:term|lease)",
    ]
    for pattern in term_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group().strip()
    return None


def extract_date(text: str) -> Optional[str]:
    date_patterns = [
        # Labeled forms with explicit labels (highest priority)
        r"Commencement\s+Date:\s*((?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/\d{4})",
        r"Commencement\s+Date:\s*((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:\d{1,2})(?:st|nd|rd|th)?,?\s+\d{4})",
        r"Start\s+Date:\s*((?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/\d{4})",
        r"Start\s+Date:\s*((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:\d{1,2})(?:st|nd|rd|th)?,?\s+\d{4})",
        r"Effective\s+Date:\s*((?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/\d{4})",
        r"Effective\s+Date:\s*((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:\d{1,2})(?:st|nd|rd|th)?,?\s+\d{4})",
        r"Lease\s+Start\s+(?:Date|):\s*((?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/\d{4})",
        # Descriptive sentences
        r"(?:This\s+)?(?:lease|Lease)\s+(?:begins|starts?|commences?|is\s+effective)\s+(?:on|:)\s*((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:\d{1,2})(?:st|nd|rd|th)?,?\s+\d{4})",
        r"(?:This\s+)?(?:lease|Lease)\s+(?:begins|starts?|commences?|is\s+effective)\s+(?:on|:)\s*((?:0[1-9]|1[0-2])/(?:0[1-9]|[12][0-9]|3[01])/\d{4})",
        # Generic date formats
        r"\b(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}\b",
        r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+\d{4}\b",
        r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group().strip()
    return None


def extract_landlord_name(text: str) -> Optional[str]:
    patterns = [
        # Labeled forms with explicit labels (highest priority)
        r"(?:Landlord|Owner|Lessor|Property Manager):\s*([A-Z][a-z]+(?:\s+[A-Z](?:\.\s+)?[a-z]+)*(?:\s+[A-Z][a-z]+)*)",
        r"(?:Landlord|Owner|Lessor|Property Manager)\s+([A-Z][a-z]+(?:\s+[A-Z](?:\.\s+)?[a-z]+)*(?:\s+[A-Z][a-z]+)*)",
        r"Landlord\s+Name:?\s*([A-Z][a-z]+(?:\s+[A-Z](?:\.\s+)?[a-z]+)*(?:\s+[A-Z][a-z]+)*)",
        # Company names (all caps with LLC/INC)
        r"(?:Landlord|Owner|Lessor|Property Manager):\s*([A-Z]{2,}(?:\s+[A-Z]{2,})+(?:\s+(?:LLC|INC|LTD|CORP|CO|COMPANY))?)",
        r"(?:Landlord|Owner|Lessor|Property Manager)\s+([A-Z]{2,}(?:\s+[A-Z]{2,})+(?:\s+(?:LLC|INC|LTD|CORP|CO|COMPANY))?)",
        r"LANDLORD,\s*([A-Z\s]+(?:LLC|INC|LTD|CORP|CO|COMPANY)?)",
        # Mixed case with suffixes
        r"(?:Landlord|Owner|Lessor):\s*([A-Z][a-zA-Z\s&]+(?:LLC|Inc\.|Ltd\.|Corp\.|Co\.|Company)?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def extract_tenant_name(text: str) -> Optional[str]:
    patterns = [
        # Labeled forms with explicit labels (highest priority)
        r"(?:Tenant|Lessee|Renter):\s*([A-Z][a-z]+(?:\s+[A-Z](?:\.\s+)?[a-z]+)*(?:\s+[A-Z][a-z]+)*)",
        r"(?:Tenant|Lessee|Renter)\s+([A-Z][a-z]+(?:\s+[A-Z](?:\.\s+)?[a-z]+)*(?:\s+[A-Z][a-z]+)*)",
        r"Tenant\s+Name:?\s*([A-Z][a-z]+(?:\s+[A-Z](?:\.\s+)?[a-z]+)*(?:\s+[A-Z][a-z]+)*)",
        # Company names (all caps with LLC/INC)
        r"(?:Tenant|Lessee|Renter):\s*([A-Z]{2,}(?:\s+[A-Z]{2,})+(?:\s+(?:LLC|INC|LTD|CORP|CO|COMPANY))?)",
        r"(?:Tenant|Lessee|Renter)\s+([A-Z]{2,}(?:\s+[A-Z]{2,})+(?:\s+(?:LLC|INC|LTD|CORP|CO|COMPANY))?)",
        r"TENANT,\s*([A-Z\s]+(?:LLC|INC|LTD|CORP|CO|COMPANY)?)",
        # Mixed case with suffixes
        r"(?:Tenant|Lessee|Renter):\s*([A-Z][a-zA-Z\s&]+(?:LLC|Inc\.|Ltd\.|Corp\.|Co\.|Company)?)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def extract_key_info(text: str) -> Dict[str, Any]:
    rent_amount = extract_rent_amount(text)
    lease_term = extract_lease_term(text)
    start_date = extract_date(text)
    landlord = extract_landlord_name(text)
    tenant = extract_tenant_name(text)
    return {
        "rent_amount": rent_amount or "Not found",
        "lease_term": lease_term or "Not found",
        "start_date": start_date or "Not found",
        "landlord": landlord or "Not found",
        "tenant": tenant or "Not found",
    }


def parse_numeric(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = re.sub(r"[,$\s]", "", value)
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def parse_iso_date(value: Any) -> Optional[str]:
    if not value:
        return None
    if isinstance(value, str):
        value = value.strip()
        if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            return value
        for fmt in ["%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%d/%m/%Y"]:
            try:
                dt = datetime.strptime(value, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
    return None


def calculate_duration_months(
    start_date: Optional[str], end_date: Optional[str]
) -> Optional[int]:
    if not start_date or not end_date:
        return None
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        months = round((end - start).days / 30.44)
        return months if months > 0 else None
    except ValueError:
        return None


def validate_summary_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    currency = raw.get("currency") or "USD"
    if isinstance(currency, str):
        currency = currency.upper()
    else:
        currency = "USD"

    monthly_rent = parse_numeric(raw.get("monthly_rent_amount"))
    start_date = parse_iso_date(raw.get("lease_start_date"))
    end_date = parse_iso_date(raw.get("lease_end_date"))
    duration = raw.get("lease_duration_months")

    if start_date and end_date and not duration:
        duration = calculate_duration_months(start_date, end_date)

    if duration is not None:
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            duration = None

    overall_risk = raw.get("overall_risk", "medium")
    if overall_risk not in ("low", "medium", "high"):
        overall_risk = "medium"

    return {
        "overall_risk": overall_risk,
        "monthly_rent_amount": monthly_rent,
        "currency": currency,
        "lease_start_date": start_date,
        "lease_end_date": end_date,
        "lease_duration_months": duration,
        "security_deposit_amount": parse_numeric(raw.get("security_deposit_amount")),
        "landlord_name": raw.get("landlord_name"),
        "tenant_name": raw.get("tenant_name"),
        "late_fee_summary_zh": raw.get("late_fee_summary_zh") or "未明确写明滞纳金条款",
        "early_termination_risk_zh": raw.get("early_termination_risk_zh")
        or "未明确写明提前解约条款",
    }


def build_key_info_from_summary(summary: Dict[str, Any]) -> Dict[str, Any]:
    rent = summary.get("monthly_rent_amount")
    currency = summary.get("currency", "USD")
    if rent is not None:
        rent_str = (
            f"${int(rent)} {currency}/month"
            if rent == int(rent)
            else f"${rent} {currency}/month"
        )
    else:
        rent_str = "Not found"

    start = summary.get("lease_start_date")
    end = summary.get("lease_end_date")
    duration = summary.get("lease_duration_months")

    if start and end:
        term_str = f"{start} to {end}"
        if duration:
            term_str += f" ({duration} months)"
    elif duration:
        term_str = f"{duration} months"
    else:
        term_str = "Not found"

    return {
        "rent_amount": rent_str,
        "lease_term": term_str,
        "start_date": start or "Not found",
        "landlord": summary.get("landlord_name") or "Not found",
        "tenant": summary.get("tenant_name") or "Not found",
    }


def filter_and_extract_high_risk_clauses(clauses: list) -> tuple:
    """
    Filter out noise clauses and extract high-risk clauses.

    Returns: (filtered_clauses, high_risk_clauses)
    """
    money_termination_keywords = {
        "rent",
        "fee",
        "deposit",
        "termination",
        "terminate",
        "penalty",
        "charge",
        "payment",
        "late",
        "evict",
        "break",
        "cancel",
        "租金",
        "费用",
        "押金",
        "终止",
        "违约",
        "罚款",
        "滞纳金",
        "解约",
    }

    filtered = []
    high_risk = []

    for clause in clauses:
        text = clause.get("clause_text", "")
        text_lower = text.lower()
        risk = clause.get("risk_level", "")

        if len(text) < 15:
            has_digits = any(c.isdigit() for c in text)
            has_currency = "$" in text or "€" in text or "£" in text or "¥" in text
            has_date_pattern = bool(re.search(r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}", text))

            if not (has_digits or has_currency or has_date_pattern):
                continue

        filtered.append(clause)

        if risk == "danger":
            high_risk.append(clause)
        elif risk == "caution":
            if any(kw in text_lower or kw in text for kw in money_termination_keywords):
                high_risk.append(clause)

    return filtered, high_risk
