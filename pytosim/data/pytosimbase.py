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


def _pytosim_strmid(s: str, idx_from: int, idx_to: int) -> str:
    idx_from = _pytosim_min(idx_from, len(s))
    idx_to = _pytosim_max(idx_to, idx_from)
    return simstr.strmid(s, idx_from, idx_to)
