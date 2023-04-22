# -*- coding: utf-8 -*-
from .types import HBuffer, HSymbol, Symbol


def SymListCount() -> int:
    pass


def SymListFree(hsyml: HSymbol):
    pass


def SymListInsert(hsyml: HSymbol, isym: int, symbolNew: Symbol):
    pass


def SymListItem(hsyml: HSymbol, isym: int):
    pass


def SymListNew() -> HSymbol:
    pass


def SymListRemove(hsyml: HSymbol, isym: int):
    pass


def GetBufSymCount(hbuf: HBuffer) -> int:
    pass


def GetBufSymLocation(hbuf: HBuffer, isym: int) -> int:
    pass


def GetBufSymName(hbuf: HBuffer, isym: int) -> str:
    pass


def GetCurSymbol() -> str:
    pass


def GetSymbolLine(symbol_name: str) -> int:
    pass


def GetSymbolLocation(symbol_name: str) -> Symbol:
    """Get the symbol location (Seems not working now)

    Try GetSymbolLocationEx()
    """
    pass


def GetSymbolLocationEx(
    symbol_name: str,
    output_buffer: HBuffer,
    fMatchCase: bool,
    fLocateFiles: bool,
    fLocateSymbols: bool,
) -> Symbol:
    """Get the symbol location

    'symbol_name': If we want to find a file, you sould give it's name with
    extension!
    """
    pass


def GetSymbolFromCursor(hbuf: HBuffer, ln: int, ich: int) -> Symbol:
    pass


def GetSymbolLocationFromLn(hbuf: HBuffer, ln: int) -> Symbol:
    pass


def JumpToLocation(symbol_record: Symbol):
    pass


def JumpToSymbolDef(symbol_name: str):
    pass


def SymbolChildren(symbol: Symbol) -> HSymbol:
    pass


def SymbolContainerName(symbol: Symbol):
    pass


def SymbolDeclaredType(symbol: Symbol):
    pass


def SymbolLeafName(symbol: Symbol):
    pass


def SymbolParent(symbol: Symbol):
    pass


def SymbolRootContainer(symbol: Symbol):
    pass


def SymbolStructureType(symbol: Symbol):
    pass
