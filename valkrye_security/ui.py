from typing import Any
import sys

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMessageBox
    from PyQt5.QtCore import Qt
except ImportError as e:
    print(f"Error occurred during PyQt5 module import: {str(e)}")
    sys.exit(1)


class UI(QMainWindow):
    def __init__(self, app_name: str = "Valkrye Security"):
        super().__init__()
        self.setWindowTitle(app_name)
        self.status_label = QLabel("Initializing...")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.status_label)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def update(self, status: str) -> None:
        self.status_label.setText(status)

    def alert(self, message: Any) -> None:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(str(message))
        msg_box.setWindowTitle("Alert")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())
