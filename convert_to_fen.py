def convert_to_fen(board_text, piece_mapping, empty_mapping, white_to_play=True, move_number=1):
    # Split text into lines and strip trailing spaces
    lines = [line.strip() for line in board_text.strip().split("\n")]
    
    # Extract only the board layout (excluding the borders)
    board_lines = [line[1:-1] for line in lines[1:-1]]
    
    # Initialize FEN parts list
    fen_parts = []
    
    # Loop through each line to generate FEN notation
    for line in board_lines:
        # print(line)
        fen_line = ""
        empty_count = 0
        for char in line:
            if char in piece_mapping:
                if empty_count > 0:
                    fen_line += str(empty_count)
                    empty_count = 0
                fen_line += piece_mapping[char]
            elif char in empty_mapping:
                empty_count += 1
        if empty_count > 0:
            fen_line += str(empty_count)
        fen_parts.append(fen_line)
    
    # Join all lines with '/'
    fen_board = "/".join(fen_parts)

    # Determine castling rights based on positions of kings and rooks
    white_castle = ''
    black_castle = ''
    
    # Helper function to get king position correctly
    def get_king_position(line, king_symbol):
        parts = line.split(king_symbol)
        if len(parts) == 2:
            left_part = parts[0]
            count = sum(int(char) for char in left_part if char.isdigit())
            if count == 0:
                return len(left_part)
            return len(left_part) -1 + count
        return -1  # King not found
    # print("\n\n")
    # print(fen_parts[7],fen_parts[0])
    # Checking white castling availability (first row)
    white_king_pos = get_king_position(fen_parts[7], "K")
    if white_king_pos == 4:
        if 'R' in fen_parts[7][-1]:  # Checking H1 rook
            white_castle += "K"
        if 'R' in fen_parts[7][0]:  # Checking A1 rook
            white_castle += "Q"
    
    # Checking black castling availability (last row)
    black_king_pos = get_king_position(fen_parts[0], "k")
    if black_king_pos == 4:
        if 'r' in fen_parts[0][-1]:  # Checking H8 rook
            black_castle += "k"
        if 'r' in fen_parts[0][0]:  # Checking A8 rook
            black_castle += "q"
    
    castling_rights = white_castle + black_castle if white_castle + black_castle else "-"

    # Determine the side to move
    side_to_move = "w" if white_to_play else "b"
    
    # Construct the final FEN string
    fen_string = f"{fen_board} {side_to_move} {castling_rights} - 0 {move_number}"
    
    return fen_string

# Example mapping dictionary
piece_mapping = {
    "\uf074": "r", "\uf054": "r", "\uf06d": "n", "\uf04d": "n", 
    "\uf076": "b", "\uf056": "b", "\uf057": "q", "\uf077": "q", 
    "\uf06c": "k", "\uf04c": "k", "\uf06f": "p", "\uf04f": "p", 
    "\uf072": "R", "\uf052": "R", "\uf06e": "N", "\uf04e": "N", 
    "\uf062": "B", "\uf042": "B", "\uf051": "Q", "\uf071": "Q", 
    "\uf06b": "K", "\uf04b": "K", "\uf070": "P", "\uf050": "P"
}

empty_mapping = {
    "\uf02b": "1",  # black square
    " ": "1"        # white square
}

# # Example board text
# board_text = """
#  
#    
#   
#      
#      
#   
#    
#   
#   
# 
# """

# # Convert to FEN with parameters for side to move and move number
# fen = convert_to_fen(board_text, piece_mapping, empty_mapping, white_to_play=True, move_number=1)
# print(fen)


def read_puzzles_from_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    puzzles = text.split('\n\n\n')
    return puzzles

def parse_puzzle(puzzle_text):
    lines = [line.strip() for line in puzzle_text.split('\n') if line.strip()]
    puzzle_number = lines[0]
    white_to_move = lines[1].lower() == 'white to move'
    game_details = lines[2]
    board_lines = lines[3:]
    return puzzle_number, white_to_move, game_details, board_lines

def format_pgn(puzzle_number, game_details, fen):
    Event = game_details.split(',')[1].strip() if len(game_details.split(',')) > 1 else game_details
    player = game_details.split(',')[0].strip() if len(game_details.split(',')) > 0 else "???"

    white = player.split('–')[0].strip() if len(player.split('–')) > 1 else "???"
    black = player.split('–')[1].strip() if len(player.split('–')) > 1 else "???"
    pgn_template = f"""
    [Event "{Event}"]
    [White "{white}"]
    [Black "{black}"]
    [Type "Intermediate"]
    [puzzle "{puzzle_number}"]
    [Result "*"]
    [FEN "{fen}"]

    1. *"""
    return pgn_template

def save_pgn_file(pgns, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for pgn in pgns:
            file.write(pgn + "\n\n")


# Read puzzles from the file
file_path = 'parsed_for_fen.txt'  # Replace with your actual file path
puzzles = read_puzzles_from_text(file_path)

# Process each puzzle and generate PGN
pgns = []
for puzzle_text in puzzles:
    puzzle_number, player_to_move, game_details, board_lines = parse_puzzle(puzzle_text)
    board_text = '\n'.join(board_lines)
    fen = convert_to_fen(board_text, piece_mapping, empty_mapping, white_to_play=player_to_move, move_number=1)
    pgn = format_pgn(puzzle_number, game_details, fen)
    pgns.append(pgn)

# Save the PGN file
pgn_file_path = 'output.pgn'  # Replace with desired file path
save_pgn_file(pgns, pgn_file_path)
print(f"PGN file saved to {pgn_file_path}")