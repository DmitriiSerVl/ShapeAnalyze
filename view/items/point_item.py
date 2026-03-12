from PySide6.QtCore import QPointF
from PySide6.QtGui import QBrush, QColor, QPen, QPolygonF
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsPolygonItem
from model.point import Point

class PointItem(QGraphicsEllipseItem):
    R = 6

    def __init__(self, model: Point):
        super().__init__(-self.R, -self.R, self.R * 2, self.R * 2)
        self.model = model
        self.setPos(model.x, model.y)
        self.setBrush(QBrush(QColor(38, 99, 255)))
        self.setPen(QPen(QColor(10, 30, 80), 1))
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemPositionHasChanged:
            pos: QPointF = self.pos()
            self.model.x = float(pos.x())
            self.model.y = float(pos.y())
        return super().itemChange(change, value)