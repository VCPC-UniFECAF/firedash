#!/usr/bin/env python3
"""
AC3 — Passo 8: testes automatizados (pytest) em `tests/test_market_utils.py`.

Uso (qualquer diretório):
  python testes/rodar_pytest_ac3.py

Requer: pip install -r requirements-dev.txt (pytest).
"""

from __future__ import annotations

import subprocess
import sys

from _raiz_projeto import raiz_firedash


def main() -> int:
    raiz = raiz_firedash()
    print("=" * 60)
    print("AC3 — Passo 8 — pytest (market_utils)")
    print("=" * 60)
    print(f"Raiz: {raiz}\n")

    cmd = [sys.executable, "-m", "pytest", str(raiz / "tests"), "-v", "--tb=short"]
    print("Comando:", " ".join(cmd), "\n")
    return subprocess.call(cmd, cwd=str(raiz))


if __name__ == "__main__":
    raise SystemExit(main())
