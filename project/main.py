"""Run the Stage 9 interactive SmartCare console menu."""

import sys
from smartcare.console import run_menu


def main() -> None:
    """Launch the interactive menu."""
    try:
        run_menu()
    except Exception as e:
        print(f"Error launching menu: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()