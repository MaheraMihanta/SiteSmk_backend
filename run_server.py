import os
import sys
import threading
import traceback
import webbrowser
from pathlib import Path


def _open_browser():
    webbrowser.open("http://localhost:8000/")


def _setup_log_file(base_dir: Path) -> Path | None:
    if not getattr(sys, "frozen", False):
        return None

    log_dir = Path(sys.executable).resolve().parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "fleetee.log"
    sys.stdout = log_file.open("a", encoding="utf-8", buffering=1)
    sys.stderr = sys.stdout
    print("=== FleeteeApp start ===")
    return log_file


def main():
    base_dir = Path(__file__).resolve().parent
    log_file = _setup_log_file(base_dir)
    os.chdir(base_dir)
    sys.path.insert(0, str(base_dir))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    # Auto-open the browser a moment after the server starts.
    threading.Timer(1.5, _open_browser).start()

    try:
        from django.core.management import execute_from_command_line

        execute_from_command_line(
            ["manage.py", "runserver", "127.0.0.1:8000", "--noreload"]
        )
    except Exception:
        traceback.print_exc()
        if log_file is not None:
            try:
                import ctypes

                ctypes.windll.user32.MessageBoxW(
                    0,
                    f"Erreur au demarrage. Voir le log:\n{log_file}",
                    "FleeteeApp",
                    0x10,
                )
            except Exception:
                pass
        raise


if __name__ == "__main__":
    main()
