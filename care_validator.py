
import streamlit as st
import fitz  # fitz
import pandas as pd
import re
import io

# Function to extract care instructions from a PDF file
def extract_care_instructions(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    care_text = ""
    for page in doc:
        text = page.get_text()
        match = re.search(r"Machine wash cold.*?dry clean\.", text, re.DOTALL)
        if match:
            care_text = match.group(0).strip()
            break
    return care_text

# Streamlit UI
st.title("Care Instruction Validator")
st.write("Upload label artwork PDFs to extract and validate care instructions.")

uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    results = []
    for file in uploaded_files:
        care_text = extract_care_instructions(file)
        status = "✅ Valid" if care_text else "❌ Missing"
        results.append({
            "File Name": file.name,
            "Care Instructions": care_text,
            "Validation Status": status
        })

    df = pd.DataFrame(results)
    st.dataframe(df)

    # Option to download results
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    st.download_button("Download Results as Excel", data=output.getvalue(), file_name="care_instructions.xlsx")
