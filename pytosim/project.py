# -*- coding: utf-8 -*-

from .types import HProj


def AddConditionVariable(hprj: HProj, szName, szValue):
    pass


def AddFileToProj(hprj: HProj, filename):
    pass


def CloseProj(hprj: HProj):
    pass


def DeleteConditionVariable(hprj: HProj, szName):
    pass


def DeleteProj(proj_name):
    pass


def EmptyProj():
    pass


def GetCurrentProj():
    pass


def GetProjDir(hprj: HProj):
    pass


def GetProjFileCount(hprj: HProj):
    pass


def GetProjFileName(hprj: HProj, ifile):
    pass


def GetProjName(hprj: HProj):
    pass


def GetProjSymCount(hprj: HProj):
    pass


def GetProjSymLocation(hprj: HProj, isym):
    pass


def GetProjSymName(hprj: HProj, isym):
    pass


def NewProj(proj_name):
    pass


def OpenProj(proj_name):
    pass


def RemoveFileFromProj(hprj: HProj, filename):
    pass


def SyncProj(hprj: HProj):
    pass


def SyncProjEx(hprj: HProj, fAddNewFiles, fForceAll, fSupressWarnings):
    pass
