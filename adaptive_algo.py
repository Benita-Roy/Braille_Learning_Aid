# adaptive_algo.py
# --------------------------------------------------
# This module contains adaptive selection logic.
# It decides WHICH character to test next based on:
#   - mastery score
#   - correct / incorrect history
# It does NOT modify database state.
# --------------------------------------------------

import sqlite3
import random
import os

# Absolute DB path (same strategy as data.py)
DB_PATH = os.path.join(os.path.dirname(__file__), "learning.db")


# --------------------------------------------------
# Fetch learner statistics for a given batch
# --------------------------------------------------
def fetch_batch_stats(student_id, batch):
    """
    Fetch mastery and performance statistics for all
    characters in the given batch.

    Returns a list of tuples:
    (character, mastery, correct_count, incorrect_count)
    """

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    placeholders = ",".join("?" * len(batch))

    cur.execute(f"""
        SELECT 
            cp.character,
            cp.mastery,
            cs.correct_count,
            cs.incorrect_count
        FROM character_progress cp
        JOIN character_stats cs
            ON cp.student_id = cs.student_id
            AND cp.character = cs.character
        WHERE cp.student_id = ?
          AND cp.character IN ({placeholders})
    """, (student_id, *batch))

    rows = cur.fetchall()
    conn.close()

    return rows


# --------------------------------------------------
# Adaptive weighted random selection
# --------------------------------------------------
def wtd_random_select(student_id, batch):
    """
    Selects the next character to test using
    weighted random sampling.

    Weight is influenced by:
      - error rate (more mistakes => higher weight)
      - low mastery (lower mastery => higher weight)
      - small exploration constant to avoid starvation
    """

    rows = fetch_batch_stats(student_id, batch)

    characters = []
    weights = []

    for character, mastery, correct, incorrect in rows:
        total_attempts = correct + incorrect

        # error rate emphasizes mistakes
        error_rate = incorrect / (total_attempts + 1)

        # mastery penalty emphasizes low mastery
        mastery_penalty = 1.0 - mastery

        # final weight (tunable but stable defaults)
        weight = (
            0.6 * error_rate +
            0.4 * mastery_penalty +
            0.05    # exploration floor
        )

        characters.append(character)
        weights.append(weight)

    # fallback safety (should never happen)
    if not characters:
        return random.choice(batch)

    # weighted random choice
    return random.choices(characters, weights=weights, k=1)[0]
