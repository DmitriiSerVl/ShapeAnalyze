import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFormLayout, QLineEdit, QSpinBox, QPushButton


class FormWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple PySide6 Form")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        form_layout = QFormLayout(central_widget)

        self.a_x = QLineEdit()
        self.a_y = QLineEdit()
        self.b_x = QLineEdit()
        self.b_y = QLineEdit()
        self.c_x = QLineEdit()
        self.c_y = QLineEdit()

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)

        form_layout.addRow("a.x coordinate:", self.a_x)
        form_layout.addRow("a.y coordinate:", self.a_y)
        form_layout.addRow("b.x coordinate:", self.b_x)
        form_layout.addRow("b.y coordinate:", self.b_y)
        form_layout.addRow("c.x coordinate:", self.c_x)
        form_layout.addRow("c.y coordinate:", self.c_y)
        form_layout.addRow(self.submit_button)

    def submit_form(self):
        pass
        # print(f"Name: {self.name_edit.text()}, Email: {self.email_edit.text()}, Age: {self.age_spinbox.value()}")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = FormWindow()
#     window.show()
#     sys.exit(app.exec())
