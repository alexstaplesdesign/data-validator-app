import argparse
import logging
import sys
from pathlib import Path

from validator.config import AppConfig
from validator.discovery import discover_files
from validator.runner import run_validation
from validator.exit_codes import EXIT_OK, EXIT_INVALID_ARGS, EXIT_UNEXPECTED


def _build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    p = argparse.ArgumentParser(
        prog="data-validator-report",
        description="Validate CSV files and generate error reports + run summary.",
        epilog="Example: python -m validator.cli --input ./data/in --reports ./reports"
    )
    p.add_argument("--input", required=True, help="Input directory containing CSV files")
    p.add_argument("--reports", required=True, help="Directory to write reports")
    p.add_argument("--pattern", default="*.csv", help='Glob pattern (default: "*.csv")')
    p.add_argument("--failOnError", default="false", help="true/false; exit non-zero if validation errors found")
    p.add_argument("--logLevel", default="INFO", help="DEBUG, INFO, WARNING, ERROR")
    return p


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    argv = argv if argv is not None else sys.argv[1:]
    parser = _build_parser()

    try:
        args = parser.parse_args(argv)
        input_dir = Path(args.input)
        reports_dir = Path(args.reports)
        pattern = args.pattern
        fail_on_error = str(args.failOnError).lower() in ("1", "true", "yes", "y")
        log_level = str(args.logLevel).upper()

        # Setup logging
        logging.basicConfig(
            level=getattr(logging, log_level, logging.INFO),
            format="%(asctime)s %(levelname)s %(name)s - %(message)s"
        )

        # Validate input directory
        if not input_dir.exists() or not input_dir.is_dir():
            raise ValueError(f"Input directory does not exist: {input_dir}")

        # Create reports directory
        reports_dir.mkdir(parents=True, exist_ok=True)

        # Create configuration
        cfg = AppConfig(
            input_dir=input_dir,
            reports_dir=reports_dir,
            pattern=pattern,
            fail_on_error=fail_on_error,
        )

        # Discover and validate files
        files = discover_files(cfg.input_dir, cfg.pattern)
        logging.getLogger(__name__).info("Discovered %d file(s) in %s", len(files), cfg.input_dir)

        exit_code = run_validation(cfg, files)
        return exit_code

    except (ValueError, argparse.ArgumentError) as e:
        logging.getLogger(__name__).error("Invalid arguments/config: %s", e)
        return EXIT_INVALID_ARGS
    except SystemExit as e:
        # argparse throws SystemExit; preserve its code but map to invalid args when non-zero
        code = int(getattr(e, "code", 1))
        return EXIT_OK if code == 0 else EXIT_INVALID_ARGS
    except Exception:
        logging.getLogger(__name__).exception("Unexpected failure")
        return EXIT_UNEXPECTED


if __name__ == "__main__":
    raise SystemExit(main())