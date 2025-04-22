import streamlit as st
import datetime
import os
import random

st.set_page_config(page_title="Growth Mind Challenge 🌱", layout="centered")

# File paths
CHALLENGE_FILE = "daily_challenges.txt"
JOURNAL_FILE = "journal_entries.txt"

# Title
st.title("🌟 Growth Mind Challenge")

# XP system
if "xp" not in st.session_state:
    st.session_state.xp = 0

# Load or create daily challenges
def load_daily_challenges():
    today = datetime.date.today().isoformat()  # Get today's date
    challenges_for_today = []

    # If challenge file exists, load data
    if os.path.exists(CHALLENGE_FILE):
        with open(CHALLENGE_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Find today's challenges from the file
        for line in lines:
            if line.startswith(today):  # Check if the challenge is for today
                challenges_for_today = line.strip().split("|")[1:]
                break  # We only need today's challenges, no need to check further

    if not challenges_for_today:  # If no challenges for today, generate new ones
        all_challenges = [
            "GYM 💪", "Read 10 pages 📖", "Drink 2L Water 💧", "Plan your day in the morning 📝",
            "Clear your email inbox 📬", "Focus on 1 deep work task 🧠", "Take a 10-minute break every 90 mins ⏳",
            "Give positive feedback to someone 🙌", "Learn something new for 15 mins 🎓", "Avoid social media for 4 hours 🚫📱",
            "Reflect on your top 3 wins today 🏆", "Update your professional portfolio 🌐", "Network with a colleague or mentor 🤝",
            "Track how you spent your time today ⏱️", "Prepare tomorrow’s priority list 📋"
        ]
        
        # Randomly select 5 challenges for the day
        challenges_for_today = random.sample(all_challenges, 5)

        # Save today's challenges to the file
        with open(CHALLENGE_FILE, "a", encoding="utf-8") as f:
            f.write(f"{today}|{'|'.join(challenges_for_today)}\n")

    return challenges_for_today

# Save journal entry
def save_journal_entry(entry):
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.date.today()}] {entry}\n")

# Load today's reflections
def get_reflections():
    today = datetime.date.today().isoformat()
    if not os.path.exists(JOURNAL_FILE):
        return []
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.startswith(f"[{today}]")]

# Section: Daily Challenges
st.header("🏆 Today's Challenges")
daily_challenges = load_daily_challenges()

completed = 0
for challenge in daily_challenges:
    if st.checkbox(challenge, key=challenge):  # Key to make sure the checkbox is unique
        completed += 1

st.write(f"✅ Completed {completed} of {len(daily_challenges)} challenges")
st.write(f"🌟 XP: {completed * 10}")

# Section: General Daily Reflection
st.subheader("📝 General Daily Reflection")
general_reflection = st.text_area("Write a thought or reflection for today")

if st.button("Save General Reflection"):
    if general_reflection.strip():
        save_journal_entry(f"General: {general_reflection}")
        st.success("Reflection saved!")
    else:
        st.warning("Please write something before saving.")

# Section: Reflection History
st.subheader("📚 Reflection History")
reflections = get_reflections()
if reflections:
    for r in reflections:
        st.write(r)
else:
    st.info("No reflections written today yet.")

# Section: Add a New Challenge
st.subheader("➕ Add a New Challenge")
new_challenge = st.text_input("Add a new challenge to today's list")

if st.button("Add Challenge"):
    if new_challenge.strip():
        today = datetime.date.today().isoformat()
        updated_lines = []
        found = False
        if os.path.exists(CHALLENGE_FILE):
            with open(CHALLENGE_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(today):
                        line = line.strip() + f"|{new_challenge}\n"
                        found = True
                    updated_lines.append(line)
        if not found:
            updated_lines.append(f"{today}|{new_challenge}\n")
        with open(CHALLENGE_FILE, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
        st.success("Challenge added! Please refresh the page to see it.")
    else:
        st.warning("Please enter a challenge.")
