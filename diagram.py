# coding=utf-8
# -----------------
# file      : diagram.py
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
from graph.graph import graph, EdgeDirection
from math import sin, cos, asin, acos, pi
from random import randint

#######################################################################################################################
#######################################################################################################################


class Node(QGraphicsPolygonItem, QObject):

    positionChanged = Signal(QGraphicsItem)

    _defaultColor = QColor(128, 128, 128, 96)

    def __init__(self, *args, **kwargs):
        QGraphicsPolygonItem.__init__(self, *args, **kwargs)
        QObject.__init__(self, *args, **kwargs)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

        self._path = QPainterPath()
        self._initializePath()
        self._boundingRect = self._path.boundingRect()

        self._pen = QPen(Qt.red, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.setPen(self._pen)

        self._backgroundBrush = QBrush(Node._defaultColor)

        self._id = 0

        self.setZValue(10)

    def highlight(self, color=_defaultColor):
        color = QColor(color)
        color.setAlpha(Node._defaultColor.alpha())
        self._backgroundBrush.setColor(color)

    def set_id(self, uid):
        self._id = uid

    def id(self):
        return self._id

    def radius(self):
        return 10

    def _initializePath(self):
        r = self.radius()
        self._path.addEllipse(QPointF(), r, r)

    def shape(self, *args, **kwargs):
        return self._path

    def boundingRect(self, *args, **kwargs):
        return self._boundingRect

    def paint(self, painter, option, widget):
        # painter.setClipRect(option.exposedRect)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self._pen)

        if self._backgroundBrush is not None:
            painter.setBrush(self._backgroundBrush)

        painter.drawPath(self._path)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged or change == QGraphicsItem.ItemPositionChange:
            self.positionChanged.emit(self)
        elif change == QGraphicsItem.ItemSelectedHasChanged or change == QGraphicsItem.ItemSelectedChange:
            if self.isSelected():
                self._pen.setWidth(2)
            else:
                self._pen.setWidth(1)
            self.setPen(self._pen)
            self.scene().update()
        return value

#######################################################################################################################
#######################################################################################################################


class Edge(QGraphicsLineItem):

    _arrowAngle = pi / 3.0
    _arrowSize = 10.0

    _defaultColor = Qt.black

    def __init__(self, *args, **kwargs):
        QGraphicsLineItem.__init__(self, *args, **kwargs)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, False)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

        pen = QPen(Edge._defaultColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        # pen.setCosmetic(True)
        self.setPen(pen)

        self._begin = None
        self._end = None
        self._id = 0
        self._direction = EdgeDirection.STRAIGHT

        self._beginPoint = QPointF()
        self._endPoint = QPointF()
        self._path = QPainterPath()
        self._text = None

        self.setZValue(-10)

    def id(self):
        return self._id

    def shape(self, *args, **kwargs):
        return self._path

    def highlight(self, color=_defaultColor):
        pen = QPen(color, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.setPen(pen)

    def _calculate(self):
        p1 = self.mapFromItem(self._begin, 0, 0)
        p2 = self.mapFromItem(self._end, 0, 0)
        line = QLineF(p1, p2)
        distance = line.length()
        line = line.unitVector()
        center = line.unitVector()
        center.setLength(distance * 0.5)
        center = center.p2()
        line.setLength(self._begin.radius())
        self._beginPoint = line.p2()
        line = QLineF(p2, p1).unitVector()
        line.setLength(self._end.radius())
        self._endPoint = line.p2()
        line = QLineF(self._endPoint, self._beginPoint)
        self.setLine(line)
        l = line.length()
        self._path = QGraphicsLineItem.shape(self)
        # self._path = QPainterPath()  # QGraphicsLineItem.shape(self)
        # self._path.moveTo(self._beginPoint)
        # ln = line.unitVector()
        # ln.setLength(l * 0.5)
        # c = ln.p2()
        # c.setX(c.x() + l * float(randint(-100, 100)) / 300.0)
        # c.setY(c.y() + l * float(randint(-100, 100)) / 300.0)
        # self._path.quadTo(c, self._endPoint)
        # self._path.addEllipse(c, 5, 5)
        if self._direction == EdgeDirection.STRAIGHT and l > 0.01:
            angle = acos(line.dx() / l)
            if line.dy() >= 0:
                angle = pi * 2.0 - angle
            p1 = line.p1() + QPointF(sin(angle + Edge._arrowAngle) * Edge._arrowSize,
                                     cos(angle + Edge._arrowAngle) * Edge._arrowSize)
            p2 = line.p1() + QPointF(sin(angle + pi - Edge._arrowAngle) * Edge._arrowSize,
                                     cos(angle + pi - Edge._arrowAngle) * Edge._arrowSize)
            arrow = QPolygonF()
            arrow.append(p1)
            arrow.append(line.p1())
            arrow.append(p2)
            self._path.addPolygon(arrow)
        edge = graph.edge(self._id)
        if edge is not None:
            w = int(max(distance, 1))
            edge.set_base_weight(w)
            if self._text is None:
                self._text = QGraphicsSimpleTextItem(str(w), self)
            else:
                self._text.setText(str(w))
            self._text.setPos(center)

    def initialize(self, edge_id):
        edge = graph.edge(edge_id)
        if edge is not None:
            self._id = edge_id
            self._direction = edge.direction()
            if self._begin is not None:
                self._begin.positionChanged.disconnect(self.onItemMove)
            if self._end is not None:
                self._end.positionChanged.disconnect(self.onItemMove)
            self._begin = self.scene().node(edge.head().id())
            self._end = self.scene().node(edge.tail().id())
            self._begin.positionChanged.connect(self.onItemMove)
            self._end.positionChanged.connect(self.onItemMove)
            self._calculate()

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(self.pen())
        painter.drawPath(self._path)

    @Slot(QGraphicsItem)
    def onItemMove(self, item):
        if item.id() in (self._begin.id(), self._end.id()):
            self._calculate()

    @Slot()
    def onDirectionChange(self):
        edge = graph.edge(self._id)
        if edge is not None:
            if self._direction != edge.direction():
                self._direction = edge.direction()
                self._calculate()

#######################################################################################################################
#######################################################################################################################
