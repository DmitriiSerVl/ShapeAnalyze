import sys

from PySide6.QtGui import QIcon, QAction

from coordinate_plane import GridView
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QLabel, QGraphicsScene, QToolBar,
)

from model.shapes import Triangle
from view.point_item import PointItem
from model.point import Point
from view.properties_panel import PropertiesPanel
from view.triangle_item import TriangleItem


class CanvasScene(QGraphicsScene):

    selectionChangedObject = Signal(object)
    pointsCountChanged = Signal(int)
    cursorMoved = Signal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.models: list[Point] = []

        self.selectionChanged.connect(self._emit_selection)

    def _emit_selection(self):
        items = self.selectedItems()
        if items and isinstance(items[0], PointItem):
            self.selectionChangedObject.emit(items[0].model)
        else:
            self.selectionChangedObject.emit(None)

    def mousePressEvent(self, event):
        p = event.scenePos()

        if event.button() == Qt.LeftButton:
            view = self.views()[0] if self.views() else None
            item = self.itemAt(p, view.transform()) if view else None

            if item is None:
                model = Point(p.x(), p.y())

                triangle_cooridinates = Triangle(Point(p.x(), p.y()), Point(p.x(), p.y()), Point(p.x(), p.y()))

                self.models.append(model)
                self.addItem(PointItem(model))
                self.addItem(TriangleItem(triangle_cooridinates))


                self.pointsCountChanged.emit(len(self.models))
                event.accept()
                return

        if event.button() == Qt.RightButton:
            view = self.views()[0] if self.views() else None
            item = self.itemAt(p, view.transform()) if view else None
            if isinstance(item, PointItem):
                try:
                    self.models.remove(item.model)
                except ValueError:
                    pass
                self.removeItem(item)
                self.pointsCountChanged.emit(len(self.models))
                self.selectionChangedObject.emit(None)
                event.accept()
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        p = event.scenePos()
        self.cursorMoved.emit(p.x(), p.y())
        super().mouseMoveEvent(event)

    def clear_all(self):
        self.clear()
        self.models.clear()
        self.pointsCountChanged.emit(0)
        self.selectionChangedObject.emit(None)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Geometric Analyzer")
        self.scene = CanvasScene(self)
        self.scene.setSceneRect(-50, -30, 100, 60)

        # View (grid)
        self.view = GridView(self.scene)

        # Properties
        self.props = PropertiesPanel()

        # Root layout
        root = QWidget()
        layout = QHBoxLayout(root)
        layout.addWidget(self.view, 1)
        layout.addWidget(self.props)
        self.setCentralWidget(root)

        # Status bar
        sb = self.statusBar()
        self.points_label = QLabel("Points: 0")
        self.cursor_label = QLabel("Cursor: (0.00, 0.00)")
        sb.addPermanentWidget(self.points_label)
        sb.addPermanentWidget(self.cursor_label)

        # Signals
        self.scene.selectionChangedObject.connect(self.props.show_object)
        self.scene.pointsCountChanged.connect(lambda n: self.points_label.setText(f"Points: {n}"))
        self.scene.cursorMoved.connect(lambda x, y: self.cursor_label.setText(f"Cursor: ({x:.2f}, {y:.2f})"))

        # Simple toolbar actions
        # tb = self.addToolBar("Tools")

        tb = QToolBar("Left Toolbar", self)

        # 2. Add toolbar to the left area
        self.addToolBar(Qt.LeftToolBarArea, tb)

        tb.setStyleSheet("QToolBar { background-color: #3a4f5e;}"
                              "QToolButton { color: white; }"
                              "QToolButton:hover { background: #00BFFF; }")

        try:
            add_point_icon = QIcon("images/add.png")
            select_point_icon = QIcon("images/select.png")
            auto_triangulate_icon = QIcon("images/auto_triangulate.png")
            largest_triangle_icon = QIcon("images/largest_triangle.png")
            convex_hall_triangle_icon = QIcon("images/convex_hall.png")
            clear_all_icon = QIcon("images/clear_all.png")
        except Exception as e:
            print(f"Error loading icon: {e}. Make sure 'exit.png' exists.")
            # Use a fallback if the icon is missing
            add_point_icon = QIcon()
            select_point_icon = QIcon()
            auto_triangulate_icon = QIcon()
            largest_triangle_icon = QIcon()
            convex_hall_triangle_icon = QIcon()
            clear_all_icon = QIcon()

        self.addActionToToolBar(tb, add_point_icon, "Add Point", self.scene.clear_all)
        self.addActionToToolBar(tb, select_point_icon, "Select", self.scene.clear_all)
        self.addActionToToolBar(tb, auto_triangulate_icon, "Auto Triangulate", self.scene.clear_all)
        self.addActionToToolBar(tb, largest_triangle_icon, "Largest Triangle", self.scene.clear_all)
        self.addActionToToolBar(tb, convex_hall_triangle_icon, "Convex Hall", self.scene.clear_all)
        self.addActionToToolBar(tb, clear_all_icon, "Clear All",self.scene.clear_all )

    def addActionToToolBar(self, tool_bar, icon, text, trigger):
        action = QAction(icon, "&" + text, self)
        action.setStatusTip(text)  # Optional: Add status bar tip
        # add_point_action.triggered.connect(self.close)  # Connect the action to a function
        tool_bar.addAction(action)
        if trigger:
            action.triggered.connect(trigger)





def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1200, 750)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()



