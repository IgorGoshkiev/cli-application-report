import re
from typing import IO, List, Dict, Optional
from .parsers.django_request import DjangoRequestParser
from .parsers.django_security import DjangoSecurityParser
from .parsers.base_parcer import BaseLogParser

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) "
    # \w+ — одно или больше "словесных" символов
    r"(?P<log_level>\w+) "
    # . — любой символ (кроме переноса строки)
    #  + — один или больше раз
    r"(?P<message>.+)$"
)


def get_default_parsers() -> List[BaseLogParser]:
    return [
        DjangoRequestParser(),
        DjangoSecurityParser()
    ]


# разбираем строку лога через доступные парсеры
def parse_log_line(line: str, parsers: List[BaseLogParser]) -> Optional[Dict[str, str]]:
    line = line.strip()
    if not line:
        return None

    log_match = LOG_PATTERN.match(line)
    # log_match = <re.Match object; span=(0, 87), match='2025-03-27 12:41:35,000 INFO django.request: GET >
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
