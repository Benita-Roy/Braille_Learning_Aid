# Braille_Learning_Aid

An **adaptive, interactive Braille learning system** designed to help visually challenged learners master Braille characters through tactile feedback, voice interaction, and data-driven personalization.

The system combines **Arduino-based Braille display hardware** with **Python-based adaptive learning software** to ensure efficient and personalized learning outcomes.

---

## 🚀 Key Features

- **Tactile Braille Display** using Arduino-controlled pins
- **Voice-based interaction** for instruction and assessment
- **Adaptive learning algorithm** based on learner performance
- **Batch-wise teaching and testing** (A–Z split into manageable groups)
- **Persistent progress tracking** using SQLite
- **Mastery-based progression** (no blind repetition)
- **Final non-adaptive evaluation (Master Test)**

---

## 🧠 System Overview

The system operates in three major phases:

1. **Teaching Phase**
   - Each Braille character is taught **only once**
   - Character is displayed on the Braille hardware
   - Audio feedback announces the character
   - Character is marked as *visited* in the database

2. **Adaptive Testing Phase**
   - Characters are tested repeatedly until mastery is achieved
   - An adaptive algorithm prioritizes:
     - Low mastery characters
     - High error-rate characters
     - Ensures exploration (no starvation)
   - Learner responses are evaluated using speech classification

3. **Master Test Phase**
   - One-time comprehensive evaluation
   - Covers **all characters (A–Z)**
   - No learning or database updates
   - Used purely for performance assessment

---

## 🗂️ Project Structure

```text
.
├── main.py        # Main control flow (teaching + adaptive testing)
├── adaptive_algo.py        # Weighted adaptive character selection logic
├── data.py                 # Database schema & progress management
├── batches.py              # Character batch definitions (A–Z)
├── master_test.py          # Final non-adaptive evaluation
├── learning.db             # SQLite database (auto-generated)
│
├── character_generator.py  # Arduino Braille display interface
├── speech_classifier.py    # Speech recognition & classification
├── feedback.py             # Audio/voice feedback module
│
└── README.md
