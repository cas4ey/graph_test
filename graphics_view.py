# coding=utf-8
# -----------------
# file      : graphics_view.py
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

from PySide.QtCore import *
from PySide.QtGui import *
from graph import graph
from graph.depth_first_search import depth_first_search as dfs
from graph.breadth_first_search import breadth_first_search as bfs
from graph.dijkstra_search import dijkstra_search as dijkstra
from graph.astar_search import astar_search as astar
import diagram

#######################################################################################################################
#######################################################################################################################

_maximumScale = 450.0
_minimumScale = 3.0
_keysPressed = []

#######################################################################################################################
#######################################################################################################################


class Scene(QGraphicsScene):

    _defaultSize = 1200.0

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self._view = parent

        self._keyHandlers = {
            Qt.Key_F1: self._showHelp,
            Qt.Key_A: self._addNewNode,
            Qt.Key_C: self._connectNodes,
            Qt.Key_S: self._setTargetNode,
            Qt.Key_0: self._clearPath,
            Qt.Key_1: self._runDFS,
            Qt.Key_2: self._runBFS,
            Qt.Key_3: self._runDijkstra,
            Qt.Key_4: self._runAstar
            }

        self._nodes = {}
        self._edges = {}
        self._begin = 0
        self._end = 0

        half_size = Scene._defaultSize
        self._topLeft = QPointF(-half_size, -half_size)
        self._bottomRight = QPointF(half_size, half_size)
        self.setSceneRect(QRectF(self._topLeft, self._bottomRight))
        # self.selectionChanged.connect(self._onSelectionChange)

        # self._test()

    # @Slot()
    # def _onSelectionChange(self):
    #     pass

    def node(self, identifier):
        return self._nodes.get(identifier, None)

    def edge(self, identifier):
        return self._edges.get(identifier, None)

    def _test(self):
        text = QGraphicsSimpleTextItem()
        text.setText("TEST")
        text.setFlag(QGraphicsItem.ItemIsMovable, True)
        text.setFlag(QGraphicsItem.ItemIsSelectable, True)
        text.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        text.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.addItem(text)

        item = diagram.Node()
        self.addItem(item)
        item.setPos(0, 50)

    def _showHelp(self):
        QMessageBox.information(None, 'Hot keys', '\'F1\' = show this window\n'
                                                  '\'A\' = add new node under mouse cursor\n'
                                                  '\'C\' = connect selected node with node under mouse cursor\n'
                                                  '\'Mouse double click\' = select node under cursor\n'
                                                  '\'S\' = set node under cursor as target node of search algorithm. \
                                                  Start node is current selected node and it must be selected already.\n'
                                                  '\'0\' = clear current path\n'
                                                  '\'1\' = Depth first search\n'
                                                  '\'2\' = Breadth first search\n'
                                                  '\'3\' = Dijkstra\'s search\n'
                                                  '\'4\' = A* search')

    def _addNewNode(self):
        new_node = graph.graph.add_node(1)

        item = diagram.Node()
        item.set_id(new_node.id())
        self._nodes[new_node.id()] = item
        self.addItem(item)
        new_node.set_data(item)

        scene_position = self._view.mapToScene(self._view.mapFromGlobal(QCursor.pos()))
        item.setPos(scene_position)

    def _connectNodes(self):
        if self.selectedItems():
            selected = self.selectedItems()[-1]
            scene_position = self._view.mapToScene(self._view.mapFromGlobal(QCursor.pos()))
            items_under_cursor = self.items(scene_position, Qt.ContainsItemShape, Qt.AscendingOrder)
            if items_under_cursor:
                for item in items_under_cursor:
                    if isinstance(item, diagram.Node):
                        if item.id() != selected.id():
                            edge = graph.graph.connect_nodes(selected.id(), item.id(),
                                                             graph.EdgeDirection.STRAIGHT, 1)
                            if edge.id() in self._edges:
                                self.edge(edge.id()).initialize(edge.id())
                            else:
                                new_item = diagram.Edge()
                                self._edges[edge.id()] = new_item
                                self.addItem(new_item)
                                new_item.initialize(edge.id())
                        break

    def _setTargetNode(self):
        call_update = False
        if self._end != 0:
            call_update = True
            self._cleanHighlight()
            self._begin = 0
            self._end = 0
        if self.selectedItems():
            scene_position = self._view.mapToScene(self._view.mapFromGlobal(QCursor.pos()))
            items_under_cursor = self.items(scene_position, Qt.ContainsItemShape, Qt.AscendingOrder)
            if not items_under_cursor:
                self._begin = 0
                if self._end != 0:
                    call_update = True
                    self._cleanHighlight()
                    self._end = 0
            else:
                self._begin = self.selectedItems()[-1].id()
                for item in items_under_cursor:
                    if isinstance(item, diagram.Node):
                        if item.id() != self._begin:
                            self._end = item.id()
                            call_update = True
                            item.highlight(Qt.red)
        if call_update:
            self.update()

    def _runDFS(self):
        # Depth-First Search
        path = self._runSearch(dfs)
        if path:
            self._cleanHighlight()
            self._highlightPath(path)
            self.update()
            print('iterations = %d // DFS' % path.iterations())

    def _runBFS(self):
        # Breadth-First Search
        path = self._runSearch(bfs)
        if path:
            self._cleanHighlight()
            self._highlightPath(path)
            self.update()
            print('iterations = %d // BFS' % path.iterations())

    def _runDijkstra(self):
        # Dijkstra's Search
        path = self._runSearch(dijkstra)
        if path:
            self._cleanHighlight()
            self._highlightPath(path)
            self.update()
            print('iterations = %d // Dijkstra' % path.iterations())

    def _runAstar(self):
        # A* Search
        path = self._runSearch(astar)
        if path:
            self._cleanHighlight()
            self._highlightPath(path)
            self.update()
            print('iterations = %d // A*' % path.iterations())

    def _clearPath(self):
        self._cleanHighlight()
        self.update()

    def mousePressEvent(self, event):
        global _keysPressed
        if Qt.Key_Control in _keysPressed:
            self.clearSelection()
            QGraphicsScene.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        global _keysPressed
        if Qt.Key_Control in _keysPressed:
            QGraphicsScene.mouseReleaseEvent(self, event)

    def keyPressEvent(self, event):
        global _keysPressed
        k = event.key()
        _keysPressed.append(k)
        if k in self._keyHandlers:
            self._keyHandlers[k]()
        if k != Qt.Key_Control:
            QGraphicsScene.keyPressEvent(self, event)

    def keyReleaseEvent(self, event):
        global _keysPressed
        try:
            _keysPressed.remove(event.key())
        except ValueError:
            pass
        if event.key() == Qt.Key_Control:
            self.clearSelection()
        QGraphicsScene.keyReleaseEvent(self, event)

    def _cleanHighlight(self):
        list(map(lambda x: self._nodes[x].highlight(), self._nodes.keys()))
        list(map(lambda x: self._edges[x].highlight(), self._edges.keys()))

    def _highlightPath(self, path):
        if path:
            highlighted = False
            for edge_info in path:
                if not highlighted:
                    highlighted = True
                    self.node(edge_info.head()).highlight(Qt.green)
                self.node(edge_info.tail()).highlight(Qt.red)
                self.edge(edge_info.id()).highlight(Qt.red)
            return True
        return False

    def _runSearch(self, search_algorithm):
        if self._begin != 0 and self._end != 0 and search_algorithm is not None:
            return search_algorithm(self._begin, self._end, graph.graph)
        return []

#######################################################################################################################
#######################################################################################################################


class View(QGraphicsView):

    scaleChanged = Signal(float)

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self._scale = 100.0
        self._scalingCoefficient = 1.25
        self._mousePressed = False
        self._mousePressPosition = QPoint()
        self._scrolling = False
        self.setScene(Scene(self))
        self._hintText = QGraphicsSimpleTextItem('Press F1 to see help!', None)
        self.scene().addItem(self._hintText)
        QTimer().singleShot(10, lambda: [self.centerOn(0, 0), self._updateHintPosition()])

    def mousePressEvent(self, event):
        global _keysPressed
        if not self._mousePressed and event.button() == Qt.LeftButton and Qt.Key_Control not in _keysPressed:
            self._mousePressed = True
            self._mousePressPosition = event.globalPos()
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self._mousePressed and event.button() == Qt.LeftButton:
            self._mousePressed = False
            if self._scrolling:
                self._scrolling = False
                # self.verticalScrollBar().setProperty('moving', False)
                # self.horizontalScrollBar().setProperty('moving', False)
                # self.verticalScrollBar().setStyle(QApplication.style())
                # self.horizontalScrollBar().setStyle(QApplication.style())
        QGraphicsView.mouseReleaseEvent(self, event)

    def mouseMoveEvent(self, event):
        global _keysPressed
        if self._mousePressed and Qt.Key_Control not in _keysPressed:
            delta = event.globalPos() - self._mousePressPosition
            self._mousePressPosition = event.globalPos()
            delta *= self._scalingCoefficient
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            if not self._scrolling:
                self._scrolling = True
                # self.verticalScrollBar().setProperty('moving', True)
                # self.horizontalScrollBar().setProperty('moving', True)
                # self.verticalScrollBar().setStyle(QApplication.style())
                # self.horizontalScrollBar().setStyle(QApplication.style())
            self._updateHintPosition()
        QGraphicsView.mouseMoveEvent(self, event)

    def wheelEvent(self, event):
        global _maximumScale, _minimumScale
        scaled = False
        if event.delta() > 0:
            if self._scale < _maximumScale:
                self.scale(self._scalingCoefficient, self._scalingCoefficient)
                self._scale *= self._scalingCoefficient
                scaled = True
        else:
            if self._scale > _minimumScale:
                scaling_coefficient = 1.0 / self._scalingCoefficient
                self.scale(scaling_coefficient, scaling_coefficient)
                self._scale /= self._scalingCoefficient
                scaled = True
        if scaled:
            self.scaleChanged.emit(self._scale)
            # if self._scale < 100.0:
            #     self.bgTransform, _ = self.transform().inverted()
            # else:
            #     self.bgTransform = None
            # if -1 < globals.background < len(globals.backgrounds):
            #     self.__onBackgroundChange(globals.background)
            self._updateHintPosition()

    def _updateHintPosition(self):
        self._hintText.setPos(self.mapToScene(QPoint(10, 10)))

