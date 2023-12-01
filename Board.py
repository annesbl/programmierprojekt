#imports
import sys
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QColor



#the board

class Board(QMainWindow):
    
    def __init__(self, m=5, n=5, k=4):
        super().__init__()
        
        self.m = m    #row
        self.n = n    #col
        self.k = k    
        #self.array = np.array(shape=(m,n))
        
        
        
    def display(self):

        #titel
        self.setWindowTitle("4 Gewinnt")
        
        
        #plazieren und formatieren des fensters
        self.setGeometry(1000, 1000, 250, 100)
        
        
        #farbe der Kästchen
        blue_color = QColor("blue")
        
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
                button = QPushButton()                                             #neue Instanz einer QPushButton erstellen
                button.setStyleSheet(f"background-color: {blue_color.name()}")     #Kästchenfarbe
                button.clicked.connect(lambda _, r=row, c=col: self.place_x(r, c)) #methode zum klicken
                button.setFixedSize(button_width, button_height)                   #Grösse der Kästchens
                row_buttons.append(button)                                         #row_buttons-Liste wird ergänzt
                self.layout.addWidget(button, row, col)                            #Gitterlayout wird ergänzt
            self.buttons.append(row_buttons)                                       #buttons wird ergänzt


    #x oder o setzen
    def place_x(self, r, c, xo_text, player1, player2):
        button = self.buttons[r][c]
        if player1 == True:
            xo_text = "x"
        elif player2 == True:
            xo_text = "o"
        button.setText(xo_text)
        
        
        
    
    def has_won(self, player1, player2):
     
       # Überprüfen ob 'player1' gewonnen hat
       if player1.check_win():
           return f"{player1} hat gewonnen"
       
       # Überprüfen ob 'player2' gewonnen hat
       elif player2.check_win():
           return f"{player2} hat gewonnen"
       
       # Wenn niemand gewonnen hat und das Spielfeld voll ist, ist es ein Unentschieden
       elif self.is_board_full():
           return "Unentschieden"
       
       # Das Spiel ist noch nicht zu Ende
       else:
           return None
       
        
    def is_board_full(self):
        for row in range(self.m):
            for col in range(self.n):
                button = self.buttons[row][col]
                if button.text() == "":
                    return False                # Es gibt mindestens eine leere Zelle
        return True                             # Das Spielfeld ist voll, wenn keine leeren Zellen gefunden wurden
    




#ausführen
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Board()
    window.display()  # Rufen Sie die display-Methode auf, um das Spielfeld anzuzeigen
    window.show()
    sys.exit(app.exec_())

    
    
    