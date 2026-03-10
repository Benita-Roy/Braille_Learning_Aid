import streamlit as st
import sqlite3
import pandas as pd
import main

# ---------------------------------
# SESSION STATE
# ---------------------------------
if "student_id" not in st.session_state:
    st.session_state.student_id = None

if "learning_active" not in st.session_state:
    st.session_state.learning_active = False

# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------
conn = sqlite3.connect("learning.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------------------------
# PAGE TITLE
# ---------------------------------
st.title("Braille Learning System")

# ---------------------------------
# MENU
# ---------------------------------
menu = st.sidebar.selectbox(
    "Menu",
    ["Student Login", "Teacher Login", "Sign Up"]
)

# =====================================================
# STUDENT LOGIN
# =====================================================
if menu == "Student Login":

    st.header("Student Login")

    student_id_input = st.text_input("Student ID")

    if st.button("Login"):

        cursor.execute(
            "SELECT * FROM students WHERE student_id=?",
            (student_id_input,)
        )

        result = cursor.fetchone()

        if result:
            st.session_state.student_id = result[0]
            st.success(f"Welcome {result[1]}")
        else:
            st.error("Student ID not found")

# ---------------------------------
# STUDENT SESSION CONTROL
# ---------------------------------
if st.session_state.student_id:

    student_id = st.session_state.student_id
    st.sidebar.success(f"Logged in as: {student_id}")

    st.sidebar.markdown("### Student Session Control")

    if st.sidebar.button("Start Learning"):
        st.session_state.learning_active = True

    if st.sidebar.button("End Session"):
        st.session_state.learning_active = False
        st.warning("Learning session ended")

    if st.session_state.learning_active:
        st.success("Learning Session Running...")
        main.running_main(student_id)

# =====================================================
# SIGN UP
# =====================================================
if menu == "Sign Up":

    st.header("Create Student Account")

    student_id_input = st.text_input("Student ID")
    name = st.text_input("Name")

    if st.button("Create Account"):

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

# =====================================================
# TEACHER DASHBOARD
# =====================================================
if menu == "Teacher Login":

    st.header("Teacher Dashboard")

    password = st.text_input("Teacher Password", type="password")

    if password == "teacher123":

        st.success("Teacher Login Successful")

        cursor.execute("SELECT student_id, name FROM students")
        students = cursor.fetchall()

        if len(students) == 0:
            st.warning("No students found in database")

        else:

            student_list = [f"{s[0]} - {s[1]}" for s in students]

            selected = st.selectbox(
                "Select Student",
                student_list
            )

            student_id = selected.split(" - ")[0]

            # ---------------------------------
            # CHARACTER PERFORMANCE
            # ---------------------------------
            st.subheader("Character Performance")

            query = """
            SELECT character, correct_count, incorrect_count
            FROM character_stats
            WHERE student_id = ?
            """

            df = pd.read_sql_query(query, conn, params=(student_id,))

            if not df.empty:
                df_plot = df.set_index("character")
                st.bar_chart(df_plot)

            # ---------------------------------
            # MASTERY GRAPH
            # ---------------------------------
            st.subheader("Mastery Score")

            query = """
            SELECT character, mastery, visited
            FROM character_progress
            WHERE student_id = ?
            """

            mastery_df = pd.read_sql_query(query, conn, params=(student_id,))

            if not mastery_df.empty:

                mastery_df = mastery_df.set_index("character")

                st.line_chart(mastery_df[["mastery"]])

            # ---------------------------------
            # OVERALL PERFORMANCE
            # ---------------------------------
            st.subheader("Overall Performance")

            total_correct = df["correct_count"].sum()
            total_incorrect = df["incorrect_count"].sum()

            overall_df = pd.DataFrame(
                {
                    "Result": ["Correct", "Incorrect"],
                    "Count": [total_correct, total_incorrect],
                }
            )

            st.bar_chart(overall_df.set_index("Result"))

            # ---------------------------------
            # WEAK CHARACTERS
            # ---------------------------------
            st.subheader("Characters Student Struggles With")

            weak = mastery_df[
                (mastery_df["mastery"] < 0.7) &
                (mastery_df["visited"] == 1)
            ]

            weak_display = weak.drop(columns=["visited"])

            if weak_display.empty:
                st.success("Student has no weak characters")
            else:
                st.dataframe(weak_display, use_container_width=True)

    else:
        if password:
            st.error("Incorrect Teacher Password")
