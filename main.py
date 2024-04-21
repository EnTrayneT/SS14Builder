import sys
import os

# Добавьте путь к директории DLL PyQt5 в переменную PATH
pyqt5_dll_path = r'C:\PyQt5\Qt\bin'  # Замените на путь к вашей директории DLL PyQt5
if pyqt5_dll_path not in os.environ['PATH'].split(os.pathsep):
    os.environ['PATH'] += os.pathsep + pyqt5_dll_path

# Загрузите модуль PyQt5
import PyQt5

from PyQt5.QtGui import QIcon

# Загрузите модуль QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QTextEdit, QLabel, QComboBox, QTabWidget, QTextBrowser
sys.path.append(r'C:\Users\gofne\OneDrive\Рабочий стол\SS14Build\src\gui')

from gui.mainwindow import TutorialWindow  # Импортируем TutorialWindow из mainwindow

# Здесь можно продолжить ваш код

from PyQt5.QtWidgets import QApplication
from gui.mainwindow import SS14BuilderApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SS14BuilderApp()
    window.setWindowTitle("SS14 Builder Beta 0.1")
    window.setWindowIcon(QIcon(r'C:\Users\gofne\OneDrive\Документы\GitHub\SS14Builder\gui\resources\images\SS14_Builder.png'))  # Используйте префикс r перед строкой пути
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())