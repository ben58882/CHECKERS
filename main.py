from board import checkers_board

board = checkers_board()


game = True

while game:
    board.available_captures.clear()
    board.available_moves.clear()
    board.update_available_moves(board.pos)
    calculate = input("Calculate?")

    if calculate == 'y':

        side = input("White/Black: ")
        mod = -1

        if side == "White":
            mod = 0

        elif side == "Black":
            mod = 1

        else:
            print("Invalid")
            continue

        tmp = board.calculate(mod,0,float('-inf'),float('inf'),board.pos.copy())

        print(tmp[1])
        continue

    print(board.available_captures)
    print(board.available_moves)
    starting_square = int(input("Piece to move: "))
    ending_square = int(input("Square to move to: "))
    capture = input("Capture: ")
    pieces_to_capture = ''
    if capture == 'y':
        pieces_to_capture = input("Piece to capture: ")

    board.get_input(starting_square,ending_square,capture,pieces_to_capture)
    print(board.pos)

