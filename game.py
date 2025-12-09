class Game:
  def __init__(self, board):
    self.board = board
    self.current_player = 1   # PLAYER = 1, AI = 2

  def player_move(self, dim, row, col):
    if not self.board.isSquareAvailable(dim, row, col):
      return False

    self.board.markSquare(dim, row, col, self.current_player)

    if self.board.checkWin(self.current_player):
      print("Player wins!")
      return True
      
    # ai turn next
    self.current_player = 2
    return True

  def ai_move(self):
    from ai.minimax import bestMove
      
    moved = bestMove(self.board)
    if not moved:
      print("AI has no moves (draw)")
      return

    if self.board.checkWin(2):
      print("AI wins!")

    self.current_player = 1