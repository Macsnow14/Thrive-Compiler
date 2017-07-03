"""This is a module for generate NFA.
"""
# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-04-15 12:25:32
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-04-15 17:02:03


class State(object):
    """class of State"""

    def __init__(self, name, is_final=False):
        self.name = name
        self.is_final = is_final


class Edge(object):
    """class of Edge"""

    def __init__(self, source, destination, symbol):
        self.source = source
        self.destination = destination
        self.symbol = symbol


class NFA(object):
    """class to manage NFA"""

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.state_set = dict()
        self.edge_set = dict()

    def renameStates(self, step):
        for state in self.state_set:
            state.name += step

    def addStart(self):
        self.renameStates(1)
        new_start = State(0)
        self.edge_set.add(Edge(new_start, self.start, "ε"))
        self.start = new_start
        self.state_set.add(new_start)

    def addEnd(self):
        new_end = State(len(self.state_set) + 1)
        self.edge_set.add(Edge(self.end, new_end, "ε"))
        self.end.is_final = False
        self.end = new_end
        self.state_set.add(new_end)

    def merge(self, nfa):
        self.state_set = self.state_set | nfa.state_set
        self.edge_set = self.edge_set | nfa.edge_set

    def link(self, nfa):
        self.end.is_final = False
        self.edge_set.add(Edge(self.end, nfa.start, "ε"))
        self.end = nfa.end
        nfa.renameStates(len(self.state_set))
        self.merge(nfa)

    def kliine(self):
        self.edge_set.add(Edge(self.end, self.start, "ε"))

        self.addStart()
        self.addEnd()

        self.edge_set.add(Edge(self.start, self.end, "ε"))

    def parallel(self, nfa):
        self.addStart()
        nfa.renameStates(len(self.state_set))
        self.merge(nfa)
        self.addEnd()
        self.edge_set.add(Edge(self.start, nfa.start))
        self.edge_set.add(Edge(nfa.end, self.end))
