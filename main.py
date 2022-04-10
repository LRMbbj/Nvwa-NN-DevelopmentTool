import sys

from PyQt5.QtWidgets import QApplication
from Src import Controller
import View

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller.Controller()
    sys.exit(app.exec_())
