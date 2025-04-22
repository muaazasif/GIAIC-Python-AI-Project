import streamlit as st
import re

# Set page configuration
st.set_page_config(page_title="🔐 Password Strength Meter", layout="centered")

# Title
st.title("🔐 Password Strength Meter")

# Password input
password = st.text_input("Enter your password", type="password")

# Password strength check function
def check_strength(pw):
    if not pw:
        return "Please enter a password."

    length = len(pw)
    has_lower = bool(re.search(r"[a-z]", pw))
    has_upper = bool(re.search(r"[A-Z]", pw))
    has_digit = bool(re.search(r"\d", pw))
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", pw))

    score = sum([has_lower, has_upper, has_digit, has_special])

    if length < 6:
        return "❌ Too short (min 6 characters)"
    elif score == 1:
        return "⚠️ Very Weak"
    elif score == 2:
        return "🔒 Weak"
    elif score == 3:
        return "🔐 Strong"
    elif score == 4 and length >= 8:
        return "✅ Very Strong"
    else:
        return "🔐 Strong"

# Evaluate password
if password:
    strength = check_strength(password)
    st.info(f"Strength: **{strength}**")
