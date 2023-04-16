# -*- coding: utf-8 -*-


def AsciiFromChar(ch: str) -> int:
    return ord(ch)


def cat(a: str, b: str) -> str:
    return a + b


def CharFromAscii(code: int) -> str:
    return chr(code)


def isLower(ch: str) -> bool:
    return ch.islower()


def isNumber(s: str) -> bool:
    return s.isnumeric()


def isupper(ch: str) -> bool:
    return ch.isupper()


def strlen(s: str) -> int:
    return len(s)


def strmid(s: str, ichFirst: int, ichLim: int) -> str:
    return s[ichFirst:ichLim]


def strtrunc(s: str, cch: int) -> str:
    return s[:cch]


def tolower(s: str) -> str:
    return s.lower()


def toupper(s: str) -> str:
    return s.upper()


def _get(s: str, idx: int) -> str:
    """A fake method to expand as "s[idx]" text"""
    return s[idx]
