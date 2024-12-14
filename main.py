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

        # Установление маски для ввода даты создания статьи
        self.ui.line_edit_data_article.setInputMask('0000-00-00;_')
    
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

        # Проверка корректности данных, Валидация данных
        errors = []

        if not first_name:
            errors.append('Необходимо указать имя автора.')
        if not last_name:
            errors.append('Необходимо указать фамилию автора.')
        if not middle_name:
            errors.append('Необходимо указать отчество автора.')
        if not info_about_author:
            errors.append('Необходимо ввести дополнительные данные об авторе.')

        if len(first_name) < 2:
            errors.append(f'Имя не может состоять из {len(first_name)} символа (символов).')
        if len(last_name) < 2:
            errors.append(f'Фамилия не может состоять из {len(last_name)} символа (символов).')
        if len(middle_name) < 5:
            errors.append(f'Отчество не может состоять из {len(middle_name)} символа (символов).')

        # Если возникла ошибка
        if errors:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("Ошибка")
            message_box.setText("\n".join(errors))
            message_box.exec_()
            return
        
        # Проверка сохранения данных
        # print(first_name, last_name, middle_name, info_about_author, end='\n')

        connection = None
        cursor = None
        try:
            connection = connect(
                host="sql7.freesqldatabase.com",
                user="sql7751998",
                password="7kPDaYU2TX",
                database="sql7751998" # Имя базы данных
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
            connection = connect(
                host="sql7.freesqldatabase.com",
                user="sql7751998",
                password="7kPDaYU2TX",
                database="sql7751998" # Имя базы данных
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
                host="sql7.freesqldatabase.com",
                user="sql7751998",
                password="7kPDaYU2TX",
                database="sql7751998" # Имя базы данных
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
    
    # Метод добавление статьи в БД
    def add_article_to_db(self):

        # Получаем выбранного автора
        text = self.ui.combo_box_authors_article.currentText()

        # Из текстовой информации делаем массив с именем и фамилией
        arr_info_about_current_author = text.split()

        first_name = arr_info_about_current_author[0]
        last_name = arr_info_about_current_author[1]
        middle_name = arr_info_about_current_author[2]
        first_name = str(first_name)
        last_name = str(last_name)
        middle_name = str(middle_name)

        # Получение id автора
        id_author_for_articel = self.get_author_id_with_first_last_middle_name(first_name, last_name, middle_name)

        # Получение данных из полей ввода для статьи
        name_articel = self.ui.line_edit_name_article.text()
        data_articel = self.ui.line_edit_data_article.text() 
        science_articel = self.ui.line_edit_scince_article.text()
        text_article = self.ui.text_edit_text_article.toPlainText()

        # Валмдация данных
        # Валидация даты
        if not self.validate_date(data_articel):
            QMessageBox.warning(self, "Ошибка", "Введите корректную дату в формате ГГГГ-ММ-ДД или РЕАЛЬНУЮ дату")
            self.ui.line_edit_data_article.clear()  # Очищаем поле ввода
            return
        elif not name_articel:
            QMessageBox.warning(self, "Ошибка", "Введите навзание статьи")
            return
        elif not science_articel:
            QMessageBox.warning(self, "Ошибка", "Введите навзание науки")
            return
        elif not text_article:
            QMessageBox.warning(self, "Ошибка", "Введите текст статьи")
            return
        elif len(name_articel) >= 255:
            QMessageBox.warning(self, "Ошибка", "Введите навзание стать меньеше 255 символов")
            return
        elif len(science_articel) >= 255:
            QMessageBox.warning(self, "Ошибка", "Введите навзание науки меньше 255 символов")
            return
        

        # Добавляем статью в БД
        connection = None
        cursor = None
        try:
            connection = connect(
                host="sql7.freesqldatabase.com",
                user="sql7751998",
                password="7kPDaYU2TX",
                database="sql7751998" # Имя базы данных
            )

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                cursor.execute("""INSERT INTO Articles (name, date_create, science, text_article)
                VALUES (%s, %s, %s, %s); """, (name_articel, data_articel, science_articel, text_article))

                print("Статья добавлена")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.commit()
                connection.close()

        # После добавления статьи очищаем поля ввода
        self.ui.line_edit_name_article.clear()
        self.ui.line_edit_data_article.clear()
        self.ui.line_edit_scince_article.clear()
        self.ui.text_edit_text_article.clear()

        # Связываем статью с выбранным пользователем
        id_article = self.get_id_article_with_name_date_science_text(name_articel, data_articel, science_articel, text_article)
        
        self.connect_author_and_article_in_db(id_author_for_articel, id_article)

        # Проверка даных для статьи
        # print(id_author_for_articel)
        # print(name_articel)
        # print(data_articel)
        # print(science_articel)
        # print(text_article)

        # Проверка
        # print(arr_info_about_current_author) 
        # print(text)

    # Метод загрузки авторов в combo box с авторами на странице статей
    def load_authors_to_combo_box_article(self):

        # Убираем старые элементы 
        self.ui.combo_box_authors_article.clear()

        # Поолучаем список всех авторов из БД
        all_authors = self.get_list_of_authors()

        arr_authors = []

        for author in all_authors:
            el_author = author[1] + " " + author[2] + " " + author[3]
            arr_authors.append(el_author)
        
        # Добавляем авторов в combobox
        self.ui.combo_box_authors_article.addItems(arr_authors)        

        # print(all_authors)
        # print(arr_authors)

    # Получение автора по его ФИО
    def get_author_id_with_first_last_middle_name(self, first, last, middle):
        connection = None
        cursor = None

        try:
            connection = connect(
                host="sql7.freesqldatabase.com",
                user="sql7751998",
                password="7kPDaYU2TX",
                database="sql7751998" # Имя базы данных
            )

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                # Формируем SQL-запрос по параметрам

                query = f"SELECT * FROM Authors WHERE first_name = %s AND last_name = %s AND middle_name = %s"
                cursor.execute(query, (first, last, middle),)

                # Получаем все результаты при помощи fetchall
                authors = cursor.fetchone()
                
                author_id = authors[0]

                print("Автор получен.")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return author_id
    
    # Получение id статьи по её данным
    def get_id_article_with_name_date_science_text(self, name, date, science, text):
        # Получаем id статьи по её данным
        connection = None
        cursor = None
        try:
            connection = connect(
                host="sql7.freesqldatabase.com",
                user="sql7751998",
                password="7kPDaYU2TX",
                database="sql7751998" # Имя базы данных
            )

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                cursor.execute("""SELECT * FROM Articles WHERE name = %s AND date_create = %s AND science = %s AND text_article = %s""", (name, date, science, text))
                articles = cursor.fetchone()
                articles_id = articles[0]
                # print(articles)
                # print("Статья получена")

                return articles_id

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.commit()
                connection.close()
    
    # Соединение автора со статьеё
    def connect_author_and_article_in_db(self, id_author, id_article):
        connection = None
        cursor = None
        try:
            connection = connect(
                host="sql7.freesqldatabase.com",
                user="sql7751998",
                password="7kPDaYU2TX",
                database="sql7751998" # Имя базы данных
            )

            if connection.is_connected():
                print("Успешное подключение")
                cursor = connection.cursor()

                cursor.execute("""INSERT INTO Authors_Articles (ID_Author,  ID_Article) 
                VALUES (%s, %s); """, (id_author, id_article))
                print("Автор и Статья подключены")

        except Error as e:
            print(f"Ошибка подключения: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.commit()
                connection.close()

    # Загрузка статей из БД на страницу статей
    def load_articles_from_db_to_page_articles(self):
        pass

    # Проверка корректоности даты на странице статей 
    def validate_date(self, date_string):
        # Проверяем, что строка имеет длину 10 символов (формат ГГГГ-ММ-ДД)
        if len(date_string) != 10:
            return False

        year = date_string[:4]
        month = date_string[5:7]
        day = date_string[8:]

        # Проверка даты
        # print(year)
        # print(month)
        # print(day)

        # Проверка года
        if int(year) >= 1000:
            # print(1)
            # Проверка месяца
            if int(month) >= 1 and int(month) <= 12:
                # Проверка дня
                if int(day) >= 1 and int(day) <= 31:
                    # Дополнительная проверка на количество дней в месяце
                    if month in ['04', '06', '09', '11'] and int(day) == 31:
                        return False  # Апрель, Июнь, Сентябрь, Ноябрь имеют максимум 30 дней
                    if month == '02':
                        # Проверка на високосный год
                        if (int(year) % 4 == 0 and int(year) % 100 != 0) or (int(year) % 400 == 0):
                            if int(day) > 29:
                                return False
                        else:
                            if int(day) > 28:
                                return False
                    return True

        return False

    # Создание БД
    def create_db(self):
        connection = None
        cursor = None
        try:
            connection = connect(
                host="sql7.freesqldatabase.com",
                user="sql7751998",
                password="7kPDaYU2TX",
                database="sql7751998" # Имя базы данных
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
            connection = connect(
                host="sql7.freesqldatabase.com",
                user="sql7751998",
                password="7kPDaYU2TX",
                database="sql7751998" # Имя базы данных
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
            connection = connect(
                host="sql7.freesqldatabase.com",
                user="sql7751998",
                password="7kPDaYU2TX",
                database="sql7751998" # Имя базы данных
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

