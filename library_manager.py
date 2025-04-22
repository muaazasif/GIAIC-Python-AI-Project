import streamlit as st
import pandas as pd
import os

# Set up page
st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")
st.title("📚 Personal Library Manager")

# Load or create library CSV
library_file = "library_data.csv"
if os.path.exists(library_file):
    df = pd.read_csv(library_file)
else:
    df = pd.DataFrame(columns=["Title", "Author", "Status"])
    df.to_csv(library_file, index=False)

# Form to add new book
with st.form("Add New Book"):
    st.subheader("➕ Add a Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    status = st.selectbox("Reading Status", ["Want to Read", "Currently Reading", "Read"])
    submitted = st.form_submit_button("Add to Library")

    if submitted:
        if title and author:
            new_entry = pd.DataFrame([[title, author, status]], columns=["Title", "Author", "Status"])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(library_file, index=False)
            st.success(f"📘 '{title}' by {author} added!")
        else:
            st.warning("Please provide both title and author.")

# Filter section
st.subheader("📖 Your Library")
status_filter = st.selectbox("Filter by Status", ["All"] + df["Status"].unique().tolist())
if status_filter != "All":
    filtered_df = df[df["Status"] == status_filter]
else:
    filtered_df = df

st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
