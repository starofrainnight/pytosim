# -*- coding: utf-8 -*-


from typing import Any, Union
from .types import HBuffer, ProgEnvInfo, ProgInfo


def GetEnv(env_name: str) -> str:
    pass


def GetReg(reg_key_name: str) -> Any:
    pass


def IsCmdEnabled(cmd_name: str) -> bool:
    pass


def PutEnv(env_name: str, value: str):
    pass


def RunCmd(cmd_name: str):
    pass


def RunCmdLine(sCmdLine: str, sWorkingDirectory: Union[str, None], fWait: bool) -> int:
    pass


def SetReg(reg_key_name: str, value):
    pass


def ShellExecute(
    sVerb: str,
    sFile: str,
    sExtraParams: str,
    sWorkingDirectory: str,
    windowstate: int,
):
    pass


def DumpMacroState(hbufOutput: HBuffer):
    pass


def GetProgramEnvironmentInfo() -> ProgEnvInfo:
    pass


def GetProgramInfo() -> ProgInfo:
    pass
