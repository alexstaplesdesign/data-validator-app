from pathlib import Path


def discover_files(input_dir: Path, pattern: str) -> list[Path]:
    """Discover CSV files matching the pattern in input directory."""
    # Deterministic ordering for consistent processing
    return sorted(input_dir.glob(pattern), key=lambda p: p.name)