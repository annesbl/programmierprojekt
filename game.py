class Game:
  def __init__(self, board):# m=5, n=5, k=4)
    self.board = Board()  #speichert spielbrett dass game zugeordnet ist
    self.player1_turn = True  #verfolgt ob spieler 1 dran ist
    self.player1_symbol = "X"  #speichert symbole für jeweiligen spieler
    self.player2_symbol = "O"

  def switch_player_turn(self):
    self.player1_turn = not self.player1_turn #zug wechseln indem man funktion umkehrt
   

  def make_move(self, col):
    row = self.board.get_next_open_row(col) #gibt nächste verfügbare zeile in spiel zurück, wenn -1 also voll
    if row != -1: #überprüfen ob spalte voll ist
      current_symbol = self.player1_symbol if self.player1_turn else self.player2_symbol
      self.board.place_symbol(row, col, current_symbol)
      return True
    else:
      return False
    
  def check_winner(self):
    for i in range(self.board.m):
      for r in range(self.board.n):
        symbol = self.board.get_symbol(i, r)
        if symbol != "":
          #horizontal
          if r +3 < self.board.n and all(self.board.get_symbol(i, r + c) == symbol for c in range(4)):
            return symbol
          #vertikal
          if i +3 < self.board.m and all(self.board.get_symbol(i + c, r) == symbol for c in range(4)):
            return symbol
          #diagonal \
          if r + 3 < self.board.n and i + 3 < self.board.m and all(selfboard.get_symbol(i +c, r + c) == symbol for c in range(4)):
            return symbol
          #diagonal /
          if r - 3 >= 0 and i + 3 < self.board.m and all(self.board.get_symbol(i +c, r - c) == symbol for c in range(4)):
            return symbol
    return None
        
  def check_draw(self): #true wenn game over (bei spielbrett voll oder wenn ein spieler gewinnt)
    return self.board.is_board_full() or self.check_winner() is not none 

    
# Spiel-Schleife
while not game.check_draw():
    board.display()  # Zeigt das Spielbrett an
    col = int(input(f"Player {(1 if game.player1_turn else 2)}, enter column (0-4): "))  # Spieler wählt Spalte
    
    if not (0 <= col < board.n):  # Überprüfe, ob die ausgewählte Spalte gültig ist
        print("Invalid column! Please enter a valid column.")
        continue
    
    if not game.make_move(col):  # Führe den Spielzug aus
        print("Column is full! Please choose another column.")
        continue
    
    winner = game.check_winner()  # Überprüfe auf einen Gewinner
    if winner:
        board.display()
        print(f"Player {winner} wins!")
        break

if game.check_draw():  # Überprüfe auf ein Unentschieden
    board.display()
    print("It's a draw!")

    
