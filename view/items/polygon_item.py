from PySide6.QtCore import QPointF, QPoint
from PySide6.QtGui import QBrush, QColor, QPen, QPolygonF, QPainter, QPolygon
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsPolygonItem, QWidget

from model.shapes import Polygon


class PolygonItem(QGraphicsPolygonItem):

    def __init__(self, model: Polygon):
        points = [
            QPointF(0, 0),
            QPointF(100, 0),
            QPointF(100, 100),
            QPointF(0, 100)
        ]
        super().__init__(QPolygonF(points))

        self.model = model
        # self.setPos(model.a.x, model.a.y)
        self.setBrush(QBrush(QColor(38, 99, 255)))
        self.setPen(QPen(QColor(10, 30, 80), 1))
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        if change == QGraphicsPolygonItem.GraphicsItemChange.ItemPositionHasChanged:
            pos: QPointF = self.pos()

            # self.model.a.x = float(pos.x())
            # self.model.a.y = float(pos.y())
            #
            # self.model.b.x = float(pos.x())
            # self.model.b.y = float(pos.y())
            #
            # self.model.c.x = float(pos.x())
            # self.model.c.y = float(pos.y())
            #
            # self.model.d.x = float(pos.x())
            # self.model.d.y = float(pos.y())


        return super().itemChange(change, value)
