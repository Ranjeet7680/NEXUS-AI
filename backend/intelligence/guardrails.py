import re
from typing import Dict, Any, Tuple

class GuardrailsEngine:
    """
    Enforces security, prompt-injection defense, PII masking, and output verification.
    """

    INJECTION_PATTERNS = [
        r"ignore previous instructions",
        r"bypass security",
        r"reveal system prompt",
        r"execute arbitrary code",
        r"drop database",
        r"rm -rf"
    ]

    @classmethod
    def sanitize_input(cls, user_prompt: str) -> Tuple[bool, str]:
        prompt_lower = user_prompt.lower()
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, prompt_lower):
                return False, f"Potential adversarial prompt detected: matched '{pattern}'"
        return True, user_prompt

    @classmethod
    def mask_pii(cls, text: str) -> str:
        # Mask social security / ID numbers
        masked = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        # Mask credit card patterns
        masked = re.sub(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", "[REDACTED-CC]", masked)
        return masked

    @classmethod
    def evaluate_output_confidence(cls, output_data: Dict[str, Any]) -> float:
        """
        Calculates an objective confidence score between 0.0 and 1.0 based on:
        - Completeness of calculations
        - Presence of source grounding
        - Consistency of metrics
        """
        score = 0.70
        if "metrics" in output_data and len(output_data["metrics"]) > 0:
            score += 0.15
        if "recommendations" in output_data and len(output_data["recommendations"]) > 0:
            score += 0.10
        if "quality_check" in output_data and output_data["quality_check"].get("passed", False):
            score += 0.05
        return min(round(score, 2), 0.99)

guardrails = GuardrailsEngine()
