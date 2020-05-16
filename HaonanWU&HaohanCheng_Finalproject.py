X = 'X'
O = 'O'
E = ' '
import copy

learn = {}


class Board:
    def __init__(self, size):
        self.board = []
        for i in range(size):
            self.board.append([])
            for j in range(size):
                if i == 0:
                    self.board[i].append(O)
                elif i == size - 1:
                    self.board[i].append(X)
                else:
                    self.board[i].append(E)
        self.size = size

    def update(self):
        cx = 0
        co = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == X:
                    cx += 1
                elif self.board[i][j] == O:
                    co += 1
        self.value = cx - co


def print_board(board):
    for i in range(len(board)):
        print('| ', end='')
        for j in range(len(board)):
            print(board[i][j], '| ', end='')
        print()


def move(board, i, j, direction, player):
    size = len(board)
    if board[i][j] != player:
        return False
    if (i == 0 and direction == 'U') or (i == size - 1 and direction == 'D') or (j == 0 and direction == 'L') or (
            j == size - 1 and direction == 'R'):
        return False
    if direction == 'U':
        if board[i - 1][j] != E:
            return False
        else:
            board[i - 1][j] = player
            board[i][j] = E
            if valid(board, i - 1, j):
                return True
            else:
                board[i - 1][j] = E
                board[i][j] = player
    if direction == 'D':
        if board[i + 1][j] != E:
            return False
        else:
            board[i + 1][j] = player
            board[i][j] = E
            if valid(board, i + 1, j):
                return True
            else:
                board[i + 1][j] = E
                board[i][j] = player
    if direction == 'L':
        if board[i][j - 1] != E:
            return False
        else:
            board[i][j - 1] = player
            board[i][j] = E
            if valid(board, i, j - 1):
                return True
            else:
                board[i][j - 1] = E
                board[i][j] = player
    if direction == 'R':
        if board[i][j + 1] != E:
            return False
        else:
            board[i][j + 1] = player
            board[i][j] = E
            if valid(board, i, j + 1):
                return True
            else:
                board[i][j + 1] = E
                board[i][j] = player


def valid(board, i, j):
    size = len(board)
    if board[i][j] == O:
        player = X
    elif board[i][j] == X:
        player = O
    else:
        print('error')
        return False
    if i <= size - 3:  # check down
        if board[i + 1][j] == player and board[i + 2][j] == player:
            if i == size - 3:
                return False
            elif board[i + 3][j] == E:
                return False
    if i >= 2:  # check up
        if board[i - 1][j] == player and board[i - 2][j] == player:
            if i == 2:
                return False
            elif board[i - 3][j] == E:
                return False
    if j <= size - 3:  # check left
        if board[i][j + 1] == player and board[i][j + 2] == player:
            if j == size - 3:
                return False
            elif board[i][j + 3] == E:
                return False
    if j >= 2:  # check right
        if board[i][j - 1] == player and board[i][j - 2] == player:
            if j == 2:
                return False
            elif board[i][j - 3] == E:
                return False
    return True


def check_eat(game):
    board = copy.deepcopy(game.board)
    for i in range(game.size):
        for j in range(game.size):
            if board[i][j] != E:
                if board[i][j] == O:
                    player = X
                else:
                    player = O
                if i <= game.size - 3:  # check down
                    if board[i + 1][j] == player and board[i + 2][j] == player:
                        if i == game.size - 3:
                            game.board[i][j] = E
                            continue
                        elif board[i + 3][j] == E:
                            game.board[i][j] = E
                            continue
                if i >= 2:  # check up
                    if board[i - 1][j] == player and board[i - 2][j] == player:
                        if i == 2:
                            game.board[i][j] = E
                            continue
                        elif board[i - 3][j] == E:
                            game.board[i][j] = E
                            continue
                if j <= game.size - 3:  # check left
                    if board[i][j + 1] == player and board[i][j + 2] == player:
                        if j == game.size - 3:
                            game.board[i][j] = E
                            continue
                        elif board[i][j + 3] == E:
                            game.board[i][j] = E
                            continue
                if j >= 2:  # check right
                    if board[i][j - 1] == player and board[i][j - 2] == player:
                        if j == 2:
                            game.board[i][j] = E
                            continue
                        elif board[i][j - 3] == E:
                            game.board[i][j] = E
                            continue
    game.update()


def is_finish(board, player):
    bboard = copy.deepcopy(board)
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == player:
                for direction in ['U', 'D', 'L', 'R']:
                    if move(bboard, i, j, direction, player):
                        return False
    return True


def minimax(game, turn, depth):
    step = (0, 0, 'U')
    if is_finish(game.board, turn) or depth == 0:
        game.update()
        return [game.value, step]
    else:
        global learn
        if turn == X:
            maxV = -9999
            for i in range(game.size):
                for j in range(game.size):
                    if game.board[i][j] == turn:
                        for dire in ['U', 'L', 'R', 'D']:
                            board = copy.deepcopy(game)
                            if move(board.board, i, j, dire, turn):
                                check_eat(board)
                                key = ''.join([''.join([str(c) for c in lst]) for lst in board.board])
                                # print('max:',key)
                                if key not in learn.keys():
                                    value = minimax(board, O, depth - 1)[0]
                                    if value > maxV:
                                        maxV = value
                                        step = (i, j, dire)
                                    learn[key] = board
                                else:
                                    if learn[key].value > maxV:
                                        maxV = learn[key].value
                                        step = (i, j, dire)
            return [maxV, step]
        else:
            minV = 9999
            for i in range(game.size):
                for j in range(game.size):
                    if game.board[i][j] == turn:
                        for dire in ['U', 'L', 'R', 'D']:
                            board = copy.deepcopy(game)
                            if move(board.board, i, j, dire, turn):
                                check_eat(board)
                                key = ''.join([''.join([str(c) for c in lst]) for lst in board.board])
                                if key not in learn.keys():
                                    value = minimax(board, X, depth - 1)[0]
                                    if minV > value:
                                        minV = value
                                        step = (i, j, dire)
                                    learn[key] = board
                                else:
                                    if minV > learn[key].value:
                                        minV = learn[key].value
                                        step = (i, j, dire)
            return [minV, step]


if __name__ == '__main__':
    def hvh():
        turn = X
        while True:
            print('choose size (4,5,6)')
            size = int(input())
            if size in [4, 5, 6]:
                break
            else:
                print('input again')
        game = Board(size)
        draw = False
        while not is_finish(game.board, turn):
            if not draw:
                print(turn, "'s turn ")
                print('choose position')
                print('input (', size, ' ', size, ') for draw')
                print_board(game.board)
                i, j = map(str, input().split())
                i = int(i)
                j = int(j)
                if i == size and j == size:
                    draw = True
                    continue
                if i not in range(size) or j not in range(size):
                    print('invalid input, try again')
                    continue
                elif game.board[i][j] != turn:
                    print('invalid input, try again')
                    continue
                print('choose direction(U,D,L,R)')
                direction = input()
                if direction not in ['U', 'D', 'L', 'R']:
                    print('invalid input, try again')
                    continue
                if not move(game.board, i, j, direction, turn):
                    print('invalid move, try again')
                    continue
                else:
                    check_eat(game)
            else:
                print_board(game.board)
                while True:
                    print('draw? (y:accept  n:reject)')
                    cin = input()
                    if cin in ['y', 'n']:
                        break
                    print('invalid input')
                if cin:
                    print('draw!')
                    break
                else:
                    print('continue!')
                    draw = False
            if turn == X:
                turn = O
            else:
                turn = X
        if is_finish(game.board, turn):
            if turn == X:
                turn = O
            else:
                turn = X
            print(turn, 'win!')
        return


    def hvc(player):
        global learn
        turn = X
        while True:
            print('choose size (4,5,6)')
            size = int(input())
            if size in [4, 5, 6]:
                break
            else:
                print('input again')
        game = Board(size)
        while True:
            if turn == player:
                print("your turn ")
                print('choose position')
                print('input (', size, ' ', size, ') to quit')
                print_board(game.board)
                i, j = map(str, input().split())
                i = int(i)
                j = int(j)
                if i == size and j == size:
                    print('you cancel the match')
                    break
                if i not in range(size) or j not in range(size):
                    print('invalid input, try again')
                    continue
                elif game.board[i][j] != turn:
                    print('invalid input, try again')
                    continue
                print('choose direction(U,D,L,R)')
                direction = input()
                if direction not in ['U', 'D', 'L', 'R']:
                    print('invalid input, try again')
                    continue
                if not move(game.board, i, j, direction, turn):
                    print('invalid move, try again')
                    continue
                else:
                    check_eat(game)
                if turn == O:
                    turn = X
                else:
                    turn = O
                if is_finish(game.board, turn):
                    print('you win!')
                    break
            else:
                print('wait AI to respond.....')
                learn = {}
                count = 0
                for i in range(game.size):
                    for j in range(game.size):
                        if game.board[i][j] != E and game.board[i][j]!= player:
                            count+=1
                [value, (i, j, direction)] = minimax(game,turn, int(50/count))
                print('move:(', i, ',', j, ',', direction, ')')
                move(game.board, i, j, direction, turn)
                check_eat(game)
                turn = player
                if is_finish(game.board, turn):
                    print('you lose!')
                    break
        return


    while True:
        print('choose what you want to do')
        print('h: human vs human')
        print('c: human vs computer')
        print('q: quit')
        cin = input()
        if cin == 'q':
            break
        if cin == 'h':
            hvh()
        if cin == 'c':
            while True:
                print('choose side(X/O)')
                cin = input()
                if cin == X or cin == O:
                    break
                else:
                    print('invalid input')
            hvc(cin)
        else:
            print('invalid input')
