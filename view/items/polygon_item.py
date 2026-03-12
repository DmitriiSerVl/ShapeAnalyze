from PySide6.QtCore import QPointF, QPoint
from PySide6.QtGui import QBrush, QColor, QPen, QPolygonF, QPainter, QPolygon
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsPolygonItem, QWidget

from model.shapes.polygon import Polygon


class PolygonItem(QGraphicsPolygonItem):

    def __init__(self, model: Polygon):
        points = [
            QPointF(model.points[0].x, model.points[0].y),
            QPointF(model.points[1].x, model.points[1].y),
            QPointF(model.points[2].x, model.points[2].y),
            QPointF(model.points[3].x, model.points[3].y)
        ]

        super().__init__(QPolygonF(points))

        self.model = model
        self.setBrush(QBrush(QColor(38, 99, 255)))
        self.setPen(QPen(QColor(10, 30, 80), 1))
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

    # def itemChange(self, change, value):
    #     if change == QGraphicsPolygonItem.GraphicsItemChange.ItemPositionHasChanged:
    #         pos: QPointF = self.pos()
    #
    #     return super().itemChange(change, value)

    def itemChange(self, change, value):
        if change == QGraphicsPolygonItem.GraphicsItemChange.ItemPositionHasChanged:
            pos: QPointF = self.pos()

            self.model.points[0].x = float(pos.x())
            self.model.points[0].y = float(pos.y())

            self.model.points[1].x = float(pos.x())
            self.model.points[1].y = float(pos.y())

            self.model.points[2].x = float(pos.x())
            self.model.points[2].y = float(pos.y())

        return super().itemChange(change, value)


