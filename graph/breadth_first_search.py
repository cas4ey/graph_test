# coding=utf-8
# -----------------
# file      : breadth_first_search.py
# date      : 2015/09/20
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


def breadth_first_search(begin, end, graph):

    start = graph.node(begin)
    if start is None:
        return Path()

    finish = graph.node(end)
    if finish is None or finish.id() == start.id():
        return Path()

    visited_nodes = [start.id()]
    path = []
    queue = [start]
    finish_found = False
    iterations = 0

    while queue and not finish_found:

        iterations += 1

        current = queue.pop(0)
        edges = current.edges()

        for uid in edges:

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

            path.append((current, tail, edge))
            if tail.id() == finish.id():
                finish_found = True
                break

            queue.append(tail)
            visited_nodes.append(tail.id())

    if finish_found and path:

        resulting_path = [path[-1]]
        if len(path) > 1:

            prev_id = path[-1][0].id()
            for i in range(-2, -(len(path) + 1), -1):

                head, tail, edge = path[i]
                if tail.id() == prev_id:

                    resulting_path.append(path[i])
                    prev_id = head.id()
                    if prev_id == start.id():
                        break

            resulting_path.reverse()

        return Path(resulting_path, iterations)

    return Path()

#######################################################################################################################
#######################################################################################################################
