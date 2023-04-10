from PyQt5 import QtSql

db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("attendance_db.sqlite")

if not db.open():
    print("Database connection Error")

user_data_query = QtSql.QSqlQuery()
user_data_query.exec_("create table userdata (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username VARCHAR(100) NOT NULL, password VARCHAR(100) NOT NULL);")
user_data_query.exec_("insert into userdata (username, password) values ('admin', 'admin');")
user_data_query.exec_("select * from userdata")
user_data_query.first()
print(user_data_query.value("username"), user_data_query.value("password"))


create_student_query = QtSql.QSqlQuery()
create_student_query.exec_("create table student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name VARCHAR(100) NOT NULL, index_number INTEGER NOT NULL);")


create_attendance_table = QtSql.QSqlQuery()
create_attendance_table.exec_("create table attendance (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name VARCHAR(100) NOT NULL, index_number INTEGER NOT NULL, time DATETIME NOT NULL, present BOOLEAN, course_code VARCHAR(10), course_date DATE );")
