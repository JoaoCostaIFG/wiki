#!/usr/bin/env python3

from pathlib import Path

# Define paths
SRC = Path("src")
WIKI = SRC / "Wiki"
SUMMARY = SRC / "SUMMARY.md"


def calculate_indent(level: int) -> str:
    """Calculate the indentation for markdown based on the directory depth."""
    return "\t" * level


def build_dir(entry: Path, level: int) -> str:
    """Build a markdown entry for a directory."""
    indent = calculate_indent(level - 3)  # Exclude Wiki and base directory
    return f"{indent}- [{entry.parent.name}]({entry})\n"


def build_entry(entry: Path, level: int) -> str:
    """Build a markdown entry for a file."""
    indent = calculate_indent(level - 2)  # Exclude Wiki
    return f"{indent}- [{entry.name}]({entry})\n"


def main():
    """Generate a SUMMARY.md file based on the directory structure of Wiki."""
    with open(SUMMARY, "w", encoding="utf-8") as summary_file:
        # Write header
        summary_file.write("# Summary\n\n")
        summary_file.write("- [Introduction](Wiki/README.md)\n\n")

        last_dir = None
        for path in WIKI.rglob("*.md"):
            if path.name.lower() == "readme.md":
                continue  # Skip README.md files to avoid redundant entries

            # Replace spaces with dashes in filenames
            if " " in path.name:
                try:
                    new_name = path.name.replace(" ", "-")
                    new_path = path.parent / new_name
                    path.rename(new_path)
                    path = new_path  # Update path after renaming
                except Exception as e:
                    print(f"Error renaming {path.name}: {e}")
                    continue

            # Adjust the path for relative output
            relative_path = path.relative_to(SRC)

            # Check if directory needs to be added
            if path.parent not in (last_dir, WIKI):
                last_dir = path.parent
                summary_file.write(build_dir(last_dir / "README.md", len(path.parts)))

            # Add the markdown entry for the file
            summary_file.write(build_entry(relative_path, len(path.parts)))


if __name__ == "__main__":
    main()
