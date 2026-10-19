"""Run the AutoOps engine and dashboard as one local development process."""

from pathlib import Path
import subprocess
import sys
import time


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main():
    processes = []
    exit_code = 0

    components = (
        ("engine", "autoops.core.engine"),
        ("dashboard", "autoops.web.web"),
    )

    try:
        for name, module in components:
            command = [sys.executable, "-u", "-m", module]
            print(f"[START] {name}: {' '.join(command)}", flush=True)
            process = subprocess.Popen(command, cwd=PROJECT_ROOT)
            processes.append((name, process))

        while True:
            for name, process in processes:
                status = process.poll()
                if status is not None:
                    print(
                        f"[START] {name} exited with code {status}; stopping AutoOps",
                        file=sys.stderr,
                        flush=True,
                    )
                    exit_code = status or 1
                    return exit_code
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("[START] stopping AutoOps", flush=True)

    except Exception as exc:
        print(f"[START] failed: {exc}", file=sys.stderr, flush=True)
        exit_code = 1

    finally:
        for _, process in processes:
            if process.poll() is None:
                process.terminate()

        for _, process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
