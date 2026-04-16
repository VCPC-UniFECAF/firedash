
from __future__ import annotations

import runpy
import sys
from pathlib import Path

from _raiz_projeto import raiz_firedash


def main() -> int:
    raiz = raiz_firedash()
    script = raiz / "scripts" / "qa_http_checks.py"
    if not script.is_file():
        print("ERRO: não encontrei", script, file=sys.stderr)
        return 1
    print("=" * 60)
    print("AC3 — Passo 7 — HTTP (scripts/qa_http_checks.py)")
    print("=" * 60)
    print(f"Raiz: {raiz}\n")
    runpy.run_path(str(script), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
