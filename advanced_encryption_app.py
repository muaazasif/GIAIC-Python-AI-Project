import streamlit as st
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
import base64
import os

# Helper to derive key from password
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Page setup
st.set_page_config(page_title="🛡️ Advanced Encryption System", layout="centered")
st.title("🛡️ Advanced Data Encryption System")

# Input password for encryption key
password = st.text_input("🔑 Enter Encryption Password", type="password")
salt = st.session_state.get("salt", os.urandom(16))  # Generate a new salt if not in session
st.session_state["salt"] = salt  # Persist salt in session

if password:
    key = derive_key(password, salt)
    fernet = Fernet(key)

    # Choose mode
    mode = st.radio("Select Mode", ["Encrypt Text", "Decrypt Text", "Encrypt File", "Decrypt File"])

    if mode == "Encrypt Text":
        plain_text = st.text_area("Enter text to encrypt")
        if st.button("Encrypt"):
            encrypted = fernet.encrypt(plain_text.encode()).decode()
            st.success("🔐 Encrypted Text")
            st.code(encrypted)

    elif mode == "Decrypt Text":
        encrypted_text = st.text_area("Paste encrypted text")
        if st.button("Decrypt"):
            try:
                decrypted = fernet.decrypt(encrypted_text.encode()).decode()
                st.success("🔓 Decrypted Text")
                st.code(decrypted)
            except:
                st.error("❌ Invalid decryption or wrong password.")

    elif mode == "Encrypt File":
        uploaded_file = st.file_uploader("Choose a file to encrypt", type=None)
        if uploaded_file and st.button("Encrypt and Download"):
            encrypted_data = fernet.encrypt(uploaded_file.read())
            st.download_button("📦 Download Encrypted File", encrypted_data, file_name="encrypted.dat")

    elif mode == "Decrypt File":
        uploaded_file = st.file_uploader("Upload encrypted file", type=None)
        if uploaded_file and st.button("Decrypt and Download"):
            try:
                decrypted_data = fernet.decrypt(uploaded_file.read())
                st.download_button("📄 Download Decrypted File", decrypted_data, file_name="decrypted_output")
            except:
                st.error("❌ Invalid decryption or file mismatch.")

    # Export Key + Salt
    with st.expander("📁 Export/Import Key"):
        st.code(f"Salt (hex): {salt.hex()}")
        st.warning("⚠️ Save this salt securely! You'll need it to derive the same key from the password.")

else:
    st.info("Enter a password to begin encryption/decryption.")
