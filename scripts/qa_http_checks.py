#!/usr/bin/env python3
"""
Checagens HTTP equivalentes ao Passo 7 da AC3 (sem API REST do Firedash).

Uso (na raiz do repositório):
  ./venv/bin/python scripts/qa_http_checks.py

Saída: status code e tamanho do corpo para 2 URLs válidas (como no app)
e 2 requisições inválidas (URL/host errados).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Reutiliza os mesmos cabeçalhos do app
_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "dashboard"))

import requests  # noqa: E402

from market_utils import DEFAULT_HEADERS  # noqa: E402

UOL_BOLSAS = "https://economia.uol.com.br/cotacoes/bolsas/"
YAHOO_INDICES = "https://finance.yahoo.com/world-indices/"


def _get(url: str) -> tuple[int, int]:
    r = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
    return r.status_code, len(r.content)


def main() -> int:
    print("=== AC3 — checagens HTTP (entrada externa do Firedash) ===\n")

    print("Válido 1 — UOL (Dashboard.py)")
    try:
        sc, n = _get(UOL_BOLSAS)
        print(f"  URL: {UOL_BOLSAS}")
        print(f"  status={sc} bytes={n}")
    except Exception as exc:  # noqa: BLE001
        print(f"  ERRO: {exc}")

    print("\nVálido 2 — Yahoo índices (3_Índices.py)")
    try:
        sc, n = _get(YAHOO_INDICES)
        print(f"  URL: {YAHOO_INDICES}")
        print(f"  status={sc} bytes={n}")
    except Exception as exc:  # noqa: BLE001
        print(f"  ERRO: {exc}")

    print("\nInválido 1 — host inexistente")
    try:
        requests.get(
            "https://firedash-invalid-host-xyz.example/cotacoes/",
            headers=DEFAULT_HEADERS,
            timeout=5,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  esperado falhar: {type(exc).__name__}: {exc}")

    print("\nInválido 2 — URL truncada / recurso inexistente (UOL)")
    bad = "https://economia.uol.com.br/cotacoes/bolsas/PAGINA_QUE_NAO_EXISTE_404"
    try:
        sc, n = _get(bad)
        print(f"  URL: {bad}")
        print(f"  status={sc} bytes={n}")
    except Exception as exc:  # noqa: BLE001
        print(f"  ERRO: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
