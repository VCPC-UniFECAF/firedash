from datetime import date, timedelta
from pathlib import Path

import streamlit as st

from market_utils import (
    last_close_and_delta_pct,
    yf_download_adj_close_frame,
    yf_download_close,
)

_PAGES_DIR = Path(__file__).resolve().parent


def _load_tickers(filename: str) -> list[str]:
    path = _PAGES_DIR / filename
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return sorted(set(lines))


tickers_br = [f"{t}.SA" for t in _load_tickers("br_tickers.txt")]
tickers_us = _load_tickers("us_tickers.txt")

principais_br = ["PETR3.SA", "MGLU3.SA", "VALE3.SA", "ITSA4.SA", "ABEV3.SA"]
principais_us = ["MSFT", "NFLX", "NVDA", "KO", "META"]


def _default_index(options: list[str], preferred: str) -> int:
    try:
        return options.index(preferred)
    except ValueError:
        return 0


def get_metric(ticker: str) -> None:
    df = yf_download_close(ticker, days=10)
    close, delta = last_close_and_delta_pct(df)
    if close is None:
        st.metric(ticker, "—", None)
        return
    st.metric(ticker, round(close, 2), delta)


with st.sidebar:
    st.subheader("Selecione um mercado")
    local = st.selectbox("Mercado", ["Brasil", "Estados Unidos"], label_visibility="collapsed")

if local == "Brasil":
    st.title("Ações brasileiras", anchor=False)
    st.subheader("Valor atual", anchor=False)

    with st.sidebar:
        st.subheader("Comparar ações")
        input_ac1_br = st.selectbox(
            "Ação 1",
            tickers_br,
            index=_default_index(tickers_br, principais_br[0]),
            key="ac_br_1",
        )
        input_ac2_br = st.selectbox(
            "Ação 2",
            tickers_br,
            index=_default_index(tickers_br, principais_br[1]),
            key="ac_br_2",
        )
        input_ac3_br = st.selectbox(
            "Ação 3",
            tickers_br,
            index=_default_index(tickers_br, principais_br[2]),
            key="ac_br_3",
        )
        input_ac4_br = st.selectbox(
            "Ação 4",
            tickers_br,
            index=_default_index(tickers_br, principais_br[3]),
            key="ac_br_4",
        )
        input_ac5_br = st.selectbox(
            "Ação 5",
            tickers_br,
            index=_default_index(tickers_br, principais_br[4]),
            key="ac_br_5",
        )
        dt_inicio_br = st.date_input("Data inicial", value=date(2024, 1, 1), key="ac_br_di0")
        dt_fim_br = st.date_input("Data final", key="ac_br_di1")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        get_metric(input_ac1_br)
    with col2:
        get_metric(input_ac2_br)
    with col3:
        get_metric(input_ac3_br)
    with col4:
        get_metric(input_ac4_br)
    with col5:
        get_metric(input_ac5_br)

    st.subheader("Comparar ações")
    chart_data = yf_download_adj_close_frame(
        [input_ac1_br, input_ac2_br, input_ac3_br, input_ac4_br, input_ac5_br],
        dt_inicio_br,
        dt_fim_br,
    )
    if chart_data.empty:
        st.warning("Sem dados no intervalo selecionado.")
    else:
        st.line_chart(chart_data)

else:
    st.title("Ações americanas (S&P 500)", anchor=False)
    st.subheader("Valor atual", anchor=False)

    with st.sidebar:
        st.subheader("Comparar ações")
        input_ac1_us = st.selectbox(
            "Ação 1",
            tickers_us,
            index=_default_index(tickers_us, principais_us[0]),
            key="ac_us_1",
        )
        input_ac2_us = st.selectbox(
            "Ação 2",
            tickers_us,
            index=_default_index(tickers_us, principais_us[1]),
            key="ac_us_2",
        )
        input_ac3_us = st.selectbox(
            "Ação 3",
            tickers_us,
            index=_default_index(tickers_us, principais_us[2]),
            key="ac_us_3",
        )
        input_ac4_us = st.selectbox(
            "Ação 4",
            tickers_us,
            index=_default_index(tickers_us, principais_us[3]),
            key="ac_us_4",
        )
        input_ac5_us = st.selectbox(
            "Ação 5",
            tickers_us,
            index=_default_index(tickers_us, principais_us[4]),
            key="ac_us_5",
        )
        dt_inicio_us = st.date_input("Data inicial", value=date(2024, 1, 1), key="ac_us_di0")
        dt_fim_us = st.date_input("Data final", key="ac_us_di1")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        get_metric(input_ac1_us)
    with col2:
        get_metric(input_ac2_us)
    with col3:
        get_metric(input_ac3_us)
    with col4:
        get_metric(input_ac4_us)
    with col5:
        get_metric(input_ac5_us)

    st.subheader("Comparar ações")
    chart_data = yf_download_adj_close_frame(
        [input_ac1_us, input_ac2_us, input_ac3_us, input_ac4_us, input_ac5_us],
        dt_inicio_us,
        dt_fim_us,
    )
    if chart_data.empty:
        st.warning("Sem dados no intervalo selecionado.")
    else:
        st.line_chart(chart_data)
