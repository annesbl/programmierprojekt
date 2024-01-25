#imports
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
            
            #überprüfung: Spielende?
            winner = self.check_winner()
            #ausgabe gewinner (falls vorhanden)
            if winner:
                print(f"{self.current_player.name} wins!")
                self.board.close()  #Schließt das Fenster
            #gleichstand
            elif self.is_board_full() == True:
                print("No one winns")
                self.board.close()  #Schließt das Fenster
            
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
            
            
            
            
    #GEWINNÜBERPRÜFUNG                       anne
    def check_winner(self):                  
      for i in range(self.board.m):
        for r in range(self.board.n):
          symbol = self.get_symbol(i, r)
          if symbol != "":
            #horizontal
            if r + self.board.k <= self.board.n and all(self.get_symbol(i, r + c) == symbol for c in range(self.board.k)):
              return symbol
            #vertikal
            if i + self.board.k <= self.board.m and all(self.get_symbol(i + c, r) == symbol for c in range(self.board.k)):
              return symbol
            #diagonal \
            if r + self.board.k <= self.board.n and i + self.board.k < self.board.m and all(self.get_symbol(i +c, r + c) == symbol for c in range(self.board.k)):
              return symbol
            #diagonal /
            if r - self.board.k >= -1 and i + self.board.k <= self.board.m and all(self.get_symbol(i +c, r - c) == symbol for c in range(self.board.k)):
              return symbol
      return None
        
  
    
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
    
    
    
    #DURCHLAUF DES SPIELES OHNE GUI --> um werte für die data Science fragen zu sammeln       beliz
    def play_game(self, player1, player2):
        self.board.reset_board()       #Spielbrett zurücksetzen
        self.current_player = player1  #Startspieler festlegen

        while not self.check_winner() and not self.is_board_full(): #sichergehen, dass niemand gewonnen hat oder gleichstand ist
            #überprüfen welche KI und Zug machen
            if isinstance(self.current_player, ZufallsKI):    #Zufalls KI
                self.current_player.make_zufallski_move()
            elif isinstance(self.current_player, EinfacheKI): #Einfache KI
                self.current_player.make_einfacheki_move()
            elif isinstance(self.current_player, KomplexeKI): #Komplexe KI
                self.current_player.make_komplexeki_move()
            
            #spieler wechsel
            #self.current_player = player1 if self.current_player == player2 else player1
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

        winner = self.check_winner()  #gewinner zurückgeben
          
        if winner:
            #gewinner-Namen zurückgeben
            return self.player1.name if self.player1.symbol == winner else self.player2.name
        else:
            #none für unendschieden
            return None
    
    
    
    #SPIEL OHNE GUI SO OFT DURCHLAUFEN LASSEN WIE MAL WILL                   beliz
    def play_multiple_games(self, player1, player2, num_games):
        
        #liste, die die Siege zählt
        results = {
        player1.name: 0,  #Siege von Player1
        player2.name: 0,  #Siege von Player 2
        "Draws": 0        #Gleichstand
        }

        for _ in range(num_games):                             #durchlaufen je nachdem welchen wert man num_games zugewiesen hat
            winner = self.play_game(player1, player2)          #einen gewinner der runde festlegen
            if winner:                                         
                results[winner] += 1                           #dem gewinner einen Winn drauf addieren
            else:
                results["Draws"] += 1                          #gleichstände zählen
                
        return results


#ausführen
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #definieren Spieler
    player1 = Player("Max", "x")
    player2 = Player("Tom", "o") 
    player3 = ZufallsKI("Zufalls KI", "o", None)
    player33 = ZufallsKI("Zufalls KI 2", "x", None)
    #player4 = EinfacheKI("Einfache KI", "o", None)
    #player5 = KomplexeKI("Einfache KI", "o", None)
    
    play_with_gui = False
    
    if play_with_gui == True:        #führt spiel mit GUI aus
        
        #game klasse aufrufen
        game = Game(5, 5, 4, player33, player3) 
        
        #KIs richtig zuweisen
        player3.game = game #zufallski
        player33.game = game #zufallski
        #player4.game = game #einfacheki
        #player5.game = game #komplexeki
        
        #GUI aufrufen und durchlaufen
        game.board.show()
        sys.exit(app.exec_())
    
    elif play_with_gui == False:     #fürht spiel ohne GUI aus
        
        #anzahl der Spiele
        num_games = 1000
        
        #game klasse aufrufen
        game = Game(5, 5, 4, player33, player3)
        
        #KIs richtig zuweisen 
        player3.game = game #zufallski
        player33.game = game #zufallski
        #player4.game = game #einfacheki
        #player5.game = game #komplexeki  
        
        #durchlaufen
        results = game.play_multiple_games(player33, player3, num_games)
        
        #Ergebnisse ausgeben
        for player_name, wins in results.items():
            print(f"{player_name}: {wins} Spiele gewonnen")

