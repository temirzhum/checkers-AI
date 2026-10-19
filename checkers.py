import tkinter as tk
from tkinter import messagebox


import time

class Checker():
    def __init__(self):
        pass

    def copying(self, desk):  # .copy function creates pointer to array but I need new one identical to the old
        new_desk = [  # I can't use numpy and have to create array with zeros manually
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        for i in range(8):
            for j in range(8):
                new_desk[i][j] = desk[i][j]
        return new_desk

    def new_successors(self, desk, i, j, sign1, sign2, color):
        desk_do_not_touch = self.copying(desk)
        eat = False
        quin = False
        eat_successor = []
        enemy_col = []
        if color % 2 != 0:
            enemy_col = [2, 4]
        elif color % 2 == 0:
            enemy_col = [1, 3]

        try:
            if i + sign1 < 0 or j + sign2 < 0:  # without this line it can move to item under index -1
                return [], eat, []

            elif 0 <= i + sign1 + sign1 < 8 and 0 <= j + sign2 + sign2 < 8 and desk[i + sign1][j + sign2] in enemy_col \
                    and desk[i + sign1][j + sign2] != 0 and desk[i + sign1 + sign1][j + sign2 + sign2] == 0:  # eating

                desk_copy = self.copying(desk_do_not_touch)
                desk_copy[i][j] = 0
                desk_copy[i + sign1][j + sign2] = 0
                if color == 1:
                    if i + sign1 + sign1 == 7:
                        quin = True
                if color == 2:
                    if i + sign1 + sign1 == 0:
                        quin = True
                if quin == False:
                    desk_copy[i + sign1 + sign1][j + sign2 + sign2] = color
                elif quin == True:
                    desk_copy[i + sign1 + sign1][j + sign2 + sign2] = color + 2

                eat = True
                k = i + sign1 + sign1
                k_1 = j + sign2 + sign2
                return desk_copy, eat, [k,k_1]  # It should return only one successor so that minimax would not choose anything more benefitial

            elif desk[i + sign1][j + sign2] == 0:  # moving

                desk_copy = self.copying(desk_do_not_touch)
                desk_copy[i][j] = 0
                if color == 1:
                    if i + sign1 == 7:

                        quin = True
                        desk_copy[i + sign1][j + sign2] = color + 2
                        return desk_copy, False,[]
                if color == 2:
                    if i + sign1 == 0:

                        quin = True
                        desk_copy[i + sign1][j + sign2] = color + 2
                        return desk_copy, False,[]

                desk_copy[i + sign1][j + sign2] = color
                return desk_copy, False, []


        except:

            pass

        return [], eat, []

    def new_successors_quin(self, desk, i, j, sign1, sign2, successors, color):

        desk_do_not_touch = self.copying(desk)
        eat = False
        eat_successor = []
        enemy_found = False
        enemy_pos = None
        step = 1

        enemy_col = []
        if color % 2 != 0:
            enemy_col = [2, 4]
        elif color % 2 == 0:
            enemy_col = [1, 3]

        while True:
            ni = i + sign1 * step
            nj = j + sign2 * step
            if ni < 0 or ni >= 8 or nj < 0 or nj >= 8:
                break
            where_to_go = desk[ni][nj]

            if not enemy_found:
                if where_to_go == 0:
                    desk_copy = self.copying(desk_do_not_touch)
                    desk_copy[i][j] = 0
                    desk_copy[ni][nj] = color
                    successors.append(desk_copy)


                elif 0 <= ni + sign1 <= 7 and 0 <= nj + sign2 <= 7 and where_to_go in enemy_col and desk[ni + sign1][
                    nj + sign2] == 0:

                    enemy_found = True
                    enemy_pos = [ni, nj]
                else:
                    return successors, eat

            else:

                desk_copy = self.copying(desk_do_not_touch)
                desk_copy[i][j] = 0
                desk_copy[enemy_pos[0]][enemy_pos[1]] = 0
                desk_copy[ni][nj] = color
                eat_successor.append(desk_copy)
                eat = True


            step += 1

            if eat:

                return eat_successor, eat

        return successors, eat

    def guin_successors_for_computeSuccessors(self, desk, i, j, sign1, sign2, successors, color):
        eat_successor = []
        succcc=[]
        successors, eat = self.new_successors_quin(desk, i, j, sign1, 1, successors, color)
        if eat == True:
            for child in successors:
                suc=self.copying(child)
                eat_successor.append(suc)
        else:
            for child in successors:
                suc = self.copying(child)
                succcc.append(suc)
        successors_2, eat_2 = self.new_successors_quin(desk, i, j, sign1, -1, successors, color)
        if eat_2 == True:
                for child in successors_2:
                    suc = self.copying(child)
                    eat_successor.append(suc)
        else:
            for child in successors_2:
                suc = self.copying(child)
                succcc.append(suc)

        if eat_successor:
            return eat_successor, True
        else:
            return successors, False

    def else_to_eat(self, desk, coor, sign1, sign2, color):
        i, j = coor[0], coor[1]
        quin = False
        eat = False

        if color % 2 != 0:
            enemy_col = [2, 4]
        elif color % 2 == 0:
            enemy_col = [1, 3]

        if i + sign1 < 0 or j + sign2 < 0:  # without this line it can move to item under index -1
            return [], eat

        elif i + sign1 > 8 or j + sign2 > 8:  # without this line it can move to item under index -1
            return [], eat

        elif 0 <= i + sign1 + sign1 < 8 and 0 <= j + sign2 + sign2 < 8 and desk[i + sign1][j + sign2] in enemy_col \
                and desk[i + sign1][j + sign2] != 0 and desk[i + sign1 + sign1][j + sign2 + sign2] == 0:
            desk_copy = self.copying(desk)
            desk_copy[i][j] = 0
            desk_copy[i + sign1][j + sign2] = 0
            if color == 1:
                if i + sign1 + sign1 == 7:
                    quin = True
            if color == 2:
                if i + sign1 + sign1 == 0:
                    quin = True

            if quin == False:
                desk_copy[i + sign1 + sign1][j + sign2 + sign2] = color
            elif quin == True:
                desk_copy[i + sign1 + sign1][j + sign2 + sign2] = color + 2
            eat = True
            return desk_copy, eat
        else:
            return desk, eat

    def computeSuccessors(self, desk, turn):
        successors = []
        eat_successor = []

        desk_do_not_touch = self.copying(desk)  # copy is not listed in the list of approved libraries
        if turn == 1:
            i, j, c = 0, 0, 0

            for i in range(8):
                for j in range(8):
                    if desk[i][j] == 1:
                        eat = False
                        eat_2 = False
                        successor_1, eat, coor_1 = self.new_successors(desk, i, j, 1, 1, 1)
                        if successor_1 != []:
                            successors.append(successor_1)
                        successor_2, eat_2, coor_2 = self.new_successors(desk, i, j, 1, -1, 1)

                        if successor_2 != []:
                            successors.append(successor_2)
                        if eat == True:
                            eat_successor.append(successor_1)
                            cont_eat_1, bool_1 = self.else_to_eat(successor_1, coor_1, 1, 1, 1)
                            cont_eat_2, bool_2 = self.else_to_eat(successor_1, coor_1, 1, -1, 1)
                            if bool_1 == True:
                                eat_successor.append(cont_eat_1)
                            if bool_2 == True:
                                eat_successor.append(cont_eat_2)
                        if eat_2 == True:
                            eat_successor.append(successor_2)
                            cont_eat_1, bool_1 = self.else_to_eat(successor_2, coor_2, 1, 1, 1)
                            cont_eat_2, bool_2 = self.else_to_eat(successor_2, coor_2, 1, -1, 1)
                            if bool_1 == True:
                                eat_successor.append(cont_eat_1)
                            if bool_2 == True:
                                eat_successor.append(cont_eat_2)
                        c += 1

                    elif desk[i][j] == 3:
                        successors, eat = self.guin_successors_for_computeSuccessors(desk, i, j, 1, -1, successors, 3)
                        if eat == True:
                            new_successor = []
                            for child in successors:
                                new_successor = self.copying(child)
                                eat_successor.append(new_successor)
                        successors_2, eat_2 = self.guin_successors_for_computeSuccessors(desk, i, j, -1, -1, successors,
                                                                                       3)
                        if eat_2 == True:
                            new_successor = []
                            for child in successors_2:
                                new_successor = self.copying(child)
                                eat_successor.append(new_successor)
                        c += 1
                    black, _ = self.count(desk)

                    if c >= black:
                        break

        elif turn == 2:
            i, j, c = 0, 0, 0
            check = 0

            for i in range(8):
                for j in range(8):

                    if desk[i][j] == 2:
                        eat = False
                        eat_2 = False
                        successor_1, eat, coor_1 = self.new_successors(desk, i, j, -1, 1, 2)
                        if successor_1 != []:
                            successors.append(successor_1)
                        successor_2, eat_2, coor_2 = self.new_successors(desk, i, j, -1, -1, 2)
                        if successor_2 != []:
                            successors.append(successor_2)
                        if eat == True:
                            eat_successor.append(successor_1)
                            cont_eat_1, bool_1 = self.else_to_eat(successor_1, coor_1, -1, 1, 2)
                            cont_eat_2, bool_2 = self.else_to_eat(successor_1, coor_1, -1, -1, 2)
                            if bool_1 == True:
                                eat_successor.append(cont_eat_1)
                            if bool_2 == True:
                                eat_successor.append(cont_eat_2)
                        if eat_2 == True:
                            eat_successor.append(successor_2)
                            cont_eat_1, bool_1 = self.else_to_eat(successor_2, coor_2, -1, 1, 2)
                            cont_eat_2, bool_2 = self.else_to_eat(successor_2, coor_2, -1, -1, 2)
                            if bool_1 == True:
                                eat_successor.append(cont_eat_1)
                            if bool_2 == True:
                                eat_successor.append(cont_eat_2)
                        c += 1



                    elif desk[i][j] == 4:


                        successors, eat_1 = self.guin_successors_for_computeSuccessors(desk, i, j, 1, -1, successors, 4)

                        if eat_1 == True:
                            new_successor=[]

                            for child in successors:

                                new_successor=self.copying(child)
                                eat_successor.append(new_successor)

                        successors_2, eat_2 = self.guin_successors_for_computeSuccessors(desk, i, j, -1, -1, successors,4)
                        if eat_2 == True:
                            if eat_2 == True:
                                new_successor = []
                                for child in successors_2:

                                    new_successor = self.copying(child)
                                    eat_successor.append(new_successor)
                        c += 1

                    _, white = self.count(desk)
                    if c >= white:
                        break

        # For some reason duplicate successors appear during successor computation. It is easier to create new array with
        # unique successors than figuring out why duplicates appear
        if eat_successor == []:
            new_successors = []
            for i in successors:
                if i in new_successors:
                    continue
                else:
                    new_successors.append(i)
            return new_successors, False
        else:
            new_successors = []
            for i in eat_successor:
                if i in new_successors:
                    continue
                else:
                    new_successors.append(i)
            return new_successors, True

    def check_step(self, desk, orig, to_go, where_to_go):
        wrong_pice = True
        if to_go == False:
            r_c = []
            for simbols in orig:
                if simbols == ',':
                    continue
                else:
                    r_c.append(int(simbols))

            if desk[r_c[0]][r_c[1]] == 2 or desk[r_c[0]][r_c[1]] == 4 :
                wrong_pice = False

            else:

                wrong_pice = True

            if wrong_pice == True:
                return False, []
            else:
                return True, []

        elif to_go == True:
            eat=False

            orig_1 = []
            for simbols in orig:
                if simbols == ',':
                    continue
                else:
                    orig_1.append(int(simbols))
            new_r_c = []
            for simbols in where_to_go:
                if simbols == ',':
                    continue
                else:
                    new_r_c.append(int(simbols))
            successors = []
            legitimate_steps, eat = self.computeSuccessors(desk, 2)

            if legitimate_steps == []:
                CheckersGame.game_over(desk)

            pretendent_0 = self.copying(desk)
            if pretendent_0[orig_1[0]][orig_1[1]] == 2:
                if new_r_c[0] == 0:
                    pretendent_0[orig_1[0]][orig_1[1]] = 0
                    pretendent_0[new_r_c[0]][new_r_c[1]] = 4
                else:
                    pretendent_0[new_r_c[0]][new_r_c[1]] = 2
            elif pretendent_0[orig_1[0]][orig_1[1]] == 4:
                pretendent_0[orig_1[0]][orig_1[1]] = 0
                pretendent_0[new_r_c[0]][new_r_c[1]] = 4

            if pretendent_0 in legitimate_steps:
                return True, pretendent_0, eat

            pretendent_5 = self.copying(desk)
            try:
                if pretendent_5[orig_1[0]][orig_1[1]] == 4:
                    step=1
                    i_cur=0
                    j_cur=0

                    while True:

                        ni = new_r_c[0]- orig_1[0]
                        nj = new_r_c[1]- orig_1[1]
                        if ni==0 and nj==0:
                            break
                        if orig_1[0]+i_cur==new_r_c[0] and orig_1[1]+j_cur==new_r_c[1]:
                            break
                        if ni >0:
                            i_cur += 1
                        elif ni < 0:
                            i_cur -= 1
                        if nj >0:
                            j_cur += 1
                        elif nj < 0:
                            j_cur -= 1


                        if pretendent_5[orig_1[0]+i_cur][orig_1[1]+j_cur]==1 or\
                                    pretendent_5[orig_1[0]+i_cur][orig_1[1]+j_cur]==3:
                            pretendent_5[orig_1[0] + i_cur][orig_1[1] + j_cur] =0
                            pretendent_5[orig_1[0]][orig_1[1]] = 0
                            pretendent_5[new_r_c[0]][new_r_c[1]] = 4

                if pretendent_5 in legitimate_steps:
                    return True, pretendent_5, eat
            except:
                pass







            pretendent = self.copying(desk)
            pretendent_2 = self.copying(desk)
            pretendent_3 = self.copying(desk)
            pretendent_4 = self.copying(desk)
            try:
                if new_r_c[0] == 0:
                    pretendent_3[new_r_c[0]][new_r_c[1]] = 4
                else:
                    pretendent_3[new_r_c[0]][new_r_c[1]] = 2
                pretendent_3[orig_1[0]][orig_1[1]] = 0

            except:
                pass

            try:
                if new_r_c[0] == 0:
                    pretendent_4[new_r_c[0]][new_r_c[1]] = 4
                else:
                    pretendent_4[new_r_c[0]][new_r_c[1]] = 2
                pretendent_4[orig_1[0]][orig_1[1]] = 0

            except:
                pass

            try:
                if new_r_c[0] == 0:
                    pretendent[new_r_c[0]][new_r_c[1]] = 4
                else:
                    pretendent[new_r_c[0]][new_r_c[1]] = 2
                pretendent[new_r_c[0] + 1][new_r_c[1] - 1] = 0

                pretendent[orig_1[0]][orig_1[1]] = 0

            except:
                pass

            try:
                if new_r_c[0] == 0:
                    pretendent_2[new_r_c[0]][new_r_c[1]] = 4
                else:
                    pretendent_2[new_r_c[0]][new_r_c[1]] = 2
                pretendent_2[new_r_c[0] + 1][new_r_c[1] + 1] = 0
                pretendent_2[orig_1[0]][orig_1[1]] = 0

            except:
                pass

            if pretendent in legitimate_steps:
                eat=True
                return True, pretendent,eat
            elif pretendent_2 in legitimate_steps:
                eat = True
                return True, pretendent_2,eat
            elif pretendent_3 in legitimate_steps:

                return True, pretendent_3,eat
            elif pretendent_4 in legitimate_steps:

                return True, pretendent_4,eat
            else:
                return False, [],eat

        return False, []

    def count_quin(self, desk):
        black_quin, white_quin = 0, 0
        for r in range(8):
            for c in range(8):
                try:
                    if desk[r][c] == 3:
                        black_quin += 1
                    elif desk[r][c] == 4:
                        white_quin += 1
                except Exception as e:
                    pass

        return black_quin, white_quin

    def count(self, node):
        black = 0  # Minimax algorithm uses self.number_of_black and white to calculate the heuristics and determine whether the
        white = 0  # node is leaf, so after one iteration it went to 0. This code is needed to restore current number of pieces
        for r in range(8):
            for c in range(8):
                try:
                    if node[r][c] == 1 or node[r][c] == 3:
                        black += 1
                    elif node[r][c] == 2 or node[r][c] == 4:
                        white += 1
                except Exception as e:
                    pass

        return black, white

    def evaluate(self, node):
        black, white = self.count(node)
        black_quin, white_quin = self.count_quin(node)
        value_black = black + 3 * black_quin
        value_white = white + 3 * white_quin
        return value_black - value_white

    def leaf(self, node):
        black, white = self.count(node)

        if black == 0 or white == 0:
            return True
        else:
            return False

    def minimax(self, node, depth, alpha, beta, player,max_depth,start):

        if depth == max_depth or self.leaf(node):
            return self.evaluate(node)
        end = time.time()

        if end - start>20:

            return self.evaluate(node)
        if player == 1:
            value = -100  # I don't think it is mandatory to use infinity
            suc, _ = self.computeSuccessors(node, 1)
            for child in suc:
                """
                print('Player child')
                for k in child:
                    print(k)
                print('-----------')"""
                value = max(value, self.minimax(child, depth + 1, alpha, beta, 2,max_depth,start))
                alpha = max(alpha, value)
                # print(f"Player is {player}, Depth is {depth}, Value is {value}, alpha is {alpha}, beta is {beta}")

                if alpha >= beta:
                    break
            return value

        elif player == 2:
            value = 100
            suc, _ = self.computeSuccessors(node, 2)
            for child in suc:
                """
                print('AI child')
                for k in child:
                    print(k)
                print('-----------')"""
                value = min(value, self.minimax(child, depth + 1, alpha, beta, 1,max_depth,start))
                beta = min(beta, value)
                # print(f"Player is {player}, Depth is {depth}, Value is {value}, alpha is {alpha}, beta is {beta}")

                if alpha >= beta:
                    break
            return value

    def get_best_move(self, state, player, depth,max_depth):
        start = time.time()
        best_value = -100
        best_move = []
        successors, _ = self.computeSuccessors(state, player)
        for move in successors:
            """
            print('Assessing move')
            for k in move:
                print(k)
            print('....................')"""
            if player == 1:
                pl = 2
            elif player == 2:
                pl = 1
            value = self.minimax(move, depth + 1, -100, 100, pl,max_depth,start)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move

#===============================================================================================================================

class CheckersGame:

    def __init__(self, ai):
        self.ai = ai

        self.square = 70
        self.red_back="#FFE4C4"
        self.black_back="#CD853F"
        self.light_color = "#FF4D4D"
        self.black="#0D0D0D"
        self.white="#F2F2F2"

        self.black_quin="#00008B"
        self.white_quin="#DAA520"

        self.desk = [
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0],
        ]
        self.sel_sq = None
        self.player_turn = True
        self.depth = self.choose_dif()


        self.root = tk.Tk()
        self.root.title("fff")

        self.label = tk.Label(self.root, text="Player turn. Select a black piece.")
        self.label.pack(pady=5)

        canvas_size = 8 * self.square
        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.start_1)

        self.redraw()
        self.root.mainloop()

    def choose_dif(self):
        root = tk.Tk()
        root.title("Select Difficulty")

        tk.Label(root, text="Choose difficulty:").pack()

        depth = tk.IntVar(value=2)

        tk.Radiobutton(root, text="Easy",   variable=depth, value=1).pack()
        tk.Radiobutton(root, text="Medium", variable=depth, value=5).pack()
        tk.Radiobutton(root, text="Hard",   variable=depth, value=10).pack()

        tk.Button(root, text="Play",command=root.destroy).pack()

        root.mainloop()
        return depth.get()

    def draw_desk(self):
        for row in range(8):
            for col in range(8):

                x0 = col * self.square
                y0 = row * self.square
                x1 = x0 + self.square
                y1 = y0 + self.square

                if (row + col) % 2 == 1:
                    color = self.black_back
                else:
                    color = self.red_back

                if (row, col) == self.sel_sq:
                    color = self.light_color

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def draw_pice(self):
        for row in range(8):
            for col in range(8):
                value = self.desk[row][col]

                if value == 0:
                    continue

                x0 = col * self.square
                y0 = row * self.square
                x1 = x0 + self.square
                y1 = y0 + self.square

                pad = 8

                if value == 2 or value == 4:
                    fill = self.black

                else:
                    fill = self.white


                self.canvas.create_oval(x0 + pad, y0 + pad,x1 - pad, y1 - pad,fill=fill, width=2)
                if value == 3:
                    self.canvas.create_oval(x0 + pad, y0 + pad,x1 - pad, y1 - pad,fill=self.white_quin, width=2)
                if value == 4:
                    self.canvas.create_oval(x0 + pad, y0 + pad,x1 - pad, y1 - pad,fill=self.black_quin, width=2)


    def redraw(self):
        self.canvas.delete("all")
        self.draw_desk()
        self.draw_pice()


    def start_1(self, event):
        if not self.player_turn:
            return

        col = int(event.x // self.square)
        row = int(event.y // self.square)
        coord = [row,col]


        if self.sel_sq is None:
            binary_check, _ = self.ai.check_step(self.desk, coord, False, coord)
            if binary_check:
                self.sel_sq = (row, col)
                self.label.config(text="Piece selected! Now click where to move it.")
                self.redraw()
            else:
                self.label.config(text="Invalid piece. Click one of your black pieces.")


        else:
            move_coord = [self.sel_sq[0], self.sel_sq[1]]
            binary_check, new_desk, eat = self.ai.check_step(self.desk, move_coord, True, coord)

            if binary_check:

                #Here I tried implementing multi capturing move for player, but failed. The idea was to use eat variable to
                # identify whether player have eaten enemy or not. After it should have given aportunity to do another move
                # but it created a strange logical loop that I was not able to solve. I am writing this comment after finishing the code
                # so I don't remember the exact specifications of that loop

                self.new_desk(self.ai.copying(new_desk))
                self.sel_sq = None
                self.redraw()

                if self.game_over():
                    return

                self.label.config(text="AI turn, please wait...")
                self.root.after(1000, self.ai_move)

            else:
                _, eat = self.ai.computeSuccessors(self.desk, 2)
                if eat:
                    self.label.config(text="There is an enemy to eat but this piece can't do it")
                else:
                    self.label.config(text="Invalid move. Try again.")

                self.sel_sq = None
                self.redraw()

    def ai_move(self):
        self.player_turn = False

        self.root.update()

        new_desk= self.ai.get_best_move(self.desk, 1, 0, self.depth)
        print('Old desk:')
        for row in self.desk:
            print(row)
        print('//////////')
        print('New desk:')
        for row in new_desk:
            print(row)
        print('***********')
        self.new_desk(new_desk)
        self.redraw()

        if self.game_over():
            return

        self.player_turn = True
        self.label.config(text="Player turn. Select a black piece.")

    def new_desk(self, new_desk):
        for row in range(8):
            for col in range(8):
                self.desk[row][col] = new_desk[row][col]

    def game_over(self):
        black_count, white_count = self.ai.count(self.desk)
        if white_count == 0:
            messagebox.showinfo("Game Over", "AI wins")
            self.root.quit()
            return True
        if black_count == 0:
            messagebox.showinfo("Game Over", "You win")
            self.root.quit()
            return True
        return False


CheckersGame(Checker())
