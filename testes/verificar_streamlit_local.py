#!/usr/bin/env python3
"""
Smoke HTTP no Streamlit já em execução (evidência tipo AC3_evidencias/terminal_streamlit_smoke).

1) Em outro terminal: cd dashboard && streamlit run Dashboard.py [--server.port 8501]
2) Rode: python testes/verificar_streamlit_local.py [--port 8501]
"""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request


def main() -> int:
    p = argparse.ArgumentParser(description="GET na raiz do Streamlit local.")
    p.add_argument("--host", default="127.0.0.1", help="Host (default 127.0.0.1)")
    p.add_argument("--port", type=int, default=8501, help="Porta (default 8501)")
    args = p.parse_args()
    url = f"http://{args.host}:{args.port}/"

    print("=" * 60)
    print("AC3 — Smoke HTTP Streamlit (app já rodando)")
    print("=" * 60)
    print(f"GET {url}\n")

    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            body = r.read(500)
            print(f"status: {r.status}")
            print(f"primeiros bytes da resposta: {len(body)} (amostra de 500)")
    except urllib.error.HTTPError as exc:
        print(f"HTTPError: {exc.code} {exc.reason}")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Falhou (servidor não está em {url}?): {type(exc).__name__}: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
