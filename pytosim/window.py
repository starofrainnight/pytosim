# -*- coding: utf-8 -*-

from .types import DIM, HWnd, HBuffer, Rect, Selection


def WndListCount() -> int:
    pass


def WndListItem(index: int) -> HWnd:
    pass


def CloseWnd(hwnd: HWnd):
    pass


def GetApplicationWnd() -> HWnd:
    pass


def GetCurrentWnd() -> HWnd:
    pass


def GetNextWnd(hwnd: HWnd) -> HWnd:
    pass


def GetWndBuf(hwnd: HWnd) -> HBuffer:
    pass


def GetWndClientRect(hwnd: HWnd) -> Rect:
    pass


def GetWndDim(hwnd: HWnd) -> DIM:
    pass


def GetWndHandle(hbuf: HBuffer) -> HWnd:
    pass


def GetWndHorizScroll(hwnd: HWnd) -> int:
    pass


def GetWndLineCount(hwnd: HWnd) -> int:
    pass


def GetWndLineWidth(hwnd: HWnd, ln: int, cch: int) -> int:
    pass


def GetWndParent(hwnd: HWnd) -> HWnd:
    pass


def GetWndRect(hwnd: HWnd) -> Rect:
    pass


def GetWndSel(hwnd: HWnd) -> Selection:
    pass


def GetWndSelIchFirst(hwnd: HWnd) -> int:
    pass


def GetWndSelIchLim(hwnd: HWnd) -> int:
    pass


def GetWndSelLnFirst(hwnd: HWnd) -> int:
    pass


def GetWndSelLnLast(hwnd: HWnd) -> int:
    pass


def GetWndVertScroll(hwnd: HWnd) -> int:
    pass


def IchFromXpos(hwnd: HWnd, ln: int, xp) -> int:
    pass


def IsWndMax(hwnd: HWnd) -> bool:
    pass


def IsWndMin(hwnd: HWnd) -> bool:
    pass


def IsWndRestored(hwnd: HWnd) -> bool:
    pass


def MaximizeWnd(hwnd: HWnd):
    pass


def MinimizeWnd(hwnd: HWnd):
    pass


def NewWnd(hbuf: HBuffer) -> HWnd:
    pass


def ScrollWndHoriz(hwnd: HWnd, pixel_count: int):
    pass


def ScrollWndToLine(hwnd: HWnd, ln: int):
    pass


def ScrollWndVert(hwnd: HWnd, line_count: int):
    pass


def SetCurrentWnd(hwnd: HWnd):
    pass


def SetWndRect(hwnd: HWnd, left: int, top: int, right: int, bottom: int):
    pass


def SetWndSel(hwnd: HWnd, selection_record: Selection):
    pass


def ToggleWndMax(hwnd: HWnd):
    pass


def XposFromIch(hwnd: HWnd, ln: int, ich) -> int:
    pass
