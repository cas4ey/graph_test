# coding=utf-8
# -----------------
# file      : depth_first_search.py
# date      : 2015/05/19
# author    : Victor Zarubkin
# contact   : victor.zarubkin@gmail.com
# copyright : Copyright (C) 2015  Victor Zarubkin
# license   : This file is part of GraphTutorial.
#           :
#           : GraphTutorial is free software: you can redistribute it and/or modify
#           : it under the terms of the GNU General Public License as published by
#           : the Free Software Foundation, either version 3 of the License, or
#           : (at your option) any later version.
#           :
#           : GraphTutorial is distributed in the hope that it will be useful,
#           : but WITHOUT ANY WARRANTY; without even the implied warranty of
#           : MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#           : GNU General Public License for more details.
#           :
#           : You should have received a copy of the GNU General Public License
#           : along with BehaviorStudio. If not, see <http://www.gnu.org/licenses/>.
#           :
#           : A copy of the GNU General Public License can be found in file LICENSE.
############################################################################

"""

"""

__author__ = 'Victor Zarubkin'
__copyright__ = 'Copyright (C) 2015  Victor Zarubkin'
__credits__ = ['Victor Zarubkin']
__license__ = ['GPLv3']
__version__ = '0.0.1'  # this is last application version when this script file was changed
__email__ = 'victor.zarubkin@gmail.com'
############################################################################

from .graph import Path

#######################################################################################################################
#######################################################################################################################


class _StackEntry(object):

    def __init__(self, node, it):
        object.__init__(self)
        self.node = node
        self.keys = it


def depth_first_search(begin, end, graph):
    start = graph.node(begin)
    if start is None:
        return Path()
    finish = graph.node(end)
    if finish is None or finish.id() == start.id():
        return Path()

    visited_nodes = [start.id()]
    path = []
    stack = [_StackEntry(start, iter(start.edges()))]
    while stack:
        go_next = False
        current = stack[-1]
        edges = current.node.edges()
        for uid in current.keys:
            edge = graph.edge(uid)
            if edge is None:
                continue
            edge_info = edges[uid]
            if edge_info.tail() in visited_nodes:
                continue
            head = graph.node(edge_info.head())
            tail = graph.node(edge_info.tail())
            if head is None or tail is None:
                continue
            entry = (head, tail, edge)
            path.append(entry)
            if tail.id() == finish.id():
                return Path(path)
            go_next = True
            stack.append(_StackEntry(tail, iter(tail.edges())))
            visited_nodes.append(tail.id())
            break
        if not go_next:
            stack.pop()
            try:
                path.pop()
            except IndexError:
                pass
    return Path()

#######################################################################################################################
#######################################################################################################################
