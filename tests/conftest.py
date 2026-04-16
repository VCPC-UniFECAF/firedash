"""Garante import de `market_utils` a partir da pasta `dashboard/`."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_DASH = _ROOT / "dashboard"
if str(_DASH) not in sys.path:
    sys.path.insert(0, str(_DASH))
