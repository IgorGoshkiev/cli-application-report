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

        # двууровневый словарь со счётчиками
        stats = defaultdict(lambda: defaultdict(int))
        for record in request_records:
            stats[record["handler"]][record["level"]] += 1

        handlers = sorted(stats.keys())
        totals = {level: 0 for level in cls.LEVELS}

        # Ширина колонки с URL-путями
        # берем наибольшее значение между длиной заголовка (HANDLER) и самым длинным URL-путем
        max_handler_len = max(len("HANDLER"), max((len(h) for h in handlers), default=0))
        # Ширина колонок с уровнями логирования
        max_level_lens = {
            level: max(
                len(level),  # Длина названия уровня
                max(  # Максимальная длина числа в этой колонке
                    (len(str(stats[h].get(level, 0))) for h in handlers), default=0)
            )
            for level in cls.LEVELS
        }

        # Форматирование строки
        def format_row(handler, counts):
            cells = [handler.ljust(max_handler_len)]
            # В цикле добавляются выровненные по правому краю значения для каждого уровня логирования.
            for level in cls.LEVELS:
                # Берёт количество запросов (или 0, если нет данных)
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

        return "\n".join(report) + f"\n\n Total requests: {total_requests}"
