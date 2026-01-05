# designed as single student as of now modify it later for multiple students

import time
from batches import BATCHES
import character_generator as gen
import speech_classifier as speech
import feedback
import data
import adaptive_algo as adapt
import master_test as master


############ FOR NOW THE ONLY STUDENT IS STUDENT_001 ##################
#--------------------------------------------------------------------#

student_id = 'student_001'


# -------------------------------
# Teaching phase (ONLY once per character)
# -------------------------------
def teach_batch(student_id, batch):
    for character in batch:
        # teach only if the character has never been visited
        if not data.visited_char(student_id, character):
            teach(character)
            data.mark_visited(student_id, character)


def teach(character):
    # display braille character on hardware
    gen.char_display_uno(character)

    # speak the character aloud
    speech.speak_char(character)

    # wait for student to process / memorize
    time.sleep(10)


# -------------------------------
# Adaptive testing phase
# -------------------------------
def test(student_id, character):
    # display the character to be tested
    gen.char_display_uno(character)

    # wait until the student presses the input button
    # NOTE: button_pressed() will come from hardware module
    while not button_pressed():
        pass

    # record student's spoken response
    # record_audio() should internally:
    #  - capture audio
    #  - run classifier
    #  - return True/False based on confidence threshold
    check = speech.record_audio()

    if check:
        # student answered correctly
        data.record_correct(student_id, character)
        feedback.correct()
    else:
        # student answered incorrectly
        data.record_incorrect(student_id, character)
        feedback.incorrect(character)

    # recompute mastery AFTER updating stats
    data.recompute_mastery(student_id, character)


# -------------------------------
# Mastery checks
# -------------------------------
def mastery_char(student_id, character):
    # check if mastery >= threshold (default 0.7)
    return data.mastery_char(student_id, character)


def mastery_batch(student_id, batch):
    for character in batch:
        if not mastery_char(student_id, character):
            return False
    return True


def visited_char(student_id, character):
    # check if character has ever been taught
    return data.visited_char(student_id, character)


def visited_batch(student_id, batch):
    for character in batch:
        if not visited_char(student_id, character):
            return False
    return True


# -------------------------------
# MAIN PROGRAM FLOW
# -------------------------------
if __name__ == "__main__":
    
    data.initialize_database()
    # iterate through predefined character batches
    for batch in BATCHES:

        # STEP 1: Teaching phase
        # teach only characters that have never been visited
        if not visited_batch(student_id, batch):
            teach_batch(student_id, batch)

        # STEP 2: Adaptive practice phase
        # adaptive algorithm controls which character is tested next
        while not mastery_batch(student_id, batch):
            char_to_test = adapt.wtd_random_select(student_id, batch)
            test(student_id, char_to_test)

    # STEP 3: Final comprehensive evaluation
    # tests all characters across all batches
    master.test_all()

