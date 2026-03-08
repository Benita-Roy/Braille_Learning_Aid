import winsound
import time

def feedback_sound(actual_character, answer_character):

    actual_character = actual_character.upper()
    answer_character = answer_character.upper()

    if actual_character == answer_character:
        winsound.PlaySound("sounds/rightAnswer.wav", winsound.SND_FILENAME)
        return True
    else:
        winsound.PlaySound("sounds/feedbackSpeech.wav", winsound.SND_FILENAME)
        time.sleep(0.7)
        winsound.PlaySound(f"sounds/{actual_character}.wav", winsound.SND_FILENAME)
        return False

def teach_char_sound(character):
    filename = f"sounds/{character.upper()}.wav"
    winsound.PlaySound(filename, winsound.SND_FILENAME) 
    
