"""
Safe Expression Evaluator
=========================

Provides ``safe_eval`` — a restricted expression evaluator that uses Python's
``ast`` module to parse and evaluate arithmetic / string expressions without
exposing the full power of ``eval()``.

Only the following node types are permitted:

* Literals (numbers, strings, booleans, None, lists, tuples, dicts)
* Unary operators (+, -, not, ~)
* Binary operators (+, -, *, /, //, %, **, <<, >>, &, |, ^)
* Boolean operators (and, or)
* Comparisons (==, !=, <, <=, >, >=, in, not in, is, is not)
* Variable / function name look-ups (resolved against an explicit allow-list)
* Function calls (only to names present in the allow-list)
* Subscript access (indexing)
* Attribute access on strings (e.g. s.upper())
* Conditional expressions (a if cond else b)

Everything else (imports, assignments, comprehensions, lambdas, walrus
operator, etc.) is rejected with a ``ValueError``.
"""

from __future__ import annotations

import ast
import operator
from typing import Any

# ---- Supported AST operators ------------------------------------------------

_UNARY_OPS: dict[type, Any] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
    ast.Not: operator.not_,
    ast.Invert: operator.invert,
}

_BIN_OPS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
    ast.BitAnd: operator.and_,
    ast.BitOr: operator.or_,
    ast.BitXor: operator.xor,
}

_CMP_OPS: dict[type, Any] = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.In: lambda a, b: a in b,
    ast.NotIn: lambda a, b: a not in b,
    ast.Is: operator.is_,
    ast.IsNot: operator.is_not,
}

# Safe string methods that can be called via attribute access
_SAFE_STR_METHODS = frozenset({
    "upper", "lower", "strip", "lstrip", "rstrip", "title", "capitalize",
    "startswith", "endswith", "find", "rfind", "index", "rindex",
    "count", "replace", "split", "join", "isdigit", "isalpha", "isalnum",
    "isupper", "islower", "isspace", "zfill", "center", "ljust", "rjust",
})


# ---- Core evaluator ---------------------------------------------------------

class _SafeEvaluator:
    """Walk an AST tree and evaluate it against an allowed-names dict."""

    def __init__(self, names: dict[str, Any]) -> None:
        self.names = names

    def evaluate(self, node: ast.AST) -> Any:  # noqa: C901
        """Recursively evaluate *node*."""
        if isinstance(node, ast.Expression):
            return self.evaluate(node.body)

        # --- literals ---
        if isinstance(node, ast.Constant):
            return node.value

        # --- containers ---
        if isinstance(node, ast.List):
            return [self.evaluate(e) for e in node.elts]
        if isinstance(node, ast.Tuple):
            return tuple(self.evaluate(e) for e in node.elts)
        if isinstance(node, ast.Dict):
            return {
                self.evaluate(k): self.evaluate(v)  # type: ignore[arg-type]
                for k, v in zip(node.keys, node.values)
            }

        # --- names (variable / function look-ups) ---
        if isinstance(node, ast.Name):
            name = node.id
            if name in self.names:
                return self.names[name]
            # Common Python constants
            if name == "True":
                return True
            if name == "False":
                return False
            if name == "None":
                return None
            raise ValueError(f"Undefined name: {name!r}")

        # --- unary operators ---
        if isinstance(node, ast.UnaryOp):
            op_func = _UNARY_OPS.get(type(node.op))
            if op_func is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op_func(self.evaluate(node.operand))

        # --- binary operators ---
        if isinstance(node, ast.BinOp):
            op_func = _BIN_OPS.get(type(node.op))
            if op_func is None:
                raise ValueError(f"Unsupported binary operator: {type(node.op).__name__}")
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            return op_func(left, right)

        # --- boolean operators (and / or) ---
        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                result = True
                for value in node.values:
                    result = self.evaluate(value)
                    if not result:
                        return result
                return result
            if isinstance(node.op, ast.Or):
                result = False
                for value in node.values:
                    result = self.evaluate(value)
                    if result:
                        return result
                return result

        # --- comparisons ---
        if isinstance(node, ast.Compare):
            left = self.evaluate(node.left)
            for op_node, comparator in zip(node.ops, node.comparators):
                op_func = _CMP_OPS.get(type(op_node))
                if op_func is None:
                    raise ValueError(
                        f"Unsupported comparison: {type(op_node).__name__}"
                    )
                right = self.evaluate(comparator)
                if not op_func(left, right):
                    return False
                left = right
            return True

        # --- function calls ---
        if isinstance(node, ast.Call):
            func = self.evaluate(node.func)
            if not callable(func):
                raise ValueError(f"Not callable: {func!r}")
            args = [self.evaluate(a) for a in node.args]
            kwargs = {kw.arg: self.evaluate(kw.value) for kw in node.keywords}
            return func(*args, **kwargs)

        # --- subscript (indexing) ---
        if isinstance(node, ast.Subscript):
            value = self.evaluate(node.value)
            slc = node.slice
            if hasattr(ast, "Index") and isinstance(slc, ast.Index):  # Python <3.9
                return value[self.evaluate(slc.value)]  # type: ignore[attr-defined,index]
            if isinstance(slc, ast.Slice):
                lower = self.evaluate(slc.lower) if slc.lower else None
                upper = self.evaluate(slc.upper) if slc.upper else None
                step = self.evaluate(slc.step) if slc.step else None
                return value[lower:upper:step]  # type: ignore[index]
            return value[self.evaluate(slc)]  # type: ignore[index]

        # --- attribute access (limited to safe string methods) ---
        if isinstance(node, ast.Attribute):
            value = self.evaluate(node.value)
            attr = node.attr
            if isinstance(value, str) and attr in _SAFE_STR_METHODS:
                return getattr(value, attr)
            raise ValueError(f"Attribute access not allowed: .{attr}")

        # --- conditional expression (ternary) ---
        if isinstance(node, ast.IfExp):
            if self.evaluate(node.test):
                return self.evaluate(node.body)
            return self.evaluate(node.orelse)

        raise ValueError(f"Unsupported expression node: {type(node).__name__}")


def safe_eval(expr: str, names: dict[str, Any] | None = None) -> Any:
    """Evaluate *expr* safely against the supplied *names* dict.

    Only arithmetic, string operations, comparisons, and calls to functions
    present in *names* are allowed.  Everything else raises ``ValueError``.

    Parameters
    ----------
    expr : str
        The expression string to evaluate.
    names : dict, optional
        Mapping of allowed names (variables and functions).

    Returns
    -------
    Any
        The result of the expression.

    Raises
    ------
    ValueError
        If the expression contains disallowed constructs.
    SyntaxError
        If the expression cannot be parsed.
    """
    if names is None:
        names = {}
    tree = ast.parse(expr.strip(), mode="eval")
    evaluator = _SafeEvaluator(names)
    return evaluator.evaluate(tree)
