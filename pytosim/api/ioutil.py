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
    """Display a message window showing the string s. The message box has a
    Cancel button that the user can click to stop the macro. The message
    window stays up after returning.

    NOTE: It have a special side effect: If you want to execute a long time
    script, StartMsg() will ignore the gui events which slow down the script!
    So, if you think the script not works as expect then just wrap it by a
    StartMsg() & EndMsg() pair!
    """
    pass
