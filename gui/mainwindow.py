from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QTextEdit, QLabel, QComboBox, QTabWidget, QTextBrowser, QStatusBar, QApplication
from PyQt5.QtCore import QTimer, QEasingCurve, QPropertyAnimation, QRect
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect  # Import from QtWidgets instead of QtGui
import subprocess
import os
import sys

class TutorialWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Инициализация вкладок
        self.tutorial_tab_1 = QWidget()
        self.tutorial_tab_2 = QWidget()

        self.tutorial_tab_widget = QTabWidget()
        self.tutorial_tab_widget.addTab(self.tutorial_tab_1, "Вкладка 1")
        self.tutorial_tab_widget.addTab(self.tutorial_tab_2, "Вкладка 2")
        self.setCentralWidget(self.tutorial_tab_widget)

        # Инициализация макетов и виджетов для вкладки 1
        self.tutorial_tab_1.layout = QVBoxLayout(self.tutorial_tab_1)
        self.tutorial_tab_1.browser = QTextBrowser(self.tutorial_tab_1)
        self.tutorial_tab_1.browser.setHtml("""
            <h1>Добро пожаловать в учебное пособие SS14Builder!</h1>
            <p>В этом учебном пособии вы узнаете, как использовать SS14Builder для создания и запуска ваших проектов SS14.</p>
            <h2>Шаг 1: Выбор пути</h2>
            <p>Для начала нажмите кнопку "Выбрать путь" и выберите каталог, где расположен ваш проект SS14.</p>
            """)
        self.tutorial_tab_1.layout.addWidget(self.tutorial_tab_1.browser)

        # Инициализация макетов и виджетов для вкладки 2
        self.tutorial_tab_2.layout = QVBoxLayout(self.tutorial_tab_2)
        self.tutorial_tab_2.browser = QTextBrowser(self.tutorial_tab_2)
        self.tutorial_tab_2.browser.setHtml("""
            <h2>Шаг 2: Сборка вашего проекта</h2>
            <p>После выбора пути используйте кнопку "Сборка" для сборки вашего проекта в нужной конфигурации.
            Вы можете выбрать конфигурацию из выпадающего меню рядом с кнопкой "Сборка".</p>
            """)
        self.tutorial_tab_2.layout.addWidget(self.tutorial_tab_2.browser)

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setGraphicsEffect(self.shadow_effect())

    def shadow_effect(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 220))
        shadow.setOffset(4, 4)
        return shadow

class SS14BuilderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.repo_directory = ""
        self.init_ui()
        self.fade_in_animation()

    def fade_in_animation(self):
        # Создание анимации плавного появления
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)  # Длительность анимации в миллисекундах
        self.animation.setStartValue(0)  # Начальное значение прозрачности
        self.animation.setEndValue(1)  # Конечное значение прозрачности
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)  # Кривая анимации
        self.animation.start()

    def init_ui(self):
        # Инициализация макетов и виджетов
        layout = QVBoxLayout()
        self.setStyleSheet("""
            background-color: #333333;
            color: #FFFFFF;
            QLabel { color: #00FF00; }
            QPushButton { font-size: 10pt; }
            QTextEdit { background-color: #000000; color: #FFFFFF; }
        """)

        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Статусная строка")
        self.setLayout(layout)
        layout.addWidget(self.status_bar)
        self.path_label = QLabel("Путь:", self)
        layout.addWidget(self.path_label)

        self.choose_path_button = AnimatedButton("Выбрать путь", self)
        self.choose_path_button.clicked.connect(self.choose_path)
        layout.addWidget(self.choose_path_button)

        self.update_submodules_button = AnimatedButton("Обновить подмодули", self)
        self.update_submodules_button.setFixedSize(150, 30)
        self.update_submodules_button.clicked.connect(self.confirm_submodule_update)
        layout.addWidget(self.update_submodules_button)

        self.build_config_box = QComboBox(self)
        self.build_config_box.addItems(["Debug|x86", "Debug|x64", "Debug|ARM", "DebugOpt|x86", "DebugOpt|x64", "DebugOpt|ARM", "Tools|x86", "Tools|x64", "Tools|ARM", "Release|x86", "Release|x64", "Release|ARM"])
        self.build_config_box.currentIndexChanged.connect(self.show_selected_configuration)
        layout.addWidget(self.build_config_box)

        self.build_button = AnimatedButton("Сборка", self)
        self.build_button.setFixedSize(100, 30)
        self.build_button.clicked.connect(self.build)
        layout.addWidget(self.build_button)

        self.tutorial_button = AnimatedButton("Учебник", self)
        self.tutorial_button.setFixedSize(100, 30)
        self.tutorial_button.clicked.connect(self.show_tutorial)
        layout.addWidget(self.tutorial_button)

        self.startup_button = AnimatedButton("Запуск", self)
        self.startup_button.clicked.connect(self.startup)
        layout.addWidget(self.startup_button)

        # Инициализация QTextEdit для терминала и добавление начального сообщения
        self.terminal = QTextEdit(self)
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background-color: #000000; color: #FFFFFF;")
        self.terminal.append("Терминал активен.")
        layout.addWidget(self.terminal)

        self.setLayout(layout)

        # Инициализация таймеров
        self.terminal_message_timer = QTimer(self)
        self.terminal_message_timer.setSingleShot(True)
        self.terminal_message_timer.timeout.connect(self.show_terminal_message)
        self.terminal_message_timer.start(5000)

    def confirm_submodule_update(self):
        reply = QMessageBox.question(self, 'Подтвердить обновление подмодулей', 'Вы уверены, что хотите обновить подмодули?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.update_submodules()

    def update_submodules(self):
        try:
            if not os.path.exists(os.path.join(self.repo_directory, ".git")):
                self.status_bar.showMessage("Ошибка: Не внутри репозитория Git.")
                return

            self.status_bar.showMessage("Текущий рабочий каталог: " + os.getcwd())
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
        self.repo_directory = QFileDialog.getExistingDirectory(self, "Выберите каталог")
        self.path_label.setText(f"Путь: {self.repo_directory}")

    def build(self):
        if self.repo_directory == "":
            QMessageBox.critical(self, "Ошибка", "Сначала выберите путь")
            return

        platforms = ["x86", "x64", "x32"]  # Замените "x32" на соответствующую вам платформу

        for platform in platforms:
            try:
                process = subprocess.Popen(["dotnet", "build", "--configuration", "Debug", "--platform", platform], cwd=self.repo_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode == 0:
                    self.terminal.append(f"Процесс сборки для платформы {platform} завершен успешно.")
                else:
                    self.terminal.append(f"Процесс сборки для платформы {platform} завершен с ошибкой {process.returncode}")
                    self.terminal.append(stderr.decode())
            except Exception as e:
                self.terminal.append(f"Произошла ошибка во время сборки для платформы {platform}.")
                self.terminal.append(str(e))

    def startup(self):
        if self.repo_directory == "":
            QMessageBox.critical(self, "Ошибка", "Сначала выберите путь")
            return

        try:
            script_path = os.path.join(self.repo_directory, "start.sh")  # Замените на путь к вашему скрипту запуска
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
        self.terminal.append("Терминал активен.")

    def show_tutorial(self):
        self.tutorial_window = TutorialWindow()
        self.tutorial_window.show()

    def show_selected_configuration(self, index):
        selected_config = self.build_config_box.itemText(index)
        self.terminal.append(f"Выбрана версия сборки: {selected_config}")