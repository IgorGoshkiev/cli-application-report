from collections import defaultdict
from typing import List, Dict
from .base import BaseReport


class HandlersReport(BaseReport):
    name = "handlers"  # Просто атрибут класса
    LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    @classmethod
    def generate(cls, records: List[Dict[str, str]]) -> str:
        stats = defaultdict(lambda: defaultdict(int))

        for record in records:
            if record["level"] in cls.LEVELS:
                stats[record["handler"]][record["level"]] += 1

        handlers = sorted(stats.keys())
        totals = {level: 0 for level in cls.LEVELS}

        max_handler_len = max((len(h) for h in handlers), default=0)
        max_level_lens = {
            level: max(len(str(stats[h].get(level, 0))) for h in handlers)
            for level in cls.LEVELS
        }

        def format_row(handler, counts):
            cells = [handler.ljust(max_handler_len)]
            for level in cls.LEVELS:
                count = str(counts.get(level, 0))
                cells.append(count.rjust(max_level_lens[level]))
            return "  ".join(cells)

        report = []
        header = ["HANDLER".ljust(max_handler_len)] + [
            level.rjust(max_level_lens[level]) for level in cls.LEVELS
        ]
        report.append("  ".join(header))

        for handler in handlers:
            counts = stats[handler]
            for level in cls.LEVELS:
                totals[level] += counts.get(level, 0)
            report.append(format_row(handler, counts))

        report.append(format_row("", totals))
        total_requests = sum(totals.values())
        return f"Total requests: {total_requests}\n\n" + "\n".join(report)