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
         

class EinfacheKI(Player):           #jule
    '''vergisst nicht self.is_einfacheki = True zu setzten'''
    '''wenn möglich die Make move methode der klasse make_einfacheki_move nennen'''
    def __init__(self, name, symbol, game):
         super().__init__(name, symbol)
         self.game = game
         self.is_einfacheki = True
         
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
        
        #waagerechte Zeilen gewinnen
    def waagerechte_zeilen(self, symbol, col):
        for row in range(self.board.m - self.board.k + 1):
            symbols_in_column = [self.board.get_symbol(row + i, col) for i in range(self.board.k)]
            if symbols_in_column.count(player_symbol) == self.board.k - 1 and '' not in symbols_in_column:
                return True
            return False
        
    def senkrechte_zeilen(self, symbol, row):
        for col in range(self.board.n - self.board.k + 1):
            symbols_in_row = [self.board.get_symbol(row , col + 1) for i in range(self.board.k)]
            if symbols_in_column.count(player_symbol) == self.board.k - 1 and '' not in symbols_in_column:
                return True
            return False
        
        
        
        
                
        
    def find_optimal_placement_defense(self):
         
    def make_einfacheki_move (self):
        
        

class KomplexeKI(Player):
    '''vergisst nicht self.is_komplexeki = True zu setzten'''
    '''wenn möglich die Make move methode der klasse make_komplexeki_move nennen'''
    pass



    
class Game:                                    
    def __init__(self, m, n, k, player1, player2):                                    
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1  # Start mit Spieler 1
        self.board = Board(m, n, k)  #Initialisierung von self.board
        self.board.display(self)     #Übergeben des 'self'-Objekts an die display-Methode
        
        
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
                
    def symbol_dict(self):      #jule
        symbole_dict = {}
        count = 1
        for row in range(self.board.m):
            for col in range (self.board.n):
                symbol = self.get_symbol(row, col)
                symbole_dict[count] = symbol
                count += 1
        return symbole_dict
            
            
            
            
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
    





#ausführen 
    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    player1 = Player("Max", "x")
    player2 = Player("Tom", "o") 
    player3 = ZufallsKI("Zufalls KI", "o", None)  
    #player4 = EinfacheKI("Einfache KI", "o", None)
    #player5 = KomplexeKI("Einfache KI", "o", None)
    
    game = Game(5, 5, 4, player1, player3)
    
    player3.game = game #zufallski
    #player4.game = game #einfacheki
    #player5.game = game #komplexeki
    
    game.board.show()
    sys.exit(app.exec_())