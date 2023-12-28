import numpy as np
from copy import deepcopy
from collections import defaultdict


class Solve8():
    def __init__(self):
        self.moves = np.array(
            [
                ('u', [0, 1, 2], -3),
                ('d', [6, 7, 8], 3),
                ('l', [0, 3, 6], -1),
                ('r', [2, 5, 8], 1)
            ],
            dtype=[
                ('move', str, 1),
                ('pos', list),
                ('delta', int)
            ]
        )

        self.STATE = [
            ('board', list),
            ('move', str, 1),
            ('parent', int),
            ('gn', int),
            ('hn', int)
        ]
    
        self.PRIORITY = [
            ('pos', int),
            ('fn', int)
        ]
        self.goal = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0])
        self.goalc = self.coor(self.goal)

    def __str__(self):
        return 'Grup Surup'
    
    
    def Solve(self,  tile):
        '''
        Input: an 8 tile object
        Output: a list of moves which will generate the winning boar
        when applied one after the other to the input 8 tile object
        check out the example moves above, howerever they are reversed and
        multiplied by -1, in your case no reverse or -1, just apply them
        one after the other
        movez should contain the minimum number of moves needed to solve the puzzle
        '''
        previous_boards = defaultdict(bool)
        board = tile.Board.copy().reshape(9)
        
        previous_boards = defaultdict(bool)

        hn = self.mhd(self.coor(board), self.goalc)
        state = np.array([(board, 'n', -1, 0, hn)], self.STATE)
        priority = np.array( [(0, hn)], self.PRIORITY)
        found = False
        i = 1
        while True:
            priority = np.sort(priority, kind='mergesort', order=['fn', 'pos'])
            pos, fn = priority[0]
            priority = np.delete(priority, 0, 0)
        
            board = state[pos][0]
            gn = state[pos][3] + 1
            loc = int(np.where(board == 0)[0])

            for m in self.moves:
                if loc not in m['pos']:
                    succ = deepcopy(board)
                    delta_loc = loc + m['delta']
                    succ[loc], succ[delta_loc] = succ[delta_loc], succ[loc]
                    succ_t = tuple(succ)
    
                    if previous_boards[succ_t]:
                        continue
    
                    previous_boards[succ_t] = True
    
                    hn = self.mhd(self.coor(succ_t), self.goalc)
                    state = np.append(
                        state,
                        np.array([(succ, m['move'], pos, gn, hn)], self.STATE),
                        0
                    )
                    priority = np.append(
                        priority,
                        np.array([(len(state) - 1, gn + hn)], self.PRIORITY),
                        0
                    )
                    # print(f'gn: {gn}, hn: {hn}')
                    if np.array_equal(succ, self.goal):
                        found = True
                        break
            if found:
                break
        
        last = len(state) - 1
        moves = []
        while last != -1:
            move = state[last]['move']    
            if move == 'u':
                moves.append([-1,0])
            if move == 'd':
                moves.append([1,0])
            if move == 'r':
                moves.append([0,1])
            if move == 'l':
                moves.append([0,-1])
            last = int(state[last]['parent'])
        moves.reverse()
        return moves

    @staticmethod
    def mhd(s, g):
        return sum((abs(s // 3 - g // 3) + abs(s % 3 - g % 3))[1:])

    @staticmethod
    def coor(s):
        c = np.array(range(9))
        for x, y in enumerate(s):
            c[y] = x
        return c