# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Bookmark:
    Name: str
    File: str
    ln: int
    ich: int


@dataclass
class Bufprop:
    Name: str
    fNew: bool
    fDirty: bool
    fReadOnly: bool
    fClip: bool
    fMacro: bool
    fRunningMacro: bool
    fCaptureResults: bool
    fSearchResults: bool
    fProtected: bool
    lnCount: int
    Language: str
    DocumentType: str


@dataclass
class DIM:
    Cxp: int
    Cyp: int


@dataclass
class Link:
    File: str
    ln: int


@dataclass
class ProgEnvInfo:
    ProgramDir: str
    TempDir: str
    BackupDir: str
    ClipDir: str
    ProjectDirectoryFile: str
    ConfigurationFile: str
    ShellCommand: str
    UserName: str
    UserOrganization: str
    SerialNumber: str


@dataclass
class ProgInfo:
    ProgramName: str
    versionMajor: int
    versionMinor: int
    versionBuild: int
    CopyrightMsg: str
    fTrialVersion: bool
    fBetaVersion: bool
    ExeFileName: str
    cchLineMax: int
    cchPathMax: int
    cchSymbolMax: int
    cchCmdMax: int
    cchBookmarkMax: int
    cchInputMax: int
    cchMacroStringMax: int
    lnMax: int
    integerMax: int
    integerMin: int


@dataclass
class Rect:
    Left: int
    Top: int
    Right: int
    Bottom: int


@dataclass
class Selection:
    lnFirst: int
    ichFirst: int
    lnLast: int
    ichLim: int
    fExtended: bool
    fRect: bool
    xLeft: int
    xRight: int


@dataclass
class Symbol:
    Symbol: str
    Type: str
    Project: str
    File: str
    lnFirst: int
    lnLim: int
    lnName: int
    ichName: int
    Instsance: int


@dataclass
class SYSTIME:
    time: str
    date: str
    Year: int
    Month: int
    DayOfWeek: int
    Day: int
    Hour: int
    Minute: int
    Second: int
    Milliseconds: int


# Source Insight handle type
class HBuffer(object):
    pass


class HWnd(object):
    pass


class HSymbol(object):
    pass


class HProj(object):
    pass
