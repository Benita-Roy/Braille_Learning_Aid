# master_test.py
# --------------------------------------------------
# Final evaluation module.
# This test is NON-adaptive and NON-learning.
# It evaluates overall character recognition
# after training is complete.
# --------------------------------------------------

import random
import sqlite3
import os
import character_generator as gen
import speech_classifier as speech
import feedback

# Absolute DB path
DB_PATH = os.path.join(os.path.dirname(__file__), "learning.db")


def fetch_all_characters(student_id):
    """
    Fetch all characters associated with the student.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT character
        FROM character_progress
        WHERE student_id = ?
        ORDER BY character
    """, (student_id,))

    chars = [row[0] for row in cur.fetchall()]
    conn.close()
    return chars


def test_character_once(student_id, character):
    """
    Test a single character ONCE.
    Does NOT update mastery or stats.
    Returns True if correct, False otherwise.
    """

    gen.char_display_uno(character)

    # wait for student input
    while not button_pressed():
        pass

    # record and classify speech
    # NOTE: confidence threshold handled inside record_audio()
    return speech.record_audio()


def test_all(student_id="student_001"):
    """
    Master test across all characters.
    """

    print("\n===== MASTER TEST STARTED =====\n")

    characters = fetch_all_characters(student_id)
    random.shuffle(characters)

    total = len(characters)
    correct = 0
    results = {}

    for char in characters:
        print(f"Testing character: {char}")

        is_correct = test_character_once(student_id, char)
        results[char] = is_correct

        if is_correct:
            correct += 1
            feedback.correct()
        else:
            feedback.incorrect(char)

    accuracy = correct / total if total > 0 else 0.0

    print("\n===== MASTER TEST COMPLETED =====")
    print(f"Total characters tested : {total}")
    print(f"Correct responses       : {correct}")
    print(f"Accuracy                : {accuracy:.2f}")

    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "per_character": results
    }
