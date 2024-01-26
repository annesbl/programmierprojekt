# class EinfacheKI(Player):
#     '''vergisst nicht self.is_einfacheki = True zu setzten'''
#     '''wenn möglich die Make move methode der klasse make_einfacheki_move nennen'''
#     def __init__(self, name, symbol, game):
#         super().__init__(name, symbol)
#         self.game = game
#         self.is_einfacheki = True

#     def make_einfacheki_move(self):
#         if self.game.is_board_empty():
#             row = random.randint(0, self.game.board.m - 1)
#             col = random.randint(0, self.game.board.n - 1)
#             if self.game.get_symbol(row, col) == "":
#                 self.game.place_symbol(row, col)
#         else:
#             row, col = self.find_strategic_move()

#         # Symbol setzen
#         self.game.place_symbol(row, col)       

#     def find_strategic_move(self):
#         for r in range(self.game.board.m):
#             for c in range(self.game.board.n):
#                 if self.game.get_symbol(r, c) == self.symbol:
#                     # Prüfen, ob rechts Platz ist
#                     if c + 1 < self.game.board.n and self.game.get_symbol(r, c + 1) == "":
#                         return r, c + 1
#                     # Prüfen, ob links Platz ist
#                     elif c - 1 >= 0 and self.game.get_symbol(r, c - 1) == "":
#                         return r, c - 1
#                     # Prüfen, ob unten Platz ist
#                     elif r + 1 < self.game.board.m and self.game.get_symbol(r + 1, c) == "":
#                         return r + 1, c
#                     # Prüfen, ob oben Platz ist
#                     elif r - 1 >= 0 and self.game.get_symbol(r - 1, c) == "":
#                         return r - 1, c
#                     # Prüfen, ob diagonal unten rechts Platz ist
#                     elif r + 1 < self.game.board.m and c + 1 < self.game.board.n and self.game.get_symbol(r + 1, c + 1) == "":
#                         return r + 1, c + 1
#                     # Prüfen, ob diagonal oben links Platz ist
#                     elif r - 1 >= 0 and c - 1 >= 0 and self.game.get_symbol(r - 1, c - 1) == "":
#                         return r - 1, c - 1
#                     # Prüfen, ob diagonal unten links Platz ist
#                     elif r + 1 < self.game.board.m and c - 1 >= 0 and self.game.get_symbol(r + 1, c - 1) == "":
#                         return r + 1, c - 1
#                     # Prüfen, ob diagonal oben rechts Platz ist
#                     elif r - 1 >= 0 and c + 1 < self.game.board.n and self.game.get_symbol(r - 1, c + 1) == "":
#                         return r - 1, c + 1

#         # Falls keine intelligenten Züge gefunden wurden, setze zufällig
#         empty_positions = [(r, c) for r in range(self.game.board.m) for c in range(self.game.board.n) if self.game.get_symbol(r, c) == ""]
#         return random.choice(empty_positions)



import time
import sys
import PyQt5
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
    def __init__(self, name, symbol, game):
        super().__init__(name, symbol)
        self.game = game
        self.is_einfacheki = True
        self.first_move = True  # Initialize the first_move flag
        
        
    def make_einfacheki_move(self):
        if self.first_move:                                 #falls es der erste move ist ist first_move = True gesetzt
            row = random.randint(0, self.game.board.m - 1)  #row des buttons (für den ersten zug) zufällig festlegen
            col = random.randint(0, self.game.board.n - 1)  #col des buttons (für den ersten zug) zufällig festlegen
            #self.game.place_symbol(row,col)        
            self.first_move = False                         #wird auf False gesetzt, nachdem der first move gemacht worden ist
        else:                                               #falls es nicht der erste zug der KI ist:
            row, col = self.find_strategic_move()           #find_strategic_move findet ein leeren Button und gint diesen zurück -> wird ind row, col gespeichert

        # Symbol setzen                            
        self.game.place_symbol(row, col)                    #plaziert symbol auf bei col, row (die im vorherigen schritt festgelegt wurden)

        # Überprüfen, ob das Spiel vorbei ist      - ist das nicht schon durch place_symbol? weil in der place_symbol methode gibt es das, und jetzt machen wir es nochmal?
        winner = self.game.check_winner() 
        if winner:
            print(f"Spieler {self.name} hat gewonnen!")
            self.game.board.close()
        elif self.game.is_board_full():
            print("Unentschieden!")
            self.game.board.close()
    
    def find_strategic_move(self):
        max_length = 0
        best_move = None
        #es wird nur Ort des leeren Buttons zruück gegeben, jedoch noch kein symbol plaziert
        for r in range(self.game.board.m):
            for c in range(self.game.board.n):
                if self.game.get_symbol(r, c) == self.symbol:
                    # Prüfen, ob rechts Platz ist
                    if c + 1 < self.game.board.n and self.game.get_symbol(r, c + 1) == "":
                        return r, c + 1
                    # Prüfen, ob links Platz ist
                    elif c - 1 >= 0 and self.game.get_symbol(r, c - 1) == "":
                        return r, c - 1
                    # Prüfen, ob unten Platz ist
                    elif r + 1 < self.game.board.m and self.game.get_symbol(r + 1, c) == "":
                        return r + 1, c
                    # Prüfen, ob oben Platz ist
                    elif r - 1 >= 0 and self.game.get_symbol(r - 1, c) == "":
                        return r - 1, c
                    # Prüfen, ob diagonal unten rechts Platz ist
                    elif r + 1 < self.game.board.m and c + 1 < self.game.board.n and self.game.get_symbol(r + 1, c + 1) == "":
                        return r + 1, c + 1
                    # Prüfen, ob diagonal oben links Platz ist
                    elif r - 1 >= 0 and c - 1 >= 0 and self.game.get_symbol(r - 1, c - 1) == "":
                        return r - 1, c - 1
                    # Prüfen, ob diagonal unten links Platz ist
                    elif r + 1 < self.game.board.m and c - 1 >= 0 and self.game.get_symbol(r + 1, c - 1) == "":
                        return r + 1, c - 1
                    # Prüfen, ob diagonal oben rechts Platz ist
                    elif r - 1 >= 0 and c + 1 < self.game.board.n and self.game.get_symbol(r - 1, c + 1) == "":
                        return r - 1, c + 1
                if self.game.get_symbol(r, c) == "":
                    length = self.calculate_chain_length(r, c)
                    if length > max_length:
                        max_length = length
                        best_move = (r, c)

        if best_move is not None:
            return best_move

        # Falls keine intelligenten Züge gefunden wurden, setze zufällig
        empty_positions = [(r, c) for r in range(self.game.board.m) for c in range(self.game.board.n) if self.game.get_symbol(r, c) == ""]
        return random.choice(empty_positions)

    def calculate_chain_length(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertikal, diagonal absteigend, diagonal aufsteigend
        max_length = 0

        for dr, dc in directions:
            length = 1
            for i in range(1, self.game.board.k):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < self.game.board.m and 0 <= c < self.game.board.n and self.game.get_symbol(r, c) == self.symbol:
                    length += 1
                else:
                    break

            for i in range(1, self.game.board.k):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < self.game.board.m and 0 <= c < self.game.board.n and self.game.get_symbol(r, c) == self.symbol:
                    length += 1
                else:
                    break

            if length >= self.game.board.k:
                return length

            if length > max_length:
                max_length = length

        return max_length
    
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
        #komlexe KI6
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
    
    #UEBERPRUEF OB DAS BOARD LEER IST        anne
    def is_board_empty(self):
        for row in range(self.board.m):                
            for col in range(self.board.n):
                if self.get_symbol(row, col) != "":    #überprüfen ob NICHT leer
                    return False                       # falls NICHT leer -> False zurückgeben
        return True
    
    
    
    
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
    player_einfacheki = EinfacheKI("Einfache KI", "o", None)
    #player_einfacheki2 = EinfacheKI("Einfache KI 2", "x", None)
    #player_komplexeki = KomplexeKI("Komplexe KI", "o", None)
    # Weitere Spielerinitialisierungen und Spiellogik
    #player_komplexeki2 = KomplexeKI("Einfache KI 2", "x", None)
    
    #Player1 und Player2 wählen (2 der oben gennanten namen wählen - auf "x" und "o" achten)
    player1 = player_mensch
    player2 = player_einfacheki
    
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
            player_einfacheki.game = game #einfacheki
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
        player_einfacheki.game = game #einfacheki
        #player_einfacheki2.game = game #einfacheki
        #player_komplexeki.game = game #komplexeki
        #player_komplexeki2.game = game #komplexeki
        
        #Spiel starten
        play_game(game)
        

