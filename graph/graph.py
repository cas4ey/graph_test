# coding=utf-8
# -----------------
# file      : graph.py
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

# imports section

#######################################################################################################################
#######################################################################################################################


class EdgeDirection(object):

    STRAIGHT = 1
    REVERSE = 2
    MUTUAL = 3

    @staticmethod
    def appropriate(direction):
        return direction in (EdgeDirection.STRAIGHT, EdgeDirection.REVERSE, EdgeDirection.MUTUAL)

#######################################################################################################################
#######################################################################################################################


class _Base(object):

    def __init__(self, uid, weight=1):
        object.__init__(self)
        self._enabled = True
        self._id = uid
        self._weight = weight
        self._dynamicWeight = 0

    def id(self):
        return self._id

    def enabled(self):
        return self._enabled

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def base_weight(self):
        return self._weight

    def weight(self):
        return self._weight + self._dynamicWeight

    def set_base_weight(self, weight):
        if weight >= 0:
            self._weight = weight

    def add_weight(self, weight):
        if weight < 0:
            self.subtract_weight(-weight)
        else:
            self._dynamicWeight += weight

    def subtract_weight(self, weight):
        self._dynamicWeight = max(self._dynamicWeight - abs(weight), 0)

#######################################################################################################################
#######################################################################################################################


class EdgeInfo(object):

    def __init__(self, uid, head, tail):
        object.__init__(self)
        self._head = head.id() if isinstance(head, _Base) else head
        self._tail = tail.id() if isinstance(tail, _Base) else tail
        self._id = uid

    def id(self):
        return self._id

    def head(self):
        return self._head

    def tail(self):
        return self._tail


class Edge(_Base):

    def __init__(self, uid, head, tail, direction=EdgeDirection.STRAIGHT, weight=1):
        _Base.__init__(self, uid, weight)
        self._head = head
        self._tail = tail
        self._direction = direction if EdgeDirection.appropriate(direction) else EdgeDirection.STRAIGHT
        if self._direction == EdgeDirection.REVERSE:
            self._direction = EdgeDirection.STRAIGHT
            self._head, self._tail = self._tail, self._head
        if self._head is not None:
            self._head.add_edge(EdgeInfo(self.id(), self._head, self._tail))
        if self._direction == EdgeDirection.MUTUAL and self._tail is not None:
            self._tail.add_edge(EdgeInfo(self.id(), self._tail, self._head))

    def direction(self):
        return self._direction

    def head(self):
        return self._head

    def tail(self):
        return self._tail

    def connect(self, head, tail, direction=None):
        self.disconnect()
        if direction is not None and EdgeDirection.appropriate(direction):
            self._direction = direction
        self._head = head
        self._tail = tail
        if self._direction == EdgeDirection.REVERSE:
            self._direction = EdgeDirection.STRAIGHT
            self._head, self._tail = self._tail, self._head
        self._head.add_edge(EdgeInfo(self.id(), self._head, self._tail))
        if self._direction == EdgeDirection.MUTUAL:
            self._tail.add_edge(EdgeInfo(self.id(), self._tail, self._head))

    def disconnect(self):
        if self._head is not None:
            self._head.remove_edge(self.id())
        if self._direction == EdgeDirection.MUTUAL and self._tail is not None:
            self._tail.remove_edge(self.id())

#######################################################################################################################
#######################################################################################################################


class Node(_Base):

    def __init__(self, uid, weight=1, data=None):
        _Base.__init__(self, uid, weight)
        self._edges = {}
        self._data = data

    def data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def edges(self):
        return self._edges

    def add_edge(self, edge):
        if isinstance(edge, EdgeInfo):
            uid = edge.id()
            if uid > 0 and uid not in self._edges:
                self._edges[uid] = edge

    def remove_edge(self, edge):
        if isinstance(edge, int):
            uid = edge
        elif isinstance(edge, (Edge, EdgeInfo)):
            uid = edge.id()
        else:
            uid = 0
        if uid > 0 and uid in self._edges:
            del self._edges[uid]

#######################################################################################################################
#######################################################################################################################


class Graph(object):

    def __init__(self):
        object.__init__(self)
        self._nodes = {}
        self._edges = {}
        self._free_id_node_max = 1
        self._free_id_edge_max = 1
        self._free_ids_node = []
        self._free_ids_edge = []

    def clear(self):
        self._nodes.clear()
        self._edges.clear()
        self._free_id_node_max = 1
        self._free_id_edge_max = 1
        self._free_ids_node = []
        self._free_ids_edge = []

    def nodes_number(self):
        return len(self._nodes)

    def edges_number(self):
        return len(self._edges)

    def node(self, identifier):
        return self._nodes.get(identifier, None)

    def edge(self, identifier):
        return self._edges.get(identifier, None)

    def nodes(self):
        return self._nodes

    def remove_edge(self, identifier):
        if identifier in self._edges:
            self._edges[identifier].disconnect()
            del self._edges[identifier]
            self._free_ids_edge.append(identifier)

    def add_node(self, weight, uid=0, data=None):
        if uid in self._nodes:
            return None
        if uid < 1:
            uid = self._get_free_id_for_node()
            if uid == self._free_id_node_max:
                self._free_id_node_max += 1
        self._nodes[uid] = Node(uid, weight, data)
        return self._nodes[uid]

    def connect_nodes(self, first, second, direction, weight=1):
        if not EdgeDirection.appropriate(direction):
            return None
        node1 = first if isinstance(first, Node) else self.node(first)
        if node1 is None:
            return None
        node2 = second if isinstance(second, Node) else self.node(second)
        if node2 is None:
            return None
        if node1.id() == node2.id():
            return None
        # try to find mutual edge
        # edge = self._find_mutual_edge(node1, node2, direction)
        # if edge is not None:
        #     if edge.direction() != direction:
        #         if direction == EdgeDirection.REVERSE and edge.head().id() == node1.id():
        #             edge.connect(node2, node1, EdgeDirection.STRAIGHT)
        #         elif direction == EdgeDirection.MUTUAL:
        #             edge.connect(node1, node2, EdgeDirection.MUTUAL)
        #     return edge
        # create new edge
        uid = self._get_free_id_for_edge()
        if uid == self._free_id_edge_max:
            self._free_id_edge_max += 1
        self._edges[uid] = Edge(uid, node1, node2, direction, weight)
        return self._edges[uid]

    def _find_mutual_edge(self, first, second, direction=None):
        if first.id() == second.id():
            return None
        edge = self._find_edge(first.edges(), second, direction)
        if edge is not None:
            return edge
        if direction == EdgeDirection.MUTUAL:
            edge = self._find_edge(second.edges(), first, EdgeDirection.MUTUAL)
            if edge is not None:
                return edge
        return None

    def _find_edge(self, edges, node, direction):
        for edge_id in edges:
            edge = self.edge(edge_id)
            if edge is None:
                continue
            if edge.tail().id() == node.id() and edge.direction() == EdgeDirection.REVERSE:
                if direction is None or edge.direction() == direction:
                    return edge
        return None

    def _get_free_id_for_node(self):
        if self._free_ids_node:
            return self._free_ids_node.pop()
        while self._free_id_node_max in self._nodes:
            self._free_id_node_max += 1
        return self._free_id_node_max

    def _get_free_id_for_edge(self):
        if self._free_ids_edge:
            return self._free_ids_edge.pop()
        while self._free_id_edge_max in self._edges:
            self._free_id_edge_max += 1
        return self._free_id_edge_max

#######################################################################################################################
#######################################################################################################################


class Path(object):

    def __init__(self, path=[]):
        object.__init__(self)
        self._path = []
        self._totalWeight = 0
        for head, tail, edge in path:
            self.append(head, tail, edge)

    def __bool__(self, *args, **kwargs):
        return bool(self._path)

    def __len__(self, *args, **kwargs):
        return self._path.__len__(*args, **kwargs)

    def __contains__(self, *args, **kwargs):
        return self._path.__contains__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return self._path.__iter__(*args, **kwargs)

    def total_weight(self):
        return self._totalWeight

    def append(self, head, tail, edge):
        self._totalWeight += edge.weight()
        self._totalWeight += tail.weight()
        if not self._path:
            self._totalWeight += head.weight()
        self._path.append(EdgeInfo(edge.id(), head, tail))

#######################################################################################################################
#######################################################################################################################

graph = Graph()

#######################################################################################################################
#######################################################################################################################
