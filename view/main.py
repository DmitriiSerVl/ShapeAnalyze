import sys
from PySide6.QtGui import QIcon, QAction

from view.components.coordinate_plane import GridView
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QLabel, QToolBar
)
from view.components.properties_panel import PropertiesPanel
from view.items.scene import CanvasScene, FormWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Geometric Analyzer")
        self.scene = CanvasScene(self)
        self.scene.setSceneRect(-50, -30, 100, 60)
        self.view = GridView(self.scene)
        self.props = PropertiesPanel()
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
            add_point_icon = QIcon()
            select_point_icon = QIcon()
            auto_triangulate_icon = QIcon()
            largest_triangle_icon = QIcon()
            convex_hall_triangle_icon = QIcon()
            clear_all_icon = QIcon()

        self.addActionToToolBar(tb, add_point_icon, "Add Point", self.scene.clear_all)
        self.addActionToToolBar(tb, select_point_icon, "Select", self.scene.clear_all)
        self.addActionToToolBar(tb, auto_triangulate_icon, "Auto Triangulate", self.scene.open_form_add_points_to_triangle)
        self.addActionToToolBar(tb, largest_triangle_icon, "Largest Triangle", self.scene.open_form_create_polygon)
        self.addActionToToolBar(tb, convex_hall_triangle_icon, "Convex Hall", self.scene.open_form_count_coordinates)
        self.addActionToToolBar(tb, clear_all_icon, "Clear All",self.scene.clear_all )




    def addActionToToolBar(self, tool_bar, icon, text, trigger):
        action = QAction(icon, "&" + text, self)
        action.setStatusTip(text)
        tool_bar.addAction(action)
        if trigger:
            action.triggered.connect(trigger)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1200, 750)
    w.show()
    sys.exit(app.exec())



