import re
from typing import Dict, Optional
from .base_parcer import BaseLogParser


class DjangoRequestParser(BaseLogParser):
    LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    REQUEST_PATTERN = re.compile(r"django\.request: (?P<method>\w+) (?P<handler>\S+) (?P<status>\d{3})")
    ERROR_PATTERN = re.compile(r"django\.request: (?:Internal Server Error: )?(?P<handler>\S+)")

    def can_parse(self, message: str) -> bool:
        return "django.request:" in message

    def parse(self, message: str) -> Optional[Dict[str, str]]:
        request_match = self.REQUEST_PATTERN.search(message)
        if request_match:
            status = int(request_match.group("status"))
            handler = request_match.group("handler")

            if not handler:
                return None

            if status >= 500:
                level = "ERROR"
            elif status >= 400:
                level = "WARNING"
            else:
                level = "INFO"  # Для 2xx/3xx статусов

            return {"type": "request", "level": level, "handler": handler}

        error_match = self.ERROR_PATTERN.search(message)
        if error_match:
            return {"type": "request", "level": "ERROR", "handler": error_match.group("handler")}

        return None
