# -*- coding: utf-8 -*-

# Decorators for events

from functools import wraps

def AppStart(f):
    return f


def AppShutdown(f):
    return f


def AppCommand(f):
    @wraps(f)
    def decorated(sCommand):
        return f(sCommand)
    return decorated


def DocumentNew(f):
    @wraps(f)
    def decorated(sFile):
        return f(sFile)
    return decorated


def DocumentOpen(f):
    @wraps(f)
    def decorated(sFile):
        return f(sFile)
    return decorated


def DocumentClose(f):
    @wraps(f)
    def decorated(sFile):
        return f(sFile)
    return decorated


def DocumentSave(f):
    @wraps(f)
    def decorated(sFile):
        return f(sFile)
    return decorated


def DocumentSaveComplete(f):
    @wraps(f)
    def decorated(sFile):
        return f(sFile)
    return decorated


def DocumentChanged(f):
    @wraps(f)
    def decorated(sFile):
        return f(sFile)
    return decorated


def DocumentSelectionChanged(f):
    @wraps(f)
    def decorated(sFile):
        return f(sFile)
    return decorated


def ProjectOpen(f):
    @wraps(f)
    def decorated(sProject):
        return f(sProject)
    return decorated


def ProjectClose(f):
    @wraps(f)
    def decorated(sProject):
        return f(sProject)
    return decorated


def StatusbarUpdate(f):
    @wraps(f)
    def decorated(sMessage):
        return f(sMessage)
    return decorated
