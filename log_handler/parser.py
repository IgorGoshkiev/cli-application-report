import re
from typing import IO, List, Dict, Optional
from .parsers.django_request import DjangoRequestParser
from .parsers.django_security import DjangoSecurityParser
from .parsers.base_parcer import BaseLogParser

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) "
    r"(?P<log_level>\w+) "
    r"(?P<message>.+)$"
)


def get_default_parsers() -> List[BaseLogParser]:
    return [
        DjangoRequestParser(),
        DjangoSecurityParser()
    ]


def parse_log_line(line: str, parsers: List[BaseLogParser]) -> Optional[Dict[str, str]]:
    line = line.strip()
    if not line:
        return None

    log_match = LOG_PATTERN.match(line)
    if not log_match:
        return None

    message = log_match.group("message")
    for parser in parsers:
        if parser.can_parse(message):
            result = parser.parse(message)
            if result:
                return {
                    "timestamp": log_match.group("timestamp"),
                    "raw_level": log_match.group("log_level"),
                    **result
                }
    return None


def parse_log_file(file: IO, parsers: Optional[List[BaseLogParser]] = None) -> List[Dict[str, str]]:
    if parsers is None:
        parsers = get_default_parsers()

    records = []
    for line in file:
        try:
            if record := parse_log_line(line, parsers):
                records.append(record)
        except Exception as e:
            print(f"Warning: failed to parse line: {line.strip()}. Error: {e}")
    return records
