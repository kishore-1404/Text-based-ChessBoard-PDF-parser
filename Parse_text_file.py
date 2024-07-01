import fitz #PyMuPDF

def parse_pdf_to_text(pdf_path, output_file):

    puzzle_num = []
    to_move = []
    # Open the PDF file
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                line = ""
                for  l in b["lines"]:
                    for s in l["spans"]:
                        if s["font"] == "Tunga":
                            puzzle_num.append(s["text"])
                        elif s["font"] == "Wingdings3":
                            if s["text"] == "\uf071":
                                to_move.append("Black to Move")
                            elif s["text"] == "\uf072":
                                to_move.append("White to Move")

    with open(output_file, "w", encoding="utf-8") as f:
        # Iterate through each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            blocks = page.get_text("dict")["blocks"]

            for b in blocks:
                if "lines" in b:
                    for  l in b["lines"]:
                        line = ""
                        if l["spans"][0]["font"] == "AGaramondPro-Bold":
                            number = puzzle_num.pop(0)
                            move = to_move.pop(0)
                            if number != "223":
                                f.write("\n\n\n"  + number + "\n" + move + "\n")
                            else:
                                f.write(number + "\n" + move + "\n")
                            for s in l["spans"]:
                                line += s["text"]
                            f.write(line + "\n")
                        else:
                            for s in l["spans"]:
                                if s["font"] == "Chess-Merida-Regular":
                                    f.write(s["text"]+ "\n")

                                    
                                
pdf_path = "wood_intermediate.pdf"
output_file = "parsed_for_fen.txt"
parse_pdf_to_text(pdf_path, output_file)