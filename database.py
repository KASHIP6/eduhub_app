# database.py
import sqlite3

def create_tables():
    conn = sqlite3.connect('eduhub.db')
    cursor = conn.cursor()

    # Create users table for login and registration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL  -- 'admin', 'student', 'faculty'
        )
    ''')

    # Create other tables (students, faculty, courses, exams, finances)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            course_id INTEGER,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            exam_date TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            amount REAL NOT NULL,
            payment_date TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    ''')

    # Insert a default admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ('admin', 'admin123', 'admin'))

    conn.commit()
    conn.close()

# Call this function to create tables when the app starts
create_tables()