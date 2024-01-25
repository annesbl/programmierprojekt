#imports
import time
import sys
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QColor
import random
from PyQt5.QtCore import QTimer, QCoreApplication


class Board(QMainWindow):                #beliz
    
    def __init__(self, m=5, n=5, k=4):  #initialisieren vom spielfeld
        super().__init__()
        
        self.m = m    #row
        self.n = n    #col
        self.k = k    
      
    
    #ERSTELLUNG DES SPIELBRETTES            
    def display(self, game):

        #titel
        self.setWindowTitle("4 Gewinnt")
        
        
        #plazieren und formatieren des fensters
        self.setGeometry(100, 100, 400, 400)
        
        
        #farbe der Kästchen
        black_color = QColor("black")
        
        #formatieren der Kästchen
        button_width = 80  # Breite jedes Kästchens
        button_height = 80  # Höhe jedes Kästchens
        
        
        #zentrales widget erstellen
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        #QGridLayout erstellen
        self.layout = QGridLayout(self.central_widget)


        #erstellen der Kästchen
        self.buttons = []
        
        for row in range(self.m):
            row_buttons = []
            for col in range(self.n):
                button = QPushButton()                                                  #neue Instanz einer QPushButton erstellen
                button.setStyleSheet(f"background-color: {black_color.name()}")         #Kästchenfarbe
                button.clicked.connect(lambda _, r=row, c=col: game.place_symbol(r, c)) #methode zum klicken + methode place_symbol aus Game
                button.setFixedSize(button_width, button_height)                        #Grösse der Kästchens
                row_buttons.append(button)                                              #row_buttons-Liste wird ergänzt
                self.layout.addWidget(button, row, col)                                 #Gitterlayout wird ergänzt
            self.buttons.append(row_buttons)                                            #buttons wird ergänzt
    
    
    #SPIELBRETT KOMPLETT SCHLIESSEN 
    def reset_board(self):
        for row in range(self.m):
            for col in range(self.n):
                self.buttons[row][col].setText("")  #setzt den Text jedes Buttons zurück
                
                   
        
        
class Player:                                  #jule
    def __init__(self, name, symbol):    #initialisierungen 
        self.name = name
        self.symbol = symbol   
        self.is_zufallski = False       
        self.is_einfacheki = False
        self.is_komplexeki = False
        
        
        
class ZufallsKI(Player):                       #anne
     
     def __init__(self, name, symbol, game):
         super().__init__(name, symbol)
         self.game = game
         self.is_zufallski = True
     
     
     #ZUG DER ZUFALLS KI
     def make_zufallski_move(self):
         while True:
             row = random.randint(0, self.game.board.m - 1)
             col = random.randint(0, self.game.board.n - 1)
             if self.game.get_symbol(row, col) == "":
                 self.game.place_symbol(row, col)
                 break
         

class EinfacheKI(Player):
    '''vergisst nicht self.is_einfacheki = True zu setzten'''
    '''wenn möglich die Make move methode der klasse make_einfacheki_move nennen'''
    pass

class KomplexeKI_test(Player):
    def __init__(self, name, symbol, game):
         super().__init__(name, symbol)
         self.game = game
         self.is_komplexeki = True
         
    def get_rechendaten_row(self):
        start_numbers_row = {}
        end_numbers_row = {}
        
        for row in range(self.m):
            start_number = row * self.n + 1 
            end_number = start_number + self.n -1
            start_numbers_row [row] = start_number
            end_numbers_row [row] = end_number
            
        return start_numbers_row, end_numbers_row
    
    def get_rechendaten_col(self):
        start_numbers_col = {}
        end_numbers_col = {}
        
        for col in range(self.n):
            start_number = col * self.m + 1 
            end_number = start_number + self.m -1
            start_numbers_col [col] = start_number
            end_numbers_col [col] = end_number
            
        return start_numbers_col, end_numbers_col
            
            
        
    def find_optimal_placement_attack(self):
        aktueller_stand = self.board.symbol.dict()
        row_start, row_end = self.get_rechendaten_row()
        col_start, col_end = self.get_rechendaten_col()
        
        for row in range (game.board.m):
            result_row = EinfacheKI.check_row(row, self.player.symbol)
            
    

    def make_move_for_row(self, player_symbol):
        for row in range(self.board.m):
            move = self.check_row(row, player_symbol)
            if move is not None:
                return move
        return None

    def make_move_for_column(self, player_symbol):
        for col in range(self.board.n):
            move = self.check_column(col, player_symbol)
            if move is not None:
                return move
        return None
        
        
        
    

    def check_row(self, row, player_symbol):
        for col in range(self.board.n - self.board.k + 1):
            symbols_in_row = [self.board.get_symbol(row, col + i) for i in range(self.board.k)]
            if (symbols_in_row.count(player_symbol) == self.board.k - 1 and '' not in symbols_in_row) or \
                    (col > 0 and col < self.board.n - self.board.k and
                    symbols_in_row[self.board.k // 2] == player_symbol and
                    symbols_in_row[self.board.k - 1] == player_symbol and
                    symbols_in_row[0] == ''):
                empty_index = symbols_in_row.index('')  
                return row, col + empty_index
        return None

    def check_column(self, col, player_symbol):
        for row in range(self.board.m - self.board.k + 1):
            symbols_in_column = [self.board.get_symbol(row + i, col) for i in range(self.board.k)]
            if (symbols_in_column.count(player_symbol) == self.board.k - 1 and '' not in symbols_in_column) or \
                    (row > 0 and row < self.board.m - self.board.k and
                    symbols_in_column[self.board.k // 2] == player_symbol and
                    symbols_in_column[self.board.k - 1] == player_symbol and
                    symbols_in_column[0] == ''):
                empty_index = symbols_in_column.index('')  
                return row + empty_index, col
        return None
        
        
        
        
                
        
    def find_optimal_placement_defense(self):
         pass
    def make_einfacheki_move (self):
        move = self.game.make_move_for_column(self.symbol) or self.game.make_move_for_row(self.symbol)
        if move is not None:
            row, col = move
            self.game.place_symbol(row, col)

'''
# Beispiel für die Verwendung der KI in Ihrer Game-Klasse
if self.current_player.is_zufallski:
    self.current_player.make_zufallski_move()
    '''
    
    
class KomplexeKI(Player):
    def __init__(self, name, symbol, game):
         super().__init__(name, symbol)
         self.game = game
         self.is_komplexeki = True

    def make_komplexeki_move(self, game_board):

        # Check for a winning move
        for row in range(game_board.m):
            for col in range(game_board.n):
                if game_board.board[row][col] == ' ':
                    game_board.board[row][col] = self.symbol
                    if self.check_win(game_board):
                        return

                    game_board.board[row][col] = ' '

        # Check for a blocking move
        opponent_symbol = 'O' if self.symbol == 'X' else 'X'
        move_made = False

        # Check rows and columns
        for i in range(game_board.m):
            if self.make_blocking_move(game_board, i, opponent_symbol):
                move_made = True
                break
            if self.make_blocking_move(game_board, i, self.symbol):
                move_made = True
                break

        # Check diagonals
        if not move_made and self.make_blocking_move(game_board, -1, opponent_symbol):  # Main diagonal
            move_made = True
        elif not move_made and self.make_blocking_move(game_board, 1, opponent_symbol):   # Anti-diagonal
            move_made = True
        elif not move_made and self.make_blocking_move(game_board, -1, self.symbol):      # Main diagonal for self
            move_made = True
        elif not move_made and self.make_blocking_move(game_board, 1, self.symbol):        # Anti-diagonal for self
            move_made = True

        # If neither winning nor blocking, make a strategic move
        if not move_made:
            self.make_strategic_move(game_board)

def make_blocking_move(self, game_board, index, symbol):
    # Check for blocking move in rows, columns, or diagonals
    if index == -1:
        # Main diagonal
        if game_board.board[0][0] == ' ' and game_board.board[1][1] == symbol and game_board.board[2][2] == symbol:
            game_board.board[0][0] = self.symbol
            return True
    elif index == 1:
        # Anti-diagonal
        if game_board.board[0][2] == ' ' and game_board.board[1][1] == symbol and game_board.board[2][0] == symbol:
            game_board.board[0][2] = self.symbol
            return True
    else:
        # Rows and columns
        for i in range(game_board.m):
            if game_board.board[i][index] == ' ' and game_board.board[i][(index + 1) % game_board.n] == symbol and \
                    game_board.board[i][(index + 2) % game_board.n] == symbol:
                game_board.board[i][index] = self.symbol
                return True
            if game_board.board[index][i] == ' ' and game_board.board[(index + 1) % game_board.m][i] == symbol and \
                    game_board.board[(index + 2) % game_board.m][i] == symbol:
                game_board.board[index][i] = self.symbol
                return True

    # If no blocking move is made, return False
    return False


    def make_strategic_move(self, game_board):
        # Implement your strategic move logic here
        # Example: Try to occupy the center if available, else pick a corner
        center = (game_board.m // 2, game_board.n // 2)
        if game_board.board[center[0]][center[1]] == ' ':
            game_board.board[center[0]][center[1]] = self.symbol
        else:
            # Implement other strategic moves
            # ...
            self.make_random_move(game_board)

    def make_random_move(self, game_board):
        # Implement making a random move
        # ...
        while True:
             row = random.randint(0, self.game.board.m - 1)
             col = random.randint(0, self.game.board.n - 1)
             if self.game.get_symbol(row, col) == "":
                 self.game.place_symbol(row, col)
                 break

    def check_win(self, game_board, symbol=None):
        symbol = symbol or self.symbol
        if game.check_winner() == True:
            return True
        else:
            return False




    
class Game:                                                          
    def __init__(self, m, n, k, player1, player2):                                    
        self.player1 = player1
        self.player2 = player2
        self.board = Board(m, n, k)         #Initialisierung von self.board
        self.board.display(self)            #Übergeben des 'self'-Objekts an die display-Methode
        
        self.current_player = self.player1  #starten mit Spieler 1
        
        #Überprüfung, ob Startspieler == KI --> falls ja: automatischen Zug machen
        #zufalls KI
        if self.current_player.is_zufallski:
            QTimer.singleShot(100, self.current_player.make_zufallski_move)
        #einfache KI
        elif self.current_player.is_einfacheki:
            QTimer.singleShot(100, self.current_player.make_einfacheki_move)
        #komlexe KI
        elif self.current_player.is_komplexeki:
            QTimer.singleShot(100, self.current_player.make_komplexeki_move)
        
        
    #RUFT SYMBOL AUF SPIELFELD AB UM ZU SCHAUEN WELCHES SYMBOL AN DIESER STELLE IST    anne
    def get_symbol(self, row, col):                  
        button = self.board.buttons[row][col]
        return button.text()


    #PLATZIEREN DER SYMBOLE                  anne, beliz   
    def place_symbol(self, row, col): 
        if self.get_symbol(row, col) == "":          #prüft ob das Kästchen leer ist
            
            #entscheiden wer dran ist und das jeweilige Symbol wählen
            self.board.buttons[row][col].setText(self.current_player.symbol)
            
            
            #überprüfung: Spielende?
            winner = self.check_winner()    #wenn von check winner ein symbol zurückgegeben wird, wurde das spiel von diesem symbol gewonnen.
            
            #ausgabe gewinner (falls vorhanden)
            if winner:
                self.board.close()  #Schließt das Fenster
            
            #gleichstand
            elif self.is_board_full() == True:
                self.board.close()  #Schließt das Fenster
            
            #kein gewinner
            elif winner == None:
            
                #spielerwechsel (falls kein gewinner/gleichstand vorhanden)
                self.current_player = self.player1 if self.current_player == self.player2 else self.player2
            
                #überprüfen, ob der neue aktuelle Spieler eine KI ist
                #zufalls KI
                if self.current_player.is_zufallski:
                    QTimer.singleShot(100, self.current_player.make_zufallski_move)
                #einfache KI
                elif self.current_player.is_einfacheki:
                    QTimer.singleShot(100, self.current_player.make_einfacheki_move)
                #komlexe KI
                elif self.current_player.is_komplexeki:
                    QTimer.singleShot(100, self.current_player.make_komplexeki_move)
            
            
            
            
    #GEWINNÜBERPRÜFUNG                       anne, beliz
    def check_winner(self):                  
      for i in range(self.board.m):
        for r in range(self.board.n):
          symbol = self.get_symbol(i, r)
          if symbol != "":
              
            #in den folgenden 4 fällen wurde die gleiche logik angewendet, weshalb nur eins der 4 besipiele näher erläutert werden
            #horizontal
                count_h = 0                              #Anzahl der gleichen symbole (nebeneinandeer) in einer Reihe zählen bzw speichern
                for c in range(r, self.board.n):         #das spielfeld horizontal durchgehen (nur zeilen durchgehen)
                    if self.get_symbol(i, c) == symbol:  #gucken, ob das aktuelle symbol zu finden ist
                        count_h += 1                     #ist das symbol in der reihe! -> +1 auf count_h addiren
                        if count_h >= self.board.k:      #sind mehr oder genau k symbole nebeneinander (count_h grösser gleich k), so gewonnen 
                            return symbol                #gewonnenes symbol wird zurück gegeben
                    else:
                        break                            #nicht mindestens k gleiche symbole nebneinander
                    
            #vertikal
                count_v = 0                              
                for c in range(i, self.board.m):
                    if self.get_symbol(c, r) == symbol:  
                        count_v += 1                     
                        if count_v >= self.board.k:      
                            return symbol                
                    else:
                        break                            
                    
            # Diagonal absteigend (\)
                count_d1 = 0                             
                for c in range(self.board.k):
                    if i + c < self.board.m and r + c < self.board.n and self.get_symbol(i + c, r + c) == symbol:
                        count_d1 += 1
                        if count_d1 >= self.board.k:
                            return symbol
                    else:
                        break

            # Diagonal aufsteigend (/)
                count_d2 = 0
                for c in range(self.board.k):
                    if i - c >= 0 and r + c < self.board.n and self.get_symbol(i - c, r + c) == symbol:
                        count_d2 += 1
                        if count_d2 >= self.board.k:
                            return symbol
                    else:
                        break

        
  
    
    #UEBERPRUEFT AUF GLEICHSTAND             beliz
    def is_board_full(self):               
        #schleifen durch das Spielfeld
        for row in range(self.board.m):
            for col in range(self.board.n):
                #Ueberpruefen jeder Zeile, ob voll oder leer
                button = self.board.buttons[row][col]
                if button.text() == "":
                    return False          #brett nicht voll
        return True                       #brett voll -> unentschieden 
    
    
    
    
    
    
    
#Spiel durchlaufen                                     beliz
def play_game(game):
    
    #GUI aufrufen und durchlaufen
    game.board.show()  
    app.exec_()        
    
    #winner für die runde festhalten
    winner = game.check_winner()
    
    #Spielbrett schliessen/zurücksetzen
    game.board.reset_board()  
    game.board.close()
    
    #gewinner zurückgeben
    return winner

#Ausführen                                              beliz
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #definieren Spieler
    player_mensch = Player("Max", "x")
    player_mensch2 = Player("Tom", "o") 
    player_zufallski = ZufallsKI("Zufalls KI", "o", None)
    player_zufallski2 = ZufallsKI("Zufalls KI 2", "x", None)
    #player_einfacheki = EinfacheKI("Einfache KI", "o", None)
    #player_einfacheki2 = EinfacheKI("Einfache KI 2", "x", None)
    player_komplexeki = KomplexeKI("Einfache KI", "o", None)
    #player_komplexeki2 = KomplexeKI("Einfache KI 2", "x", None)
    
    #Player1 und Player2 wählen (2 der oben gennanten namen wählen - auf "x" und "o" achten)
    player1 = player_mensch
    player2 = player_komplexeki
    
    play_several_times = False
    num_games = 5  # Anzahl der Spiele
    
    #Gewinnzählung in einem dictionary
    wins = {player1.name: 0, player2.name: 0, "Unentschieden": 0}


    if play_several_times:                                           #mehrere male durchlaufen --> für Data Science Fragen
        for _ in range(num_games):                                   #für jedes game einmal die Schleife durchlaufen
            
            #game klasse aufrufen und m,n,k,player1,player2 wählen
            game = Game(5, 5, 4, player1, player2)
            
            #KIs richtig zuweisen
            player_zufallski.game = game #zufallski
            player_zufallski2.game = game #zufallski
            #player_einfacheki.game = game #einfacheki
            #player_einfacheki2.game = game #einfacheki
            #player_komplexeki.game = game #komplexeki
            #player_komplexeki2.game = game #komplexeki
            
            #Spiel starten
            winner = play_game(game)           #spiel läuft und gibt einen gewinner (x bzw o) wieder

            #gewinne zählen  - jede runde wird ein gewinner draufaddiert
            if winner == player1.symbol:
                wins[player1.name] += 1       # +1 wenn player 1 gewinnt
            elif winner == player2.symbol:
                wins[player2.name] += 1       # +1 wenn player 2 gewinnt
            elif winner is None:
                wins["Unentschieden"] += 1    # +1 wenn unendschieden 

            #Pause
            time.sleep(0.15)
            
        
        #Gewinne ausgeben nachdem alle spiele gelaufen sind und die Schleife verlassen wurde
        print(wins)


            
    else:                           #ein einziges Spiel
        #game klasse aufrufen und m,n,k wählen
        game = Game(5, 5, 4, player1, player2)
        
        #KIs richtig zuweisen
        player_zufallski.game = game #zufallski
        player_zufallski2.game = game #zufallski
        #player_einfacheki.game = game #einfacheki
        #player_einfacheki2.game = game #einfacheki
        player_komplexeki.game = game #komplexeki
        #player_komplexeki2.game = game #komplexeki
        
        #Spiel starten
        play_game(game)
        

