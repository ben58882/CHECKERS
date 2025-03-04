
class checkers_board:

    def __init__(self):

        self.pos = [0] * 32
        self.pieces = set()
        self.available_moves = {}
        self.available_captures = {}
        self.seen = {}

        # 0 = no piece, 1 = black, 2 = white , 3 = black king, 4 = white king
        for i in range(32):

            row = i // 4

            if row == 3 or row == 4:

                continue

            elif row < 3:

                self.pos[i] = 1

            else:

                self.pos[i] = 2

            self.pieces.add(i)

        print(self.pos)


    def update_available_moves(self,pos):

        for piece in range(32):

            if pos[piece] == 0:
                continue

            steps = []

            row = -1

            if piece//4 > 3:
                row = ((7-piece)//4) % 2
            else:
                row = (piece//4) % 2

            if pos[piece] == 1:

                steps.append(4)
                if row == 0:
                    steps.append(5)
                else:
                    steps.append(3)



            elif pos[piece] == 2:

                steps.append(-4)
                if row == 0:
                    steps.append(-5)
                else:
                    steps.append(-3)

            else:

                steps.append(4)
                steps.append(-4)
                if row == 0:
                    steps.append(5)
                    steps.append(-5)
                else:
                    steps.append(3)
                    steps.append(-3)


            for step in steps:

                if piece + step >= 32 or piece + step < 0 or (pos[piece+step] != 0 and pos[piece+step] % 2 == pos[piece] % 2) or abs(piece // 4 - (piece + step) // 4) != 1:
                    continue

                if pos[piece+step] == 0:

                    if piece in self.available_moves:

                        self.available_moves[piece].add(piece + step)

                    else:

                        self.available_moves[piece] = set()
                        self.available_moves[piece].add(piece + step)

                else:

                    self.update_capture_helper(tuple(),piece,piece,step,steps,0,pos)


        return


    def update_capture_helper(self,captured,start_square,piece,initial_step,steps,depth,pos):

        if depth > 8:
            return

        if piece >= 32 or piece < 0:
            return

        curr_steps = []

        if start_square == piece:

            curr_steps.append(initial_step)

        else:

            curr_steps = steps

        for step in curr_steps:

            captured_piece = piece + step

            if captured_piece in captured:
                return

            resultant_square = piece + step + step

            if step == 3 or step == -3:
                if step == 3:
                    resultant_square += 1
                else:
                    resultant_square -= 1

            elif step == 5 or step == -5:
                if step == -5:
                    resultant_square += 1
                else:
                    resultant_square -= 1

            else:
                tmp_piece = piece

                if piece // 4> 3:
                    tmp_piece = 7 - piece

                if (tmp_piece//4) % 2 == 0:
                    if step == 4:
                        resultant_square -= 1
                    else:
                        resultant_square += 1

                else:
                    if step == 4:
                        resultant_square += 1
                    else:
                        resultant_square -= 1

            if captured_piece >= 32 or captured_piece  < 0 or pos[captured_piece] ==0 or pos[captured_piece] % 2 == pos[piece] % 2 or abs(piece // 4 - captured_piece // 4) != 1:
                if len(captured) > 0:

                    if start_square not in self.available_captures:
                        self.available_captures[start_square] = set()

                    self.available_captures[start_square].add((piece,captured))
                continue

            if resultant_square >= 32 or resultant_square < 0 or pos[resultant_square] != 0 or abs(resultant_square // 4 - captured_piece // 4) != 1:
                if len(captured) > 0:

                    if start_square not in self.available_captures:
                        self.available_captures[start_square] = set()

                    self.available_captures[start_square].add((piece,captured))
                continue

            if resultant_square >= 0 and resultant_square < 32:
                self.update_capture_helper(captured + (captured_piece,),start_square,resultant_square,initial_step,steps,depth + 1,pos)

        return


    def get_input(self,start,end,capture,pieces_to_capture):

        self.available_moves.clear()
        self.available_captures.clear()
        self.update_available_moves(self.pos)

        if capture == 'n':

            if start not in self.available_moves or end not in self.available_moves[start]:

                print("Illegal Move")

                return

        elif capture == 'y':

            if start not in self.available_captures:

                print("Illegal Move")

                return

            check_capture = tuple()
            curr = ''

            for char in pieces_to_capture:

                if char == ',':

                    check_capture += (int(curr),)
                    curr = ''

                elif char == ' ':
                    continue

                else:

                    curr += char

            check_capture += (int(curr),)

            valid = False

            for options in self.available_captures[start]:

                if options[0] == end and check_capture == options[1]:
                    valid = True
                    break

            if valid:

                for piece in check_capture:

                    self.pos[piece] = 0

            else:

                print("Illegal move")
                return


        else:

            print('invalid')

            return




        self.pos[end] = self.pos[start]

        self.pos[start] = 0

        self.available_moves.clear()

        self.available_captures.clear()

        self.update_available_moves(self.pos)



        return

    def get_points(self,pos):

        white = 0
        black = 0

        for squares in pos:

            if squares == 1 or squares == 3:
                black += 1

            elif squares == 2 or squares== 4:
                white += 1

        return [black,white]

    def calculate(self,colour_mod,depth,alpha,beta,pos):

        id = (tuple(pos),colour_mod)

        if id in self.seen:
            return self.seen[id]

        self.available_moves.clear()
        self.available_captures.clear()
        self.update_available_moves(pos)

        points = self.get_points(pos)
        black_points = points[0]
        white_points = points[1]

        if white_points == 0:

            return (float('inf'),0)

        if black_points == 0:

            return (float('-inf'),0)


        if depth > 9:

            return (black_points - white_points,0)


        moves = []

        for start in self.available_captures:

            if pos[start] % 2 != colour_mod:
                continue

            for options in self.available_captures[start]:
                end = options[0]
                capture = options[1]
                moves.append((start,end,capture))

        if len(moves) == 0:

            for start in self.available_moves:

                if pos[start] % 2 != colour_mod:
                    continue

                for end in self.available_moves[start]:

                    moves.append((start,end,-1))

        if len(moves) == 0:

            if colour_mod == 1:
                return (float('-inf'),0)

            else:
                return(float('inf'),1)

        best_move = []

        if colour_mod == 1:

            highest_score = float('-inf')

            for move in moves:


                start = move[0]
                end = move[1]
                capture = move[2]

                type_of_start_piece = pos[start]
                type_of_end_piece = pos[end]
                captured_pieces = tuple()

                if isinstance(capture,tuple):

                    for square in capture:

                        captured_pieces += (self.pos[square],)
                        pos[square] = 0

                pos[start] = 0
                pos[end] = type_of_start_piece

                if end >= 0 and end <= 3 and colour_mod == 0:

                    pos[end] = 4

                if end >= 28 and end <= 31 and colour_mod == 1:

                    pos[end] = 3

                curr = self.calculate((colour_mod+1)%2,depth+1,alpha,beta,pos.copy())

                #self.pos[start] = type_of_start_piece
                #self.pos[end] = type_of_end_piece

                #if isinstance(capture,tuple):

                    #for i,square in enumerate(capture):

                        #self.pos[square] = captured_pieces[i]

                pos = list(id[0])

                if curr[0] > highest_score:

                    highest_score = curr[0]
                    best_move = move


                alpha = max(alpha,highest_score)

                if beta <= alpha:
                    break

            self.seen[id] = (highest_score,best_move)

            return (highest_score,best_move)

        else:

            lowest_score = float('inf')

            for move in moves:

                start = move[0]
                end = move[1]
                capture = move[2]

                type_of_start_piece = pos[start]
                type_of_end_piece = pos[end]
                captured_pieces = tuple()

                if isinstance(capture, tuple):

                    for square in capture:
                        captured_pieces += (pos[square],)
                        pos[square] = 0

                pos[start] = 0
                pos[end] = type_of_start_piece

                if end >= 0 and end <= 3 and colour_mod == 0:
                    pos[end] = 4

                if end >= 28 and end <= 31 and colour_mod == 1:
                    pos[end] = 3

                curr = self.calculate((colour_mod + 1) % 2, depth + 1, alpha, beta,pos.copy())


                '''self.pos[start] = type_of_start_piece
                self.pos[end] = type_of_end_piece

                if isinstance(capture, tuple):

                    for i, square in enumerate(capture):
                        self.pos[square] = captured_pieces[i]'''

                pos = list(id[0])

                if curr[0] < lowest_score:
                    lowest_score = curr[0]
                    best_move = move

                beta = min(beta, lowest_score)

                if beta <= alpha:
                    break

            self.seen[id] = (lowest_score, best_move)

            return (lowest_score, best_move)






