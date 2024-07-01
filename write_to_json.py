import fitz
import json

def extract_text_with_details(pdf_path, output_file):
    doc = fitz.open(pdf_path)
    output_text = []
    print("Performing")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for b in blocks:
            if "lines" in b: 
                # output_text.append(b)   
                for l in b["lines"]:
                    # continue
                    output_text.append(l)
                    # for s in l["spans"]:
                    #     output_text.append(s)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_text, f, indent=4)

# Example usage
pdf_path = "test.pdf"
output_file = "wood_easy_details.json"
extract_text_with_details(pdf_path, output_file)
