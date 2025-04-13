from collections import defaultdict
from typing import List, Dict
from .base_report import BaseReport


class SecurityReport(BaseReport):
    name = "security"  # Уникальное имя для CLI

    @classmethod
    def generate(cls, records: List[Dict[str, str]]) -> str:
        # Фильтруем только security события
        security_events = [r for r in records if r.get("type") == "security"]

        # Собираем статистику
        stats = defaultdict(int)
        for event in security_events:
            stats[event["event_type"]] += 1

        # Формируем отчёт
        report = ["SECURITY EVENTS REPORT", "=" * 30]
        for event_type, count in sorted(stats.items()):
            report.append(f"{event_type.ljust(25)}: {count} events")

        report.append(f"\nTotal security events: {len(security_events)}")
        return "\n".join(report)
