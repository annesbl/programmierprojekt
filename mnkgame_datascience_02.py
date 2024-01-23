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
    def __init__(self, name, symbol):
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

class KomplexeKI(Player):
    '''vergisst nicht self.is_komplexeki = True zu setzten'''
    '''wenn möglich die Make move methode der klasse make_komplexeki_move nennen'''
    pass



    
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
            
            time.sleep(0.2)
            
            #überprüfung: Spielende?
            winner = self.check_winner()    #wenn von check winner ein symbol zurückgegeben wird, wurde das spiel von diesem symbol gewonnen.
            #ausgabe gewinner (falls vorhanden)
            if winner:
                print(f"{self.current_player.name} wins!")
                self.board.close()  #Schließt das Fenster
            #gleichstand
            elif self.is_board_full() == True:
                print("No one winns")
                self.board.close()  #Schließt das Fenster
            
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
              
            #horizontal
                count_h = 0                              #Anzahl der gleichen symbole in einer Reihe zählen
                for c in range(r, self.board.n):
                    if self.get_symbol(i, c) == symbol:
                        count_h += 1                     #wird ein
                        if count_h >= self.board.k:
                            return symbol
                    else:
                        break
                    
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
    #player_komplexeki = KomplexeKI("Einfache KI", "o", None)
    
    #Player1 und Player2 definieren
    player1 = player_mensch2
    player2 = player_zufallski2
    
    play_several_times = False
    num_games = 5  # Anzahl der Spiele
    
    #Gewinnzählung
    wins = {player1.name: 0, player2.name: 0, "Unentschieden": 0}


    if play_several_times:
        for _ in range(num_games):
            
            #game klasse aufrufen und m,n,k,player1,player2 wählen
            game = Game(5, 5, 4, player1, player2)
            
            #KIs richtig zuweisen
            player1.game = game #zufallski
            player2.game = game #zufallski
            #player4.game = game #einfacheki
            #player5.game = game #komplexeki
            
            #Spiel starten
            winner = play_game(game)

            #gewinne zählen
            if winner == player1.name:
                wins[player1.name] += 1
            elif winner == player2.name:
                wins[player2.name] += 1
            else:
                wins["Unentschieden"] += 1

            #Pause
            time.sleep(0.5)
            
        # Gewinne ausgeben
        for player, win_count in wins.items():
            print(f"{player} hat {win_count} Spiele gewonnen")
            
    else:
        #game klasse aufrufen und m,n,k,player1,player2 wählen
        game = Game(5, 5, 4, player1, player2)
        
        #KIs richtig zuweisen
        player1.game = game #zufallski
        player2.game = game #zufallski
        #player4.game = game #einfacheki
        #player5.game = game #komplexeki
        
        #Spiel starten
        play_game(game)
        

