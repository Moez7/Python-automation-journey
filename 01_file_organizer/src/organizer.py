from pathlib import Path
import logging


logger = logging.getLogger(__name__)

FILE_CATEGORIES = {
    ".pdf": "pdf",
    ".jpg": "images",
    ".jpeg": "images",
    ".png": "images",
    ".csv": "csv",
    ".xlsx": "excel",
    ".xls": "excel",
    ".py": "python",
    ".txt": "text",
}


def classify_file(file_path: Path) -> str:
    """
    Determine the category of a file based on its extension.

    Args:
        file_path: Path object representing the file.

    Returns:
        The category name.
    """
    extension = file_path.suffix.lower()

    if not extension:
        return "no_extension"

    return FILE_CATEGORIES.get(extension, "other")


def get_unique_destination(destination: Path) -> Path:
    """
    Return a unique destination path.

    If the destination already exists, append an incrementing
    number to the filename.
    """

    if not destination.exists():
        return destination

    counter = 1

    while True:
        candidate = (
            destination.parent
            / f"{destination.stem}_{counter}{destination.suffix}"
        )

        if not candidate.exists():
            return candidate

        counter += 1

def organize_file(source_file: Path, output_directory: Path) -> Path:
    """
    Move a file into the appropriate category directory.

    Args:
        source_file: Path of the file to organize.
        output_directory: Root directory where organized files
            will be stored.

    Returns:
        The final destination path.

    Raises:
        FileNotFoundError: If source_file does not exist.
        IsADirectoryError: If source_file is a directory.
    """
    if not source_file.exists():
        raise FileNotFoundError(
            f"Source file does not exist: {source_file}"
        )

    if not source_file.is_file():
        raise IsADirectoryError(
            f"Expected a file but received: {source_file}"
        )

    category = classify_file(source_file)

    category_directory = output_directory / category
    category_directory.mkdir(parents=True, exist_ok=True)

    destination = category_directory / source_file.name
    destination = get_unique_destination(destination)

    logger.info(
        "Moving %s -> %s",
        source_file,
        destination,
    )

    source_file.rename(destination)

    return destination

def organize_directory(
    input_directory: Path,
    output_directory: Path,
) -> list[Path]:
    """
    Organize all files directly inside an input directory.

    Subdirectories are ignored.

    Args:
        input_directory: Directory containing files to organize.
        output_directory: Root directory where organized files
            will be stored.

    Returns:
        A list of final destination paths.

    Raises:
        FileNotFoundError: If input_directory does not exist.
        NotADirectoryError: If input_directory is not a directory.
    """
    if not input_directory.exists():
        raise FileNotFoundError(
            f"Input directory does not exist: {input_directory}"
        )

    if not input_directory.is_dir():
        raise NotADirectoryError(
            f"Expected a directory but received: {input_directory}"
        )
    
    logger.info(
        "Starting organization: %s -> %s",
        input_directory,
        output_directory,
    )

    organized_files = []

    for item in input_directory.iterdir():
        if not item.is_file():
            continue

        destination = organize_file(
            source_file=item,
            output_directory=output_directory,
        )

        organized_files.append(destination)

    logger.info(
        "Organization completed: %d files processed",
        len(organized_files),
    )

    return organized_files