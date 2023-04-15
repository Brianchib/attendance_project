import sqlite3

con = sqlite3.connect("../attendance_db.sqlite")
cur = con.cursor()


create_user_data_table = "create table userdata (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username VARCHAR(100) NOT NULL, password VARCHAR(100) NOT NULL);"
insert_user_data = (
    "insert into userdata (username, password) values ('admin', 'admin');"
)
create_student_table = "create table student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name VARCHAR(100) NOT NULL, index_number VARCHAR(100) NOT NULL);"
create_attendance_table = "create table attendance (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name VARCHAR(100) NOT NULL, index_number VARCHAR(100) NOT NULL, time DATETIME NOT NULL, present VARCHAR(10), course_code VARCHAR(10), course_date DATE );"

cur.execute(create_user_data_table)
cur.execute(insert_user_data)
cur.execute(create_student_table)
cur.execute(create_attendance_table)
con.commit()
