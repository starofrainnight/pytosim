# -*- coding: utf-8 -*-


from typing import Any
from .types import Bufprop, HBuffer


def BufListCount() -> int:
    pass


def BufListItem(index: int) -> HBuffer:
    pass


def AppendBufLine(hbuf: HBuffer, s: str):
    pass


def ClearBuf(hbuf: HBuffer):
    pass


def CloseBuf(hbuf: HBuffer):
    pass


def CopyBufLine(hbuf: HBuffer, ln: int):
    pass


def DelBufLine(hbuf: HBuffer, ln: int):
    pass


def GetBufHandle(filename: str) -> HBuffer:
    pass


def GetBufLine(hbuf: HBuffer, ln: int) -> str:
    pass


def GetBufLineCount(hbuf: HBuffer) -> int:
    pass


def GetBufLineLength(hbuf: HBuffer, ln: int) -> int:
    pass


def GetBufLnCur(hbuf: HBuffer) -> int:
    pass


def GetBufName(hbuf: HBuffer) -> str:
    pass


def GetBufProps(hbuf: HBuffer) -> Bufprop:
    pass


def GetBufSelText(hbuf: HBuffer) -> str:
    pass


def GetCurrentBuf() -> HBuffer:
    pass


def InsBufLine(hbuf: HBuffer, ln: int, s: str):
    pass


def IsBufDirty(hbuf: HBuffer) -> bool:
    pass


def IsBufRW(hbuf: HBuffer) -> bool:
    pass


def MakeBufClip(hbuf: HBuffer, fClip: bool):
    pass


def NewBuf(name: str) -> HBuffer:
    pass


def OpenBuf(filename: str) -> HBuffer:
    pass


def OpenMiscFile(filename: str) -> bool:
    pass


def PasteBufLine(hbuf: HBuffer, ln: int):
    pass


def PrintBuf(hbuf: HBuffer, fUseDialogBox: bool):
    pass


def PutBufLine(hbuf: HBuffer, ln: int, s: str):
    pass


def RenameBuf(hbuf: HBuffer, szNewName: str):
    pass


def SaveBuf(hbuf: HBuffer):
    pass


def SaveBufAs(hbuf: HBuffer, filename: str):
    pass


def SetBufDirty(hbuf: HBuffer, fDirty: bool):
    pass


def SetBufIns(hbuf: HBuffer, ln: int, ich: int):
    pass


def SetBufSelText(hbuf: HBuffer, s: str):
    pass


def SetCurrentBuf(hbuf: HBuffer):
    pass
