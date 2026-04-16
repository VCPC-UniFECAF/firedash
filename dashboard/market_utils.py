"""Utilitários compartilhados: leitura HTML com User-Agent e normalização do yfinance."""

from __future__ import annotations

from io import StringIO
from typing import Any

import pandas as pd
import requests
import yfinance as yf

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}


def read_html_tables(url: str, **read_html_kwargs: Any) -> list[pd.DataFrame]:
    """Lê tabelas HTML com cabeçalhos de navegador (evita 403 em vários sites)."""
    resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
    resp.raise_for_status()
    kwargs = {"flavor": "lxml"}
    kwargs.update(read_html_kwargs)
    return pd.read_html(StringIO(resp.text), **kwargs)


def _close_1d_series(df: pd.DataFrame) -> pd.Series:
    if df is None or df.empty:
        return pd.Series(dtype=float)
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        if close.shape[1] == 1:
            return close.iloc[:, 0].dropna()
        raise ValueError("vários tickers: use coluna específica de Close")
    return close.dropna()


def last_close_and_delta_pct(
    df: pd.DataFrame,
) -> tuple[float | None, str | None]:
    """Último preço de fechamento e variação percentual vs. penúltimo pregão."""
    s = _close_1d_series(df)
    if len(s) < 2:
        return None, None
    last, prev = float(s.iloc[-1]), float(s.iloc[-2])
    if prev == 0:
        return last, None
    pct = (last - prev) / prev * 100
    return last, f"{pct:.2f}%"


def yf_download_close(ticker: str, days: int = 8) -> pd.DataFrame:
    end = pd.Timestamp.today().normalize()
    start = end - pd.Timedelta(days=days)
    return yf.download(
        ticker,
        start=start,
        end=end + pd.Timedelta(days=1),
        progress=False,
        auto_adjust=False,
        threads=False,
    )


def yf_download_adj_close_frame(
    tickers: list[str],
    start,
    end,
) -> pd.DataFrame:
    raw = yf.download(
        tickers,
        start=start,
        end=end + pd.Timedelta(days=1),
        progress=False,
        auto_adjust=False,
        threads=False,
    )
    if raw.empty:
        return pd.DataFrame()
    adj = raw["Adj Close"]
    if isinstance(adj, pd.Series):
        return pd.DataFrame({tickers[0]: adj})
    adj = adj.copy()
    adj.columns = [str(c) for c in adj.columns]
    return adj


def selectbox_index_for_symbol(
    df: pd.DataFrame,
    symbol_col: str,
    label_col: str,
    symbol: str,
) -> int:
    """Índice inteiro da linha em `df[label_col]` para usar em st.selectbox(..., index=...)."""
    labels = df[label_col].tolist()
    hit = df.index[df[symbol_col] == symbol].tolist()
    if not hit:
        return 0
    name = df.loc[hit[0], label_col]
    try:
        return labels.index(name)
    except ValueError:
        return 0
