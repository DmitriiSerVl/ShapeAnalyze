from PySide6.QtCore import QPointF, QPoint
from PySide6.QtGui import QBrush, QColor, QPen, QPolygonF, QPainter, QPolygon
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsPolygonItem, QWidget

from model.shapes import Triangle


class TriangleItem(QGraphicsPolygonItem):
    R = 6

    def __init__(self, model: Triangle):

        points = [
            QPointF(200, 50),
            QPointF(50, 350),
            QPointF(350, 350)
        ]
        super().__init__(QPolygonF(points))
        self.model = model
        self.setBrush(QBrush(QColor(38, 99, 255)))
        self.setPen(QPen(QColor(10, 30, 80), 1))
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        # super().__init__()
        # painter = QPainter(self)
        # painter.setRenderHint(QPainter.Antialiasing)
        # points = [
        #     QPoint(200, 50),
        #     QPoint(50, 350),
        #     QPoint(350, 350)
        # ]
        #
        # # Create a QPolygon from the points
        # triangle = QPolygon(points)
        #
        # # Set the brush (fill color)
        # painter.setBrush(QBrush(QColor(0, 255, 0, 255)))  # Green color
        #
        # # Draw the polygon
        # painter.drawPolygon(triangle)

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemPositionHasChanged:
            pos: QPointF = self.pos()
        return super().itemChange(change, value)
