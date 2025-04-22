# streamlit_app.py

import streamlit as st

# Set page config
st.set_page_config(page_title="Universal Unit Converter 🌍", layout="centered")

# Title
st.title("🔄 Universal Unit Converter")

# Category and Units
unit_map = {
    "Temperature 🌡️": ["Celsius", "Fahrenheit", "Kelvin"],
    "Length 📏": ["Meters", "Feet", "Inches"],
    "Weight ⚖️": ["Kilograms", "Pounds", "Grams"]
}

# Conversion function
def convert_value(category, from_unit, to_unit, value):
    try:
        val = float(value)
    except ValueError:
        return "❌ Invalid number"
    
    # Temperature
    if category == "Temperature 🌡️":
        if from_unit == "Celsius":
            if to_unit == "Fahrenheit":
                return val * 9/5 + 32
            elif to_unit == "Kelvin":
                return val + 273.15
        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                return (val - 32) * 5/9
            elif to_unit == "Kelvin":
                return (val - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                return val - 273.15
            elif to_unit == "Fahrenheit":
                return (val - 273.15) * 9/5 + 32

    # Length
    elif category == "Length 📏":
        meters = {"Meters": 1, "Feet": 0.3048, "Inches": 0.0254}
        base = val * meters[from_unit]
        return base / meters[to_unit]

    # Weight
    elif category == "Weight ⚖️":
        kilograms = {"Kilograms": 1, "Pounds": 0.453592, "Grams": 0.001}
        base = val * kilograms[from_unit]
        return base / kilograms[to_unit]

    return val  # Same unit

# Select category
category = st.selectbox("Choose Category", list(unit_map.keys()))

# Show unit selectors
units = unit_map[category]
from_unit = st.selectbox("From Unit", units, key="from_unit")
to_unit = st.selectbox("To Unit", units, key="to_unit")

# Input value
value = st.text_input("Enter Value")

# Perform conversion
if st.button("Convert"):
    if not value:
        st.warning("Please enter a value.")
    else:
        result = convert_value(category, from_unit, to_unit, value)
        st.success(f"Converted Value: {result} {to_unit}")
