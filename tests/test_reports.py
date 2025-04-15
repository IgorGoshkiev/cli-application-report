from log_handler.reports.handler_report import HandlersReport
from log_handler.reports.security_report import SecurityReport

REQUEST_RECORDS = [
    {"type": "request", "handler": "/api/users", "level": "INFO"},
    {"type": "request", "handler": "/api/users", "level": "ERROR"},
    {"type": "request", "handler": "/admin", "level": "WARNING"},
]

SECURITY_RECORDS = [
    {"type": "security", "event_type": "CsrfViewMiddleware", "level": "WARNING"},
    {"type": "security", "event_type": "CsrfViewMiddleware", "level": "WARNING"},
    {"type": "security", "event_type": "XFrameOptionsMiddleware", "level": "WARNING"},
]


def test_handlers_report():
    report = HandlersReport.generate(REQUEST_RECORDS)
    assert "HANDLER" in report
    assert "/api/users" in report
    assert "TOTAL" in report
    assert "INFO" in report
    assert "ERROR" in report


def test_security_report():
    report = SecurityReport.generate(SECURITY_RECORDS)
    assert "SECURITY EVENTS REPORT" in report
    assert "CsrfViewMiddleware" in report
    assert "XFrameOptionsMiddleware" in report
    assert "Total security events: 3" in report


def test_empty_handlers_report():
    report = HandlersReport.generate([])
    assert "Total requests: 0" in report


def test_empty_security_report():
    report = SecurityReport.generate([])
    assert "Total security events: 0" in report
