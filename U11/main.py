import sys
from PyQt5 import QtWidgets


class MyWindow(object):
    def setupUI(self, main_window):
        main_window.setGeometry(200, 200, 300, 300)
        main_window.setWindowTitle("GUI Example")

        self.label = QtWidgets.QLabel(main_window)
        self.label.setText("Testtext")
        self.label.move(50, 50)

        self.button = QtWidgets.QPushButton(main_window)
        self.button.setText("Click me!")
        self.button.clicked.connect(self.clicked)


    def clicked(self):
        self.label.setText("Button pressed")
        self.update()

    def update(self):
        self.label.adjustSize()


def window():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = MyWindow()
    ui.setupUI(main_window)

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()