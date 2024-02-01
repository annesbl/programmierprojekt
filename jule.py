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
            row, col = self.find_strategic_move()           #find_strategic_move findet ein leeren Button und gibt diesen zurück -> wird in row, col gespeichert

        # Symbol setzen                            
        self.game.place_symbol(row, col)                    #plaziert symbol auf bei col, row (die im vorherigen schritt festgelegt wurden)

        # Überprüfen, ob das Spiel vorbei ist      - ist das nicht schon durch place_symbol? weil in der place_symbol methode gibt es das, und jetzt machen wir es nochmal?
        # winner = self.game.check_winner() 
        # if winner:
        #     print(f"Spieler {self.name} hat gewonnen!")
        #     self.game.board.close()
        # elif self.game.is_board_full():
        #     print("Unentschieden!")
        #     self.game.board.close()
    
    def find_strategic_move(self):
        max_length = 0
        best_move = None
        chainlenght_dict = {}
        #es wird nur Ort des leeren Buttons zruück gegeben, jedoch noch kein symbol plaziert
        for r in range(self.game.board.m):                       #durchgehen der rows
            for c in range(self.game.board.n):                   #durchgehen der cols
                if self.game.get_symbol(r, c) == self.symbol:    #wenn das symbol an der stelle r,c das symbol der KI ist:
                    #Prüfen, ob rechts Platz ist
                    if c + 1 < self.game.board.n and self.game.get_symbol(r, c + 1) == "":  #wenn der Button an der stelle c + 1 innerhalb des boards ist und leer ist:
                        lenght_r = self.calculate_chain_length(r, c + 1)                                                  #dann wird row und col des leeren buttons zurück gegeben
                        chainlenght_dict[lenght_r] = (r, c+1)
                    #Prüfen, ob links Platz ist
                    if c - 1 >= 0 and self.game.get_symbol(r, c - 1) == "":
                        lenght_l = self.calculate_chain_length(r, c - 1)
                        chainlenght_dict[lenght_l] = (r, c-1)
                    #Prüfen, ob unten Platz ist
                    if r + 1 < self.game.board.m and self.game.get_symbol(r + 1, c) == "":
                        lenght_u = self.calculate_chain_length( r + 1, c)
                        chainlenght_dict[lenght_u] = (r+1, c)
                    #Prüfen, ob oben Platz ist
                    if r - 1 >= 0 and self.game.get_symbol(r - 1, c) == "":
                        lenght_o = self.calculate_chain_length( r - 1, c)
                        chainlenght_dict[lenght_o] = (r-1, c)
                    #Prüfen, ob diagonal unten rechts Platz ist
                    if r + 1 < self.game.board.m and c + 1 < self.game.board.n and self.game.get_symbol(r + 1, c + 1) == "":
                        lenght_ur = self.calculate_chain_length( r + 1, c + 1)
                        chainlenght_dict[lenght_ur] = (r+1, c+1)
                    #Prüfen, ob diagonal oben links Platz ist
                    if r - 1 >= 0 and c - 1 >= 0 and self.game.get_symbol(r - 1, c - 1) == "":
                        lenght_ol = self.calculate_chain_length( r - 1, c - 1)
                        chainlenght_dict[lenght_ol] = (r-1, c-1)
                    #Prüfen, ob diagonal unten links Platz ist
                    if r + 1 < self.game.board.m and c - 1 >= 0 and self.game.get_symbol(r + 1, c - 1) == "":
                        lenght_ul = self.calculate_chain_length( r + 1, c - 1)
                        chainlenght_dict[lenght_ul] = (r+1, c-1)
                    #Prüfen, ob diagonal oben rechts Platz ist
                    if r - 1 >= 0 and c + 1 < self.game.board.n and self.game.get_symbol(r - 1, c + 1) == "":
                        lenght_or = self.calculate_chain_length( r - 1, c + 1)
                        chainlenght_dict[lenght_or] = (r-1, c+1)
                # if self.game.get_symbol(r, c) == "":
                #     length = self.calculate_chain_length(r, c)
                #     if length > max_length:
                #         max_length = length
                #         best_move = (r, c)
        if chainlenght_dict:                               # geht das dictionary durch
            best_length = max(chainlenght_dict)            # speichert die maximale länge als best_lenght
            best_move = chainlenght_dict[best_length]      # speichert den best_move als best lenght(eig unnötig aber dsachte wir lasse best move einfach mal drinnen)
            return best_move                               # gibt best_move wieder

        # Falls keine intelligenten Züge gefunden wurden, setze zufällig
        empty_positions = [(r, c) for r in range(self.game.board.m) for c in range(self.game.board.n) if self.game.get_symbol(r, c) == ""]
        return random.choice(empty_positions)

    def calculate_chain_length(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertikal, diagonal absteigend, diagonal aufsteigend, dargestellt durch (dr, dc)
                   #     -      |        \       /
        max_length = 1

        for dr, dc in directions:                       #durchgehen der directions
            length = 1                                  #1, weil das aktuelle Feld/Startpunkt (dr,dc) als erstes Element der Kette gezählt wird.
            for i in range(1, self.game.board.k):       #prüft ob k gleiche symbole in eineer reihe sind
                r, c = row + i * dr, col + i * dc       #prüft die Symbole in der aktuellen Richtung, beginnend beim Startpunkt und bewegt sich in positiver Richtung (berechnung der nächstn Position)
                if 0 <= r < self.game.board.m and 0 <= c < self.game.board.n and self.game.get_symbol(r, c) == self.symbol: #falls das Symbol an der berechneten Position gleich dem Symbol der KI ist...
                    length += 1                         #...wird die länge der kette um 1 erhöht
                else:
                    break                                #Schleife bricht ab, sobald ein anderes Symbol oder das Ende von Board erreicht wird

            for i in range(1, self.game.board.k):
                r, c = row - i * dr, col - i * dc       #prüft die Symbole in der entgegengesetzten Richtung und bewegt sich in negative Richtung (berechnung der nächstn Position)
                if 0 <= r < self.game.board.m and 0 <= c < self.game.board.n and self.game.get_symbol(r, c) == self.symbol:
                    length += 1
                else:
                    break

            if length >= self.game.board.k:    #überptüft ob Kette grösser gleich k ist
                return length                  #wenn ja dann kette zurück geben

            if length > max_length:            #überprüft ob die aktuelle Kette länger ist als die bisherige längste Kette
                max_length = length            #wenn ja, dann aktuelle Kette aktualisieruen   

        return max_length            #längste gefundene Kette wird zurück gegeben
    
    
    
class KomplexeKI(Player):
    def __init__(self, name, symbol, game):
         super().__init__(name, symbol)
         self.game = game           #Übergeben des 'self'-Objekts an die display-Methode
         self.is_komplexeki = True

    def make_komplexeki_move(self):
        zwickmuehle = self.zwickmühle_bauen()
        best_move = self.find_strategic_move()
        block = self.make_blocking_move()
        if block is not None:
            row, col = block
            self.game.place_symbol(row, col)
            print("RDJLOVE")
        elif zwickmuehle is not None:
            row,col = zwickmuehle
            self.game.place_symbol(row, col) 
        elif best_move is not None:
            row, col = best_move
            self.game.place_symbol(row,col)
        else:
            row = random.randint(0, self.game.board.m - 1)  #row des buttons (für den ersten zug) zufällig festlegen
            col = random.randint(0, self.game.board.n - 1)  #col des buttons (für den ersten zug) zufällig festlegen
            self.game.place_symbol(row,col)
    
    
    
    def zwichmuehlen_dict(self):
        zwickmuhlen_liste = []

        # Überprüfe horizontale Zwickmühlen
        for i in range(self.game.board.m):
            for j in range(self.game.board.n - self.game.board.k + 1):
                zwickmuhlen_liste.append([(i, j + x) for x in range(self.game.board.k)])

        # Überprüfe vertikale Zwickmühlen
        for i in range(self.game.board.m - self.game.board.k + 1):
            for j in range(self.game.board.n):
                zwickmuhlen_liste.append([(i + x, j) for x in range(self.game.board.k)])

        # Überprüfe diagonale Zwickmühlen von links oben nach rechts unten
        for i in range(self.game.board.m - self.game.board.k + 1):
            for j in range(self.game.board.n - self.game.board.k + 1):
                zwickmuhlen_liste.append([(i + x, j + x) for x in range(self.game.board.k)])

        # Überprüfe diagonale Zwickmühlen von links unten nach rechts oben
        for i in range(self.game.board.m - self.game.board.k + 1):
            for j in range(self.game.board.k - 1, self.game.board.n):
                zwickmuhlen_liste.append([(i + x, j - x) for x in range(self.game.board.k)])

        return zwickmuhlen_liste
    
    
    
    
    def zwickmühle_bauen(self):
        zwickmuehlen_liste = self.zwichmuehlen_dict()
        for zwickmuehle in zwickmuehlen_liste:
            count = 0
            empty_positions = []
            
            for position in zwickmuehle:
                if self.game.get_symbol(position[0], position[1]) == self.symbol:
                    count += 1
                elif self.game.get_symbol(position[0], position[1]) == "":
                    empty_positions.append(position)
        chain_lengths = {}
        if empty_positions:
            for position in empty_positions:
                chain_length = self.calculate_chain_length(position[0], position[1], self.symbol)
                chain_lengths[chain_length] = position[0], position[1]
        else:
            return None
            
        if chain_lengths:                               # geht das dictionary durch
            best_length = max(chain_lengths)            # speichert die maximale länge als best_lenght
            best_move = chain_lengths[best_length]      # speichert den best_move als best lenght(eig unnötig aber dsachte wir lasse best move einfach mal drinnen)
            return best_move                               # gibt best_move wieder
        else:
            return None




    def find_strategic_move(self):
            max_length = 0
            best_move = None
            chainlenght_dict = {}
            #es wird nur Ort des leeren Buttons zruück gegeben, jedoch noch kein symbol plaziert
            for r in range(self.game.board.m):                       #durchgehen der rows
                for c in range(self.game.board.n):                   #durchgehen der cols
                    if self.game.get_symbol(r, c) == self.symbol:    #wenn das symbol an der stelle r,c das symbol der KI ist:
                        #Prüfen, ob rechts Platz ist
                        if c + 1 < self.game.board.n and self.game.get_symbol(r, c + 1) == "":  #wenn der Button an der stelle c + 1 innerhalb des boards ist und leer ist:
                            lenght_r = self.calculate_chain_length(r, c + 1, self.symbol)                                                  #dann wird row und col des leeren buttons zurück gegeben
                            chainlenght_dict[lenght_r] = (r, c+1)
                        #Prüfen, ob links Platz ist
                        if c - 1 >= 0 and self.game.get_symbol(r, c - 1) == "":
                            lenght_l = self.calculate_chain_length(r, c - 1, self.symbol)
                            chainlenght_dict[lenght_l] = (r, c-1)
                        #Prüfen, ob unten Platz ist
                        if r + 1 < self.game.board.m and self.game.get_symbol(r + 1, c) == "":
                            lenght_u = self.calculate_chain_length( r + 1, c, self.symbol)
                            chainlenght_dict[lenght_u] = (r+1, c)
                        #Prüfen, ob oben Platz ist
                        if r - 1 >= 0 and self.game.get_symbol(r - 1, c) == "":
                            lenght_o = self.calculate_chain_length( r - 1, c, self.symbol)
                            chainlenght_dict[lenght_o] = (r-1, c)
                        #Prüfen, ob diagonal unten rechts Platz ist
                        if r + 1 < self.game.board.m and c + 1 < self.game.board.n and self.game.get_symbol(r + 1, c + 1) == "":
                            lenght_ur = self.calculate_chain_length( r + 1, c + 1, self.symbol)
                            chainlenght_dict[lenght_ur] = (r+1, c+1)
                        #Prüfen, ob diagonal oben links Platz ist
                        if r - 1 >= 0 and c - 1 >= 0 and self.game.get_symbol(r - 1, c - 1) == "":
                            lenght_ol = self.calculate_chain_length( r - 1, c - 1, self.symbol)
                            chainlenght_dict[lenght_ol] = (r-1, c-1)
                        #Prüfen, ob diagonal unten links Platz ist
                        if r + 1 < self.game.board.m and c - 1 >= 0 and self.game.get_symbol(r + 1, c - 1) == "":
                            lenght_ul = self.calculate_chain_length( r + 1, c - 1, self.symbol)
                            chainlenght_dict[lenght_ul] = (r+1, c-1)
                        #Prüfen, ob diagonal oben rechts Platz ist
                        if r - 1 >= 0 and c + 1 < self.game.board.n and self.game.get_symbol(r - 1, c + 1) == "":
                            lenght_or = self.calculate_chain_length( r - 1, c + 1, self.symbol)
                            chainlenght_dict[lenght_or] = (r-1, c+1)
                    # if self.game.get_symbol(r, c) == "":
                    #     length = self.calculate_chain_length(r, c)
                    #     if length > max_length:
                    #         max_length = length
                    #         best_move = (r, c)
            if chainlenght_dict:                               # geht das dictionary durch
                best_length = max(chainlenght_dict)            # speichert die maximale länge als best_lenght
                best_move = chainlenght_dict[best_length]      # speichert den best_move als best lenght(eig unnötig aber dsachte wir lasse best move einfach mal drinnen)
                return best_move                               # gibt best_move wieder

            # Falls keine intelligenten Züge gefunden wurden, setze zufällig
            empty_positions = [(r, c) for r in range(self.game.board.m) for c in range(self.game.board.n) if self.game.get_symbol(r, c) == ""]
            return random.choice(empty_positions)
    
    
    
    
    def calculate_chain_length(self, row, col, symbol):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertikal, diagonal absteigend, diagonal aufsteigend, dargestellt durch (dr, dc)
                   #     -      |        \       /
        max_length = 1

        for dr, dc in directions:                       #durchgehen der directions
            length = 1                                  #1, weil das aktuelle Feld/Startpunkt (dr,dc) als erstes Element der Kette gezählt wird.
            for i in range(1, self.game.board.k):       #prüft ob k gleiche symbole in eineer reihe sind
                r, c = row + i * dr, col + i * dc       #prüft die Symbole in der aktuellen Richtung, beginnend beim Startpunkt und bewegt sich in positiver Richtung (berechnung der nächstn Position)
                if 0 <= r < self.game.board.m and 0 <= c < self.game.board.n and self.game.get_symbol(r, c) == symbol: #falls das Symbol an der berechneten Position gleich dem Symbol der KI ist...
                    length += 1                         #...wird die länge der kette um 1 erhöht
                else:
                    break                                #Schleife bricht ab, sobald ein anderes Symbol oder das Ende von Board erreicht wird

            for i in range(1, self.game.board.k):
                r, c = row - i * dr, col - i * dc       #prüft die Symbole in der entgegengesetzten Richtung und bewegt sich in negative Richtung (berechnung der nächstn Position)
                if 0 <= r < self.game.board.m and 0 <= c < self.game.board.n and self.game.get_symbol(r, c) == symbol:
                    length += 1
                else:
                    break

            if length >= self.game.board.k:    #überptüft ob Kette grösser gleich k ist
                return length                  #wenn ja dann kette zurück geben

            if length > max_length:            #überprüft ob die aktuelle Kette länger ist als die bisherige längste Kette
                max_length = length            #wenn ja, dann aktuelle Kette aktualisieruen   

        return max_length            #längste gefundene Kette wird zurück gegeben
    
    
    
    def get_opponent_symbol(self):
        # Nehmen wir an, es gibt eine Methode im Spiel, die alle Symbole zurückgibt.
        all_symbols = self.game.get_all_player_symbols()
        return next((symbol for symbol in all_symbols if symbol != self.symbol), None)

    
    
    # def prevent_opponent_win(self):
    #     opponent_symbol = self.get_opponent_symbol()
    #     for row in range(self.game.board.m):
    #         for col in range(self.game.board.n):
    #             if self.game.get_symbol(row, col) == "":
    #                 # Überprüfe, ob der Gegner nach diesem Zug gewinnen kann
    #                 #opponent_symbol =  'o' if self.symbol == 'x' else 'x'
    #                 print(opponent_symbol)
              
    #                 # Horizontale Überprüfung
    #                 if self.check_line(row, col, 0, 1, opponent_symbol, self.game.board.k-1):
    #                     return row, col

    #                 # Vertikale Überprüfung
    #                 if self.check_line(row, col, 1, 0, opponent_symbol, self.game.board.k-1):
    #                     return row, col

    #                 # Diagonale Überprüfung absteigend
    #                 if self.check_line(row, col, 1, 1, opponent_symbol, self.game.board.k-1):
    #                     return row, col

    #                 # Diagonale Überprüfung aufsteigend
    #                 if self.check_line(row, col, -1, 1, opponent_symbol, self.game.board.k-1):
    #                     return row, col
        
    #     # Falls keine Aktion erforderlich ist
    #     return None

    # def check_line(self, start_row, start_col, delta_row, delta_col, symbol, length):
    #     count = 0
    #     for i in range(length):
    #         if 0 <= start_row < self.game.board.m and 0 <= start_col < self.game.board.n and self.game.get_symbol(start_row, start_col) == symbol:
    #             count += 1
    #             start_row += delta_row
    #             start_col += delta_col
    #         else:
    #             break
    #     if count >= length:
    #         return True
    #     else:
    #         return False
    
    # def check_line(self, start_row, start_col, delta_row, delta_col, symbol, length):
    #     count = 0
    #     for i in range(length):
    #         print(f"Checking position ({start_row}, {start_col})")
    #         if 0 <= start_row < self.game.board.m and 0 <= start_col < self.game.board.n and self.game.get_symbol(start_row, start_col) == symbol:
    #             count += 1
    #             start_row += delta_row
    #             start_col += delta_col
    #         else:
    #             break
    #     print(f"Final count: {count}")
    #     if count >= length:
    #         return True
    #     else:
    #         return False
    
    def make_blocking_move(self):
        opponent_symbol = self.get_opponent_symbol()
        for row in range(self.game.board.m):
           for col in range(self.game.board.n):
               if self.game.get_symbol(row, col) == opponent_symbol: 
                    best_move = self.find_strategic_move_defense(row, col, opponent_symbol)
                    return best_move
        return None
                    
            

    
    def find_strategic_move_defense(self,row, col, symbol):
        if self.game.get_symbol(row, col) == symbol:    #wenn das symbol an der stelle r,c das symbol der KI ist:
            if self.calculate_chain_length(row, col, symbol) == self.game.board.k - 1:
                #Prüfen, ob rechts Platz ist
                if col + 1 < self.game.board.n and self.game.get_symbol(row, col + 1) == "":  #wenn der Button an der stelle c + 1 innerhalb des boards ist und leer ist:
                    return row, col
                #Prüfen, ob links Platz ist
                elif col - 1 >= 0 and self.game.get_symbol(row, col - 1) == "":
                    return row, col
                #Prüfen, ob unten Platz ist
                elif row + 1 < self.game.board.m and self.game.get_symbol(row + 1, col) == "":
                    return row, col
                #Prüfen, ob oben Platz ist
                elif row - 1 >= 0 and self.game.get_symbol(row - 1, col) == "":
                    return row, col
                #Prüfen, ob diagonal unten rechts Platz ist
                elif row + 1 < self.game.board.m and col + 1 < self.game.board.n and self.game.get_symbol(row + 1, col + 1) == "":
                    return row, col
                #Prüfen, ob diagonal oben links Platz ist
                elif row - 1 >= 0 and col - 1 >= 0 and self.game.get_symbol(row - 1, col - 1) == "":
                    return row, col
                #Prüfen, ob diagonal unten links Platz ist
                elif row + 1 < self.game.board.m and col - 1 >= 0 and self.game.get_symbol(row + 1, col - 1) == "":
                    return row, col
                #Prüfen, ob diagonal oben rechts Platz ist
                elif row - 1 >= 0 and col + 1 < self.game.board.n and self.game.get_symbol(row - 1, col + 1) == "":
                    return row, col
                else:
                    pass
        return None
    
                    
    
    

        

        
    


        
                
                
    
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
        
           
     
    #GIBT ALLE SYMBOLE DER SPIELER ZURÜCK   beliz
    def get_all_player_symbols(self):
        symbols = {self.player1.symbol, self.player2.symbol}
        return symbols       
           
             
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
    player_einfacheki2 = EinfacheKI("Einfache KI 2", "x", None)
    player_komplexeki = KomplexeKI("Komplexe KI", "o", None)
    player_komplexeki2 = KomplexeKI("Einfache KI 2", "x", None)
    
    #Player1 und Player2 wählen (2 der oben gennanten namen wählen - auf "x" und "o" achten)
    player1 = player_mensch
    player2 = player_komplexeki
    
    play_several_times = False
    num_games = 100  # Anzahl der Spiele
    
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
            player_einfacheki2.game = game #einfacheki
            player_komplexeki.game = game #komplexeki
            player_komplexeki2.game = game #komplexeki
            
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
        player_einfacheki2.game = game #einfacheki
        player_komplexeki.game = game #komplexeki
        player_komplexeki2.game = game #komplexeki
        
        #Spiel starten
        play_game(game)
        

