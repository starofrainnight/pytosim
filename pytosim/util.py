# -*- coding: utf-8 -*-


def str_quote(s: str):
    return '"%s"' % s


def str_unquote(s: str):
    s = s.strip()
    if len(s) < 2:
        return s

    if s[0] != '"':
        return s

    if s[-1] != '"':
        return s

    return s[1:-1]
