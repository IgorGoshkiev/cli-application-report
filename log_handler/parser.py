import re
from typing import IO, List, Dict, Optional

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"\[(?P<level>\w+)\s*\] "
    r"(?P<message>.+)$"
)

REQUEST_PATTERN = re.compile(
    r"^django\.request: "
    r"(?P<handler>\S+) - "
    r".*$"
)


def parse_log_line(line: str) -> Optional[Dict[str, str]]:
    line = line.strip()
    if not line:
        return None

    log_match = LOG_PATTERN.match(line)
    if not log_match:
        return None

    request_match = REQUEST_PATTERN.match(log_match.group("message"))
    if not request_match:
        return None

    return {
        "level": log_match.group("level").upper(),
        "handler": request_match.group("handler")
    }


def parse_log_file(file: IO) -> List[Dict[str, str]]:
    return [record for line in file if (record := parse_log_line(line))]
