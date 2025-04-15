import pytest
from unittest.mock import patch, mock_open, MagicMock
from log_handler.cli import validate_files, parse_args, main
import argparse
from pathlib import Path


# Тесты для validate_files()
def test_validate_files_success(tmp_path):
    # Создаем временный файл
    test_file = tmp_path / "test.log"
    test_file.write_text("test data")

    # Проверяем функцию
    result = validate_files([str(test_file)])
    assert len(result) == 1
    assert isinstance(result[0], Path)


def test_validate_files_not_found():
    with pytest.raises(FileNotFoundError):
        validate_files(["nonexistent.log"])


def test_validate_files_not_file(tmp_path):
    # Создаем временную директорию (не файл)
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    with pytest.raises(ValueError):
        validate_files([str(test_dir)])


# Тесты для parse_args()
def test_parse_args():
    args = parse_args(["file1.log", "file2.log", "--report", "security"])
    assert args.log_files == ["file1.log", "file2.log"]
    assert args.report == "security"


def test_parse_args_missing_report():
    with pytest.raises(SystemExit):
        parse_args(["file1.log"])


# Тесты для main()
@patch("log_handler.cli.parse_args")
@patch("log_handler.cli.validate_files")
@patch("log_handler.cli.get_report")
@patch("builtins.open", new_callable=mock_open, read_data="log data")
@patch("log_handler.cli.parse_log_file")
@patch("builtins.print")
def test_main_success(mock_print, mock_parse_log, mock_open_file,
                      mock_get_report, mock_validate, mock_parse):
    # Настраиваем моки
    mock_parse.return_value = argparse.Namespace(
        log_files=["test.log"],
        report="handlers"
    )
    mock_validate.return_value = [Path("test.log")]
    mock_parse_log.return_value = [{"type": "request"}]
    mock_report = MagicMock()
    mock_report.generate.return_value = "test report"
    mock_get_report.return_value = mock_report

    # Вызываем main
    main()

    # Проверяем вызовы
    mock_parse.assert_called_once()
    mock_validate.assert_called_once_with(["test.log"])
    mock_open_file.assert_called_once_with(Path("test.log"), "r", encoding="utf-8")
    mock_parse_log.assert_called_once()
    mock_print.assert_called_once_with("test report")


@patch("log_handler.cli.parse_args")
@patch("log_handler.cli.validate_files")
@patch("builtins.print")
def test_main_file_error(mock_print, mock_validate, mock_parse):
    mock_parse.return_value = argparse.Namespace(
        log_files=["missing.log"],
        report="handlers"
    )
    mock_validate.side_effect = FileNotFoundError("File not found")

    with pytest.raises(SystemExit):
        main()

    mock_print.assert_called_once_with("Ошибка: File not found")

