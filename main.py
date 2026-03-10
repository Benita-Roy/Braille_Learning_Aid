import time
import streamlit as st

from batches import BATCHES
import character_generator as gen
from speech import predict_letter_from_mic
from audioTest import feedback_sound, teach_char_sound
import data
import adaptive_algo as adapt


# -------------------------------
# Teaching phase
# -------------------------------
def teach_batch(student_id, batch):

    for character in batch:

        if not st.session_state.get("learning_active", False):
            return

        if not data.visited_char(student_id, character):

            teach(character)
            data.mark_visited(student_id, character)


def teach(character):

    gen.char_display_uno(character)

    teach_char_sound(character)

    time.sleep(10)


# -------------------------------
# Adaptive testing phase
# -------------------------------
def test(student_id, character):

    if not st.session_state.get("learning_active", False):
        return

    gen.char_display_uno(character)

    letter, confidence = predict_letter_from_mic()

    print(letter.upper(), confidence)
    print("\n")

    check = feedback_sound(character, letter)

    if check:
        data.record_correct(student_id, character)
    else:
        data.record_incorrect(student_id, character)

    data.recompute_mastery(student_id, character)


# -------------------------------
# Mastery checks
# -------------------------------
def mastery_char(student_id, character):
    return data.mastery_char(student_id, character)


def mastery_batch(student_id, batch):

    for character in batch:
        if not mastery_char(student_id, character):
            return False

    return True


def visited_char(student_id, character):
    return data.visited_char(student_id, character)


def visited_batch(student_id, batch):

    for character in batch:
        if not visited_char(student_id, character):
            return False

    return True


# -------------------------------
# MAIN PROGRAM FLOW
# -------------------------------
def running_main(student_id):

    data.initialize_database()

    for batch in BATCHES:

        if not st.session_state.get("learning_active", False):
            break

        if not visited_batch(student_id, batch):
            teach_batch(student_id, batch)

        while not mastery_batch(student_id, batch):

            if not st.session_state.get("learning_active", False):
                return

            char_to_test = adapt.wtd_random_select(student_id, batch)

            test(student_id, char_to_test)

    print("Session completed")
