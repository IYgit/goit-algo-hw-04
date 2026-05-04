import argparse
import shutil
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Recursively copy files from source directory to destination, sorted by extension."
    )
    parser.add_argument(
        "source",
        type=str,
        nargs="?",
        default=".",
        help="Path to the source directory (default: current directory)",
    )
    parser.add_argument(
        "destination",
        type=str,
        nargs="?",
        default="dist",
        help="Path to the destination directory (default: dist)",
    )
    return parser.parse_args()


def read_folder(source: Path, destination: Path) -> None:
    """
    Recursively reads the source directory and copies files
    to subdirectories in destination named after file extensions.
    """
    try:
        for item in source.iterdir():
            if item.is_dir():
                read_folder(item, destination)
            elif item.is_file():
                copy_file(item, destination)
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except OSError as e:
        print(f"OS error while reading '{source}': {e}")


def copy_file(file: Path, destination: Path) -> None:
    """
    Copies a file to a subdirectory in destination named after the file's extension.
    """
    extension = file.suffix.lstrip(".").lower() or "no_extension"
    target_dir = destination / extension

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / file.name

        # Avoid overwriting by adding a counter suffix if file already exists
        counter = 1
        while target_path.exists():
            target_path = target_dir / f"{file.stem}_{counter}{file.suffix}"
            counter += 1

        shutil.copy2(file, target_path)
        print(f"Copied: '{file}' -> '{target_path}'")
    except PermissionError as e:
        print(f"Permission denied while copying '{file}': {e}")
    except OSError as e:
        print(f"OS error while copying '{file}': {e}")


def main():
    args = parse_args()

    source = Path(args.source)
    destination = Path(args.destination)

    if not source.exists():
        print(f"Error: Source directory '{source}' does not exist.")
        return

    if not source.is_dir():
        print(f"Error: '{source}' is not a directory.")
        return

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error creating destination directory '{destination}': {e}")
        return

    print(f"Source:      {source.resolve()}")
    print(f"Destination: {destination.resolve()}")
    print("-" * 50)

    read_folder(source, destination)

    print("-" * 50)
    print("Done.")


if __name__ == "__main__":
    main()

