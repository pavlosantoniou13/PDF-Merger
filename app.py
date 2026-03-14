import streamlit as st
from pypdf import PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

# Function to create a divider page
def create_divider_page(title):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(width / 2, height / 2, title)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- Streamlit UI ---
st.set_page_config(page_title="PDF Merger", layout="centered")
st.title("📄 PDF Divider & Merger")
st.write("Each file uploaded will have its own divider page placed directly in front of it.")

# 1. File Uploader
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.subheader("Edit Divider Titles")
    
    # Using a dictionary or list to ensure order is preserved
    titles = []
    for i, file in enumerate(uploaded_files):
        default_val = f"Part {i+1}" 
        user_title = st.text_input(f"Divider for {file.name}:", value=default_val, key=f"title_{i}")
        titles.append(user_title)

    # 3. Execution Button
    if st.button("Merge PDFs with Dividers", type="primary"):
        merger = PdfMerger()
        
        try:
            with st.spinner("Merging..."):
                # We use the length of uploaded_files to drive the loop
                for pdf_file, title in zip(uploaded_files, titles):
                    
                    merger.append(create_divider_page(title))
                    pdf_file.seek(0)
                    merger.append(pdf_file)

                output = io.BytesIO()
                merger.write(output)
                merger.close()
                output.seek(0)
            st.download_button(
                label="📥 Download Interleaved PDF",
                file_name="merged_document.pdf",
                mime="application/pdf",
                data=output,
                use_container_width=True
            )
        
        except Exception as e:
            st.error(f"Logic Error: {e}")