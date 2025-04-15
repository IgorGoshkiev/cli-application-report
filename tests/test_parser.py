from io import StringIO

from log_handler.parser import parse_log_file, parse_log_line
from log_handler.parsers.django_request import DjangoRequestParser
from log_handler.parsers.django_security import DjangoSecurityParser


VALID_REQUEST_LOG = "2025-03-27 12:41:35,000 INFO django.request: GET /api/users 200"
VALID_SECURITY_LOG = "2025-03-27 12:42:00,000 WARNING django.security: CsrfViewMiddleware: Rejected request"
INVALID_LOG = "This is not a valid log line"


def test_parse_log_line_request():
    parsers = [DjangoRequestParser(), DjangoSecurityParser()]
    result = parse_log_line(VALID_REQUEST_LOG, parsers)

    assert result is not None
    assert result["type"] == "request"
    assert result["handler"] == "/api/users"
    assert result["level"] == "INFO"


def test_parse_log_line_security():
    parsers = [DjangoRequestParser(), DjangoSecurityParser()]
    result = parse_log_line(VALID_SECURITY_LOG, parsers)

    assert result is not None
    assert result["type"] == "security"
    assert result["event_type"] == "CsrfViewMiddleware"
    assert result["level"] == "WARNING"


def test_parse_log_line_invalid():
    parsers = [DjangoRequestParser(), DjangoSecurityParser()]
    result = parse_log_line(INVALID_LOG, parsers)
    assert result is None


def test_parse_log_file():
    log_data = f"{VALID_REQUEST_LOG}\n{VALID_SECURITY_LOG}\n{INVALID_LOG}"
    file = StringIO(log_data)
    records = parse_log_file(file)

    assert len(records) == 2
    assert records[0]["type"] == "request"
    assert records[1]["type"] == "security"
