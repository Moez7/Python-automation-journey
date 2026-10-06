import subprocess
import sys
from pathlib import Path


def run_cli(
    input_directory: Path,
    output_directory: Path,
) -> subprocess.CompletedProcess:
    """Run the file organizer CLI as a subprocess."""
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli",
            str(input_directory),
            str(output_directory),
        ],
        capture_output=True,
        text=True,
    )


def test_cli_success(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()

    pdf_file = input_directory / "report.pdf"
    pdf_file.write_text("fake pdf")

    result = run_cli(
        input_directory,
        output_directory,
    )

    assert result.returncode == 0
    assert (output_directory / "pdf" / "report.pdf").exists()
    assert not pdf_file.exists()


def test_cli_handles_multiple_files(tmp_path):
    input_directory = tmp_path / "inputs"
    output_directory = tmp_path / "outputs"

    input_directory.mkdir()

    files = {
        "report.pdf": "pdf content",
        "photo.jpg": "image content",
        "data.csv": "name,email",
        "script.py": "print('hello')",
    }

    for filename, content in files.items():
        (input_directory / filename).write_text(content)

    result = run_cli(
        input_directory,
        output_directory,
    )

    assert result.returncode == 0

    assert (output_directory / "pdf" / "report.pdf").exists()
    assert (output_directory / "images" / "photo.jpg").exists()
    assert (output_directory / "csv" / "data.csv").exists()
    assert (output_directory / "python" / "script.py").exists()


def test_cli_missing_input_directory(tmp_path):
    input_directory = tmp_path / "does_not_exist"
    output_directory = tmp_path / "outputs"

    result = run_cli(
        input_directory,
        output_directory,
    )

    assert result.returncode == 1
    assert "Input directory does not exist" in result.stderr


def test_cli_input_is_file(tmp_path):
    input_file = tmp_path / "input.txt"
    output_directory = tmp_path / "outputs"

    input_file.write_text("not a directory")

    result = run_cli(
        input_file,
        output_directory,
    )

    assert result.returncode == 1
    assert "Expected a directory" in result.stderr


def test_cli_help():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.cli",
            "--help",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Organize files into category-based directories." in result.stdout
    assert "input_directory" in result.stdout
    assert "output_directory" in result.stdout