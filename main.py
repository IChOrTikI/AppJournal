import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout

from MainWindow import Ui_MainWindow

import mysql.connector
from mysql.connector import connect, Error

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui =Ui_MainWindow()
        self.ui.setupUi(self)

        self.test_connection()

        # Первым делом открываем страницу с авторами
        self.open_page_of_authors()

        # Кнопка выхода из программы
        self.ui.button_exit.clicked.connect(self.close_app)

        # Кнопки для переключения между окнами
        self.ui.button_open_page_author.clicked.connect(self.open_page_of_authors)
        self.ui.button_open_page_articles.clicked.connect(self.open_page_of_articles)
        self.ui.button_open_page_journals.clicked.connect(self.open_page_of_journals)

        # Вызов метода для добавления элементов в ComboBox на страницк авторов
        self.add_to_combo_box_authors()    

        # Вызов метода для добавление элементов в ComboBox на странице статей    
        self.add_to_combo_box_articles()

        # Вызов метода для добавления элементов в ComboBox на странице журналов
        self.add_to_combo_box_journals()

    # Метод для закрытия приложения
    def close_app(self):
        self.close()

    # Методы для переключения окон
    def open_page_of_authors(self):
        self.ui.Main_widgets_pages.setCurrentIndex(0)
    
    def open_page_of_articles(self):
        self.ui.Main_widgets_pages.setCurrentIndex(2)
    
    def open_page_of_journals(self):
        self.ui.Main_widgets_pages.setCurrentIndex(1)
    
    # Метод для добавления элементов в ComboBox на странице автор
    def add_to_combo_box_authors(self):

        self.ui.combo_box_authors.addItem("Имя")
        self.ui.combo_box_authors.addItem("Фамилия")
        self.ui.combo_box_authors.addItem("Отчество")
        self.ui.combo_box_authors.addItem("Дополнительная информация")

    # Метод для добавления в ComboBox на странице статей
    def add_to_combo_box_articles(self):
        
        self.ui.combo_box_articles.addItem("Имя автора")
        self.ui.combo_box_articles.addItem("Фамилия автора")
        self.ui.combo_box_articles.addItem("Отчество автора")
        self.ui.combo_box_articles.addItem("Название статьи")
        self.ui.combo_box_articles.addItem("Дата")
        self.ui.combo_box_articles.addItem("Наука")
        # self.ui.combo_box_articles.addItem("Текст статьи")

    # Метод для добавления в ComboBox на странице журналов
    def add_to_combo_box_journals(self):
        self.ui.combo_box_journals.addItem("Название")
        self.ui.combo_box_journals.addItem("Дата")
        self.ui.combo_box_journals.addItem("Номер")


    # Ткстовое подключение к БД
    def test_connection(self):
        
        try:
            connection = connect(
                host="sql12.freesqldatabase.com",  # IP-адрес или доменное имя сервера
                user="sql12747795",  # Имя пользователя
                password="ujFlrPM1xw",  # Пароль пользователя
                database="sql12747795"  # Имя базы данных (если необходимо)
            )

            if connection.is_connected():
                print("Успешное подключение")

                # cursor = connection.cursor()

                # cursor.execute("DROP TABLE authors")

                # cursor.close()


        except Error as e:
            print("Ошибка подключения")
        finally:
            connection.close()

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())

