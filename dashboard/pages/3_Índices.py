import streamlit as st

from market_utils import (
    read_html_tables,
    selectbox_index_for_symbol,
    yf_download_close,
)

YAHOO_INDICES = "https://finance.yahoo.com/world-indices/"


@st.cache_data(ttl=600)
def _load_indices():
    df_html = read_html_tables(YAHOO_INDICES)
    df = df_html[0]
    return df[["Symbol", "Name"]]


try:
    indices = _load_indices()
except Exception as exc:  # noqa: BLE001
    st.error(f"Não foi possível carregar a tabela de índices do Yahoo Finance: {exc}")
    st.stop()

principais = ["^BVSP", "^GSPC", "^N100", "^N225", "000001.SS"]


def get_metric(name: str) -> None:
    hit = indices.index[indices["Name"] == name].tolist()
    if not hit:
        st.metric(name, "—", None)
        return
    ticker = indices.loc[hit[0], "Symbol"]
    df = yf_download_close(ticker, days=10)
    close, delta = last_close_and_delta_pct(df)
    if close is None:
        st.metric(str(ticker), "—", None)
        return
    close_k = f"{round(float(close) / 1000, 2)}K"
    st.metric(str(ticker), close_k, delta)


with st.sidebar:
    st.subheader("Comparar índices")
    input_ac1 = st.selectbox(
        "Índice 1",
        indices["Name"],
        index=selectbox_index_for_symbol(indices, "Symbol", "Name", principais[0]),
        key="idx_1",
    )
    input_ac2 = st.selectbox(
        "Índice 2",
        indices["Name"],
        index=selectbox_index_for_symbol(indices, "Symbol", "Name", principais[1]),
        key="idx_2",
    )
    input_ac3 = st.selectbox(
        "Índice 3",
        indices["Name"],
        index=selectbox_index_for_symbol(indices, "Symbol", "Name", principais[2]),
        key="idx_3",
    )
    input_ac4 = st.selectbox(
        "Índice 4",
        indices["Name"],
        index=selectbox_index_for_symbol(indices, "Symbol", "Name", principais[3]),
        key="idx_4",
    )
    input_ac5 = st.selectbox(
        "Índice 5",
        indices["Name"],
        index=selectbox_index_for_symbol(indices, "Symbol", "Name", principais[4]),
        key="idx_5",
    )

st.title("Índices mundiais")
st.subheader("Valor atual")

col10, col20, col30, col40, col50 = st.columns(5)

with col10:
    get_metric(input_ac1)
with col20:
    get_metric(input_ac2)
with col30:
    get_metric(input_ac3)
with col40:
    get_metric(input_ac4)
with col50:
    get_metric(input_ac5)

st.markdown("---")

# Grade fixa por posição na tabela do Yahoo (ordem pode mudar levemente ao longo do tempo)
fixed_rows = [
    [1, 2, 12],
    [15, 16, 24],
    [20, 17, 18],
    [4, 8, 10],
    [19, 32, 0],
]

col1, col2, col3, col4, col5 = st.columns(5)
for col, rows in zip((col1, col2, col3, col4, col5), fixed_rows):
    with col:
        for j, row_i in enumerate(rows):
            if row_i < len(indices):
                get_metric(indices.iloc[row_i]["Name"])
            if j < len(rows) - 1:
                st.markdown("---")
