import streamlit as st
import qrcode
from PIL import Image
import base64

st.set_page_config(page_title="QR Code Reader", layout="wide")

# ---------------------------------------------------------
# SCRAMBLING AND UNSCRAMBLING LOGIC
# ---------------------------------------------------------
def scramble_text(text, shift=3):
    """Scramble text by shifting characters."""
    scrambled = "".join(chr((ord(char) + shift) % 256) for char in text)
    return scrambled

def unscramble_text(text, shift=3):
    """Unscramble text by reversing the character shift."""
    unscrambled = "".join(chr((ord(char) - shift) % 256) for char in text)
    return unscrambled

# ---------------------------------------------------------
# QR CODE READER LOGIC
# ---------------------------------------------------------
def decode_qr_code(image):
    """Decode the QR code and extract the data."""
    try:
        qr = qrcode.QRCode()
        decoded_data = qr.decode(image)
        return decoded_data
    except Exception as e:
        st.error(f"Failed to decode QR code: {e}")
        return None

# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------
st.title("📱 QR Code Reader and Puzzle Solution Decoder")

# Upload QR Code
uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display the uploaded QR code image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded QR Code", use_column_width=True)

    # Decode the QR code
    qr_data = decode_qr_code(image)
    if qr_data:
        st.success("QR Code decoded successfully!")
        st.write("Scrambled Data from QR Code:")
        st.code(qr_data)

        # Extract scrambled puzzle solution and password
        try:
            data_lines = qr_data.split("\n")
            scrambled_solution = data_lines[0].split(": ")[1]
            qr_password = data_lines[1].split(": ")[1]

            # Ask for password to unscramble
            st.write("Enter the password to unscramble the puzzle solution:")
            entered_password = st.text_input("Password", type="password")

            if st.button("Unscramble Solution"):
                if entered_password == qr_password:
                    unscrambled_solution = unscramble_text(scrambled_solution)
                    st.success("Puzzle Solution Unscrambled Successfully!")
                    st.write(f"The puzzle solution is: {unscrambled_solution}")
                else:
                    st.error("Incorrect password! Please try again.")
        except Exception as e:
            st.error(f"Failed to process QR code data: {e}")
