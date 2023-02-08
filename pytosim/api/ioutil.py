# -*- coding: utf-8 -*-

from .types import SYSTIME


def Ask(prompt: str):
    pass


def AssignKeyToCmd(key_value: int, cmd_name: str):
    pass


def Beep():
    pass


def CharFromKey(key_code: int) -> str:
    pass


def CmdFromKey(key_value: int) -> str:
    pass


def EndMsg():
    pass


def FuncFromKey(key_code: int) -> str:
    pass


def GetChar() -> str:
    pass


def GetKey() -> int:
    pass


def GetSysTime(fLocalTime: int) -> SYSTIME:
    pass


def IsAltKeyDown(key_code: int) -> bool:
    pass


def IsCtrlKeyDown(key_code: int) -> bool:
    pass


def IsFuncKey(key_code: int) -> bool:
    pass


def KeyFromChar(ch: str, fCtrl: bool, fShift: bool, fAlt: bool) -> int:
    pass


def Msg(s: str):
    pass


def StartMsg(s: str):
    pass
