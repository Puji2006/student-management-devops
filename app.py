import streamlit as st
import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "password"),
        database=os.getenv("DB_NAME", "student_db")
    )

st.set_page_config(page_title="Student Management System")
st.title("🎓 Student Management System")

menu = st.sidebar.selectbox("Menu", ["Add Student", "View Students", "Delete Student"])

if menu == "Add Student":
    st.subheader("Add a New Student")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    course = st.text_input("Course")

    if st.button("Add Student"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, age, course) VALUES (%s, %s, %s)",
            (name, age, course)
        )
        conn.commit()
        cursor.close()
        conn.close()
        st.success(f"Student '{name}' added successfully!")

elif menu == "View Students":
    st.subheader("All Students")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if rows:
        st.table(rows)
    else:
        st.info("No students found.")

elif menu == "Delete Student":
    st.subheader("Delete a Student")
    student_id = st.number_input("Student ID to delete", min_value=1, step=1)
    if st.button("Delete"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        cursor.close()
        conn.close()
        st.success(f"Student ID {student_id} deleted.")
