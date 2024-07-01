import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path, output_txt_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text("text")
    
    with open(output_txt_path, 'w', encoding='utf-8') as file:
        file.write(text)


def extract_with_blocks(pdf_path, output_txt_path):
    num = 223
    with open(output_txt_path, 'w', encoding='utf-8') as file:
        document = fitz.open(pdf_path)
        # text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:
                block_text = ""
                line_text = ""
                line_dict = []
                if "lines" in b:
                    for  l in b["lines"]:
                        for s in l["spans"]: 
                            block_text += s["text"]
                            line_text += s["text"]
                            s_dict = {"text" :s["text"], "font": s["font"]}
                            line_dict.append(s_dict)
                        line_text += "\n"
                block_text += "\n\n"
                # file.write(block_text)
                puzzle_num = block_text.split(".")[0]
                if puzzle_num.isdigit() :
                    puzzle = int(puzzle_num)
                    if (puzzle == num or (puzzle < num + 5 and num > 100)): 
                        file.write(line_text+ "\n\n")
                        num = puzzle
                        num +=1







pdf_path = 'test.pdf'
output_txt_path = 'wood_easy_to_text.txt'
# extract_text_from_pdf(pdf_path, output_txt_path)
extract_with_blocks(pdf_path, output_txt_path)


