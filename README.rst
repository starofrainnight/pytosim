=======
pytosim
=======

A compiler for convert Python source to Source Insight 3.5 Macro

You should notice that, it's just supports a subset python features, and will never supports them all.

I just want to provide a python like macro language to replace the one Source Insight provided.

* License: Apache-2.0

Features
--------

* Control Flow Tools
    + if Statements
    + for Statements
    + The range() Function (Like but not fully supports)
    + break and continue
    + pass
    + Defining Functions
* Data Structures
    * Dictionaries
* Data Types
    * int
    * float
    * str (Just simple mapped to SIM's string, no unicode supports)
