# programmierprojekt
#unser super tolles Projekt
import numpy as np
class Game:
  def __init__(self, board, player1, player2, m=5, n=5, k=4):
    self.m = m
    self.n = n
    self.k = k
    self.board = Board(m, n, k)
    self.player1 = Player(1)
    self.player2 = Player(2)

def start():
  
  pass

def game_loop():
  pass

    


class Board:
  def __init__(self, array, m=5, n=5, k=4):
    self.m = m
    self.n = n
    self.k = k
    self.array = np.array(shape=(m,n))


  def display():
    
    pass


  def has_won():
    pass
    
  

  
class Player:
  def __init__(self, player_number, name):
    self.player_number = player_number
    self.name = name


def make_move(Board):
  pass



class MyBot(Player):
  def __init__(self):
    super().__init__(self)
    pass





 
