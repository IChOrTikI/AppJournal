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

        #Создание БД
        self.create_db()

        # self.test_connection_create_db()

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

        # Подключение кнопки к функции
        self.ui.button_add_author.clicked.connect(self.add_author_to_db)

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

    #Метод для добавления пользователя
    def add_author_to_db(self):
        first_name = self.ui.author_first_name.text()
        last_name = self.ui.author_last_name.text()
        middle_name = self.ui.author_middle_name.text()
        info_about_author = self.ui.author_additional_info.toPlainText()
        
        # Проверка сохранения данных
        # print(first_name, last_name, middle_name, info_about_author, end='\n')

        connection = None
        cursor = None
        try:
            connection = connect(
                host="sql12.freesqldatabase.com",
                user="sql12749774",
                password="kmYMIq9h6G",
                database="sql12749774" # Имя базы данных
            )

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                cursor.execute("""INSERT INTO Authors (first_name, last_name, middle_name, info)
                VALUES (%s, %s, %s, %s); """, (first_name, last_name, middle_name, info_about_author))

                print("Пользователь добавлен")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.commit()
                connection.close()
                

        self.ui.author_first_name.clear()
        self.ui.author_last_name.clear()
        self.ui.author_middle_name.clear()
        self.ui.author_additional_info.clear()
        
    #Метод для загрузки авторов из БД на страницу с авторами (метод принимает список авторов для отображения)    
    def loading_authors_from_the_database_to_page(self, list_of_authors):
        pass

    #Создание БД
    def create_db(self):
        connection = None
        cursor = None
        try:
            connection = connect(
                host="sql12.freesqldatabase.com",
                user="sql12749774",
                password="kmYMIq9h6G",
                database="sql12749774" # Имя базы данных
            )

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                # Создание БД если её нет
                # cursor.execute(""" CREATE DATABASE IF NOT EXISTS AppJournal; """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Authors (
                        ID_Author INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        first_name VARCHAR(150) NOT NULL,
                        last_name VARCHAR(150) NOT NULL,
                        middle_name VARCHAR(150) NOT NULL,
                        info TEXT NOT NULL,
                        count_articles INT NOT NULL DEFAULT 0
                    );
                """)


                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Articles (
                        ID_Article INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        date_create DATE NOT NULL,
                        science VARCHAR(255) NOT NULL,
                        text_article TEXT NOT NULL,
                        isUse BOOLEAN NOT NULL DEFAULT FALSE
                    );
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Authors_Articles (
                        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        ID_Author INT,
                        ID_Article INT UNIQUE,
                        FOREIGN KEY (ID_Author) REFERENCES Authors(ID_Author) ON DELETE CASCADE,
                        FOREIGN KEY (ID_Article) REFERENCES Articles(ID_Article) ON DELETE CASCADE
                    );
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Journals (
                        ID_Journal INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        date_create DATE NOT NULL,
                        number_journal INT NOT NULL
                    );
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Articles_Journals (
                        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        ID_Journal INT,
                        ID_Article INT UNIQUE,
                        FOREIGN KEY (ID_Journal) REFERENCES Journals(ID_Journal) ON DELETE CASCADE,
                        FOREIGN KEY (ID_Article) REFERENCES Articles(ID_Article) ON DELETE CASCADE
                    );
                """)



                

                print("Таблицы успешно созданы.")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # Ткстовое подключение к БД
    def test_connection_create_db(self):
        connection = None
        cursor = None
        try:
            connection = connect(
                host="sql12.freesqldatabase.com",
                user="sql12747795",
                password="ujFlrPM1xw",
                database="sql12747795"
            )

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS authors (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        firstName VARCHAR(150) NOT NULL,
                        lastName VARCHAR(150) NOT NULL,
                        middleName VARCHAR(150),
                        info TEXT NOT NULL,
                        count_articles INT DEFAULT 0  
                )   ;
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS articles (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        date DATE NOT NULL,
                        science VARCHAR(100) NOT NULL,
                        text TEXT NOT NULL
                    );
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS journals (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        date DATE NOT NULL,
                        number INT NOT NULL
                    );
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS author_article (
                        authorId INT,
                        articleId INT,
                        PRIMARY KEY (authorId, articleId),
                        FOREIGN KEY (authorId) REFERENCES authors(id) ON DELETE CASCADE,
                        FOREIGN KEY (articleId) REFERENCES articles(id) ON DELETE CASCADE
                    );
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS journal_article (
                        JournalId INT,
                        ArticleId INT,
                        PRIMARY KEY (JournalId, ArticleId),
                        FOREIGN KEY (JournalId) REFERENCES journals(id) ON DELETE CASCADE,
                        FOREIGN KEY (ArticleId) REFERENCES articles(id) ON DELETE CASCADE
                    );
                """)

                print("Таблицы успешно созданы.")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())

