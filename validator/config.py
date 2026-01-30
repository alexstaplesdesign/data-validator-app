from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """Application configuration for validation runs."""
    input_dir: Path
    reports_dir: Path
    pattern: str
    fail_on_error: bool