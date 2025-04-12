import re
from typing import IO, List, Dict, Optional

# Уровни логирования, которые мы будем учитывать
LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) "
    r"(?P<log_level>\w+) "
    r"(?P<message>.+)$"
)

REQUEST_PATTERN = re.compile(
    r"django\.request: "
    r"(?P<method>\w+) "
    r"(?P<handler>\S+) "
    r"(?P<status>\d{3}) "
    r"(?P<status_text>\w+)"
)

ERROR_PATTERN = re.compile(
    r"django\.request: "
    r"(?:Internal Server Error: )?"
    r"(?P<handler>\S+)"
)


def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    line = line.strip()
    if not line:
        return None

    log_match = LOG_PATTERN.match(line)
    if not log_match:
        return None

    message = log_match.group("message")
    if "django.request:" not in message:
        return None

    # Определяем уровень ошибки на основе статуса
    request_match = REQUEST_PATTERN.search(message)
    if request_match:
        status = int(request_match.group("status"))
        handler = request_match.group("handler")

        if status >= 500:
            level = "ERROR"
        elif status >= 400:
            level = "WARNING"
        else:
            level = log_match.group("log_level").upper()

        return {
            "level": level if level in LOG_LEVELS else "INFO",
            "handler": handler
        }

    # Для сообщений об ошибках в другом формате
    error_match = ERROR_PATTERN.search(message)
    if error_match:
        level = log_match.group("log_level").upper()
        return {
            "level": level if level in LOG_LEVELS else "ERROR",
            "handler": error_match.group("handler")
        }

    return None


def parse_log_file(file: IO) -> List[Dict[str, str]]:
    records = []
    for line in file:
        try:
            if record := parse_log_line(line):
                records.append(record)
        except Exception as e:
            print(f"Warning: failed to parse line: {line.strip()}. Error: {e}")
    return records
