import sys

from PySide6.QtGui import QIcon, QAction

from view.components.coordinate_plane import GridView
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QLabel, QGraphicsScene, QToolBar,
)

from model.shapes import Triangle, Polygon
from view.items.point_item import PointItem
from model.point import Point
from view.components.properties_panel import PropertiesPanel
from view.items.polygon_item import PolygonItem
from view.items.triangle_item import TriangleItem
from view.forms.application_forms import FormWindow


class CanvasScene(QGraphicsScene):

    selectionChangedObject = Signal(object)
    pointsCountChanged = Signal(int)
    cursorMoved = Signal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.points: list[Point] = []
        self.triangles: list[Triangle] = []

        self.form_window = None

        self.selectionChanged.connect(self.emit_selection)

    def emit_selection(self):
        items = self.selectedItems()
        print(items)
        if items and isinstance(items[0], PointItem):
            self.selectionChangedObject.emit(items[0].model)
        elif items and isinstance(items[0], TriangleItem):
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
                self.points.append(model)
                self.addItem(PointItem(model))
                self.pointsCountChanged.emit(len(self.points))
                event.accept()
                return

        if event.button() == Qt.RightButton:
            view = self.views()[0] if self.views() else None
            item = self.itemAt(p, view.transform()) if view else None
            if isinstance(item, PointItem):
                try:
                    self.points.remove(item.model)
                except ValueError:
                    pass
                self.removeItem(item)
                self.pointsCountChanged.emit(len(self.points))
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
        self.points.clear()
        self.pointsCountChanged.emit(0)
        self.selectionChangedObject.emit(None)

    def create_triangle(self):
        triangle_coordinates = Triangle(Point(60, 60), Point(15, 140), Point(140, 140))
        self.addItem(TriangleItem(triangle_coordinates))


    def create_polygon(self):
        triangle_coordinates = Polygon(Point(60, 60), Point(15, 140)
                                       ,Point(140, 140), Point(240, 240))
        self.addItem(PolygonItem(triangle_coordinates))

    def open_add_points_to_triangle(self):
        """Creates and shows the new window."""
        if self.form_window is None:
            self.form_window = FormWindow()
        self.form_window.show()
        self.form_window.raise_()
        self.form_window.activateWindow()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Geometric Analyzer")
        self.scene = CanvasScene(self)
        self.scene.setSceneRect(-50, -30, 100, 60)

        self.view = GridView(self.scene)

        self.props = PropertiesPanel()

        # Root layout
        root = QWidget()
        layout = QHBoxLayout(root)
        layout.addWidget(self.view, 1)
        layout.addWidget(self.props)
        self.setCentralWidget(root)

        sb = self.statusBar()
        self.points_label = QLabel("Points: 0")
        self.cursor_label = QLabel("Cursor: (0.00, 0.00)")
        sb.addPermanentWidget(self.points_label)
        sb.addPermanentWidget(self.cursor_label)

        self.scene.selectionChangedObject.connect(self.props.show_object)
        self.scene.pointsCountChanged.connect(lambda n: self.points_label.setText(f"Points: {n}"))
        self.scene.cursorMoved.connect(lambda x, y: self.cursor_label.setText(f"Cursor: ({x:.2f}, {y:.2f})"))

        tb = QToolBar("Left Toolbar", self)

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
        self.addActionToToolBar(tb, select_point_icon, "Select", self.scene.open_add_points_to_triangle)
        self.addActionToToolBar(tb, auto_triangulate_icon, "Auto Triangulate", self.scene.create_triangle)
        self.addActionToToolBar(tb, largest_triangle_icon, "Largest Triangle", self.scene.clear_all)
        self.addActionToToolBar(tb, convex_hall_triangle_icon, "Convex Hall", self.scene.create_polygon)
        self.addActionToToolBar(tb, clear_all_icon, "Clear All",self.scene.clear_all )

    def addActionToToolBar(self, tool_bar, icon, text, trigger):
        action = QAction(icon, "&" + text, self)
        action.setStatusTip(text)
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



