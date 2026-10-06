from pathlib import Path
import pytest

from src.organizer import (
    classify_file,
    get_unique_destination,
    organize_file,
    organize_directory,
)

def test_pdf_file():
    assert classify_file(Path("report.pdf")) == "pdf"


def test_jpg_file():
    assert classify_file(Path("photo.jpg")) == "images"


def test_jpeg_file():
    assert classify_file(Path("photo.jpeg")) == "images"


def test_png_file():
    assert classify_file(Path("photo.png")) == "images"


def test_csv_file():
    assert classify_file(Path("customers.csv")) == "csv"


def test_excel_file():
    assert classify_file(Path("report.xlsx")) == "excel"


def test_old_excel_file():
    assert classify_file(Path("report.xls")) == "excel"


def test_python_file():
    assert classify_file(Path("script.py")) == "python"


def test_text_file():
    assert classify_file(Path("notes.txt")) == "text"


def test_unknown_extension():
    assert classify_file(Path("archive.zip")) == "other"


def test_file_without_extension():
    assert classify_file(Path("README")) == "no_extension"


def test_uppercase_extension():
    assert classify_file(Path("REPORT.PDF")) == "pdf"


def test_unique_destination_when_file_does_not_exist(tmp_path):
    destination = tmp_path / "report.pdf"

    result = get_unique_destination(destination)

    assert result == destination


def test_unique_destination_when_file_exists(tmp_path):
    destination = tmp_path / "report.pdf"
    destination.touch()

    result = get_unique_destination(destination)

    assert result == tmp_path / "report_1.pdf"


def test_unique_destination_skips_existing_numbered_files(tmp_path):
    destination = tmp_path / "report.pdf"

    destination.touch()
    (tmp_path / "report_1.pdf").touch()
    (tmp_path / "report_2.pdf").touch()

    result = get_unique_destination(destination)

    assert result == tmp_path / "report_3.pdf"

def test_organize_pdf_file(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()
    output_directory.mkdir()

    source_file = input_directory / "report.pdf"
    source_file.write_text("PDF content")

    result = organize_file(source_file, output_directory)

    expected_destination = output_directory / "pdf" / "report.pdf"

    assert result == expected_destination
    assert expected_destination.exists()
    assert not source_file.exists()

def test_organize_image_file(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()
    output_directory.mkdir()

    source_file = input_directory / "photo.JPG"
    source_file.write_text("fake image content")

    result = organize_file(source_file, output_directory)

    expected_destination = output_directory / "images" / "photo.JPG"

    assert result == expected_destination
    assert expected_destination.exists()
    assert not source_file.exists()

def test_organize_unknown_file(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()
    output_directory.mkdir()

    source_file = input_directory / "archive.zip"
    source_file.write_text("fake zip content")

    result = organize_file(source_file, output_directory)

    expected_destination = output_directory / "other" / "archive.zip"

    assert result == expected_destination
    assert expected_destination.exists()
    assert not source_file.exists()

def test_organize_file_without_extension(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()
    output_directory.mkdir()

    source_file = input_directory / "README"
    source_file.write_text("documentation")

    result = organize_file(source_file, output_directory)

    expected_destination = output_directory / "no_extension" / "README"

    assert result == expected_destination
    assert expected_destination.exists()
    assert not source_file.exists()

def test_organize_duplicate_file(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()
    output_directory.mkdir()

    existing_directory = output_directory / "pdf"
    existing_directory.mkdir()

    existing_file = existing_directory / "report.pdf"
    existing_file.write_text("existing")

    source_file = input_directory / "report.pdf"
    source_file.write_text("new")

    result = organize_file(source_file, output_directory)

    expected_destination = existing_directory / "report_1.pdf"

    assert result == expected_destination
    assert expected_destination.exists()
    assert existing_file.exists()
    assert not source_file.exists()

def test_organize_nonexistent_file(tmp_path):
    output_directory = tmp_path / "outputs"
    output_directory.mkdir()

    source_file = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        organize_file(source_file, output_directory)

def test_organize_directory_instead_of_file(tmp_path):
    output_directory = tmp_path / "outputs"
    output_directory.mkdir()

    source_directory = tmp_path / "documents"
    source_directory.mkdir()

    with pytest.raises(IsADirectoryError):
        organize_file(source_directory, output_directory)

def test_organize_empty_directory(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()

    result = organize_directory(
        input_directory,
        output_directory,
    )

    assert result == []


def test_organize_directory_with_one_file(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()

    pdf_file = input_directory / "report.pdf"
    pdf_file.write_text("fake pdf content")

    result = organize_directory(
        input_directory,
        output_directory,
    )

    destination = output_directory / "pdf" / "report.pdf"

    assert len(result) == 1
    assert result[0] == destination
    assert destination.exists()
    assert not pdf_file.exists()


def test_organize_directory_with_multiple_files(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()

    pdf_file = input_directory / "report.pdf"
    jpg_file = input_directory / "photo.jpg"
    csv_file = input_directory / "data.csv"
    python_file = input_directory / "script.py"

    pdf_file.write_text("fake pdf")
    jpg_file.write_text("fake image")
    csv_file.write_text("name,email")
    python_file.write_text("print('hello')")

    result = organize_directory(
        input_directory,
        output_directory,
    )

    assert len(result) == 4

    assert (output_directory / "pdf" / "report.pdf").exists()
    assert (output_directory / "images" / "photo.jpg").exists()
    assert (output_directory / "csv" / "data.csv").exists()
    assert (output_directory / "python" / "script.py").exists()

    assert not pdf_file.exists()
    assert not jpg_file.exists()
    assert not csv_file.exists()
    assert not python_file.exists()


def test_organize_directory_with_mixed_file_types(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()

    pdf_file = input_directory / "report.pdf"
    jpg_file = input_directory / "photo.jpg"
    zip_file = input_directory / "archive.zip"
    readme_file = input_directory / "README"

    pdf_file.write_text("fake pdf")
    jpg_file.write_text("fake image")
    zip_file.write_text("fake zip")
    readme_file.write_text("documentation")

    result = organize_directory(
        input_directory,
        output_directory,
    )

    assert len(result) == 4

    assert (output_directory / "pdf" / "report.pdf").exists()
    assert (output_directory / "images" / "photo.jpg").exists()
    assert (output_directory / "other" / "archive.zip").exists()
    assert (output_directory / "no_extension" / "README").exists()


def test_organize_directory_ignores_subdirectories(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()

    pdf_file = input_directory / "report.pdf"
    pdf_file.write_text("fake pdf")

    nested_directory = input_directory / "nested"
    nested_directory.mkdir()

    nested_file = nested_directory / "secret.pdf"
    nested_file.write_text("secret")

    result = organize_directory(
        input_directory,
        output_directory,
    )

    assert len(result) == 1

    assert (output_directory / "pdf" / "report.pdf").exists()

    assert nested_directory.exists()
    assert nested_file.exists()


def test_organize_directory_nonexistent_input(tmp_path):
    input_directory = tmp_path / "does_not_exist"
    output_directory = tmp_path / "outputs"

    with pytest.raises(FileNotFoundError):
        organize_directory(
            input_directory,
            output_directory,
        )


def test_organize_directory_input_is_file(tmp_path):
    input_file = tmp_path / "input.txt"
    output_directory = tmp_path / "outputs"

    input_file.write_text("not a directory")

    with pytest.raises(NotADirectoryError):
        organize_directory(
            input_file,
            output_directory,
        )

def test_organize_directory_logs_completion(tmp_path, caplog):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()

    pdf_file = input_directory / "report.pdf"
    pdf_file.write_text("fake pdf")

    with caplog.at_level("INFO"):
        organize_directory(
            input_directory,
            output_directory,
        )

    assert "Starting organization" in caplog.text
    assert "Moving" in caplog.text
    assert "Organization completed: 1 files processed" in caplog.text