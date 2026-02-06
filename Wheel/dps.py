import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode

st.set_page_config(page_title="QR Code Decoder", layout="wide")
#v1.1
# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------
st.title("🔓 QR Code Decoder for Puzzle Solution")

# Upload QR Code
uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display the uploaded QR code image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded QR Code", width=300)

    # Decode the QR code
    try:
        decoded_data = decode(image)
        if decoded_data:
            qr_data = decoded_data[0].data.decode("utf-8")
            st.success("QR Code decoded successfully!")
            st.write("Data from QR Code:")
            st.code(qr_data)

            # Extract hashed phrase and code
            try:
                data_lines = qr_data.split("\n")
                hashed_phrase = data_lines[0].split(": ")[1]
                qr_code = data_lines[1].split(": ")[1]

                # Ask for 4-digit code to verify
                st.write("Enter the 4-digit code to decode the puzzle solution:")
                entered_code = st.text_input("Code", type="password")

                if st.button("Decode Solution"):
                    if entered_code == qr_code:
                        st.success("Code verified successfully!")
                        st.write(f"The hashed phrase is: {hashed_phrase}")
                        st.info("Note: The original phrase cannot be retrieved from the hash directly.")
                    else:
                        st.error("Incorrect code! Unable to decode the solution.")
            except Exception as e:
                st.error(f"Failed to process QR code data: {e}")
        else:
            st.error("No QR code detected in the uploaded image.")
    except Exception as e:
        st.error(f"Failed to decode QR code: {e}")
