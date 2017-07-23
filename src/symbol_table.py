"""
this module contains the util class for symbol table.
"""
from typing import Dict, Tuple
from functools import reduce


class SymbolTable(object):
    """symbol table util"""
    _var_size: Dict[str, int] = {"int": 2, "bool": 1, "char": 1, "float": 4}

    def __init__(self):
        self._symbol_table: Dict[str, Dict[str, str or int]] = dict()
        self._addr: int = 0

    def __repr__(self):
        pass

    def create_item(self, name: str, value_type: str,
                    scope: str, array: Tuple[int, ...] or None=None):
        """create a symbol item"""
        self._symbol_table[name] = {
            "addr": self._addr, "type": value_type, "scope": scope}
        if array:
            size: int = reduce(lambda curr, last: curr * last, array)
            self._symbol_table[name]["size"] = size
            self._addr += size
        else:
            self._addr += self._var_size[value_type]

    def validate(self, name: str, scope: str) -> bool:
        """validate an variable"""
        return self._symbol_table.get(name) is not None and self._symbol_table[name]["scope"] in ("global", scope)
