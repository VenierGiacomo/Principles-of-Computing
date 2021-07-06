# The Fifteen Puzzle

'''
Loyd's Fifteen puzzle (solver and visualizer)
note that solved configuration has the blank (zero) tile in upper left;
use the arrows key to swap this tile with its neighbors
'''

#classes of the game

class Puzzle:
    '''
    class representation for The Fifteen Puzzle
    '''

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        '''
        initialize puzzle with default height and width;
        returns a Puzzle object
        '''
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        '''
        generate string representation for puzzle;
        returns a string
        '''
        answer = ''
        for row in range(self._height):
            answer += str(self._grid[row])
            answer += '\n'
        return answer



    def get_height(self):
        '''
        getter for puzzle height; returns an integer
        '''
        return self._height

    def get_width(self):
        '''
        getter for puzzle width; returns an integer
        '''
        return self._width

    def get_number(self, row, col):
        '''
        getter for the number at tile position pos; returns an integer
        '''
        return self._grid[row][col]

    def set_number(self, row, col, value):
        '''
        setter for the number at tile position pos
        '''
        self._grid[row][col] = value

    def clone(self):
        '''
        make a copy of the puzzle to update during solving;
        returns a Puzzle object
        '''
        puzzle = Puzzle(self._height, self._width, self._grid)
        return puzzle



    def current_position(self, solved_row, solved_col):
        '''
        locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved;
        returns a tuple of two integers
        '''
        solved = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved:
                    return (row, col)
        assert False, 'Value ' + str(solved) + ' not found'

    def update_puzzle(self, move_string):
        '''
        updates the puzzle state based on the provided move string
        '''
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == 'l':
                assert zero_col > 0, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == 'r':
                assert zero_col < self._width - 1, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == 'u':
                assert zero_row > 0, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == 'd':
                assert zero_row < self._height - 1, 'move off grid: ' + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, 'invalid direction: ' + direction




    def lower_row_invariant(self, target_row, target_col):
        '''
        check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1);
        returns a boolean
        '''
    
        if self.get_number(target_row, target_col) == 0:
           
            for columns in range(target_col + 1, self.get_width()):
                if not (target_row, columns) == self.current_position(target_row, columns):
                    return False
        
            if not target_row + 1 == self.get_height():
                for columns_down in range(0, self.get_width()):
                    if not (target_row + 1, columns_down) == self.current_position(target_row + 1, columns_down):
                        return False
            return True

        return False

    def move(self, target_row, target_col, row, column):
        '''
        place a tile at target position;
        target tile's current position must be either above the target position
        (k < i) or on the same row to the left (i = k and l < j);
        returns a move string
        '''
        move = ''
        combo = 'druld'

        
        column_dif = target_col - column
        row_dif = target_row - row

       
        move += row_dif * 'u'
        
        if column_dif == 0:
            move += 'ld' + (row_dif - 1) * combo
        else:
           
            if column_dif > 0:
                move += column_dif * 'l'
                if row == 0:
                    move += (abs(column_dif) - 1) * 'drrul'
                else:
                    move += (abs(column_dif) - 1) * 'urrdl'
            
            elif column_dif < 0:
                move += (abs(column_dif) - 1)  * 'r'
                if row == 0:
                    move += abs(column_dif) * 'rdllu'
                else:
                    move += abs(column_dif) * 'rulld'
            
            move += row_dif * combo

        return move
            

    def solve_interior_tile(self, target_row, target_col):
        '''
        makes use of helper function move()
        updates puzzle and returns a move string
        '''
        assert self.lower_row_invariant(target_row, target_col)
      
        row, column = self.current_position(target_row, target_col)
        move = self.move(target_row, target_col, row, column)
        
        self.update_puzzle(move)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move
       
    def solve_col0_tile(self, target_row):
        '''
        solve tile in column zero on specified row (> 1);
        updates puzzle and returns a move string
        '''
        assert self.lower_row_invariant(target_row, 0)
        move = 'ur'       
        self.update_puzzle(move)

        
        row, column = self.current_position(target_row, 0)
       
        if row == target_row and column == 0:
           
            step = (self.get_width() - 2) * 'r'
            self.update_puzzle(step)
            move += step
        else:
           
            step = self.move(target_row - 1, 1, row, column)
            step += 'ruldrdlurdluurddlu' + (self.get_width() - 1) * 'r'
            self.update_puzzle(step)
            move += step

        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        return move


#secodn phase methonds 

    def row0_invariant(self, target_col):
        '''
        check whether the puzzle satisfies the row zero invariant at the given column (col > 1);
        returns a boolean
        '''
       
        if not self.get_number(0, target_col) == 0:
            return False

        for column in range(self.get_width()):
            for row in range(self.get_height()):
              
                if (row == 0 and column > target_col) or (row == 1 and column >= target_col) or row > 1:
                    if not (row, column) == self.current_position(row, column):
                        return False
                    
        return True
    

    def row1_invariant(self, target_col):
        '''
        check whether the puzzle satisfies the row one invariant at the given column (col > 1);
        returns a boolean
        '''
     
        if not self.lower_row_invariant(1, target_col):
            return False

     
        for column in range(0, self.get_width()):
            for row in range(2, self.get_height()):
                if not (row, column) == self.current_position(row, column):
                    return False

        return True
    

    def solve_row0_tile(self, target_col):
        '''
        solve the tile in row zero at the specified column;
        updates puzzle and returns a move string
        '''
        assert self.row0_invariant(target_col)
        move = 'ld'       
        self.update_puzzle(move)

       
        row, column = self.current_position(0, target_col)
       
        if row == 0 and column == target_col:
            return move
        else:
           
            step = self.move(1, target_col - 1, row, column)
            
            step += 'urdlurrdluldrruld'
            self.update_puzzle(step)
            move += step


        return move


    def solve_row1_tile(self, target_col):
        '''
        solve the tile in row one at the specified column;
        updates puzzle and returns a move string
        '''
        
        row, column = self.current_position(1, target_col)
        move = self.move(1, target_col, row, column)
        move += 'ur'
        
        self.update_puzzle(move)
        return move
    

# phase 3 methods

    def solve_2x2(self):
        '''
        solves the upper left 2x2 part of the puzzle;
        doesn't check for insolvable configuration!,
        updates the puzzle and returns a move string
        '''
       
        move = ''
        first_step = ''
              
        if self.get_number(1, 1) == 0:
            first_step += 'ul'
            self.update_puzzle(first_step)
           
            if (0, 1) == self.current_position(0, 1) and (1, 1) == self.current_position(1, 1):
                return first_step

           
            if self.get_number(0, 1) < self.get_number(1, 0):
                move += 'rdlu'
            else:
                move += 'drul'        
            self.update_puzzle(move)
            
        return first_step + move


    def solve_puzzle(self):
        '''
        generate a solution string for a puzzle;
        updates the puzzle and returns a move string
        '''
        move = ''

       
        row = self.get_height() - 1
        column = self.get_width() - 1
       
        curr_row, curr_col = self.current_position(0, 0)
        # calculate diff
        column_dif = curr_col - column
        row_dif = curr_row - row
        step = abs(column_dif) * 'r' + abs(row_dif) * 'd'
        self.update_puzzle(step)
        move += step

       
        for _ in range(row, 1, -1):
            for dummy in range(column, 0, -1):
                move += self.solve_interior_tile(_, dummy)
            move += self.solve_col0_tile(_)

       
        for _ in range(column, 1, -1):
            move += self.solve_row1_tile(_)
            move += self.solve_row0_tile(_)

        
        move += self.solve_2x2()
        return move


# start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
