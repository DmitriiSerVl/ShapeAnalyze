from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
import math

class GridView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.grid_step = 1.0
        self.grid_bold_every = 5      # каждая N-я линия жирная
        self.setBackgroundBrush(Qt.white)


    def drawBackground(self, painter: QPainter, rect):
        super().drawBackground(painter, rect)

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, False)

        thin = QPen(QColor(0, 0, 0, 18), 0)
        bold = QPen(QColor(0, 0, 0, 35), 0)
        axis = QPen(QColor(0, 0, 0, 90), 0)

        step = self.grid_step

        left = math.floor(rect.left() / step) * step
        right = math.ceil(rect.right() / step) * step
        top = math.floor(rect.top() / step) * step
        bottom = math.ceil(rect.bottom() / step) * step

        # Вертикальные линии
        x = left
        while x <= right:
            idx = int(round(x / step))
            painter.setPen(bold if (idx % self.grid_bold_every == 0) else thin)
            painter.drawLine(QPointF(x, top), QPointF(x, bottom))
            x += step

        y = top
        while y <= bottom:
            idx = int(round(y / step))
            painter.setPen(bold if (idx % self.grid_bold_every == 0) else thin)
            painter.drawLine(QPointF(left, y), QPointF(right, y))
            y += step


        painter.setPen(axis)
        painter.drawLine(QPointF(0, top), QPointF(0, bottom))
        painter.drawLine(QPointF(left, 0), QPointF(right, 0))

        painter.restore()


    def wheelEvent(self, event):
        zoom_in = 1.15
        zoom_out = 1 / zoom_in
        if event.angleDelta().y() > 0:
            self.scale(zoom_in, zoom_in)
        else:
            self.scale(zoom_out, zoom_out)

