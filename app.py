
import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import numpy as np
from fpdf import FPDF
import tempfile
import os

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Document Scanner",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Document Scanner App")
st.write(
    "Upload a document image, convert it to black & white like Adobe Scan, "
    "then download it as a PDF."
)

# -----------------------------------
# FILE UPLOAD
# -----------------------------------
uploaded_file = st.file_uploader(
    "Upload a document image",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------------
# IMAGE PROCESSING FUNCTION
# -----------------------------------
def process_document(image):
    # Convert to grayscale
    gray = ImageOps.grayscale(image)

    # Increase sharpness
    sharp = gray.filter(ImageFilter.SHARPEN)

    # Convert to numpy array
    img_array = np.array(sharp)

    # Adaptive threshold effect
    threshold = 150
    bw = np.where(img_array > threshold, 255, 0)

    # Convert back to image
    processed = Image.fromarray(np.uint8(bw))

    return processed

# -----------------------------------
# PDF CREATION FUNCTION
# -----------------------------------
def create_pdf(image):
    temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    image.save(temp_img.name)

    pdf = FPDF()
    pdf.add_page()

    # A4 dimensions
    pdf_w = 210
    pdf_h = 297

    pdf.image(temp_img.name, x=0, y=0, w=pdf_w, h=pdf_h)

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_pdf.name)

    return temp_pdf.name

# -----------------------------------
# MAIN APP
# -----------------------------------
if uploaded_file is not None:

    original_image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(original_image, use_container_width=True)

    if st.button("✨ Scan Document"):

        with st.spinner("Processing document..."):

            # Process image
            scanned_image = process_document(original_image)

            st.subheader("Scanned Black & White Image")
            st.image(scanned_image, use_container_width=True)

            # Create PDF
            pdf_path = create_pdf(scanned_image)

            # Download PDF
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_file,
                    file_name="scanned_document.pdf",
                    mime="application/pdf"
                )

            # Cleanup
            os.remove(pdf_path)

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")
st.caption("Built with Streamlit • Adobe Scan Style Document Converter")
