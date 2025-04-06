import os
import PyPDF2
from .path_stuff import make_abs

def get_pdfs(pdf_location: str):
    dir = os.listdir(pdf_location)
    original_dir = os.getcwd()
    os.chdir(pdf_location)
    pdf_files = [item for item in dir if item.endswith(".pdf")]
    pdf_files = make_abs(pdf_files)
    os.chdir(original_dir)
    return pdf_files

def is_valid_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            PyPDF2.PdfReader(f)
        return True
    except PyPDF2.errors.PdfReadError:
        return False

def combine_pdfs(pdf_list, output_filename, output_path):
    pdf_merger = PyPDF2.PdfMerger()
    dir = os.getcwd()
    os.chdir(output_path)

    for pdf_file in sorted(pdf_list):
        if not is_valid_pdf(pdf_file):
            print(f"Skipping invalid PDF file: {pdf_file}")
            continue

        pdf_merger.append(pdf_file)
    if not output_filename.endswith(".pdf"):
        output_filename += ".pdf"
    
    with open(output_filename, 'wb') as f:
        pdf_merger.write(f)
    os.chdir(dir)
    return output_filename