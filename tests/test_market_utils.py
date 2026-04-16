"""Testes automatizados (AC3) para funções puras em `dashboard/market_utils.py`."""

from __future__ import annotations

import sys
from pathlib import Path

_dash = Path(__file__).resolve().parents[1] / "dashboard"
if str(_dash) not in sys.path:
    sys.path.insert(0, str(_dash))

import pandas as pd
import pytest

from market_utils import last_close_and_delta_pct, selectbox_index_for_symbol


def test_last_close_and_delta_pct_com_serie_valida() -> None:
    df = pd.DataFrame({"Close": [100.0, 102.0, 101.0, 103.5]})
    close, delta = last_close_and_delta_pct(df)
    assert close == pytest.approx(103.5)
    assert delta is not None
    assert delta.endswith("%")
    pct = (103.5 - 101.0) / 101.0 * 100
    assert delta == f"{pct:.2f}%"


def test_last_close_and_delta_pct_sem_pontos_suficientes_retorna_none() -> None:
    df = pd.DataFrame({"Close": [10.0]})
    close, delta = last_close_and_delta_pct(df)
    assert close is None
    assert delta is None


def test_selectbox_index_for_symbol_encontra_simbolo() -> None:
    df = pd.DataFrame(
        {
            "Symbol": ["^BVSP", "^GSPC"],
            "Name": ["IBOVESPA", "S&P 500"],
        }
    )
    idx = selectbox_index_for_symbol(df, "Symbol", "Name", "^GSPC")
    assert idx == 1


def test_selectbox_index_for_symbol_inexistente_retorna_zero() -> None:
    df = pd.DataFrame({"Symbol": ["A"], "Name": ["Alpha"]})
    idx = selectbox_index_for_symbol(df, "Symbol", "Name", "ZZZ")
    assert idx == 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v", "--tb=short"]))
