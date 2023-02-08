# -*- coding: utf-8 -*-

from .types import Bookmark


def BookmarksAdd(name: str, filename: str, ln: int, ich: int) -> bool:
    pass


def BookmarksCount() -> int:
    pass


def BookmarksDelete(name: str):
    pass


def BookmarksItem(index: int) -> Bookmark:
    pass


def BookmarksLookupLine(filename: str, ln: int) -> Bookmark:
    pass


def BookmarksLookupName(name: str) -> Bookmark:
    pass
