"""Resolve a raiz do repositório firedash (pasta que contém `dashboard/` e `tests/`)."""

from __future__ import annotations

from pathlib import Path


def raiz_firedash() -> Path:
    """A partir de `testes/*.py`: pai da pasta `testes`."""
    aqui = Path(__file__).resolve().parent
    raiz = aqui.parent
    if not (raiz / "dashboard" / "market_utils.py").is_file():
        raise FileNotFoundError(
            "Não encontrei `dashboard/market_utils.py` acima de `testes/`. "
            "Mantenha a pasta `testes` na raiz do clone."
        )
    return raiz


def raiz_desde_cwd() -> Path:
    """Para notebook: sobe diretórios até achar `dashboard/market_utils.py`."""
    for base in [Path.cwd(), *Path.cwd().parents]:
        if (base / "dashboard" / "market_utils.py").is_file():
            return base
    raise FileNotFoundError(
        "Inicie o Jupyter a partir da raiz do firedash ou de `testes/`, "
        "ou faça `os.chdir` para a raiz do clone antes de rodar as células."
    )
