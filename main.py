# main.py
import streamlit as st
import sqlite3
from database import create_tables

# Custom CSS for styling (swapped colors)
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #585E6C;  /* Steel Blue Gray */
        color: #B5BBC9;  /* Cool Gray */
    }}
    .stButton>button {{
        background-color: #B5BBC9;  /* Cool Gray */
        color: #585E6C;  /* Steel Blue Gray */
    }}
    .stTextInput>div>div>input {{
        background-color: #585E6C;  /* Steel Blue Gray */
        color: #B5BBC9;  /* Cool Gray */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize database tables
create_tables()

# Function to check login credentials
def check_login(username, password):
    conn = sqlite3.connect('eduhub.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Login Page
def login_page():
    st.title("EDUHUB: Comprehensive College Management System")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = check_login(username, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['username'] = user[1]
            st.session_state['role'] = user[3]
            st.session_state['page'] = 'main'  # Redirect to main page
            st.success(f"Welcome, {user[1]}!")
        else:
            st.error("Invalid username or password")

# Main Application
def main_app():
    st.title("EDUHUB: Comprehensive College Management System")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    if st.session_state['role'] == 'admin':
        menu = st.sidebar.radio("Choose a module", ["Admin", "Student", "Faculty", "Examination", "Finance", "Reports"])
    elif st.session_state['role'] == 'student':
        menu = st.sidebar.radio("Choose a module", ["Student"])
    elif st.session_state['role'] == 'faculty':
        menu = st.sidebar.radio("Choose a module", ["Faculty"])

    if menu == "Admin":
        st.header("Admin Module")
        st.subheader("Manage Users, Courses, and Departments")

        # Add a new course
        st.write("Add a new course:")
        course_name = st.text_input("Course Name")
        department = st.text_input("Department")
        if st.button("Add Course"):
            conn = sqlite3.connect('eduhub.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO courses (name, department) VALUES (?, ?)", (course_name, department))
            conn.commit()
            conn.close()
            st.success("Course added successfully!")

    elif menu == "Student":
        st.header("Student Module")
        st.subheader("Course Registration and Attendance Tracking")

        # Student registration
        st.write("Register a new student:")
        student_name = st.text_input("Student Name")
        student_email = st.text_input("Student Email")
        course_id = st.number_input("Course ID", min_value=1)
        if st.button("Register Student"):
            conn = sqlite3.connect('eduhub.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, email, course_id) VALUES (?, ?, ?)", (student_name, student_email, course_id))
            conn.commit()
            conn.close()
            st.success("Student registered successfully!")

    elif menu == "Faculty":
        st.header("Faculty Module")
        st.subheader("Class Schedule and Performance Evaluation")

        # Add a new faculty member
        st.write("Add a new faculty member:")
        faculty_name = st.text_input("Faculty Name")
        faculty_email = st.text_input("Faculty Email")
        faculty_department = st.text_input("Department")

        if st.button("Add Faculty"):
            conn = sqlite3.connect('eduhub.db')
            cursor = conn.cursor()

            # Check if the email already exists
            cursor.execute("SELECT * FROM faculty WHERE email = ?", (faculty_email,))
            if cursor.fetchone():
                st.error("A faculty member with this email already exists. Please use a different email.")
            else:
                # Insert the new faculty member
                cursor.execute("INSERT INTO faculty (name, email, department) VALUES (?, ?, ?)", (faculty_name, faculty_email, faculty_department))
                conn.commit()
                st.success("Faculty added successfully!")

            conn.close()

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'  # Default to login page

# Page Navigation
if st.session_state['page'] == 'login':
    login_page()
elif st.session_state['page'] == 'main':
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        main_app()
    else:
        st.session_state['page'] = 'login'  # Redirect to login if not logged in