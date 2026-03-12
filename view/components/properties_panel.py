from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from model.point import Point
from model.shapes.polygon import Polygon
from model.shapes.triangle import Triangle


class PropertiesPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumWidth(280)

        title = QLabel("PropertiesPanel")
        title.setStyleSheet("font-weight: 700; font-size: 16px;")

        self.info = QLabel("Ничего не выбрано")
        self.info.setWordWrap(True)
        self.info.setStyleSheet("font-size: 14px;")

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(self.info)
        layout.addStretch(1)

    def show_object(self, obj):
        if obj is None:
            self.info.setText("Ничего не выбрано")
            return
        if isinstance(obj, Point):
            self.info.setText(f"Точка\nx: {obj.x:.2f}\ny: {obj.y:.2f}")
            return
        elif isinstance(obj, Triangle):
            triangle_area = obj.area()
            triangle_angles = obj.angles()
            self.info.setText(f"Треугольник\na: x: {obj.a.x:.2f} y: {obj.a.y:.2f}\n"
                              f"b: x: {obj.b.x:.2f} y: {obj.b.y:.2f}\n"
                              f"c: x: {obj.c.x:.2f} y: {obj.c.y:.2f}\n\n"
                              f"Площадь: {triangle_area}\n\n"
                              f"Углы: {triangle_angles}\n\n"
                              )
            return
        elif isinstance(obj, Polygon):
            triangle_area = obj.area()
            self.info.setText(f"Фигура\na: x: {obj.a.x:.2f} y: {obj.a.y:.2f}\n"
                              f"b: x: {obj.b.x:.2f} y: {obj.b.y:.2f}\n"
                              f"c: x: {obj.c.x:.2f} y: {obj.c.y:.2f}\n\n"
                              f"Площадь: {triangle_area}\n\n"
                              )
            return

        self.info.setText("Неизвестный объект")