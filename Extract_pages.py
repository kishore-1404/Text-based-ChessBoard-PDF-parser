import fitz  # PyMuPDF

def extract_pages(input_pdf, output_pdf, start_page, end_page):
    doc = fitz.open(input_pdf)
    output_doc = fitz.open()
    
    for page_num in range(start_page - 1, min(end_page, len(doc))):
        output_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    
    output_doc.save(output_pdf)
    output_doc.close()
    doc.close()

# Example usage
input_pdf = "wood.pdf"
output_pdf = "int_sol.pdf"
start_page = 249
end_page = 345
extract_pages(input_pdf, output_pdf, start_page, end_page )

print(f"Pages {start_page} to {end_page} have been extracted and saved to {output_pdf}")