from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from model.point import Point


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

        self.info.setText("Неизвестный объект")