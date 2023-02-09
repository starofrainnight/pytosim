import ast
import os
import os.path
import click
import weakref
from typing import Any, Union
from pathlib import Path
from ast import (
    AST,
    Add,
    Assign,
    BinOp,
    Break,
    Call,
    Compare,
    Constant,
    Continue,
    Div,
    Eq,
    Expr,
    For,
    FormattedValue,
    FunctionDef,
    Global,
    Gt,
    GtE,
    If,
    IfExp,
    Import,
    ImportFrom,
    JoinedStr,
    List,
    Load,
    Lt,
    LtE,
    Mod,
    Module,
    Mult,
    NodeVisitor,
    Name,
    Pass,
    Return,
    Store,
    Tuple,
    While,
    arg,
    arguments,
)
from .util import str_quote, str_unquote


class SimBlock(object):
    def __init__(self) -> None:
        self._parent: Union[SimBlock, None] = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    def get_indent_levels(self):
        block = self

        cnt = -1
        while block:
            cnt = cnt + 1
            block = block._parent

        return cnt


class SimScope(SimBlock):
    def __init__(self) -> None:
        super().__init__()


class SimContext(object):
    def __init__(self, parent=None) -> None:
        self._indent_symbol = " " * 4
        self._src_lines = []
        self._cur_block = None
        self._cur_line = []
        self._elem_id = 0

    def gen_elem_id(self) -> int:
        self._elem_id += 1
        return self._elem_id

    def gen_var(self) -> str:
        return "_pytosim_var%s" % self.gen_elem_id()

    def get_indents(self) -> str:
        return self._indent_symbol * self._cur_block.get_indent_levels()

    def enter_block(self, block: SimBlock) -> None:
        if self._cur_block is not None:
            block.parent = self._cur_block

        self._cur_block = block

    def leave_block(self) -> None:
        if self._cur_line:
            self.pack_cur_line()

        if self._cur_block is not None:
            self._cur_block = self._cur_block.parent

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


class SimVisitor(NodeVisitor):
    def __init__(self) -> None:
        super().__init__()

        self._ctx = SimContext()

    def run(self, node: AST, filename=None) -> Any:
        self._filename = filename
        self.visit(node)

        for line in self._ctx._src_lines:
            print(line)

    def generic_visit(self, node: AST) -> Any:
        raise click.ClickException(
            "%s (%s): Unsupported python element: %s!"
            % (os.path.basename(self._filename), node.lineno, node)
        )

    def visit_arguments(self, node: arguments):
        texts = []
        for arg in node.args:
            texts.append(arg.arg)

        return ", ".join(texts)

    def visit_Tuple(self, node: Tuple) -> Any:
        # Just silent ignored
        pass

    def visit_Name(self, node: Name) -> Any:
        return node.id

    def visit_Store(self, node: Store) -> Any:
        return "="

    def visit_Mod(self, node: Mod) -> Any:
        return "%"

    def visit_BinOp(self, node: BinOp) -> Any:
        if isinstance(node.op, Mod):
            # Only support raw string format
            raise click.ClickException(
                "%s (%s): No support for Modulo operation!"
                % (os.path.basename(self._filename), node.lineno)
            )

        return "(%s %s %s)" % (
            super().visit(node.left),
            super().visit(node.op),
            super().visit(node.right),
        )

    def visit_Add(self, node: Add) -> Any:
        return "+"

    def visit_Mult(self, node: Mult) -> Any:
        return "*"

    def visit_Div(self, node: Div) -> Any:
        return "/"

    def visit_Constant(self, node: Constant) -> Any:
        return (
            '"%s"' % node.value if isinstance(node.value, str) else node.value
        )

    def visit_Eq(self, node: Eq) -> Any:
        return "=="

    def visit_Gt(self, node: Gt) -> Any:
        return ">"

    def visit_GtE(self, node: GtE) -> Any:
        return ">="

    def visit_Lt(self, node: Lt) -> Any:
        return "<"

    def visit_LtE(self, node: LtE) -> Any:
        return "<="

    def visit_Compare(self, node: Compare) -> Any:
        return "%s %s %s" % (
            super().visit(node.left),
            super().visit(node.ops[0]),
            super().visit(node.comparators[0]),
        )

    def visit_FormattedValue(self, node: FormattedValue) -> Any:
        return super().visit(node.value)

    def visit_JoinedStr(self, node: JoinedStr) -> Any:
        result = list()
        for elem in node.values:
            if isinstance(elem, FormattedValue):
                value = super().visit(elem)
                if value.isidentifier():
                    result.append("%%%s%%" % value)
                else:
                    variable = self._ctx.gen_var()
                    self._ctx.prepend_line("%s = %s" % (variable, value))
                    result.append("%%%s%%" % variable)
            else:
                result.append(str_unquote(super().visit(elem)))

        return str_quote("".join(result))

    def visit_Global(self, node: Global) -> Any:
        for elem in node.names:
            self._ctx.append_line("global %s" % elem)

    def visit_Pass(self, node: Pass) -> Any:
        # Silent ignores
        pass

    def visit_Load(self, node: Load) -> Any:
        # Silent ignored
        pass

    def visit_Expr(self, node: Expr) -> Any:
        value = self.visit(node.value)
        if value:
            self._ctx.append_cur_line(str(value))
            self._ctx.pack_cur_line()

    def visit_Return(self, node: Return) -> Any:
        self._ctx.pack_cur_line()
        self._ctx.append_cur_line("return ")
        if node.value:
            self._ctx.append_cur_line(str(self.visit(node.value)))
        self._ctx.pack_cur_line()

    def visit_Continue(self, node: Continue) -> Any:
        self._ctx.append_line("continue")

    def visit_Break(self, node: Break) -> Any:
        self._ctx.append_line("break")

    def visit_Assign(self, node: Assign) -> Any:
        lop = node.targets[0]
        rop = node.value

        if isinstance(lop, Name):
            self._ctx.pack_cur_line()
            self._ctx.append_cur_line(
                "%s = %s" % (super().visit(lop), super().visit(rop))
            )
            self._ctx.pack_cur_line()
        else:
            # Assume rop as Tuple
            self._ctx.pack_cur_line()
            for name_node, value_node in zip(lop.elts, rop.elts):
                self._ctx.append_cur_line(
                    "%s = %s"
                    % (super().visit(name_node), super().visit(value_node))
                )
                self._ctx.pack_cur_line()

    def visit_Module(self, node: Module) -> Any:
        self._ctx.enter_block(SimBlock())
        try:
            super().generic_visit(node)
        finally:
            self._ctx.leave_block()

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        self._ctx.pack_cur_line()

        # Parse function declaration with arguments
        self._ctx.append_cur_line("macro %s" % node.name)
        self._ctx.append_cur_line("(%s)" % self.visit(node.args))
        self._ctx.pack_cur_line()
        self._ctx.append_cur_line("{")
        self._ctx.pack_cur_line()

        self._ctx.enter_block(SimScope())
        try:
            # super().generic_visit(node)
            for stmt in node.body:
                self.visit(stmt)
        finally:
            self._ctx.leave_block()

        self._ctx.append_cur_line("}")
        self._ctx.pack_cur_line()

    def visit_ImportFrom(self, node: ImportFrom) -> Any:
        # Ignore import keyword
        pass

    def visit_Import(self, node: Import) -> Any:
        # Ignore import keyword
        pass

    def visit_Call(self, node: Call) -> Any:
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        else:
            func_name = node.func.id

        texts = []
        texts.append(self.visit(node.func))
        texts.append("(")

        arg_texts = []
        for arg in node.args:
            value = self.visit(arg)
            if isinstance(value, str):
                arg_texts.append('"%s"' % value)
            else:
                arg_texts.append(str(value))

        texts.append(", ".join(arg_texts))
        texts.append(")")

        return "".join(texts)

    def visit_If(self, node: If) -> Any:
        self._ctx.append_cur_line("if (%s)" % (self.visit(node.test),))
        self._ctx.pack_cur_line()

        self._ctx.append_cur_line("{")
        self._ctx.pack_cur_line()
        self._ctx.enter_block(SimBlock())
        for child in node.body:
            super().visit(child)
        self._ctx.leave_block()
        self._ctx.pack_cur_line()
        self._ctx.append_cur_line("}")
        self._ctx.pack_cur_line()

        if len(node.orelse):
            if (len(node.orelse) == 1) and isinstance(node.orelse[0], If):
                self._ctx.append_cur_line("else ")
                super().visit(node.orelse[0])
            else:
                self._ctx.append_cur_line("else")
                self._ctx.pack_cur_line()

                self._ctx.append_cur_line("{")
                self._ctx.pack_cur_line()

                self._ctx.enter_block(SimBlock())
                for child in node.orelse:
                    super().visit(child)
                self._ctx.leave_block()

                self._ctx.append_cur_line("}")
                self._ctx.pack_cur_line()

    def visit_IfExp(self, node: IfExp) -> Any:
        var_name = self._ctx.gen_var()
        self._ctx.prepend_line("if (%s)" % self.visit(node.test))
        self._ctx.enter_block(SimBlock())
        self._ctx.prepend_line("%s = %s" % (var_name, self.visit(node.body)))
        self._ctx.leave_block()
        self._ctx.prepend_line("else")
        self._ctx.enter_block(SimBlock())
        self._ctx.prepend_line("%s = %s" % (var_name, self.visit(node.orelse)))
        self._ctx.leave_block()
        return var_name

    def visit_While(self, node: While) -> Any:
        var_name = self._ctx.gen_var()

        self._ctx.append_line("%s = %s" % (var_name, self.visit(node.test)))
        self._ctx.append_line("while (%s)" % var_name)
        self._ctx.append_line("{")
        self._ctx.enter_block(SimBlock())
        for child in node.body:
            super().visit(child)
        self._ctx.leave_block()
        self._ctx.append_line("}")

        if node.orelse:
            self._ctx.append_line("if (!%s)" % var_name)
            self._ctx.append_line("{")
            self._ctx.enter_block(SimBlock())
            for child in node.orelse:
                super().visit(child)
            self._ctx.leave_block()
            self._ctx.append_line("}")

    def visit_For(self, node: For) -> Any:
        if node.orelse:
            raise click.ClickException(
                "%s (%s): Unsupported for loop with 'else' statement!"
                % (os.path.basename(self._filename), node.lineno)
            )

        if not (isinstance(node.iter, Call) and node.iter.func.id == "range"):
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
        self._ctx.enter_block(SimBlock())
        self._ctx.append_line(
            "%s = %s + (%s)" % (var_name, var_name, iter_step)
        )
        for elem in node.body:
            self.visit(elem)
        self._ctx.leave_block()
        self._ctx.append_line("}")


@click.command()
@click.argument("pyscript")
def main(pyscript):
    """A compiler for convert Python source to Source Insight 3.5 Macro"""
    out_path = Path(pyscript).with_suffix(".em")
    with open(pyscript, "r") as f:
        root = ast.parse(f.read(), filename=pyscript)
    visitor = SimVisitor()
    visitor.run(root, pyscript)


if __name__ == "__main__":
    # execute only if run as a script
    main()
