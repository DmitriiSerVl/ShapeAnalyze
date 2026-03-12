from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QGraphicsScene, QMainWindow, QWidget, QFormLayout, QLineEdit, QPushButton, QSpinBox
from model.point import Point
from model.shapes.polygon import Polygon
from model.shapes.triangle import Triangle
from view.items.point_item import PointItem
from view.items.polygon_item import PolygonItem
from view.items.triangle_item import TriangleItem


class CanvasScene(QGraphicsScene):

    selectionChangedObject = Signal(object)
    pointsCountChanged = Signal(int)
    cursorMoved = Signal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.points: list[Point] = []
        self.triangles: list[Triangle] = []
        self.polygones: list[Polygon] = []

        self.form_window_creare_polygon = None
        self.form_window = None
        self.form_coordinates_count = None

        self.selectionChanged.connect(self.emit_selection)

    def emit_selection(self):
        items = self.selectedItems()
        print(items)
        if items and isinstance(items[0], PointItem):
            self.selectionChangedObject.emit(items[0].model)
        elif items and isinstance(items[0], TriangleItem):
            self.selectionChangedObject.emit(items[0].model)
        elif items and isinstance(items[0], PolygonItem):
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

    def open_form_add_points_to_triangle(self):
        if self.form_window is None:
            self.form_window = FormWindow()
        self.form_window.show()
        self.form_window.raise_()
        self.form_window.activateWindow()

        self.form_window.submit_button.clicked.connect(self.open_form_add_points_to_triangle)
        if self.form_window.submit_action:
            self.addItem(TriangleItem(self.form_window.triangle_coordinates))
            self.form_window.submit_action = False

    def open_form_count_coordinates(self):
        if self.form_coordinates_count is None:
            self.form_coordinates_count = FormCountCoordinatesWindow()
        self.form_coordinates_count.show()
        self.form_coordinates_count.raise_()
        self.form_coordinates_count.activateWindow()

    def open_form_create_polygon(self):
        if self.form_window_creare_polygon is None:
            self.form_window_creare_polygon = FormCreatePolygon()
        self.form_window_creare_polygon.show()
        self.form_window_creare_polygon.raise_()
        self.form_window_creare_polygon.activateWindow()

        self.form_window_creare_polygon.submit_button.clicked.connect(self.open_form_create_polygon)
        if self.form_window_creare_polygon.submit_action:
            self.addItem(PolygonItem(self.form_window_creare_polygon.polygon_coordinates))
            print("Hello")
            self.form_window_creare_polygon.submit_action = False


class FormWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Triangle")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        form_layout = QFormLayout(central_widget)

        self.canvas_scene = CanvasScene(self)
        triangle_coordinates = Triangle(Point(60, 60), Point(15, 140), Point(140, 140))

        self.a_x = QLineEdit()
        self.a_y = QLineEdit()
        self.b_x = QLineEdit()
        self.b_y = QLineEdit()
        self.c_x = QLineEdit()
        self.c_y = QLineEdit()

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)

        self.submit_action = False

        self.triangle_coordinates = Triangle(Point(60, 60), Point(15, 140), Point(140, 140))

        form_layout.addRow("a.x coordinate:", self.a_x)
        form_layout.addRow("a.y coordinate:", self.a_y)
        form_layout.addRow("b.x coordinate:", self.b_x)
        form_layout.addRow("b.y coordinate:", self.b_y)
        form_layout.addRow("c.x coordinate:", self.c_x)
        form_layout.addRow("c.y coordinate:", self.c_y)
        form_layout.addRow(self.submit_button)

    def submit_form(self):
        ax = float(self.a_x.text())
        ay = float(self.a_y.text())
        bx = float(self.b_x.text())
        by = float(self.b_y.text())
        cx = float(self.c_x.text())
        cy = float(self.c_y.text())
        self.triangle_coordinates = Triangle(
                                        Point(ax, ay),
                                        Point(bx, by),
                                        Point(cx, cy))
        self.submit_action = True

class FormCountCoordinatesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select coordinates count")
        self.form_create_polygon = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        form_layout = QFormLayout(central_widget)

        self.canvas_scene = CanvasScene(self)
        self.count = QLineEdit()

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)

        self.submit_action = False
        form_layout.addRow("Count:", self.count)

        form_layout.addRow(self.submit_button)


    def submit_form(self):
        self.canvas_scene.open_form_create_polygon()

class FormCreatePolygon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Polygon")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        form_layout = QFormLayout(central_widget)

        self.canvas_scene = CanvasScene(self)
        self.polygon_coordinates = None

        self.a_x = QLineEdit()
        self.a_y = QLineEdit()
        self.b_x = QLineEdit()
        self.b_y = QLineEdit()
        self.c_x = QLineEdit()
        self.c_y = QLineEdit()
        self.d_x = QLineEdit()
        self.d_y = QLineEdit()

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)

        self.submit_action = False

        form_layout.addRow("a.x coordinate:", self.a_x)
        form_layout.addRow("a.y coordinate:", self.a_y)
        form_layout.addRow("b.x coordinate:", self.b_x)
        form_layout.addRow("b.y coordinate:", self.b_y)
        form_layout.addRow("c.x coordinate:", self.c_x)
        form_layout.addRow("c.y coordinate:", self.c_y)
        form_layout.addRow("d.x coordinate:", self.d_x)
        form_layout.addRow("d.y coordinate:", self.d_y)

        form_layout.addRow(self.submit_button)
    def submit_form(self):
        ax = float(self.a_x.text())
        ay = float(self.a_y.text())
        bx = float(self.b_x.text())
        by = float(self.b_y.text())
        cx = float(self.c_x.text())
        cy = float(self.c_y.text())
        dx = float(self.d_x.text())
        dy = float(self.d_y.text())
        self.polygon_coordinates = [ax, ay, bx, by, cx, cy, dx, dy]
        self.polygon_coordinates = Polygon(
            Point(ax, ay),
            Point(bx, by),
            Point(cx, cy),
            Point(dx, dy))
        print(self.polygon_coordinates)
        self.submit_action = True