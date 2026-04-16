import streamlit as st
import pandas as pd

from market_utils import read_html_tables

st.set_page_config(page_title="Firedash — Destaques", layout="wide")

UOL_BOLSAS = "https://economia.uol.com.br/cotacoes/bolsas/"


@st.cache_data(ttl=300)
def _uol_destaque_frames() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df_html = read_html_tables(UOL_BOLSAS)
    if len(df_html) < 4:
        raise ValueError("Layout da UOL inesperado: tabelas insuficientes.")
    return (
        pd.DataFrame(data=df_html[1]),
        pd.DataFrame(data=df_html[2]),
        pd.DataFrame(data=df_html[3]),
    )


def get_metric(metric: pd.DataFrame, indice: int) -> None:
    ticker = metric.iloc[indice, 0]
    close = metric.iloc[indice, 2]
    delta = metric.iloc[indice, 1]
    st.metric(str(ticker), close, delta)


try:
    altas, baixas, negociadas = _uol_destaque_frames()
except Exception as exc:  # noqa: BLE001 — exibir erro útil na UI
    st.error(f"Não foi possível carregar cotações da UOL: {exc}")
    st.stop()

st.title("Ações em destaque", anchor=False)
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Altas", anchor=False)
    for i in range(5):
        get_metric(altas, i)

with col2:
    st.subheader("Baixas", anchor=False)
    for i in range(5):
        get_metric(baixas, i)

with col3:
    st.subheader("Mais negociadas", anchor=False)
    for i in range(5):
        get_metric(negociadas, i)
