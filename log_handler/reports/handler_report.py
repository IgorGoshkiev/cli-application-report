from collections import defaultdict
from typing import List, Dict
from .base_report import BaseReport


class HandlersReport(BaseReport):
    name = "handlers"
    LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    @classmethod
    def generate(cls, records: List[Dict[str, str]]) -> str:

        # Фильтруем только request записи
        request_records = [r for r in records if r.get("type") == "request"]

        stats = defaultdict(lambda: defaultdict(int))

        for record in request_records:
            stats[record["handler"]][record["level"]] += 1

        handlers = sorted(stats.keys())
        totals = {level: 0 for level in cls.LEVELS}

        # Рассчитываем ширину колонок
        max_handler_len = max(len("HANDLER"), max((len(h) for h in handlers), default=0))
        max_level_lens = {
            level: max(len(level), max((len(str(stats[h].get(level, 0))) for h in handlers), default=0))
            for level in cls.LEVELS
        }

        # Форматирование строки
        def format_row(handler, counts):
            cells = [handler.ljust(max_handler_len)]
            for level in cls.LEVELS:
                count = str(counts.get(level, 0))
                cells.append(count.rjust(max_level_lens[level]))
                totals[level] += counts.get(level, 0)
            return "  ".join(cells)

        report = []
        total_requests = sum(sum(level_counts.values()) for level_counts in stats.values())

        # Заголовок
        header = ["HANDLER".ljust(max_handler_len)] + [
            level.rjust(max_level_lens[level]) for level in cls.LEVELS
        ]
        report.append("  ".join(header))

        # Данные
        for handler in handlers:
            report.append(format_row(handler, stats[handler]))

        # Итоговая строка
        report.append(format_row("TOTAL", totals))

        return f"Total requests: {total_requests}\n\n" + "\n".join(report)