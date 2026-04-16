#!/usr/bin/env python3
"""
Executa, em sequência, os scripts de `testes/` úteis para captura no terminal (AC3).

Ordem: smoke de fontes → HTTP checks → pytest.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from _raiz_projeto import raiz_firedash


def _run(script: Path) -> int:
    print("\n\n")
    return subprocess.call([sys.executable, str(script)])


def main() -> int:
    raiz = raiz_firedash()
    pasta = raiz / "testes"
    scripts = [
        pasta / "smoke_fontes_dashboard.py",
        pasta / "rodar_http_checks_ac3.py",
        pasta / "rodar_pytest_ac3.py",
    ]
    print("#" * 60)
    print("# AC3 — sequência completa (smoke + HTTP + pytest)")
    print("#" * 60)
    for s in scripts:
        if not s.is_file():
            print("Arquivo ausente:", s, file=sys.stderr)
            return 1
        code = _run(s)
        if code != 0:
            print(f"\nInterrompido: {s.name} retornou {code}", file=sys.stderr)
            return code
    print("\n" + "#" * 60)
    print("# Fim da sequência — todos os passos retornaram 0")
    print("#" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
