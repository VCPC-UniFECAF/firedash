import csv
from datetime import date
from pathlib import Path

import streamlit as st

from market_utils import (
    last_close_and_delta_pct,
    yf_download_adj_close_frame,
    yf_download_close,
)

_BASE = Path(__file__).resolve().parent
_IFIX = _BASE / "ifix.csv"

with _IFIX.open(newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    fundos = [f"{row[0]}.SA" for row in reader if row and row[0].strip()]

principais = ["DEVA11.SA", "MFII11.SA", "MXRF11.SA", "XPSF11.SA", "RBFF11.SA"]


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
    st.subheader("Comparar fundos")
    input_ac1 = st.selectbox(
        "Fundo 1",
        fundos,
        index=_default_index(fundos, principais[0]),
        key="fii_1",
    )
    input_ac2 = st.selectbox(
        "Fundo 2",
        fundos,
        index=_default_index(fundos, principais[1]),
        key="fii_2",
    )
    input_ac3 = st.selectbox(
        "Fundo 3",
        fundos,
        index=_default_index(fundos, principais[2]),
        key="fii_3",
    )
    input_ac4 = st.selectbox(
        "Fundo 4",
        fundos,
        index=_default_index(fundos, principais[3]),
        key="fii_4",
    )
    input_ac5 = st.selectbox(
        "Fundo 5",
        fundos,
        index=_default_index(fundos, principais[4]),
        key="fii_5",
    )
    dt_inicio = st.date_input("Data inicial", value=date(2024, 1, 1), key="fii_di0")
    dt_fim = st.date_input("Data final", key="fii_di1")

st.title("Fundos imobiliários")
st.subheader("Valor atual")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    get_metric(input_ac1)
with col2:
    get_metric(input_ac2)
with col3:
    get_metric(input_ac3)
with col4:
    get_metric(input_ac4)
with col5:
    get_metric(input_ac5)

st.subheader("Comparar FIIs")
chart_data = yf_download_adj_close_frame(
    [input_ac1, input_ac2, input_ac3, input_ac4, input_ac5],
    dt_inicio,
    dt_fim,
)
if chart_data.empty:
    st.warning("Sem dados no intervalo selecionado.")
else:
    st.line_chart(chart_data)
