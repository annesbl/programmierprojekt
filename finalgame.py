#imports
import sys
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QColor



#the board

class Board(QMainWindow):
    
    def __init__(self, m=5, n=5, k=4):  #initialisieren vom spielfeld
        super().__init__()
        
        self.m = m    #row
        self.n = n    #col
        self.k = k 
        self.player1_turn = True     #glaub das muss nicht unbedingt mit rein
        self.display()
        
    
        
    def display(self): #von beliz

        #titel
        self.setWindowTitle("4 Gewinnt")
        
        
        #plazieren und formatieren des fensters
        self.setGeometry(100, 100, 400, 400)
        
        
        #farbe der Kästchen
        blue_color = QColor("black")
        
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
                button.setStyleSheet(f"background-color: {blue_color.name()}")          #Kästchenfarbe
                button.clicked.connect(lambda _, r=row, c=col: self.place_symbol(r, c)) #methode zum klicken HIER NOCH METHODE PLACE_SYMBOL HINZUGEFÜGT
                button.setFixedSize(button_width, button_height)                        #Grösse der Kästchens
                row_buttons.append(button)                                              #row_buttons-Liste wird ergänzt
                self.layout.addWidget(button, row, col)                                 #Gitterlayout wird ergänzt
            self.buttons.append(row_buttons)                                            #buttons wird ergänzt

    

    """HABE ICH NEU HINZUGEFÜGT, DA ICH IN GAME DARAUF ZUGREIFEN MUSS"""
    #RUFT SYMBOL AUF SPIELFELD AB UM ZU SCHAUEN WELCHES SYMBOL AN DIESER STELLE IST
    def get_symbol(self, row, col): 
        button = self.buttons[row][col]
        return button.text()
    
    
    
    """HABE ICH IN DIE BOARD KLASSE HOCHGEHOLT, DA HIER AUCH DIE SYMBOLE GESETZT WERDEN"""
    #GEWINNÜBERPRÜFUNG
    def check_winner(self):
      for i in range(self.m):
        for r in range(self.n):
          symbol = self.get_symbol(i, r)
          if symbol != "":
            #horizontal
            if r + self.k <= self.n and all(self.get_symbol(i, r + c) == symbol for c in range(self.k)):
              return symbol
            #vertikal
            if i + self.k <= self.m and all(self.get_symbol(i + c, r) == symbol for c in range(self.k)):
              return symbol
            #diagonal \
            if r + self.k <= self.n and i + self.k < self.m and all(self.get_symbol(i +c, r + c) == symbol for c in range(self.k)):
              return symbol
            #diagonal /
            if r - self.k >= -1 and i + self.k <= self.m and all(self.get_symbol(i +c, r - c) == symbol for c in range(self.k)):
              return symbol
      return None
    
    
    
    """NEUE METHODE, DA ICH UNTEN DRAUF ZUGREIFE, HABE IM ENDEFFEKT DAS VON BELIZ UND MIR (WAS WIR JEWEILS EINZELN IN UNSEREN 
       KLASSEN HATTEN) IN EINER NEUEN METHODE ZUSAMMENGEFASST"""
    #PLATZIEREN DER SYMBOLE
    def place_symbol(self, row, col):
        #SCHAUT OB DAS FELD LEER IST
        if self.get_symbol(row, col) == "": 
            #SCHAUEN WER DRAN IST
            current_symbol = "x" if self.player1_turn else "o"  
            #TEXT DES BUTTENS DER GEWÄHLTEN POSITION WIRD ZU X ODER O UMGESCHRIEBEN
            self.buttons[row][col].setText(current_symbol)
            #ÜBERPRÜFUNG AUF GEWINNER DURCH DAS AUFRUFEN DER CHECK_WINNER METHODE
            winner = self.check_winner()
            #AUSGABE GEWINNER FALLS VORHANDEN
            if winner:
                print(f"Player {current_symbol} wins!")
            #WENN KEIN GEWINNER, DANN SPIELERWECHSEL
            self.player1_turn = not self.player1_turn
                
            
    #ÜBERNOMMEN VON VORHER                
    def is_board_full(self):
        #SCHLEIFEN DURCH DAS SPIELFELD
        for row in range(self.m):
            for col in range(self.n):
                #ÜBERPRÜFUNG JEDE ZEILE, OB VOLL ODER LEER
                button = self.buttons[row][col]
                if button.text() == "":
                    return False 
        #VOLL, WENN KEINE LEEREN ZEILEN --> UNENTSCHIEDEN
        return True                             
    
    
#VON JULE
class Player:
    def __init__(self, name, player_number):
        self.name = name
        self.player_number = player_number    
    
    
class Game:
    def __init__(self, board):# m=5, n=5, k=4)
        #SPEICHERT SPIELBRETT 
        self.board = Board() 
        #SYMBOL FÜR SPIELER 1
        self.player1_symbol = "x"
        #SYMBOL FÜR SPIELER 2
        self.player2_symbol = "o"
    
    #DIE MAKE MOVE METHODE KANN WEGGELASSEN WERDEN, DA WIR IN DER BOARD KLASSE PLACE_SYMBOL HABEN
    """def make_move(self, col):
        for row in range(self.board.m):
            #SCHAUT OB FELD LEER IST
            if self.board.get_symbol(row, col) == "":
                #WENN FELD LEER, SYMBOL VON SPIELER FESTLEGEN
                current_symbol = self.player1_symbol if self.board.player1_turn else self.player2_symbol
                #SYMBOL WIRD AUF GEWÜNSCHTE STELLE GESETZT
                self.board.place_symbol(row, col, current_symbol)
            return True
        return False"""
    
  
        
    def check_draw(self): #true wenn game over (bei spielbrett voll oder wenn ein spieler gewinnt)
      return self.board.is_board_full() or self.board.check_winner() is not None 

#ausführen ÜBERNOMMEN
    
if __name__ == "__main__":
    app = QApplication(sys.argv) 
    #BELIZ BOARD WIRD ERSTELLT
    window = Board()
    #ANZEIGE JETZT SCHON OBEN IN DER INIT METHODE VON BOARD --> BRETT WIRD ALSO AUTOMATISCH GEÖFFNET 
    #window.display() 
    #SPIELFENSTER WIRD ANGEZEIGT
    window.show()
    #ANWENDUNGSSCHLEIFE WIRD BEENDET
    sys.exit(app.exec_())




    
    
    
    
    
    
    
    