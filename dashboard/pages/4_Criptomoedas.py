from datetime import date

import streamlit as st

from market_utils import (
    last_close_and_delta_pct,
    read_html_tables,
    selectbox_index_for_symbol,
    yf_download_adj_close_frame,
    yf_download_close,
)

YAHOO_CRYPTO = "https://finance.yahoo.com/markets/crypto/all/"


@st.cache_data(ttl=600)
def _load_criptos():
    df_html = read_html_tables(YAHOO_CRYPTO)
    df = df_html[0][["Symbol", "Name"]].copy()
    df["Symbol"] = (
        df["Symbol"]
        .astype(str)
        .str.strip()
        .str.replace(r"^[A-Z]\s+", "", regex=True)
    )
    return df


try:
    criptos = _load_criptos()
except Exception as exc:  # noqa: BLE001
    st.error(f"Não foi possível carregar a tabela de criptomoedas do Yahoo Finance: {exc}")
    st.stop()

principais = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "DOGE-USD"]


def get_metric(name: str) -> None:
    hit = criptos.index[criptos["Name"] == name].tolist()
    if not hit:
        st.metric(name, "—", None)
        return
    ticker = criptos.loc[hit[0], "Symbol"]
    df = yf_download_close(ticker, days=10)
    close, delta = last_close_and_delta_pct(df)
    if close is None:
        st.metric(str(ticker), "—", None)
        return
    st.metric(str(ticker), round(float(close), 2), delta)


def get_ticker(name: str) -> str:
    hit = criptos.index[criptos["Name"] == name].tolist()
    if not hit:
        return ""
    return str(criptos.loc[hit[0], "Symbol"])


with st.sidebar:
    st.subheader("Comparar criptoativos")
    input_ac1 = st.selectbox(
        "Cripto 1",
        criptos["Name"],
        index=selectbox_index_for_symbol(criptos, "Symbol", "Name", principais[0]),
        key="cr_1",
    )
    input_ac2 = st.selectbox(
        "Cripto 2",
        criptos["Name"],
        index=selectbox_index_for_symbol(criptos, "Symbol", "Name", principais[1]),
        key="cr_2",
    )
    input_ac3 = st.selectbox(
        "Cripto 3",
        criptos["Name"],
        index=selectbox_index_for_symbol(criptos, "Symbol", "Name", principais[2]),
        key="cr_3",
    )
    input_ac4 = st.selectbox(
        "Cripto 4",
        criptos["Name"],
        index=selectbox_index_for_symbol(criptos, "Symbol", "Name", principais[3]),
        key="cr_4",
    )
    input_ac5 = st.selectbox(
        "Cripto 5",
        criptos["Name"],
        index=selectbox_index_for_symbol(criptos, "Symbol", "Name", principais[4]),
        key="cr_5",
    )
    dt_inicio = st.date_input("Data inicial", value=date(2024, 1, 1), key="cr_di0")
    dt_fim = st.date_input("Data final", key="cr_di1")

st.title("Criptomoedas")
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

st.subheader("Comparar cripto")
sel = [
    get_ticker(input_ac1),
    get_ticker(input_ac2),
    get_ticker(input_ac3),
    get_ticker(input_ac4),
    get_ticker(input_ac5),
]
sel = [t for t in sel if t]
chart_data = yf_download_adj_close_frame(sel, dt_inicio, dt_fim) if sel else None
if chart_data is None:
    st.warning("Nenhum ativo válido para o gráfico.")
elif chart_data.empty:
    st.warning("Sem dados no intervalo selecionado.")
else:
    st.line_chart(chart_data)
