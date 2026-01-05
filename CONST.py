from board import board
HEIGHT = 810
WIDTH = 1170
TILE_SIZE_X = WIDTH  // 41
TILE_SIZE_Y = (HEIGHT - 50)// 29
#Wysokość grywalna (ilość kafelek) planszy - 4 kafelki, 2 na obrzeża góry i dołu
BOARD_HEIGHT = len(board) - 4
DIRECTION = None
#Początkowa pozycja Cap-Mana na mapie
STARTING_POSITION_X = 572
STARTING_POSITION_Y = 612