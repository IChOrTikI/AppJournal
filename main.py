import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout
from PyQt5 import QtGui

from MainWindow import Ui_MainWindow
from EditAuthorWindow import Ui_EditAuthorWindow
from EditArticleWindow import Ui_EditArticleWindow
from EditAuthorWidget import Ui_Form  

import mysql.connector
from mysql.connector import connect, Error

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
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

        # Подключение кнопки к функции добавления авторов в БД
        self.ui.button_add_author.clicked.connect(self.add_author_to_db)

        # Подключение кнопки для поиска авторов по параметрам
        self.ui.button_search_authors_with_param.clicked.connect(self.search_authors_with_param)

        # Подключение кнопки к функции добавления статьи в БД
        self.ui.button_add_articles.clicked.connect(self.add_article_to_db)



    # Метод для закрытия приложения
    def close_app(self):
        self.close()

    # Методы для переключения окон
    def open_page_of_authors(self):
        self.ui.Main_widgets_pages.setCurrentIndex(0)
        
        # Получаем список всех авторов, так как не передаем параметры
        list_of_authors = self.get_list_of_authors()

        # Передаем список авторов для добавления авторов на окно
        self.loading_authors_from_the_database_to_page(list_of_authors)

    def open_page_of_articles(self):
        self.ui.Main_widgets_pages.setCurrentIndex(2)

        # Вызываем функцю для заргрузки авторов в поля для выбора автора сатьи при добавлении статьи
        self.load_authors_to_combo_box_article()
    
    def open_page_of_journals(self):
        self.ui.Main_widgets_pages.setCurrentIndex(1)
    
    # Метод для добавления элементов в ComboBox на странице автор
    def add_to_combo_box_authors(self):

        self.ui.combo_box_authors.addItem("Имя")
        self.ui.combo_box_authors.addItem("Фамилия")
        self.ui.combo_box_authors.addItem("Отчество")
        self.ui.combo_box_authors.addItem("Дополнительная информация")
        self.ui.combo_box_authors.addItem("Сброс параметров")

    # Метод для добавления в ComboBox на странице статей
    def add_to_combo_box_articles(self):
        
        self.ui.combo_box_articles.addItem("Имя автора")
        self.ui.combo_box_articles.addItem("Фамилия автора")
        self.ui.combo_box_articles.addItem("Отчество автора")
        self.ui.combo_box_articles.addItem("Название статьи")
        self.ui.combo_box_articles.addItem("Дата")
        self.ui.combo_box_articles.addItem("Наука")
        self.ui.combo_box_articles.addItem("Сброс параметров")
        # self.ui.combo_box_articles.addItem("Текст статьи")

    # Метод для добавления в ComboBox на странице журналов
    def add_to_combo_box_journals(self):
        self.ui.combo_box_journals.addItem("Название")
        self.ui.combo_box_journals.addItem("Дата")
        self.ui.combo_box_journals.addItem("Номер")

    # Метод для добавления авторов
    def add_author_to_db(self):
        first_name = self.ui.author_first_name.text()
        last_name = self.ui.author_last_name.text()
        middle_name = self.ui.author_middle_name.text()
        info_about_author = self.ui.author_additional_info.toPlainText()

        # Добавление валидации данных
        
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

        # После добавления автора обновляем список
        # Получаем список всех авторов, так как не передаем параметры
        list_of_authors = self.get_list_of_authors()

        # Передаем список авторов для добавления авторов на окно
        self.loading_authors_from_the_database_to_page(list_of_authors)

    # Метод для загрузки авторов из списка авторов на страницу с авторами (метод принимает список авторов для отображения)    
    def loading_authors_from_the_database_to_page(self, list_of_authors):
        self.ui.Widget_authors.clear()

        for author in list_of_authors:
            item = QListWidgetItem()
            item_widget = QWidget()
            name_author = QLabel(str(author[1]) + " " + str(author[2]) + " " + str(author[3]))
            separator_name = QLabel()
            text_info = QLabel(str(author[4][:95]) + "... ")
            separator_info = QLabel()

            edit_push_button = QPushButton("Редактировать")
            delete_push_button = QPushButton("Удалить")

            edit_push_button.setObjectName(str(author[0])) # Именем кнопки для редактирования будет являться id пользователя
            delete_push_button.setObjectName(str(author[0]))  # Именем кнопки для удаления будет являться id пользователя

            edit_push_button.clicked.connect(self.edit_author_push_button)
            delete_push_button.clicked.connect(self.delete_author_push_button)

            item_layout = QHBoxLayout()
            item_layout.addWidget(name_author)
            item_layout.addWidget(separator_name)
            item_layout.addWidget(text_info)
            item_layout.addWidget(separator_info)
            item_layout.addWidget(edit_push_button)
            item_layout.addWidget(delete_push_button)
            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self.ui.Widget_authors.addItem(item)
            self.ui.Widget_authors.setItemWidget(item, item_widget)

    # Метод для получения списка авторов из БД по параметрам (если параметры не переадются то, поиск происход по всем авторам )    
    def get_list_of_authors(self, param=None, value=None):
        connection = None
        cursor = None
        authors = []

        try:
            connection = mysql.connector.connect(
                host="sql12.freesqldatabase.com",
                user="sql12749774",
                password="kmYMIq9h6G",
                database="sql12749774"  # Имя базы данных
            )

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                # Формируем SQL-запрос в зависимости от наличия параметров фильтрации
                
                if param == "info":
                    query = f"SELECT * FROM Authors WHERE {param} LIKE %s;"
                    cursor.execute(query, (f'%{value}%',))  # Добавляем символы подстановки
                elif param and value:
                    query = f"SELECT * FROM Authors WHERE {param} = %s;"
                    cursor.execute(query, (value,))
                else:
                    cursor.execute("SELECT * FROM Authors;")

                # Получаем все результаты при помощи fetchall
                authors = cursor.fetchall()
                print("Авторы получены.")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return authors

    # КНопки для взаимодействия с авторами на окне авторов
    # Кнопка для редактирования (функция знает id автораM открывает окно для изменения данных)
    def edit_author_push_button(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
        print(F"Кнопка редкатирования автора с ID{push_button.objectName()}")

        # Создаём новое окно MainWindow для редактирования информации о авторе
        # self.edit_window = EditAuthorWindow(str(push_button.objectName()))
        # self.edit_window.show()
        
        # Создаём окно Widget для редактирования информации о авторе
        # Передаем в окно себя и id автора
        self.edit_author_widget = EditAuthorWidget(self, str(push_button.objectName()))
        self.edit_author_widget.show()
    
    # Кнопка для удаления автора (функция знает id автора)
    def delete_author_push_button(self):
        sender = self.sender()
        push_button = self.findChild(QPushButton, sender.objectName())
  
        # print(F"Кнопка удаления автора с ID{push_button.objectName()}")

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

                query = f"DELETE FROM Authors WHERE ID_Author = %s;"
                cursor.execute(query, (push_button.objectName(),))

                print(f"Пользователь удалён. {push_button.objectName()}")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.commit()
                connection.close()

        
        # После удаления автора обновляем список
        # Получаем список всех авторов, так как не передаем параметры
        list_of_authors = self.get_list_of_authors()

        # Передаем список авторов для добавления авторов на окно
        self.loading_authors_from_the_database_to_page(list_of_authors)

    def search_authors_with_param(self):
        
        # Получаем данные из параметров поиска
        value_text = self.ui.line_edit_author_param.text()
        value_param = self.ui.combo_box_authors.currentText()
        
        print(1)

        if value_param == "Имя":
            current_param = "first_name"
        elif value_param == "Фамилия":
            current_param = "last_name"
        elif value_param == "Отчество":
            current_param = "middle_name"
        elif value_param == "Дополнительная информация":
            current_param = "info"
        elif value_param == "Сброс параметров": # Если выбра элемент "Сброс параметров"
            value_param = None
            current_param = None
            self.ui.line_edit_author_param.clear()
            

        
        # print(value_text)
        # print(value_param)
        # value_text = str(value_text).lower()
        # print(value_text)

        info = self.get_list_of_authors(current_param, value_text)
        self.loading_authors_from_the_database_to_page(info)

    # Метод добавление к БД
    def add_article_to_db(self):
        pass

    # Метод загрузки авторов в combo box с авторами на странице статей
    def load_authors_to_combo_box_article(self):

        # Поолучаем список всех авторов из БД
        all_authors = self.get_list_of_authors()
        # print(all_authors)

        # Массив для хранения информации авторов
        arr_data_aithors = []

        # Добавляем в массив данные
        for author in all_authors:
            data_author = []
            name_author = str(author[1]) + " " + str(author[2])
            id_author = str(author[0])
            data_author.append(name_author)
            data_author.append(id_author)
            arr_data_aithors.append(data_author)
        
        # print(arr_data_aithors)

        # Создание модели
        model = QtGui.QStandardItemModel(0, 1)

        for author in arr_data_aithors:
            item = QtGui.QStandardItem(author[0]) # Устанавливаем данные для элемента
            item.setData(author[1])  # Устанавливаем данные для элемента
            model.appendRow(item)
            
        # Установка модели в QComboBox
        self.ui.combo_box_authors_article.setModel(model)


    # Создание БД
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

class EditAuthorWindow(QtWidgets.QMainWindow, Ui_EditAuthorWindow):
    def __init__(self, id_author):
        super(EditAuthorWindow, self).__init__()
        self.ui = Ui_EditAuthorWindow()
        self.ui.setupUi(self)
        self.author_id = id_author


        # Вызываем метод для запроса данный о пользоватеде по id из БД 
        info = self.get_info_about_author()

        # Устанавливаем стартовые значениея текущих данных из БД
        self.ui.edit_author_first_name.setText(str(info[1]))
        self.ui.edit_author_last_name.setText(str(info[2]))
        self.ui.edit_author_middle_name.setText(str(info[3]))
        self.ui.edit_author_info.setPlainText(str(info[4]))

        # Подключаем кнопку для сохранения(изменения) информации
        self.ui.putton_edit_author_save.clicked.connect(self.save_changes_info_author)

        # Установление фиксированного размеа окна
        self.setFixedSize(500, 380)
    
    # Метод для получения данных по текущем авторе
    def get_info_about_author(self):
        try:
            connection = mysql.connector.connect(
                host="sql12.freesqldatabase.com",
                user="sql12749774",
                password="kmYMIq9h6G",
                database="sql12749774"  # Имя базы данных
            )

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                query = f"SELECT * FROM Authors WHERE ID_Author = %s;"
                cursor.execute(query, (self.author_id,))
    

                # Получаем все результаты при помощи fetchone
                authors = cursor.fetchone()
                print("Автор получен.")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return authors
        
    def save_changes_info_author(self):
        try:
            connection = mysql.connector.connect(
                host="sql12.freesqldatabase.com",
                user="sql12749774",
                password="kmYMIq9h6G",
                database="sql12749774"  # Имя базы данных
            )   

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()
                print(0)
                # Получаем данные из полей
                new_first_name = str(self.ui.edit_author_first_name.text())
                new_last_name = str(self.ui.edit_author_last_name.text())
                new_middle_name = str(self.ui.edit_author_middle_name.text())
                new_info = str(self.ui.edit_author_info.toPlainText())
                print(1)

                # Запрос на обновление данных
                query = """
                    UPDATE Authors 
                    SET first_name = %s, last_name = %s, middle_name = %s, info = %s 
                    WHERE ID_Author = %s
                """
                data = (new_first_name, new_last_name, new_middle_name, new_info, self.author_id)

                cursor.execute(query, data)
                connection.commit()  # Сохраняем изменения в базе данных

                print("Данные изменены.")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

class EditArticleWindow(QtWidgets.QMainWindow, Ui_EditArticleWindow):
    def __init__(self):
        super(EditArticleWindow, self).__init__()
        self.ui = Ui_EditArticleWindow()
        self.ui.setupUi(self)

class EditAuthorWidget(QWidget, Ui_Form):
    def __init__(self, main_window, id_author):
        super().__init__()
        self.ui = Ui_Form()  
        self.ui.setupUi(self)  

        self.main_window = main_window
        self.id_author = id_author
        
        # Подключаем нопку
        self.ui.putton_edit_author_save.clicked.connect(self.save_author_info)

        # self.ui.edit_author_first_name.setText(str(self.id_author))

        # Вызываем метод для запроса данный о пользоватеде по id из БД 
        info = self.get_info_about_author()

        # Устанавливаем стартовые значениея текущих данных из БД
        self.ui.edit_author_first_name.setText(str(info[1]))
        self.ui.edit_author_last_name.setText(str(info[2]))
        self.ui.edit_author_middle_name.setText(str(info[3]))
        self.ui.edit_author_info.setPlainText(str(info[4]))

        # Подключаем кнопку к методу
        # self.ui.someButton.clicked.connect(self.call_main_method)  # Замените 'someButton' на фактическое имя кнопки

    # Метод для сохранения изменений и обновления данных в списке авторов
    def save_author_info(self):

        # # Получаем список всех авторов, так как не передаем параметры
        # list_of_authors = self.get_list_of_authors()

        # # Передаем список авторов для добавления авторов на окно
        # self.loading_authors_from_the_database_to_page(list_of_authors)

        # Метод для изменени данных об авторе
        self.change_info_abot_author()

        # Получаем список всех авторов, так как не передаем параметры
        list_of_authors = self.main_window.get_list_of_authors()

        # Передаем список авторов для добавления авторов на окно
        self.main_window.loading_authors_from_the_database_to_page(list_of_authors)

        self.close()
    
    # Метод для получения данных о автора по его id
    def get_info_about_author(self):
        try:
            connection = mysql.connector.connect(
                host="sql12.freesqldatabase.com",
                user="sql12749774",
                password="kmYMIq9h6G",
                database="sql12749774"  # Имя базы данных
            )

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                query = f"SELECT * FROM Authors WHERE ID_Author = %s;"
                cursor.execute(query, (self.id_author,))
    

                # Получаем все результаты при помощи fetchone
                authors = cursor.fetchone()
                print("Автор получен.")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return authors

    # Метод для изменения данных автора в БД
    def change_info_abot_author(self):
        try:
            connection = mysql.connector.connect(
                host="sql12.freesqldatabase.com",
                user="sql12749774",
                password="kmYMIq9h6G",
                database="sql12749774"  # Имя базы данных
            )   

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                # Получаем данные из полей
                new_first_name = str(self.ui.edit_author_first_name.text())
                new_last_name = str(self.ui.edit_author_last_name.text())
                new_middle_name = str(self.ui.edit_author_middle_name.text())
                new_info = str(self.ui.edit_author_info.toPlainText())

                # Запрос на обновление данных
                query = """
                    UPDATE Authors 
                    SET first_name = %s, last_name = %s, middle_name = %s, info = %s 
                    WHERE ID_Author = %s
                """
                data = (new_first_name, new_last_name, new_middle_name, new_info, self.id_author)

                cursor.execute(query, data)
                connection.commit()  # Сохраняем изменения в базе данных

                print("Данные изменены.")

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

    # app = QtWidgets.QApplication(sys.argv)
    # window = EditAuthorWindow()
    # window.show()
    # sys.exit(app.exec_())

    # app = QtWidgets.QApplication(sys.argv)
    # window = EditArticleWindow()
    # window.show()
    # sys.exit(app.exec_())

