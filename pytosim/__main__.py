# -*- coding: utf-8 -*-
import ast
import os
import os.path
import click
import weakref
from collections import deque
from typing import Any, Union, List, Deque, Callable
from pathlib import Path
from contextlib import contextmanager
from .util import str_quote, str_unquote


class VisitorError(click.ClickException):
    def __init__(self, message: str, filename=None, node=None):
        if node is not None:
            message = '%s\n\nTraceback:\n  File "%s", line %s' % (
                message,
                filename,
                node.lineno,
            )

        super().__init__(message)

        self.node = node


class NameError(VisitorError):
    pass


class VariableNotFoundError(VisitorError):
    pass


class VisitResult(object):
    def __init__(self, text: str, node, value_type=None):
        self.text = text
        self.node = node
        self.value_type = value_type

    def __str__(self):
        return self.text


class SimElement(object):
    pass


class SimFunction(SimElement):
    def __init__(self, name: str, node: ast.FunctionDef) -> None:
        self.name = name
        self.node = node


class SimVariable(SimElement):
    def __init__(self, name: str, value_type=str) -> None:
        self.name = name
        self.value_type = value_type


class SimModule(SimElement):
    def __init__(self, nchain: List[str]) -> None:
        self.nchain = nchain


class SimNChain(object):
    def __init__(
        self, source: List[str], module: List[str], children: List[str]
    ) -> None:
        self.module = module
        self.children = children
        self.source = source

    def resolve(self):
        return self.module + self.children


class SimBlock(object):
    BLOCK = 0
    SCOPE = 1

    def __init__(self, atype=BLOCK) -> None:
        self.type = atype
        self.vars: List[SimVariable] = list()
        self.funcs: List[SimFunction] = list()
        self.imports: List[Union[ast.Import, ast.ImportFrom]] = list()


class SimContext(object):
    def __init__(self, parent=None) -> None:
        self._indent_symbol = " " * 4
        self._src_lines = []
        self._block_stack = deque()  # type: Deque[SimBlock]
        self._cur_line = []
        self._elem_id = 0

    @contextmanager
    def open_block(self, block_type=SimBlock.BLOCK):
        try:
            block = SimBlock(block_type)
            self._block_stack.append(block)
            yield block
        finally:
            if self._cur_line:
                self.pack_cur_line()

            self._block_stack.pop()

    def get_last_scope(self) -> SimBlock:
        for it in reversed(self._block_stack):
            if it.type == SimBlock.SCOPE:
                return it

        raise IndexError()

    def gen_elem_id(self) -> int:
        self._elem_id += 1
        return self._elem_id

    def gen_var(self) -> str:
        return "_pytosim_var%s" % self.gen_elem_id()

    def get_indent_levels(self):
        return len(self._block_stack) - 1

    def get_indents(self) -> str:
        return self._indent_symbol * self.get_indent_levels()

    def prepend_line(self, text):
        self._src_lines.append(self.get_indents() + text)

    def append_line(self, text):
        self.pack_cur_line()
        self._src_lines.append(self.get_indents() + text)

    def append_cur_line(self, text) -> None:
        self._cur_line.append(text)

    def pack_cur_line(self):
        if not self._cur_line:
            return

        self._src_lines.append(self.get_indents() + "".join(self._cur_line))
        self._cur_line.clear()


class SimVisitor(ast.NodeVisitor):
    def __init__(self, filename: str) -> None:
        super().__init__()

        self._ctx = SimContext()
        self._filename = filename
        self._buildins = {
            "ord": "CharFromAscii",
            "chr": "AsciiFromChar",
            "len": "strlen",
            "min": "_pytosim_min",
            "max": "_pytosim_max",
        }

    def run(self, node: ast.AST, filename=None) -> Any:
        self._filename = filename
        self.visit(node)

        for line in self._ctx._src_lines:
            print(line)

    def get_name_chain(self, node) -> List[str]:
        names = list()
        while True:
            if isinstance(node, ast.Attribute):
                names.insert(0, node.attr)
                node = node.value
            else:
                names.insert(0, node.id)
                break

        return names

    def find_var(self, name):
        for block in filter(
            lambda it: it.type == SimBlock.SCOPE,
            reversed(self._ctx._block_stack),
        ):
            for avar in block.vars:
                # if avar in block.vars:
                if avar.name == name:
                    return avar

        raise VariableNotFoundError(name)

    def _get_nchain_from_call(self, node: ast.Call):
        nchain = []
        node = node.func
        while node:
            if isinstance(node, ast.Attribute):
                nchain.append(node.attr)
            else:
                nchain.append(node.id)
                break
            node = node.value

        return list(reversed(nchain))

    def _is_buildin_nchain(self, nchain) -> bool:
        return (len(nchain) == 1) and (nchain[0] in self._buildins)

    def _resolve_nchain_from_import(
        self, node: ast.Import, nchain: List[str]
    ) -> SimNChain:
        for analias in node.names:
            if analias.asname:
                if nchain[0] == analias.asname:
                    module_nchain = analias.name.split(".")
                    return SimNChain(nchain, module_nchain, nchain[1:])
                continue

            # No alias
            module_nchain = analias.name.split(".")
            if len(module_nchain) < len(nchain):
                continue

            matched_nchain = nchain[: len(module_nchain)]
            if module_nchain != matched_nchain:
                continue

            return SimNChain(
                nchain, module_nchain, nchain[len(module_nchain) - 1 :]
            )

        raise NameError("name '%s' is not defined" % nchain[0])

    def _resolve_nchain_from_import_from(
        self, node: ast.ImportFrom, nchain: List[str]
    ):
        for analias in node.names:
            if nchain[0] in [analias.asname or analias.name]:
                return SimNChain(
                    nchain, node.module.split("."), [analias.name]
                )

        raise NameError("name '%s' is not defined" % nchain[0])

    def _resolve_nchain(self, nchain) -> SimNChain:
        for scope in self._ctx._block_stack:
            if scope.type != SimBlock.SCOPE:
                continue

            for it in scope.vars:
                if nchain[0] == it.name:
                    return SimNChain(nchain, ["."], nchain)

            for it in scope.funcs:
                if nchain[0] == it.name:
                    return SimNChain(nchain, ["."], nchain)

            for it in scope.imports:
                if isinstance(it, ast.Import):
                    try:
                        return self._resolve_nchain_from_import(it, nchain)
                    except NameError:
                        pass

                elif isinstance(it, ast.ImportFrom):
                    try:
                        return self._resolve_nchain_from_import_from(
                            it, nchain
                        )
                    except NameError:
                        pass

        raise NameError("name '%s' is not defined" % nchain[0])

    def generic_visit(self, node: ast.AST) -> Any:
        raise click.ClickException(
            "%s (%s): Unsupported python element: %s!"
            % (os.path.basename(self._filename), node.lineno, node)
        )

    def visit_arguments(self, node: ast.arguments) -> VisitResult:
        texts = []
        for arg in node.args:
            texts.append(arg.arg)

        return VisitResult(", ".join(texts), node)

    def visit_Tuple(self, node: ast.Tuple) -> Any:
        # Just silent ignored
        pass

    def visit_Name(self, node: ast.Name) -> VisitResult:
        return VisitResult(node.id, node)

    def visit_Store(self, node: ast.Store) -> VisitResult:
        return VisitResult("=", node)

    def visit_Mod(self, node: ast.Mod) -> VisitResult:
        return VisitResult("%", node)

    def visit_BinOp(self, node: ast.BinOp) -> VisitResult:
        lvalue = super().visit(node.left)
        opvalue = super().visit(node.op)
        rvalue = super().visit(node.right)
        result_value_type = None

        if lvalue.value_type == float or rvalue.value_type == float:
            result_value_type = float
        elif lvalue.value_type == int or rvalue.value_type == int:
            result_value_type = int

        if isinstance(node.op, ast.Mod):
            if lvalue.value_type == str:
                # Only support raw string format
                raise click.ClickException(
                    "%s (%s): Unsupport modulo operation!"
                    % (os.path.basename(self._filename), node.lineno)
                )
            else:
                lvar = self._ctx.gen_var()
                mvar = self._ctx.gen_var()  # Middle variable
                rvar = self._ctx.gen_var()

                self._ctx.prepend_line("%s = %s" % (lvar, lvalue))
                self._ctx.prepend_line("%s = %s / %s" % (mvar, lvalue, rvalue))
                self._ctx.prepend_line("%s = %s" % (rvar, rvalue))
                return VisitResult(
                    "(%s - %s * %s)" % (lvar, mvar, rvar),
                    node,
                    result_value_type,
                )

        return VisitResult(
            "(%s %s %s)" % (lvalue, opvalue, rvalue),
            node,
            result_value_type,
        )

    def visit_Add(self, node: ast.Add) -> VisitResult:
        return VisitResult("+", node)

    def visit_Sub(self, node: ast.Sub) -> VisitResult:
        return VisitResult("-", node)

    def visit_USub(self, node: ast.USub) -> VisitResult:
        return VisitResult("-", node)

    def visit_Mult(self, node: ast.Mult) -> VisitResult:
        return VisitResult("*", node)

    def visit_Div(self, node: ast.Div) -> VisitResult:
        return VisitResult("/", node)

    def visit_Constant(self, node: ast.Constant) -> VisitResult:
        return VisitResult(
            ('"%s"' % node.value)
            if isinstance(node.value, str)
            else str(node.value),
            node,
            type(node.value),
        )

    def visit_Eq(self, node: ast.Eq) -> VisitResult:
        return VisitResult("==", node)

    def visit_Gt(self, node: ast.Gt) -> VisitResult:
        return VisitResult(">", node)

    def visit_GtE(self, node: ast.GtE) -> VisitResult:
        return VisitResult(">=", node)

    def visit_Lt(self, node: ast.Lt) -> VisitResult:
        return VisitResult("<", node)

    def visit_LtE(self, node: ast.LtE) -> VisitResult:
        return VisitResult("<=", node)

    def visit_Attribute(self, node: ast.Attribute) -> VisitResult:
        return VisitResult(node.attr, node)

    def visit_Compare(self, node: ast.Compare) -> VisitResult:
        return VisitResult(
            "%s %s %s"
            % (
                super().visit(node.left),
                super().visit(node.ops[0]),
                super().visit(node.comparators[0]),
            ),
            node,
            bool,
        )

    def visit_FormattedValue(self, node: ast.FormattedValue) -> VisitResult:
        return VisitResult(super().visit(node.value).text, node)

    def visit_JoinedStr(self, node: ast.JoinedStr) -> VisitResult:
        result = list()
        for elem in node.values:
            if isinstance(elem, ast.FormattedValue):
                value = super().visit(elem)
                if value.text.isidentifier():
                    result.append("@%s@" % value)
                else:
                    variable = self._ctx.gen_var()
                    self._ctx.prepend_line("%s = %s" % (variable, value))
                    result.append("@%s@" % variable)
            else:
                value = str_unquote(str(super().visit(elem)))
                value = value.replace("@", r"\@")
                result.append(value)

        return VisitResult(str_quote("".join(result)), node)

    def visit_Subscript(self, node: ast.Subscript) -> Any:
        # a[x] # The subscript x of a
        return VisitResult(
            "%s[%s]" % (super().visit(node.value), super().visit(node.slice)),
            node,
        )

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        return VisitResult(
            "%s%s" % (super().visit(node.op), super().visit(node.operand)),
            node,
        )

    def visit_Global(self, node: ast.Global) -> Any:
        for elem in node.names:
            self._ctx.append_line("global %s" % elem)

    def visit_Pass(self, node: ast.Pass) -> Any:
        # Silent ignores
        pass

    def visit_Load(self, node: ast.Load) -> Any:
        # Silent ignored
        pass

    def visit_Expr(self, node: ast.Expr) -> Any:
        value = self.visit(node.value)
        if value:
            self._ctx.append_cur_line(str(value))
            self._ctx.pack_cur_line()

    def visit_Return(self, node: ast.Return) -> Any:
        self._ctx.pack_cur_line()
        self._ctx.append_cur_line("return ")
        if node.value:
            self._ctx.append_cur_line(str(self.visit(node.value)))
        self._ctx.pack_cur_line()

    def visit_Continue(self, node: ast.Continue) -> Any:
        self._ctx.append_line("continue")

    def visit_Break(self, node: ast.Break) -> Any:
        self._ctx.append_line("break")

    def visit_Assign(self, node: ast.Assign) -> Any:
        lop = node.targets[0]
        rop = node.value

        if isinstance(lop, ast.Name):
            self._ctx.pack_cur_line()
            lname = super().visit(lop)
            rname = super().visit(rop)
            self._ctx.append_cur_line("%s = %s" % (lname, rname))
            self._ctx.pack_cur_line()

            scope = self._ctx.get_last_scope()
            scope.vars.append(SimVariable(lname))
        else:
            # Assume rop as Tuple
            self._ctx.pack_cur_line()
            for name_node, value_node in zip(lop.elts, rop.elts):
                lname = super().visit(name_node)
                rname = super().visit(value_node)
                self._ctx.append_cur_line("%s = %s" % (lname, rname))
                self._ctx.pack_cur_line()
                scope = self._ctx.get_last_scope()
                scope.vars.append(SimVariable(lname))

    def visit_Module(self, node: ast.Module) -> Any:
        with self._ctx.open_block(SimBlock.SCOPE):
            super().generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self._ctx.pack_cur_line()

        # Parse function declaration with arguments
        self._ctx.append_cur_line("macro %s" % node.name)
        self._ctx.append_cur_line("(%s)" % self.visit(node.args))
        self._ctx.pack_cur_line()
        self._ctx.append_cur_line("{")
        self._ctx.pack_cur_line()

        with self._ctx.open_block(SimBlock.SCOPE):
            for stmt in node.body:
                self.visit(stmt)

        self._ctx.append_cur_line("}")
        self._ctx.pack_cur_line()

        # Only supports module area function definition
        last_scope = self._ctx.get_last_scope()
        first_scope = self._ctx._block_stack[0]
        if last_scope != first_scope:
            raise VisitorError(
                "Function definition only allowed in module level!",
                self._filename,
                node,
            )

        first_scope.funcs.append(SimFunction(node.name, node))

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        # Ignore import keyword
        scope = self._ctx.get_last_scope()
        scope.imports.append(node)

    def visit_Import(self, node: ast.Import) -> Any:
        # Ignore import keyword
        scope = self._ctx.get_last_scope()
        scope.imports.append(node)

    def visit_BuildIns(self, node: ast.Call) -> Any:
        nchain = self._get_nchain_from_call(node)
        var_name = nchain[-1]
        replaced_name = self._buildins.get(var_name, "")

        return VisitResult(replaced_name, Any)

    def visit_Call(self, node: ast.Call) -> Any:
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        else:
            func_name = node.func.id

        nchain = self._get_nchain_from_call(node)
        is_buildin = False
        try:
            nchain = self._resolve_nchain(nchain)
        except NameError as e:
            is_buildin = self._is_buildin_nchain(nchain)
            if not is_buildin:
                raise NameError(e.message, self._filename, node)

        if is_buildin:
            mapped_func_name = self.visit_BuildIns(node).text
        else:
            # Support special pytosim.api.cmds convertion
            cmds_api_nchain = ["pytosim", "api", "cmds"]
            if (len(nchain.module) >= len(cmds_api_nchain)) and (
                nchain.module[: len(cmds_api_nchain)] == cmds_api_nchain
            ):
                return nchain.children[0]

            mapped_func_name = nchain.children[-1]

        texts = []
        texts.append(mapped_func_name)
        texts.append("(")

        arg_texts = []
        for arg in node.args:
            value = self.visit(arg)
            arg_texts.append(str(value))

        texts.append(", ".join(arg_texts))
        texts.append(")")

        return VisitResult("".join(texts), node, value_type=Callable)

    def visit_If(self, node: ast.If) -> Any:
        self._ctx.append_cur_line("if (%s)" % (self.visit(node.test),))
        self._ctx.pack_cur_line()

        self._ctx.append_cur_line("{")
        self._ctx.pack_cur_line()
        with self._ctx.open_block():
            for child in node.body:
                super().visit(child)
        self._ctx.pack_cur_line()
        self._ctx.append_cur_line("}")
        self._ctx.pack_cur_line()

        if len(node.orelse):
            if (len(node.orelse) == 1) and isinstance(node.orelse[0], ast.If):
                self._ctx.append_cur_line("else ")
                super().visit(node.orelse[0])
            else:
                self._ctx.append_cur_line("else")
                self._ctx.pack_cur_line()

                self._ctx.append_cur_line("{")
                self._ctx.pack_cur_line()

                with self._ctx.open_block():
                    for child in node.orelse:
                        super().visit(child)

                self._ctx.append_cur_line("}")
                self._ctx.pack_cur_line()

    def visit_IfExp(self, node: ast.IfExp) -> Any:
        var_name = self._ctx.gen_var()
        self._ctx.prepend_line("if (%s)" % self.visit(node.test))
        with self._ctx.open_block():
            self._ctx.prepend_line(
                "%s = %s" % (var_name, self.visit(node.body))
            )
        self._ctx.prepend_line("else")
        with self._ctx.open_block():
            self._ctx.prepend_line(
                "%s = %s" % (var_name, self.visit(node.orelse))
            )
        return VisitResult(var_name, node)

    def visit_While(self, node: ast.While) -> Any:
        var_name = self._ctx.gen_var()

        self._ctx.append_line("%s = 0" % var_name)
        self._ctx.append_line("while (1)")
        self._ctx.append_line("{")
        with self._ctx.open_block():
            self._ctx.append_line(
                "%s = %s" % (var_name, self.visit(node.test))
            )
            self._ctx.append_line("if (!%s) break" % var_name)
            for child in node.body:
                super().visit(child)
        self._ctx.append_line("}")

        if node.orelse:
            self._ctx.append_line("if (!%s)" % var_name)
            self._ctx.append_line("{")
            with self._ctx.open_block():
                for child in node.orelse:
                    super().visit(child)
            self._ctx.append_line("}")

    def visit_For(self, node: ast.For) -> Any:
        if not (
            isinstance(node.iter, ast.Call) and node.iter.func.id == "range"
        ):
            raise click.ClickException(
                "%s (%s): Unsupported for loop with iterator not a range object!"
                % (os.path.basename(self._filename), node.lineno)
            )

        var_name = self.visit(node.target)
        iter_start = 0
        iter_stop = 0
        iter_step = 1
        if len(node.iter.args) == 1:
            iter_stop = self.visit(node.iter.args[0])
        elif len(node.iter.args) == 2:
            iter_start = self.visit(node.iter.args[0])
            iter_stop = self.visit(node.iter.args[1])
        elif len(node.iter.args) == 3:
            iter_start = self.visit(node.iter.args[0])
            iter_stop = self.visit(node.iter.args[1])
            iter_step = self.visit(node.iter.args[2])
        else:
            raise click.ClickException(
                "%s (%s): Unsupported for loop with iterator and a range object with unknow arguments!"
                % (os.path.basename(self._filename), node.lineno)
            )

        self._ctx.append_line("%s = %s" % (var_name, iter_start))
        self._ctx.append_line("while (%s < %s)" % (var_name, iter_stop))
        self._ctx.append_line("{")
        with self._ctx.open_block():
            for elem in node.body:
                self.visit(elem)

            self._ctx.append_line(
                "%s = %s + (%s)" % (var_name, var_name, iter_step)
            )
        self._ctx.append_line("}")

        if node.orelse:
            self._ctx.append_line("if (%s >= %s)" % (var_name, iter_stop))
            self._ctx.append_line("{")
            with self._ctx.open_block():
                for child in node.orelse:
                    super().visit(child)
            self._ctx.append_line("}")


@click.group()
def main():
    pass


@main.command()
def compile_base():
    """Generate the pytosim base macro file"""

    pyscript = os.path.join(
        os.path.dirname(__file__), "data", "pytosimbase.py"
    )
    out_path = Path(pyscript).with_suffix(".em")
    with open(pyscript, "r") as f:
        root = ast.parse(f.read(), filename=pyscript)
    visitor = SimVisitor(pyscript)
    visitor.run(root, pyscript)


@main.command()
@click.argument("pyscript")
def compile(pyscript):
    """A compiler for convert Python source to Source Insight 3.5 Macro"""
    out_path = Path(pyscript).with_suffix(".em")
    with open(pyscript, "r") as f:
        root = ast.parse(f.read(), filename=pyscript)
    visitor = SimVisitor(pyscript)
    visitor.run(root, pyscript)


if __name__ == "__main__":
    # execute only if run as a script
    main()
