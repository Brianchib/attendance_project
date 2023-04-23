# Import the sqlite3 module
import sqlite3

# Connect to the 'attendance_db.sqlite' database using the sqlite3.connect() method.
con = sqlite3.connect("../attendance_db.sqlite")

# Create a cursor object using the connection object
cur = con.cursor()

# Define SQL statements to create three database tables: 'userdata', 'student', and 'attendance'
create_user_data_table = "create table userdata (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username VARCHAR(100) NOT NULL, password VARCHAR(100) NOT NULL);"
create_student_table = "create table student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name VARCHAR(100) NOT NULL, index_number VARCHAR(100) NOT NULL);"
create_attendance_table = "create table attendance (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name VARCHAR(100) NOT NULL, index_number VARCHAR(100) NOT NULL, time DATETIME NOT NULL, present VARCHAR(10), course_code VARCHAR(10), course_date DATE );"

# Define an SQL statement to insert a row of data into the 'userdata' table
insert_user_data = "insert into userdata (username, password) values ('admin', 'admin');"

# Execute the SQL statements to create the three tables and insert a row of data into the 'userdata' table.
cur.execute(create_user_data_table)
cur.execute(insert_user_data)
cur.execute(create_student_table)
cur.execute(create_attendance_table)

# Save the changes made to the database
con.commit()