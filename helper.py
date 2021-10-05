from colors import * 
import pygame
import math

# Grid cell position is empty if it is equal to ''

class Grid:
    """Grid Interface
    """
    def __init__(self, rows = 3, cols = 3, cell_w = 100, cell_h = 100) -> None:
        """Initialize Grid

        Args:
            rows (int, optional): No. of rows in grid. Defaults to 3.
            cols (int, optional): No. of cols in grid. Defaults to 3.
            cell_w (int, optional): Cell width. Defaults to 100.
            cell_h (int, optional): Cell height. Defaults to 100.
        """
        self.rows = rows
        self.cols = cols
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.grid = [['' for _ in range(cols)] for _ in range(rows)]
        self.grid_pos = None
        self.font = pygame.font.SysFont(None, min(cell_w, cell_h))
        self.winner = None

    def reset(self):
        """Reset the grid and its attributes to default
        """
        self = self.__init__(self.rows, self.cols, self.cell_w, self.cell_h)

    def draw_grid(self, screen: pygame.Surface):
        """Display the grid in the pygame window

        Args:
            screen (pygame.Surface): Surface on which the grid has to be displayed
        """
        resX, resY = screen.get_width(), screen.get_height()
        self.grid_pos = posX, posY = (resX//2 - ((self.cell_h/2)*self.rows), resY//2 - ((self.cell_w/2)*self.cols))

        for i in range(self.rows):
            for j in range(self.cols):
                cell_posX, cell_posY = posX + i*self.cell_w, posY + j*self.cell_h
                pygame.draw.rect(screen, WHITE, pygame.Rect(cell_posX, cell_posY, self.cell_w, self.cell_h), width=1)
                if self.grid[i][j] != '':
                    text = self.font.render(self.grid[i][j].upper(), True, YELLOW)
                    text_rect = text.get_rect(center=(cell_posX + self.cell_w/2, cell_posY + self.cell_h/2))
                    screen.blit(text, text_rect)

    def get_cell_position(self, mouseX, mouseY):
        """Convert the provided mouse coordinate into corresponding grid cell position

        Args:
            mouseX (int): Mouse Pointer's x-coordinate
            mouseY (int): Mouse Pointer's y-coordinate

        Returns:
            tuple[int, int]: Cell position in grid
        """
        ''
        if not self.grid_pos:
            # Grid has not been initialized
            return None, None
        posX, posY = self.grid_pos
        rows, cols = self.rows, self.cols
        cell_w, cell_h = self.cell_w, self.cell_w

        if not (posX < mouseX < posX + rows*cell_w and posY < mouseY < posY + cols*cell_h):
            # Mouse Point is not inside the grid
            return None, None
        return int((mouseX-posX)//cell_w), int((mouseY-posY)//cell_h)

    def set(self, i, j, sign='O'):
        """Set grid[i][j] to sign

        Args:
            i (int): row
            j (int): column
            sign (str, optional): 'O' or 'X'. Defaults to 'O'.
        """
        self.grid[int(i)][int(j)] = sign

    def isEmpty(self):
        """Is there a empty cell left in grid?

        Returns:
            bool: True if some empty cell exists else False
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == '':
                    return True
        return False

    def winner_status(self):
        """Is there a winning position?

        Returns:
            bool | str: Returns False if there is no tie/win else returns winning player or tie
        """
        for i in range(len(self.grid)):
            'Row wise checking for any winning move'
            state = True
            for j in range(len(self.grid[i]) - 1):
                if self.grid[i][j] == '' or self.grid[i][j + 1] == '':
                    state = False
                if not state: break
                state = state and (self.grid[i][j] == self.grid[i][j + 1])
            if state: 
                self.winner = self.grid[i][0]
                return self.winner
        for j in range(len(self.grid[0])):
            'Col wise checking for any winning move'
            state = True
            for i in range(len(self.grid) - 1):
                if self.grid[i][j] == '' or self.grid[i + 1][j] == '':
                    state = False
                state = state and (self.grid[i][j] == self.grid[i + 1][j])
            if state:
                self.winner = self.grid[0][j]
                return self.winner
        diagonalState0 = True
        for i, j in zip(range(len(self.grid)-1), range(len(self.grid[0])-1)):
            if self.grid[i][j] == '' or self.grid[i + 1][j + 1] == '':
                diagonalState0 = False
            diagonalState0 = diagonalState0 and (self.grid[i][j] == self.grid[i + 1][j + 1])
        if diagonalState0:
            self.winner = self.grid[0][0]
            return self.winner

        diagonalState1 = True
        for i, j in zip(range(len(self.grid)-1, 0, -1), range(len(self.grid[0])-1)):
            if self.grid[i][j] == '' or self.grid[i - 1][j + 1] == '':
                diagonalState1 = False
            diagonalState1 = diagonalState1 and (self.grid[i][j] == self.grid[i - 1][j + 1])
        if diagonalState1: 
            self.winner = self.grid[0][-1]
            return self.winner
        
        if not self.isEmpty():
            self.winner = 'Tie'
            return self.winner
        return False


def miniMax(grid: Grid, ai, player, depth=8, maximize=True):
    if depth == 0:
        return 0, None
    elif not grid.winner_status():
        pass
    elif grid.winner_status() == ai:
        return 10, None
    elif grid.winner_status() == player:
        return -10, None
    elif grid.winner_status() == 'Tie':
        return 0, None

    best_move = None

    if maximize: # AI
        best_score = -math.inf
        for i in range(len(grid.grid)):
            for j in range(len(grid.grid[0])):
                if grid.grid[i][j] == '':
                    grid.grid[i][j] = ai
                    score, _ = miniMax(grid, ai, player, depth-1, maximize=False)
                    grid.grid[i][j] = ''
                    if score > best_score:
                        best_score = score
                        best_move = i, j
    else: # Player
        best_score = math.inf
        for i in range(len(grid.grid)):
            for j in range(len(grid.grid[0])):
                if grid.grid[i][j] == '':
                    grid.grid[i][j] = player
                    score, _ = miniMax(grid, ai, player, depth-1, maximize=True)
                    grid.grid[i][j] = ''
                    if score < best_score:
                        best_score = score
                        best_move = i, j
    return best_score, best_move



