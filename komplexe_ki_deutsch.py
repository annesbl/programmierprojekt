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
        mitte_spalten = (self.spiel.brett.n - 1) / 2 if self.spiel.brett.n % 2 == 1 else (
        self.spiel.brett.n / 2, (self.spiel.brett.n / 2) - 1)
        mitte_zeilen = (self.spiel.brett.m - 1) / 2 if self.spiel.brett.m % 2 == 1 else (
        self.spiel.brett.m / 2, (self.spiel.brett.m / 2) - 1)
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
