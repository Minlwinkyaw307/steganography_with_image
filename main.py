import sys

from widgets.home_page import *

if __name__ == '__main__':
    steganography = Steganography()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    home_page = HomePage()
    home_page.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
