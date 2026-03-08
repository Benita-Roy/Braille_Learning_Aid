# Braille Learning Aid

An adaptive Braille learning system designed to help visually impaired students learn Braille characters using tactile feedback, audio guidance, and speech recognition.  

The system teaches Braille characters in batches, evaluates learners through voice input, and dynamically adjusts practice using an adaptive learning algorithm.

---

# Overview

This project integrates:

- Braille character output (for tactile learning)
- Speech recognition for student responses
- Audio feedback for reinforcement
- Adaptive testing algorithms
- SQLite database for progress tracking

The goal is to create a learning system that adapts to the learner’s progress and focuses on characters that require more practice.

---

# System Architecture

```
                +-------------------+
                |      main.py      |
                |   learning flow   |
                +---------+---------+
                          |
        +-----------------+------------------+
        |                                    |
+-------v--------+                    +-------v--------+
| character      |                    | speech         |
| generator      |                    | recognition    |
|                |                    | speech.py      |
+-------+--------+                    +-------+--------+
        |                                     |
        |                                     |
+-------v--------+                    +-------v--------+
| audio feedback |                    | adaptive algo  |
| audioTest.py   |                    | adaptive_algo  |
+-------+--------+                    +-------+--------+
        |                                     |
        +----------------+--------------------+
                         |
                 +-------v--------+
                 | SQLite Database|
                 | learning.db    |
                 | data.py        |
                 +----------------+
```

---

# Learning Flow

## Teaching Phase

Characters are introduced in small batches.

Example batch:

```
[a, b, c, d, e]
```

For each character:

1. The Braille pattern is generated.
2. The system plays the pronunciation of the character.
3. The student touches the Braille representation.
4. The system pauses to allow memorization.

---

## Adaptive Testing Phase

After teaching a batch, the system tests the learner.

1. A Braille character is displayed.
2. The student speaks the character aloud.
3. The speech recognition model predicts the spoken letter.
4. The system provides audio feedback.
5. Performance statistics are updated in the database.

Characters with lower mastery scores are tested more frequently.

---

# Features

## Braille Pattern Generation

The system generates the 6-dot Braille representation of characters.

Example mapping:

```
a → [1,0,0,0,0,0]
b → [1,1,0,0,0,0]
c → [1,0,0,1,0,0]
```

Handled by:

```
character_generator.py
```

---

## Speech Recognition

Student responses are captured through a microphone and classified using a neural network.

Model structure:

```
CNN → CNN → LSTM → Attention → Classifier
```

Implemented in:

```
speech.py
```

Libraries used:

- PyTorch
- Librosa
- NumPy
- SoundDevice

---

## Audio Feedback

The system provides reinforcement using audio.

Correct answer:

```
rightAnswer.wav
```

Incorrect answer:

```
feedbackSpeech.wav
```

Handled by:

```
audioTest.py
```

---

## Adaptive Learning Algorithm

The adaptive system determines which character should be tested next.

Factors considered:

- mastery score
- number of correct attempts
- number of incorrect attempts

Goal:

Focus more practice on characters that the learner struggles with.

Implemented in:

```
adaptive_algo.py
```

---

## Student Progress Tracking

Student progress is stored in an SQLite database.

Database tables include:

### Students

```
student_id
name
```

### Character Progress

```
student_id
character
visited
mastery
```

### Character Statistics

```
student_id
character
correct_count
incorrect_count
```

Handled by:

```
data.py
```

---

# File Structure

```
braille-learning-aid/

main.py
speech.py
adaptive_algo.py
character_generator.py
audioTest.py
data.py
batches.py
master_test.py

learning.db

sounds/
    A.wav
    B.wav
    ...
    Z.wav
    rightAnswer.wav
    feedbackSpeech.wav
```

---

# Module Description

## main.py

Controls the overall learning pipeline.

Responsibilities:

- teaching characters
- running adaptive tests
- coordinating system modules

---

## speech.py

Handles speech recognition.

Functions include:

- microphone recording
- audio preprocessing
- spectrogram generation
- neural network prediction

---

## adaptive_algo.py

Implements adaptive character selection based on student performance.

---

## character_generator.py

Generates Braille patterns for characters and prepares them for hardware output.

---

## audioTest.py

Plays audio prompts and feedback sounds.

---

## data.py

Handles database operations:

- database initialization
- storing student progress
- updating performance statistics

---

## batches.py

Defines learning batches of characters.

Example:

```
[a,b,c,d,e]
[f,g,h,i,j]
[k,l,m,n,o]
[p,q,r,s,t]
[u,v,w,x,y,z]
```

---

## master_test.py

Runs a final evaluation test after all characters are learned.

Purpose:

Measure overall Braille recognition accuracy.

---

# Installation

Clone the repository:

```
git clone <repository-url>
cd braille-learning-aid
```

Install dependencies:

```
pip install torch librosa numpy sounddevice keyboard
```

---

# Setup Audio Files

Create a folder:

```
sounds/
```

Add pronunciation files:

```
A.wav
B.wav
C.wav
...
Z.wav
rightAnswer.wav
feedbackSpeech.wav
```

---

# Database Initialization

Run once to create the database:

```python
import data
data.initialize_database()
```

---

# Running the Program

Start the learning system:

```
python main.py
```

---

# Hardware Integration (Future Work)

The system is designed to integrate with a refreshable Braille display controlled by Arduino.

Current output example:

```
a [1,0,0,0,0,0]
```

Future implementation will send data using serial communication:

```
Python → Serial → Arduino → Braille actuators
```

---

# Future Improvements

Possible extensions:

- multi-student support
- physical refreshable Braille display
- improved speech recognition models
- student progress analytics
- teacher dashboard

---

# Project Goal

The aim of this project is to develop an accessible Braille learning system that:

- reinforces tactile learning
- provides instant audio feedback
- adapts to the learner’s pace
- reduces dependency on constant teacher supervision

The long-term objective is to create an affordable learning tool for visually impaired students.

---

# License

This project is intended for educational and research purposes.
