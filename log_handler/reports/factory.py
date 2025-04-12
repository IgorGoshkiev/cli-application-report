from typing import Dict, Type
from .base import BaseReport
from .handlers import HandlersReport

_REPORTS: Dict[str, Type[BaseReport]] = {
    HandlersReport.name: HandlersReport
}


def get_report(report_name: str) -> Type[BaseReport]:
    if report_name not in _REPORTS:
        available = list(_REPORTS.keys())
        raise ValueError(f"Unknown report: {report_name}. Available: {available}")
    return _REPORTS[report_name]


def register_report(report_class: Type[BaseReport]):
    """Функция для регистрации новых отчетов"""
    _REPORTS[report_class.name] = report_class
