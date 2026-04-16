#!/usr/bin/env python3
"""
Smoke das fontes externas equivalentes às páginas do Streamlit (sem subir o servidor).

Útil para evidência no terminal alinhada ao escopo: UOL, Yahoo, yfinance, ifix.csv.
"""

from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

from _raiz_projeto import raiz_firedash


def main() -> int:
    raiz = raiz_firedash()
    sys.path.insert(0, str(raiz / "dashboard"))
    from market_utils import (  # noqa: E402
        last_close_and_delta_pct,
        read_html_tables,
        yf_download_close,
    )

    print("=" * 60)
    print("AC3 — Smoke de fontes (equivalente às páginas do dashboard)")
    print("=" * 60)
    print(f"Raiz: {raiz}\n")

    # --- Dashboard / UOL ---
    print("[CT-01 / Dashboard] UOL — read_html_tables (≥4 tabelas)")
    uol_url = "https://economia.uol.com.br/cotacoes/bolsas/"
    last_exc: Exception | None = None
    for tentativa in range(1, 4):
        try:
            dfs = read_html_tables(uol_url)
            print(f"  OK: {len(dfs)} tabela(s); destaques altas shape={dfs[1].shape}")
            break
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if tentativa < 3:
                time.sleep(1.5)
            else:
                print(f"  FALHOU após 3 tentativas: {type(last_exc).__name__}: {last_exc}")

    # --- 1_Ações: listas ---
    print("\n[1_Ações] Arquivos de tickers")
    br = raiz / "dashboard" / "pages" / "br_tickers.txt"
    us = raiz / "dashboard" / "pages" / "us_tickers.txt"
    n_br = len([ln for ln in br.read_text(encoding="utf-8").splitlines() if ln.strip()])
    n_us = len([ln for ln in us.read_text(encoding="utf-8").splitlines() if ln.strip()])
    print(f"  br_tickers.txt: {n_br} linhas")
    print(f"  us_tickers.txt: {n_us} linhas")

    # --- 2_FIIs: ifix ---
    print("\n[2_FIIs] ifix.csv")
    ifix = raiz / "dashboard" / "pages" / "ifix.csv"
    with ifix.open(encoding="utf-8", newline="") as f:
        n_fii = sum(1 for _ in csv.reader(f))
    print(f"  OK: {n_fii} fundo(s) listado(s)")

    # --- 3_Índices ---
    print("\n[3_Índices] Yahoo world-indices")
    try:
        df = read_html_tables("https://finance.yahoo.com/world-indices/")[0]
        print(f"  OK: tabela com {len(df)} linha(s); colunas: {list(df.columns)[:3]}...")
    except Exception as exc:  # noqa: BLE001
        print(f"  FALHOU: {type(exc).__name__}: {exc}")

    # --- 4_Criptomoedas ---
    print("\n[4_Criptomoedas] Yahoo markets/crypto/all")
    try:
        raw = read_html_tables("https://finance.yahoo.com/markets/crypto/all/")[0]
        sym = raw["Symbol"].astype(str).str.strip().str.replace(r"^[A-Z]\s+", "", regex=True)
        print(f"  OK: {len(sym)} linha(s); primeiro símbolo normalizado: {sym.iloc[0]!r}")
    except Exception as exc:  # noqa: BLE001
        print(f"  FALHOU: {type(exc).__name__}: {exc}")

    # --- yfinance ---
    print("\n[yfinance] download curto PETR4.SA")
    try:
        petr = yf_download_close("PETR4.SA", days=10)
        close, delta = last_close_and_delta_pct(petr)
        print(f"  último Close≈{close}; delta={delta}")
    except Exception as exc:  # noqa: BLE001
        print(f"  FALHOU: {type(exc).__name__}: {exc}")

    print("\n" + "=" * 60)
    print("Fim do smoke.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
