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
    def __init__(self, name, symbol, spiel):
        super().__init__(name, symbol)
        self.spiel = spiel  # Übergeben des 'self'-Objekts an die display-Methode
        self.ist_komplexe_ki = True
        self.erster_zug = True

    def mache_komplexe_ki_zug(self):
        # Überprüfen, ob die KI kurz vor einer Zwickmühle steht
        zwickmuehle = self.kurz_vor_zwickmuehle()
        # Den besten Zug finden
        bester_zug = self.finde_zug()
        # Blockierenden Zug machen, um den Gegner zu stoppen
        block = self.mache_blockierenden_zug()
        # Gewinnenden Zug machen, wenn möglich
        gewinnender_zug = self.mache_gewinnenden_zug()

        if self.erster_zug:
            # Wenn es der erste Zug ist, platziere das Symbol in der Mitte
            zeile, spalte = self.berechne_mitte()
            if self.game.get_symbol(zeile, spalte)== self.get_opponent_symbol():
                zeile, spalte = zeile+1, spalte
            self.spiel.platziere_symbol(int(zeile), int(spalte))
            self.erster_zug = False
        elif gewinnender_zug is not None:
            # Wenn ein gewinnender Zug möglich ist, mache diesen Zug
            zeile, spalte = gewinnender_zug
            self.spiel.platziere_symbol(zeile, spalte)
        elif block is not None:
            # Wenn ein blockierender Zug möglich ist, blockiere den Gegner
            zeile, spalte = block
            self.spiel.platziere_symbol(zeile, spalte)
        elif zwickmuehle is not None:
            # Wenn die KI kurz vor einer Zwickmühle steht, mache diesen Zug
            zeile, spalte = zwickmuehle
            self.spiel.platziere_symbol(zeile, spalte)
        elif bester_zug is not None:
            # Andernfalls mache den besten verfügbaren Zug
            zeile, spalte = bester_zug
            self.spiel.platziere_symbol(zeile, spalte)
        else:
            # Wenn keine der obigen Bedingungen erfüllt ist, mache einen zufälligen Zug
            while True:
                zeile = random.randint(0, self.spiel.brett.m - 1)
                spalte = random.randint(0, self.spiel.brett.n - 1)
                if self.spiel.hole_symbol(zeile, spalte) == "":
                    self.spiel.platziere_symbol(zeile, spalte)
                    break

    def berechne_mitte(self):
        # Berechne die Mitte des Spielfelds
        mitte_spalten = (self.game.board.n - 1) / 2 if self.game.board.n % 2 == 1 else (self.game.board.n / 2, (self.game.board.n / 2) - 1)
        mitte_zeilen = (self.game.board.m - 1) / 2 if self.game.board.m % 2 == 1 else (self.game.board.m / 2, (self.game.board.m / 2) - 1)
        move = mitte_zeilen, mitte_spalten
        return move
    
    def calculate_chain_length(self, row, col, symbol):
        # Berechne die Länge einer Symbolkette in verschiedenen Richtungen
        directions = [(0, 1), (1, 0), (1, 1), (-1, +1)]
        max_length = []

        for dr, dc in directions:
            chain_coordinates = []

            # Überprüfe in positive Richtung
            r, c = row, col
            while 0 <= r < self.spiel.brett.m and 0 <= c < self.spiel.brett.n:
                if self.spiel.hole_symbol(r, c) == symbol:
                    chain_coordinates.append((r, c))
                r, c = r + dr, c + dc

            if len(chain_coordinates) >= self.spiel.brett.k - 1:
                return chain_coordinates
            if len(chain_coordinates) > len(max_length):
                max_length = chain_coordinates

        return max_length

    def get_opponent_symbol(self):
        # Nehmen wir an, es gibt eine Methode im Spiel, die alle Symbole zurückgibt.
        alle_symbole = self.spiel.hole_alle_spieler_symbole()
        return next((symbol for symbol in alle_symbole if symbol != self.symbol), None)

    def finde_zug(self):
        # Finde den besten Zug, indem die Längen von Symbolketten bewertet werden
        max_laenge = 0
        bester_zug = None
        kettenlaenge_dict = {}

        for r in range(self.spiel.brett.m):
            for c in range(self.spiel.brett.n):
                if self.spiel.hole_symbol(r, c) == self.symbol:
                    # Überprüfe, ob rechts Platz ist
                    if c + 1 < self.spiel.brett.n and self.spiel.hole_symbol(r, c + 1) == "":
                        laenge_r = len(self.calculate_chain_length(r, c + 1, self.symbol))
                        kettenlaenge_dict[laenge_r] = (r, c + 1)
                    # Überprüfe, ob links Platz ist
                    if c - 1 >= 0 and self.spiel.hole_symbol(r, c - 1) == "":
                        laenge_l = len(self.calculate_chain_length(r, c - 1, self.symbol))
                        kettenlaenge_dict[laenge_l] = (r, c - 1)
                    # Überprüfe, ob unten Platz ist
                    if r + 1 < self.spiel.brett.m and self.spiel.hole_symbol(r + 1, c) == "":
                        laenge_u = len(self.calculate_chain_length(r + 1, c, self.symbol))
                        kettenlaenge_dict[laenge_u] = (r + 1, c)
                    # Überprüfe, ob oben Platz ist
                    if r - 1 >= 0 and self.spiel.hole_symbol(r - 1, c) == "":
                        laenge_o = len(self.calculate_chain_length(r - 1, c, self.symbol))
                        kettenlaenge_dict[laenge_o] = (r - 1, c)
                    # Überprüfe, ob diagonal unten rechts Platz ist
                    if r + 1 < self.spiel.brett.m and c + 1 < self.spiel.brett.n and self.spiel.hole_symbol(
                            r + 1, c + 1) == "":
                        laenge_ur = len(self.calculate_chain_length(r + 1, c + 1, self.symbol))
                        kettenlaenge_dict[laenge_ur] = (r + 1, c + 1)
                    # Überprüfe, ob diagonal oben links Platz ist
                    if r - 1 >= 0 and c - 1 >= 0 and self.spiel.hole_symbol(r - 1, c - 1) == "":
                        laenge_ol = len(self.calculate_chain_length(r - 1, c - 1, self.symbol))
                        kettenlaenge_dict[laenge_ol] = (r - 1, c - 1)
                    # Überprüfe, ob diagonal unten links Platz ist
                    if r + 1 < self.spiel.brett.m and c - 1 >= 0 and self.spiel.hole_symbol(r + 1, c - 1) == "":
                        laenge_ul = len(self.calculate_chain_length(r + 1, c - 1, self.symbol))
                        kettenlaenge_dict[laenge_ul] = (r + 1, c - 1)
                    # Überprüfe, ob diagonal oben rechts Platz ist
                    if r - 1 >= 0 and c + 1 < self.spiel.brett.n and self.spiel.hole_symbol(r - 1, c + 1) == "":
                        laenge_or = len(self.calculate_chain_length(r - 1, c + 1, self.symbol))
                        kettenlaenge_dict[laenge_or] = (r - 1, c + 1)

        if kettenlaenge_dict:
            best_laenge = max(kettenlaenge_dict)
            bester_zug = kettenlaenge_dict[best_laenge]
            return bester_zug

    def mache_gewinnenden_zug(self):
        # Überprüfe, ob ein gewinnender Zug möglich ist
        for i in range(self.spiel.brett.m):
            for j in range(self.spiel.brett.n):
                if self.spiel.hole_symbol(i, j) == self.symbol:
                    # Berechne die Länge der Symbolkette
                    kette = self.calculate_chain_length(i, j, self.symbol)
                    if kette is not None and len(kette) >= self.spiel.brett.k - 1:
                        # Bestimme die Richtung der Kette und finde einen leeren Spot in dieser Richtung
                        richtung = self.richtung_herausfinden(i, j, self.symbol, kette)
                        zug = self.finde_leeren_spot(kette, richtung)
                        if zug is not None:
                            return zug
                        else:
                            return None

    def kurz_vor_zwickmuehle(self):
        # Erhalte Positionen der KI-Symbole
        ki_positionen = []
        zwickmuehle_liste = self.zwickmuehlen_liste()

        for i in range(self.spiel.brett.m):
            for j in range(self.spiel.brett.n):
                if self.spiel.hole_symbol(i, j) == self.symbol:
                    ki_positionen.append((i, j))

        # Berechne die Differenzen zwischen erwarteten und aktuellen Positionen
        differences = self.hole_differenzkoordinaten(zwickmuehle_liste, ki_positionen)

        if differences is not None:
            move = random.choice(differences)
            return move

    def hole_differenzkoordinaten(self, zwickmuehle_coords, brett_coords):
        # Erhalte Koordinaten, die in der erwarteten Zwickmühle, aber nicht auf dem aktuellen Spielfeld sind
        differences = [coord for coord in zwickmuehle_coords if coord not in brett_coords]
        if differences is not None:
            if len(differences) <= 3:
                return differences
        else:
            return None

    def zwickmuehlen_liste(self):
        # Erstelle eine Liste von erwarteten Zwickmühlen-Koordinaten
        zwickmuehlen_liste = []

        # Überprüfe horizontale Zwickmühlen
        for i in range(self.spiel.brett.m):
            for j in range(self.spiel.brett.n - self.spiel.brett.k + 1):
                zwickmuehlen_liste.append([(i, j + x) for x in range(self.spiel.brett.k)])

        # Überprüfe vertikale Zwickmühlen
        for i in range(self.spiel.brett.m - self.spiel.brett.k + 1):
            for j in range(self.spiel.brett.n):
                zwickmuehlen_liste.append([(i + x, j) for x in range(self.spiel.brett.k)])

        # Überprüfe diagonale Zwickmühlen von links oben nach rechts unten
        for i in range(self.spiel.brett.m - self.spiel.brett.k + 1):
            for j in range(self.spiel.brett.n - self.spiel.brett.k + 1):
                zwickmuehlen_liste.append([(i + x, j + x) for x in range(self.spiel.brett.k)])

        # Überprüfe diagonale Zwickmühlen von links unten nach rechts oben
        for i in range(self.spiel.brett.m - self.spiel.brett.k + 1):
            for j in range(self.spiel.brett.k - 1, self.spiel.brett.n):
                zwickmuehlen_liste.append([(i + x, j - x) for x in range(self.spiel.brett.k)])

        return zwickmuehlen_liste
    
    def zwickmühle_bauen(self):
        # Liste der Zwickmühlen auf dem Spielfeld erhalten
        zwickmuehlen_liste = self.zwickmuehlen_liste()
        
        # Durchlaufe jede Zwickmühle
        for zwickmuehle in zwickmuehlen_liste:
            anzahl = 0
            leere_positionen = []

            # Durchlaufe jede Position in der aktuellen Zwickmühle
            for position in zwickmuehle:
                # Zähle die Symbole des Spielers an der aktuellen Position
                if self.spiel.get_symbol(position[0], position[1]) == self.symbol:
                    anzahl += 1
                # Speichere leere Positionen
                elif self.spiel.get_symbol(position[0], position[1]) == "":
                    leere_positionen.append(position)
                    
            ketten_laengen = {}
            
            # Wenn es leere Positionen gibt
            if leere_positionen:
                # Berechne die Kettenlängen für jede leere Position
                for position in leere_positionen:
                    ketten_laenge = self.berechne_ketten_laenge(position[0], position[1], self.symbol)
                    ketten_laengen[ketten_laenge] = position[0], position[1]
            else:
                return None

            # Falls es Kettenlängen gibt
            if ketten_laengen:
                # Finde die maximale Kettenlänge
                beste_laenge = max(ketten_laengen)
                # Speichere die Position der besten Bewegung
                beste_position = ketten_laengen[beste_laenge]
                return beste_position
            else:
                return None


    def blockierenden_zug_machen(self):
        # Symbol des Gegners erhalten
        gegner_symbol = self.hole_gegner_symbol()
        
        # Durchlaufe das Spielfeld
        for i in range(self.spiel.brett.m):
            for j in range(self.spiel.brett.n):
                # Überprüfe, ob das Symbol des Gegners an der aktuellen Position ist
                if self.spiel.hole_symbol(i, j) == gegner_symbol:
                    # Berechne die Länge der Kette des Gegners
                    kette = self.berechne_ketten_laenge(i, j, gegner_symbol) 
                    
                    # Falls die Kette vorhanden und lang genug ist
                    if kette is not None and len(kette) >= self.spiel.brett.k - 1:
                        # Finde die Richtung der Kette
                        richtung = self.richtung_herausfinden(i, j, gegner_symbol, kette)
                        print(f"Richtung: {richtung}")
                        
                        # Überprüfe, ob die Kette bereits blockiert ist
                        bereits_blockiert = self.bereits_geblockt(kette, richtung)
                        
                        if bereits_blockiert: 
                            print("Ich bin so schlau")
                            pass
                        else:
                            # Finde eine leere Stelle, um die Kette zu blockieren
                            zug = self.finde_freien_platz(kette, richtung)
                            
                            if zug is not None:
                                print("RDJLOVE")
                                return zug
                            else:
                                return None


    def richtung_herausfinden(self, zeile, spalte, symbol, koordinaten_liste):
        # Bestimme die Richtung der Kette
        # Überprüfe, ob das Symbol rechts von der Liste ist
        if spalte + 1 < self.spiel.brett.n and (zeile, spalte + 1) in koordinaten_liste and self.spiel.hole_symbol(zeile, spalte + 1) == symbol:
            return "Waagerecht, rechts"
        # Überprüfe, ob das Symbol links von der Liste ist
        elif spalte - 1 >= 0 and (zeile, spalte - 1) in koordinaten_liste and self.spiel.hole_symbol(zeile, spalte - 1) == symbol:
            return "Waagerecht, links"
        # Überprüfe, ob das Symbol unterhalb von der Liste ist
        elif zeile + 1 < self.spiel.brett.m and (zeile + 1, spalte) in koordinaten_liste and self.spiel.hole_symbol(zeile + 1, spalte) == symbol:
            return "Senkrecht, unten"
        # Überprüfe, ob das Symbol oberhalb von der Liste ist
        elif zeile - 1 >= 0 and (zeile - 1, spalte) in koordinaten_liste and self.spiel.hole_symbol(zeile - 1, spalte) == symbol:
            return "Senkrecht, oben"
        # Überprüfe, ob das Symbol diagonal unten rechts von der Liste ist
        elif zeile + 1 < self.spiel.brett.m and spalte + 1 < self.spiel.brett.n and (zeile + 1, spalte + 1) in koordinaten_liste and self.spiel.hole_symbol(zeile + 1, spalte + 1) == symbol:
            return "Diagonal, rechts unten"
        # Überprüfe, ob das Symbol diagonal oben links von der Liste ist
        elif zeile - 1 >= 0 and spalte - 1 >= 0 and (zeile - 1, spalte - 1) in koordinaten_liste and self.spiel.hole_symbol(zeile - 1, spalte - 1) == symbol:
            return "Diagonal, links oben"
        # Überprüfe, ob das Symbol diagonal unten links von der Liste ist
        elif zeile + 1 < self.spiel.brett.m and spalte - 1 >= 0 and (zeile + 1, spalte - 1) in koordinaten_liste and self.spiel.hole_symbol(zeile + 1, spalte - 1) == symbol:
            return "Diagonal, links unten"
        # Überprüfe, ob das Symbol diagonal oben rechts von der Liste ist
        elif zeile - 1 >= 0 and spalte + 1 < self.spiel.brett.n and (zeile - 1, spalte + 1) in koordinaten_liste and self.spiel.hole_symbol(zeile - 1, spalte + 1) == symbol:
            return "Diagonal, rechts oben"
        else:
            return None

    def finde_freien_platz(self, liste, richtung):
        if not liste:
            return None  # Return None if the list is empty

        if len(liste) < 2:
            return None  # Not enough elements in the list
        print(liste)
        #da Abstand zwischen zwei Punkten immer k ist die Summe aller (Row/Col - Row/Col+1 (pro Objekt +1) = k
        aufeinanderfolgend = self.sind_koordinaten_aufeinanderfolgend(liste)
        #bei waagerechter Kette, die alle in einer Reihe sind
        if aufeinanderfolgend == True and (richtung == "Waagerecht, rechts" or richtung == "Waagerecht, links"):
            #Prüfen, ob rechts Platz ist
            if liste[-1][1] + 1 < self.spiel.brett.n and self.spiel.hole_symbol(liste[-1][0], liste[-1][1] + 1) == "":  
                return liste[-1][0], liste[-1][1] + 1
            #Prüfen, ob links Platz ist
            if liste[0][1] - 1 >= 0 and self.spiel.hole_symbol(liste[0][0], liste[0][1] - 1) == "":
                return liste[0][0], liste[0][1] - 1
        elif aufeinanderfolgend is not None and (richtung == "Waagerecht, rechts" or richtung == "Waagerecht, links"):
            zeile, spalte = aufeinanderfolgend
            #Prüfen, ob rechts Platz ist
            if spalte + 1 < self.spiel.brett.n and self.spiel.hole_symbol(zeile, spalte + 1) == "":  
                return zeile, spalte + 1
            #Prüfen, ob links Platz ist
            if spalte - 1 >= 0 and self.spiel.hole_symbol(zeile, spalte - 1) == "":
                return zeile, spalte - 1
        #bei senkrechter Kette, die alle in einer Reihe sind
        elif aufeinanderfolgend == True and (richtung == "Senkrecht, unten" or richtung == "Senkrecht, oben"):
            #Prüfen, ob unten Platz ist
            if liste[-1][0] + 1 < self.spiel.brett.m and self.spiel.hole_symbol(liste[-1][0] + 1, liste[-1][1]) == "":
                return liste[-1][0] + 1, liste[-1][1]
            #Prüfen, ob oben Platz ist
            if liste[0][0] - 1 >= 0 and self.spiel.hole_symbol(liste[0][0] - 1, liste[0][1]) == "":
                return liste[0][0] - 1, liste[0][1]
        elif aufeinanderfolgend is not None and (richtung == "Senkrecht, unten" or richtung == "Senkrecht, oben"):
            zeile, spalte = aufeinanderfolgend
            #Prüfen, ob unten Platz ist
            if zeile + 1 < self.spiel.brett.m and self.spiel.hole_symbol(zeile + 1, spalte) == "":
                return zeile + 1, spalte
            #Prüfen, ob oben Platz ist
            if zeile - 1 >= 0 and self.spiel.hole_symbol(zeile - 1, spalte) == "":
                return zeile - 1, spalte
        elif aufeinanderfolgend == True and (richtung == "Diagonal, links oben" or richtung == "Diagonal, rechts unten"):
            # Prüfen, ob diagonal unten rechts kein Platz ist
            if liste[-1][0] + 1 < self.spiel.brett.m and liste[-1][1] + 1 < self.spiel.brett.n and self.spiel.hole_symbol(liste[-1][0] + 1, liste[-1][1] + 1) == "":
                return liste[-1][0] + 1, liste[-1][1] + 1
            # Prüfen, ob diagonal oben links kein Platz ist
            if liste[0][0] - 1 >= 0 and liste[0][1] - 1 >= 0 and self.spiel.hole_symbol(liste[0][0] - 1, liste[0][1] - 1) == "":
                return liste[0][0] - 1, liste[0][1] - 1
        elif aufeinanderfolgend is not None and (richtung == "Diagonal, links oben" or richtung == "Diagonal, rechts unten"):
            zeile, spalte = aufeinanderfolgend
            #Prüfen, ob diagonal unten rechts Platz ist
            if zeile + 1 < self.spiel.brett.m and spalte + 1 < self.spiel.brett.n and self.spiel.hole_symbol(zeile + 1, spalte + 1) == "":
                return zeile + 1, spalte + 1
            #Prüfen, ob diagonal oben links Platz ist
            if zeile - 1 >= 0 and spalte - 1 >= 0 and self.spiel.hole_symbol(zeile - 1, spalte - 1) == "":
                return zeile - 1, spalte - 1
        elif aufeinanderfolgend == True and (richtung == "Diagonal, links unten" or richtung == "Diagonal, rechts oben"):
            if liste[-1][0] + 1 < self.spiel.brett.m and liste[-1][1] - 1 >= 0 and  self.spiel.hole_symbol(liste[-1][0] + 1, liste[-1][1] - 1) == "":
                return liste[-1][0] + 1, liste[-1][1] - 1
            # Prüfen, ob diagonal oben rechts das Symbol in der Liste ist
            if liste[0][0] - 1 >= 0 and liste[0][1] + 1 < self.spiel.brett.n and self.spiel.hole_symbol(liste[0][0] - 1, liste[0][1] + 1) == "":
                return liste[0][0] - 1, liste[0][1] + 1
        elif aufeinanderfolgend is not None and (richtung == "Diagonal, links unten" or richtung == "Diagonal, rechts oben"):
            zeile, spalte = aufeinanderfolgend
            #Prüfen, ob diagonal unten links Platz ist
            if zeile + 1 < self.spiel.brett.m and spalte - 1 >= 0 and self.spiel.hole_symbol(zeile + 1, spalte - 1) == "":
                return zeile + 1, spalte - 1
            #Prüfen, ob diagonal oben rechts Platz ist
            if zeile - 1 >= 0 and spalte + 1 < self.spiel.brett.n and self.spiel.hole_symbol(zeile - 1, spalte + 1) == "":
                return zeile - 1, spalte + 1
        else:
            return None

    def bereits_geblockt(self, liste, richtung):
        # Bei waagerechter Kette, die alle in einer Reihe sind
        aufeinanderfolgend = self.sind_koordinaten_aufeinanderfolgend(liste)
        #if (summe_rows_plus1 - summe_rows) == self.spiel.brett.k-1:#and direction == "Waagerecht, rechts" or direction == "Waagerecht, links":
        # Prüfen, ob rechts Platz ist
        if liste and aufeinanderfolgend == True and liste[-1][1] + 1 < self.spiel.brett.n and liste[0][0] - 1 >= 0 and (richtung == "Waagerecht, rechts" or richtung == "Waagerecht, links"):     
            if self.spiel.hole_symbol(liste[-1][0], liste[-1][1] + 1) != "" and self.spiel.hole_symbol(liste[0][0], liste[0][1] - 1) != "" :  
                return True
        # Bei senkrechter Kette, die alle in einer Reihe sind
        elif liste and aufeinanderfolgend == True and liste[-1][0] + 1 < self.spiel.brett.m and liste[0][0] - 1 >= 0 and (richtung == "Senkrecht, unten" or richtung == "Senkrecht, oben"): 
            if self.spiel.hole_symbol(liste[-1][0] + 1, liste[-1][1]) != "" and self.spiel.hole_symbol(liste[0][0] - 1, liste[0][1]) != "":
                return True
        elif liste and aufeinanderfolgend == True and liste[-1][0] + 1 < self.spiel.brett.m and liste[-1][1] + 1 < self.spiel.brett.n and liste[0][0] - 1 >= 0 and liste[0][1] - 1 >= 0 and (richtung == "Diagonal, links oben" or richtung == "Diagonal, rechts unten"):
            if liste and self.spiel.hole_symbol(liste[0][0] + 1, liste[0][1] + 1) != "" and self.spiel.hole_symbol(liste[-1][0] - 1, liste[-1][1] - 1) != "" :
                return True
        elif aufeinanderfolgend is not None  and (richtung == "Waagerecht, rechts" or richtung == "Waagerecht, links"):
            zeile, spalte = aufeinanderfolgend
            if self.spiel.hole_symbol(zeile, spalte + 1) != "" and self.spiel.hole_symbol(zeile, spalte - 1) != "":
                return True
        else:
            return False

    def sind_koordinaten_aufeinanderfolgend(self, koordinaten_liste):
        if not koordinaten_liste:
            return False

        for i in range(len(koordinaten_liste) - 1):
            aktuelle_koordinate = koordinaten_liste[i]
            naechste_koordinate = koordinaten_liste[i + 1]

            # Überprüfe, ob beide Teile der Koordinaten in jeder Richtung direkt nebeneinander liegen
            if (
                (abs(aktuelle_koordinate[0] - naechste_koordinate[0]) == 1 and abs(aktuelle_koordinate[1] - naechste_koordinate[1]) == 0) or  # Vertikal
                (abs(aktuelle_koordinate[0] - naechste_koordinate[0]) == 0 and abs(aktuelle_koordinate[1] - naechste_koordinate[1]) == 1) or  # Horizontal
                (abs(aktuelle_koordinate[0] - naechste_koordinate[0]) == 1 and abs(aktuelle_koordinate[1] - naechste_koordinate[1]) == 1)     # Diagonal
            ):
                continue
            else:
                zeile, spalte = aktuelle_koordinate
                return (zeile, spalte)

        return True

    
       
        
    


        
                
                
    
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
        

