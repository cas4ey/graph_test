# coding=utf-8
# -----------------
# file      : dijkstra_search.py
# date      : 2015/09/22
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
from sortedcontainers.sortedlistwithkey import SortedListWithKey as sortedList

#######################################################################################################################
#######################################################################################################################

_infinite_weight = 1e28


class _DijkstraNode(object):

    def __init__(self, node, cost, parent, edge):
        object.__init__(self)
        self.id = node.id()
        self.parent_id = parent.id() if parent is not None else 0
        self.node = node
        self.parent = parent
        self.edge = edge
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.id == other.id


def dijkstra_search(begin, end, graph):

    global _infinite_weight

    start = graph.node(begin)
    if start is None:
        return Path()

    finish = graph.node(end)
    if finish is None or finish.id() == start.id():
        return Path()

    nodes = {}
    for node_id in graph.nodes():
        node = graph.node(node_id)
        cost = 0 if node_id == begin else _infinite_weight
        nodes[node_id] = _DijkstraNode(node, cost, None, None)

    visited_nodes = []
    priority_queue = sortedList([nodes[start.id()]], key=lambda x: x.cost, load=len(nodes))
    iterations = 0

    # "resulting_cost" is used to reduce total number of visited nodes.
    # Explanation: when you have already found target node you can check if other search paths are shorter than
    # the found one, and if not then there is no need to explore such path further.
    resulting_cost = _infinite_weight

    while priority_queue:

        iterations += 1

        current = priority_queue.pop(0)
        visited_nodes.append(current.id)
        edges = current.node.edges()

        for edge_id in edges:

            edge = graph.edge(edge_id)
            if edge is None:
                continue

            edge_info = edges[edge_id]
            if edge_info.tail() in visited_nodes:
                continue

            tail = nodes.get(edge_info.tail(), None)
            if tail is None:
                continue

            cost = current.cost + edge.weight() + tail.node.weight()
            if tail.id == end:
                resulting_cost = min(cost, resulting_cost)

            if cost < tail.cost:
                tail.cost = cost
                tail.parent_id = current.id
                tail.parent = current.node
                tail.edge = edge
                priority_queue.discard(tail)
                if cost < resulting_cost:
                    priority_queue.add(tail)
            elif cost < resulting_cost and tail not in priority_queue:
                priority_queue.add(tail)

    path = []
    current = nodes[end]
    while current.parent_id != 0 and current.edge is not None:
        path.append((current.parent, current.node, current.edge))
        current = nodes[current.parent_id]

    if path and current.id == begin:
        path.reverse()
        return Path(path, iterations)

    return Path()

#######################################################################################################################
#######################################################################################################################
