import argparse
from pathlib import Path
from typing import List
from .parser import parse_log_file
from .reports import get_report


def validate_files(file_paths: List[str]) -> List[Path]:
    valid_files = []
    for path in file_paths:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        if not file_path.is_file():
            raise ValueError(f"Это не файл: {file_path}")
        valid_files.append(file_path)
    return valid_files


def parse_args(args=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Анализатор логов Django",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "log_files",
        nargs="+",
        help="Пути к файлам логов (через пробел)"
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=["handlers"],
        help="Тип отчета (доступные: handlers)"
    )
    return parser.parse_args(args)


def main():
    try:
        args = parse_args()
        log_files = validate_files(args.log_files)
        report_class = get_report(args.report)

        all_records = []
        for log_file in log_files:
            with open(log_file, "r", encoding="utf-8") as f:
                all_records.extend(parse_log_file(f))

        report = report_class.generate(all_records)
        print(report)

    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1)
