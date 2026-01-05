import sqlite3
import string
import os

# Absolute path to avoid accidental multiple DB files
DB_PATH = os.path.join(os.path.dirname(__file__), "learning.db")

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # ---------------------------
    # Students table
    # ---------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)

    # ---------------------------
    # Character progress table
    # ---------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS character_progress (
        student_id TEXT NOT NULL,
        character TEXT NOT NULL,
        visited INTEGER NOT NULL DEFAULT 0,
        mastery REAL NOT NULL DEFAULT 0.0,

        PRIMARY KEY (student_id, character),
        FOREIGN KEY (student_id) REFERENCES students(student_id)
    )
    """)

    # ---------------------------
    # Character stats table (NEW)
    # ---------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS character_stats (
        student_id TEXT NOT NULL,
        character TEXT NOT NULL,
        correct_count INTEGER NOT NULL DEFAULT 0,
        incorrect_count INTEGER NOT NULL DEFAULT 0,

        PRIMARY KEY (student_id, character),
        FOREIGN KEY (student_id) REFERENCES students(student_id)
    )
    """)

    # ---------------------------
    # Default student
    # ---------------------------
    student_id = "student_001"
    student_name = "Default Student"

    cursor.execute("""
    INSERT OR IGNORE INTO students (student_id, name)
    VALUES (?, ?)
    """, (student_id, student_name))

    # ---------------------------
    # Initialize A–Z for progress + stats
    # ---------------------------
    characters = [(student_id, char) for char in string.ascii_lowercase]

    cursor.executemany("""
    INSERT OR IGNORE INTO character_progress (student_id, character)
    VALUES (?, ?)
    """, characters)

    cursor.executemany("""
    INSERT OR IGNORE INTO character_stats (student_id, character)
    VALUES (?, ?)
    """, characters)

    conn.commit()
    conn.close()


def view_students():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    print("\nSTUDENTS TABLE")
    print("-" * 30)
    for row in rows:
        print(row)

    conn.close()

def view_character_progress(student_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if student_id:
        cursor.execute("""
        SELECT student_id, character, visited, mastery
        FROM character_progress
        WHERE student_id = ?
        ORDER BY character
        """, (student_id,))
    else:
        cursor.execute("""
        SELECT student_id, character, visited, mastery
        FROM character_progress
        ORDER BY student_id, character
        """)

    rows = cursor.fetchall()

    print("\nCHARACTER PROGRESS TABLE")
    print("-" * 50)
    for row in rows:
        print(row)

    conn.close()

def view_character_stats(student_id=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if student_id:
        cursor.execute("""
        SELECT student_id, character, correct_count, incorrect_count
        FROM character_stats
        WHERE student_id = ?
        ORDER BY character
        """, (student_id,))
    else:
        cursor.execute("""
        SELECT student_id, character, correct_count, incorrect_count
        FROM character_stats
        ORDER BY student_id, character
        """)

    rows = cursor.fetchall()

    print("\nCHARACTER STATS TABLE")
    print("-" * 50)
    for row in rows:
        print(row)

    conn.close()

def mark_visited(student_id, character):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE character_progress
        SET visited = 1
        WHERE student_id = ? AND character = ?
    """, (student_id, character))

    conn.commit()
    conn.close()

def visited_char(student_id, character):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT visited
        FROM character_progress
        WHERE student_id = ? AND character = ?
    """, (student_id, character))

    row = cur.fetchone()
    conn.close()

    return bool(row and row[0] == 1)

def record_correct(student_id, character):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE character_stats
        SET correct_count = correct_count + 1
        WHERE student_id = ? AND character = ?
    """, (student_id, character))

    conn.commit()
    conn.close()

def record_incorrect(student_id, character):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE character_stats
        SET incorrect_count = incorrect_count + 1
        WHERE student_id = ? AND character = ?
    """, (student_id, character))

    conn.commit()
    conn.close()

def recompute_mastery(student_id, character):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT correct_count, incorrect_count
        FROM character_stats
        WHERE student_id = ? AND character = ?
    """, (student_id, character))

    correct, incorrect = cur.fetchone()
    total = correct + incorrect

    mastery = correct / total if total > 0 else 0.0

    cur.execute("""
        UPDATE character_progress
        SET mastery = ?
        WHERE student_id = ? AND character = ?
    """, (mastery, student_id, character))

    conn.commit()
    conn.close()

def mastery_char(student_id, character, threshold=0.7):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT mastery
        FROM character_progress
        WHERE student_id = ? AND character = ?
    """, (student_id, character))

    row = cur.fetchone()
    conn.close()

    return bool(row and row[0] >= threshold)


#i initialised this in the main_modified file just in case ig thats the right way, do remember to maybe delete the learning.db file while actually running the pgm for evaluation
initialize_database()
view_students()
view_character_progress()
view_character_stats()

