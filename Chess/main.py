from ChessBoard import *

g = Game()

turn = "WHITE"
while True:
    print("Turn:", turn)
    # Check if the moves are valid
    try:
        src_input = input("   Enter the source position (x,y): ")
        dst_input = input("   Enter the destination position (x,y): ")
        
        # Split the input into x and y coordinates
        src_parts = src_input.split(',')
        dst_parts = dst_input.split(',')
        
        # Convert the column letter to an integer
        src_x = ord(src_parts[0].strip().lower()) - ord('a')
        src_y = int(src_parts[1].strip()) - 1
        
        dst_x = ord(dst_parts[0].strip().lower()) - ord('a')
        dst_y = int(dst_parts[1].strip()) - 1
        
        src_pos = Position(src_x, src_y)
        dst_pos = Position(dst_x, dst_y)
        
        g.move_piece(src_pos, dst_pos)
    except Exception as e:
        print("Error:", e)
        continue

    g.print()

    if g.is_check():
        print("Check!")

    if g.is_checkmate():
        print("Checkmate!")
        break

    turn = "BLACK" if turn == "WHITE" else "WHITE"
