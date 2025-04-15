# cli_application_report
### Добавление нового отчета:

1. Создайте новый класс отчёта.
Создайте файл в папке reports/ (например, performance_report.py):


class PerformanceReport(BaseReport):
    name = "performance"  # Идентификатор отчёта
    
    @classmethod
    def generate(cls, records: List[Dict[str, str]]) -> str:
        # Фильтруем записи по нужному типу
        perf_events = [r for r in records if r.get("type") == "performance"]
        
        # Логика формирования отчёта
        report_lines = ["PERFORMANCE REPORT", "="*30]
        # ... ваша логика обработки ...
        
        return "\n".join(report_lines)

2. Зарегистрируйте отчёт в фабрике
* _REPORTS = {
    ...,
    PerformanceReport.name: PerformanceReport
}

3. Добавьте парсер
 * Создайте парсер в parsers/ (наследуйте от BaseLogParser)

 * Добавьте его в get_default_parsers() в parser.py


# Запуск тестов 
* pytest tests/ -v
* pytest --cov=log_handler tests/




