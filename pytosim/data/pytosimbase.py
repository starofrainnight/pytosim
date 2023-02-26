# -*- coding: utf-8 -*-
from pytosim.api import string as simstr


def _pytosim_min(a, b) -> float:
    if a < b:
        return a

    return b


def _pytosim_max(a, b) -> float:
    if a > b:
        return a

    return b


def _pytosim_normalize_idx(len: int, idx: int) -> int:
    """Normalize the index value"""

    if idx < 0:
        if idx < -len:
            idx = -len

        idx = len + idx
    elif idx > len:
        # idx use as stop index could after the array's end
        idx = len

    return idx


def _pytosim_mid(s: str, idx_from: int, idx_to: int) -> str:
    s_len = len(s)
    if s_len <= 0:
        return ""

    idx_from = _pytosim_normalize_idx(s_len, idx_from)
    idx_from = _pytosim_min(idx_from, s_len - 1)
    idx_to = _pytosim_normalize_idx(s_len, idx_to)
    idx_to = _pytosim_max(idx_to, idx_from + 1)
    return simstr.strmid(s, idx_from, idx_to)
