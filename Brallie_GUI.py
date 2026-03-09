import streamlit as st
import sqlite3
import main

# ---------------------------------
# GLOBAL VARIABLE (imported by main)
# ---------------------------------
student_id = None


# ---------------------------------
# SESSION STATE
# ---------------------------------
if "student_id" not in st.session_state:
    st.session_state.student_id = None


# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------
conn = sqlite3.connect("learning.db")
cursor = conn.cursor()


st.title("Student Login System")

menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])


# ---------------------------------
# LOGIN
# ---------------------------------
if menu == "Login":

    st.subheader("Login")

    student_id_input = st.text_input("Student ID")

    if st.button("Login"):

        cursor.execute(
            "SELECT * FROM students WHERE student_id=?",
            (student_id_input,)
        )

        result = cursor.fetchone()

        if result:
            st.session_state.student_id = result[0]

            # update global variable
            student_id = result[0]

            st.success(f"Welcome {result[1]}")

        else:
            st.error("Student ID not found")


# ---------------------------------
# SIGN UP
# ---------------------------------
if menu == "Sign Up":

    st.subheader("Create Account")

    student_id_input = st.text_input("Student ID")
    name = st.text_input("Name")

    if st.button("Sign Up"):

        cursor.execute(
            "SELECT * FROM students WHERE student_id=?",
            (student_id_input,)
        )

        if cursor.fetchone():
            st.error("Student ID already exists")

        else:
            cursor.execute(
                "INSERT INTO students VALUES (?,?)",
                (student_id_input, name)
            )

            conn.commit()

            st.success("Signup successful!")


# ---------------------------------
# STORE CURRENT STUDENT
# ---------------------------------
if st.session_state.student_id:
    student_id = st.session_state.student_id

    st.sidebar.success(f"Logged in as: {student_id}")
    main.running_main(student_id)