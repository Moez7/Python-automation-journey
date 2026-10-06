import argparse
import logging
from pathlib import Path

from .organizer import organize_directory


def configure_logging() -> None:
    """Configure application-wide logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
    )


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Organize files into category-based directories."
    )

    parser.add_argument(
        "input_directory",
        type=Path,
        help="Directory containing files to organize.",
    )

    parser.add_argument(
        "output_directory",
        type=Path,
        help="Directory where organized files will be stored.",
    )

    return parser


def main() -> int:
    """
    Run the file organizer CLI.

    Returns:
        0 when organization succeeds.
        1 when an expected error occurs.
    """
    parser = create_parser()
    args = parser.parse_args()

    configure_logging()

    try:
        organized_files = organize_directory(
            input_directory=args.input_directory,
            output_directory=args.output_directory,
        )

    except (FileNotFoundError, NotADirectoryError) as error:
        logging.error("%s", error)
        return 1

    logging.info(
        "Successfully organized %d file(s).",
        len(organized_files),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())