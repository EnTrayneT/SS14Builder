from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSizePolicy, QTextEdit, QComboBox, QMessageBox, QFileDialog, QTabWidget, QTextBrowser, QMainWindow, QStatusBar, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
import subprocess
import os

class TutorialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Создаем вкладки
        self.tutorial_tab_1 = QWidget()
        self.tutorial_tab_2 = QWidget()
        self.tutorial_tab_widget = QTabWidget()
        self.tutorial_tab_widget.addTab(self.tutorial_tab_1, "Вкладка 1")
        self.tutorial_tab_widget.addTab(self.tutorial_tab_2, "Вкладка 2")
        self.setCentralWidget(self.tutorial_tab_widget)

        # Вкладка 1: информация о SS14Builder
        self.tutorial_tab_1.layout = QVBoxLayout(self.tutorial_tab_1)
        self.tutorial_tab_1.browser = QTextBrowser(self.tutorial_tab_1)
        self.tutorial_tab_1.browser.setHtml("""
            <h1>Добро пожаловать в учебное пособие SS14Builder!</h1>
            <p>Здесь вы научитесь создавать проекты SS14Builder и запускать их.</p>
            <h2>Шаг 1: Выбор пути</h2>
            <p>Нажмите кнопку "Выбрать путь" и укажите папку с проектом SS14.</p>
            """)
        self.tutorial_tab_1.layout.addWidget(self.tutorial_tab_1.browser)

        # Вкладка 2: сборка проекта
        self.tutorial_tab_2.layout = QVBoxLayout(self.tutorial_tab_2)
        self.tutorial_tab_2.browser = QTextBrowser(self.tutorial_tab_2)
        self.tutorial_tab_2.browser.setHtml("""
            <h2>Шаг 2: Сборка проекта</h2>
            <p>После выбора пути нажмите "Сборка" для сборки проекта.</p>
            """)
        self.tutorial_tab_2.layout.addWidget(self.tutorial_tab_2.browser)

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setGraphicsEffect(self.shadow_effect())

    def shadow_effect(self):
        # Создаем эффект тени
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.black)
        shadow.setOffset(4, 4)
        return shadow

class SS14BuilderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.repo_directory = ""
        self.init_ui()
        self.fade_in_animation()

    def fade_in_animation(self):
        # Анимация появления окна
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    def init_ui(self):
        # Основной интерфейс приложения
        layout = QVBoxLayout()
        self.setStyleSheet("""
            background-color: #222222;
            color: #FFFFFF;
            QLabel { color: #00FF00; font-family: 'Arial', sans-serif; font-size: 16pt; }
            QPushButton { font-size: 12pt; background-color: #000000; color: #FFFFFF; border: 2px solid #00FF00; border-radius: 10px; }
            QPushButton:hover { background-color: #111111; }
            QPushButton:pressed { background-color: #333333; }
            QTextEdit { background-color: #000000; color: #FFFFFF; border: 2px solid #00FF00; border-radius: 10px; }
            QTextEdit:focus { border: 2px solid #FFFFFF; }
            QComboBox { background-color: #000000; color: #FFFFFF; border: 2px solid #00FF00; border-radius: 10px; }
            QComboBox:focus { border: 2px solid #FFFFFF; }
        """)
        
        # Заголовок
        title_label = QLabel("SS14 Builder", self)
        title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Статусная строка
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Статус")
        layout.addWidget(self.status_bar)

        # Выбор пути
        path_layout = QHBoxLayout()
        self.path_label = QLabel("Путь:", self)
        path_layout.addWidget(self.path_label)
        self.choose_path_button = AnimatedButton("Выбрать путь", self)
        self.choose_path_button.clicked.connect(self.choose_path)
        path_layout.addWidget(self.choose_path_button)
        layout.addLayout(path_layout)

        # Разделитель
        layout.addWidget(QLabel("", self))

        # Кнопка сборки подмодулей
        self.update_submodules_button = AnimatedButton("Обновить подмодули", self)
        self.update_submodules_button.setFixedSize(150, 30)
        self.update_submodules_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.update_submodules_button.clicked.connect(self.confirm_submodule_update)
        layout.addWidget(self.update_submodules_button)

        # Разделитель
        layout.addWidget(QLabel("", self))

        # Выбор конфигурации сборки
        self.build_config_box = QComboBox(self)
        self.build_config_box.addItems(["Release", "DebugOpt", "Debug", "Tools"])

        info_text = {
            "Release": "Описание Release.",
            "DebugOpt": "Описание DebugOpt.",
            "Debug": "Описание Debug.",
            "Tools": "Описание Tools."
        }

        def show_info(index):
            selected_config = self.build_config_box.itemText(index)
            if selected_config in info_text:
                QMessageBox.information(self, selected_config, info_text[selected_config])

        self.build_config_box.currentIndexChanged.connect(show_info)
        layout.addWidget(self.build_config_box)

        # Кнопка сборки
        self.build_button = AnimatedButton("Сборка", self)
        self.build_button.setFixedSize(100, 30)
        self.build_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.build_button.clicked.connect(self.build)
        layout.addWidget(self.build_button)

        # Кнопка учебника
        self.tutorial_button = AnimatedButton("Учебник", self)
        self.tutorial_button.setFixedSize(100, 30)
        self.tutorial_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.tutorial_button.clicked.connect(self.show_tutorial)
        layout.addWidget(self.tutorial_button)

        # Кнопка запуска
        self.startup_button = AnimatedButton("Запуск", self)
        self.startup_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.startup_button.clicked.connect(self.startup)
        layout.addWidget(self.startup_button)

        # Разделитель
        layout.addWidget(QLabel("", self))

        # Терминал
        self.terminal = QTextEdit(self)
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background-color: #000000; color: #FFFFFF; font-family: 'Courier New', monospace;")
        layout.addWidget(self.terminal)

        self.setLayout(layout)
        self.terminal.cursorPositionChanged.connect(self.scroll_to_bottom)

        # Инициализация таймера
        self.terminal_message_timer = QTimer(self)
        self.terminal_message_timer.setSingleShot(True)
        self.terminal_message_timer.timeout.connect(self.show_terminal_message)
        self.terminal_message_timer.start(5000)

    def scroll_to_bottom(self):
        scrollbar = self.terminal.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def confirm_submodule_update(self):
        reply = QMessageBox.question(self, 'Подтвердить обновление подмодулей', 'Вы уверены?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.update_submodules()

    def update_submodules(self):
        try:
            if not os.path.exists(os.path.join(self.repo_directory, ".git")):
                self.status_bar.showMessage("Ошибка: не в репозитории Git.")
                return

            result = subprocess.run(["git", "submodule", "update", "--init", "--recursive"], capture_output=True, text=True, cwd=self.repo_directory)
            self.terminal.append("Результат обновления подмодулей: " + result.stdout)
            if result.returncode != 0:
                self.terminal.append("Ошибка обновления подмодулей: " + result.stderr)
            else:
                self.terminal.append("Подмодули успешно обновлены.")
        except subprocess.CalledProcessError as e:
            self.terminal.append("Ошибка: Не удалось обновить подмодули.")
            self.terminal.append(str(e))

    def choose_path(self):
        repo_directory = QFileDialog.getExistingDirectory(self, "Выберите каталог")
        if repo_directory:
            if self.validate_path(repo_directory):
                self.repo_directory = repo_directory
                self.path_label.setText(f"<font color='green'>Путь найден</font>")
                self.status_bar.showMessage("Путь верифицирован")
            else:
                self.path_label.setText(f"<font color='red'>Неверный путь</font>")
                QMessageBox.critical(self, "Ошибка", "Выбран неверный каталог")
                self.status_bar.showMessage("Ошибка: Неверный путь")
        else:
            self.status_bar.showMessage("Выбор пути отменен")

    def validate_path(self, path):
        return os.path.isdir(path)

    def build(self):
        if self.repo_directory == "":
            QMessageBox.critical(self, "Ошибка", "Сначала выберите путь")
            return

        selected_config = self.build_config_box.currentText()
        try:
            process = subprocess.Popen(["dotnet", "build", "--configuration", selected_config], cwd=self.repo_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                self.terminal.append(f"Процесс сборки завершен успешно.")
            else:
                self.terminal.append(f"Процесс сборки завершен с ошибкой {process.returncode}")
                self.terminal.append(stderr.decode())
        except Exception as e:
            self.terminal.append(f"Произошла ошибка во время сборки.")
            self.terminal.append(str(e))

    def startup(self):
        if self.repo_directory == "":
            QMessageBox.critical(self, "Ошибка", "Сначала выберите путь")
            return

        try:
            script_path = os.path.join(self.repo_directory, "start.sh")  # Укажите путь к скрипту запуска
            if os.path.exists(script_path):
                subprocess.Popen(["bash", script_path])
                self.terminal.append("Скрипт запуска выполнен.")
            else:
                self.terminal.append("Ошибка: Скрипт запуска не найден.")
        except Exception as e:
            self.terminal.append("Произошла ошибка при запуске.")
            self.terminal.append(str(e))


    def show_terminal_message(self):
        self.terminal_message_timer.stop()
        self.terminal.append("Добро пожаловать в SS14Builder!")
        self.terminal.append("Терминал активен.")
        
    def show_tutorial(self):
        self.tutorial_window = TutorialWindow()
        self.tutorial_window.show()

if __name__ == '__main__':
    app = QApplication([])
    ss14_builder = SS14BuilderApp()
    ss14_builder.show()
    app.exec_()