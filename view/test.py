from __future__ import annotations

import sys
from dataclasses import dataclass


from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
        QApplication,
        QDoubleSpinBox,
        QGridLayout,
        QLabel,
        QMainWindow,
        QPushButton,
        QSpinBox,
        QStackedWidget,
        QTabWidget,
        QVBoxLayout,
        QWidget,
)

class Point:
    x: float
    y: float


class RowCountWidget(QWidget):
    rowCountSelected = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.count_spin = QSpinBox(self)
        self.count_spin.setRange(2, 50)
        self.count_spin.setValue(4)

        title = QLabel("Choose how many rows of points you need:", self)
        create_button = QPushButton("Open point input tab", self)
        create_button.clicked.connect(self._emit_count)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.count_spin)
        layout.addWidget(create_button)
        layout.addStretch(1)

    def _emit_count(self) -> None:
        self.rowCountSelected.emit(self.count_spin.value())


class PointInputWidget(QWidget):
    pointsSubmitted = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._row_editors: list[tuple[QDoubleSpinBox, QDoubleSpinBox]] = []

        self.title_label = QLabel("Create rows first", self)
        self.grid = QGridLayout()

        submit_button = QPushButton("Submit points", self)
        submit_button.clicked.connect(self._submit_points)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addLayout(self.grid)
        layout.addWidget(submit_button)
        layout.addStretch(1)

    def set_row_count(self, count: int) -> None:
        self.title_label.setText(f"Input coordinates for {count} rows")

        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self._row_editors.clear()

        self.grid.addWidget(QLabel("Row"), 0, 0)
        self.grid.addWidget(QLabel("X"), 0, 1)
        self.grid.addWidget(QLabel("Y"), 0, 2)

        for row in range(count):
            x_spin = self._make_coord_spin()
            y_spin = self._make_coord_spin()
            self.grid.addWidget(QLabel(str(row + 1)), row + 1, 0)
            self.grid.addWidget(x_spin, row + 1, 1)
            self.grid.addWidget(y_spin, row + 1, 2)
            self._row_editors.append((x_spin, y_spin))

    @staticmethod
    def _make_coord_spin() -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(-10000.0, 10000.0)
        spin.setDecimals(3)
        spin.setSingleStep(1.0)
        return spin

    def _submit_points(self) -> None:
        points = [Point(x_spin.value(), y_spin.value()) for x_spin, y_spin in self._row_editors]
        self.pointsSubmitted.emit(points)


class ResultWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel("Submitted points will appear here.", self)
        self.label.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addStretch(1)

    def show_points(self, points: list[Point]) -> None:
        if not points:
            self.label.setText("No points submitted.")
            return

        lines = [f"{index + 1}. x={point.x:.3f}, y={point.y:.3f}" for index, point in enumerate(points)]
        self.label.setText("Points:\n" + "\n".join(lines))


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Point Input In One File")
        self.resize(700, 500)

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.row_count_widget = RowCountWidget(self)
        self.point_input_widget = PointInputWidget(self)
        self.result_widget = ResultWidget(self)

        self.tabs.addTab(self.row_count_widget, "Select Rows")
        self.tabs.addTab(self.point_input_widget, "Point Input")
        self.tabs.addTab(self.result_widget, "Result")

        self.row_count_widget.rowCountSelected.connect(self._open_input_tab)
        self.point_input_widget.pointsSubmitted.connect(self._show_result)

    def _open_input_tab(self, count: int) -> None:
        self.point_input_widget.set_row_count(count)
        self.tabs.setCurrentWidget(self.point_input_widget)

    def _show_result(self, points: list[Point]) -> None:
        self.result_widget.show_points(points)
        self.tabs.setCurrentWidget(self.result_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec())
