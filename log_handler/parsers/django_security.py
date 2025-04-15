import re
from typing import Dict, Optional
from .base_parcer import BaseLogParser


class DjangoSecurityParser(BaseLogParser):
    SECURITY_PATTERN = re.compile(
        #  ищет точную строку django.security
        r"django\.security: "
        r"(?P<event_type>\w+): "
        r"(?P<message>.+)"
    )

    def can_parse(self, message: str) -> bool:
        return "django.security:" in message

    def parse(self, message: str) -> Optional[Dict[str, str]]:
        match = self.SECURITY_PATTERN.search(message)
        if not match:
            return None

        return {
            "type": "security",
            "level": "WARNING",  # Все события security считаем WARNING
            "event_type": match.group("event_type"),
            "message": match.group("message")
        }
