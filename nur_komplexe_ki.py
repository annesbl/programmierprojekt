class KomplexeKI(Player):
    def __init__(self, name, symbol, game):
         super().__init__(name, symbol)
         self.game = game           #Übergeben des 'self'-Objekts an die display-Methode
         self.is_komplexeki = True
         self.first_move = True

    def make_komplexeki_move(self):
        zwickmuehle = self.kurz_vor_zwickmuehle()
        best_move = self.find_move()
        block = self.make_blocking_move()
        winning_move = self.make_winning_move()
        if self.first_move:
            row, col = self.berechne_mitte()
            self.game.place_symbol(int(row),int(col))
            self.first_move = False
        elif winning_move is not None:
            row, col = winning_move
            self.game.place_symbol(row, col)
        elif block is not None:
            row, col = block
            self.game.place_symbol(row, col)

        elif zwickmuehle is not None:
              row,col = zwickmuehle
              self.game.place_symbol(row, col) 
        elif best_move is not None:
            row, col = best_move
            self.game.place_symbol(row,col)
        else:
             while True:
                row = random.randint(0, self.game.board.m - 1)
                col = random.randint(0, self.game.board.n - 1)
                if self.game.get_symbol(row, col) == "":
                    self.game.place_symbol(row, col)
                    break
    
    def berechne_mitte(self):
        mitte_spalten = (self.game.board.n - 1) / 2 if self.game.board.n % 2 == 1 else (self.game.board.n / 2, (self.game.board.n / 2) - 1)
        mitte_zeilen = (self.game.board.m - 1) / 2 if self.game.board.m % 2 == 1 else (self.game.board.m / 2, (self.game.board.m / 2) - 1)
        move = mitte_zeilen, mitte_spalten
        return move
    
    
    def calculate_chain_length(self, row, col, symbol):
        directions = [(0, 1), (1, 0), (1, 1), (-1, +1)]
        max_length = []

        for dr, dc in directions:
            chain_coordinates = []

            # Check in positive direction
            r, c = row, col
            while 0 <= r < self.game.board.m and 0 <= c < self.game.board.n:
                if self.game.get_symbol(r, c) == symbol:
                    chain_coordinates.append((r, c))
                r, c = r + dr, c + dc
                

            if len(chain_coordinates) >= self.game.board.k-1:
                print(chain_coordinates)
                return chain_coordinates
            if len(chain_coordinates) > len(max_length):            #überprüft ob die aktuelle Kette länger ist als die bisherige längste Kette
                max_length = chain_coordinates           #wenn ja, dann aktuelle Kette aktualisieruen   

        return max_length     


    def get_opponent_symbol(self):
        # Nehmen wir an, es gibt eine Methode im Spiel, die alle Symbole zurückgibt.
        all_symbols = self.game.get_all_player_symbols()
        return next((symbol for symbol in all_symbols if symbol != self.symbol), None)
    
    
    
    def find_move(self):
        max_length = 0
        best_move = None
        chainlenght_dict = {}
        #es wird nur Ort des leeren Buttons zruück gegeben, jedoch noch kein symbol plaziert
        for r in range(self.game.board.m):                       #durchgehen der rows
            for c in range(self.game.board.n):                   #durchgehen der cols
                if self.game.get_symbol(r, c) == self.symbol:    #wenn das symbol an der stelle r,c das symbol der KI ist:
                    #Prüfen, ob rechts Platz ist
                    if c + 1 < self.game.board.n and self.game.get_symbol(r, c + 1) == "":  #wenn der Button an der stelle c + 1 innerhalb des boards ist und leer ist:
                        lenght_r = len(self.calculate_chain_length(r, c + 1, self.symbol))                                                #dann wird row und col des leeren buttons zurück gegeben
                        chainlenght_dict[lenght_r] = (r, c+1)
                    #Prüfen, ob links Platz ist
                    if c - 1 >= 0 and self.game.get_symbol(r, c - 1) == "":
                        lenght_l = len(self.calculate_chain_length(r, c - 1, self.symbol))
                        chainlenght_dict[lenght_l] = (r, c-1)
                    #Prüfen, ob unten Platz ist
                    if r + 1 < self.game.board.m and self.game.get_symbol(r + 1, c) == "":
                        lenght_u = len(self.calculate_chain_length( r + 1, c, self.symbol))
                        chainlenght_dict[lenght_u] = (r+1, c)
                    #Prüfen, ob oben Platz ist
                    if r - 1 >= 0 and self.game.get_symbol(r - 1, c) == "":
                        lenght_o = len(self.calculate_chain_length( r - 1, c, self.symbol))
                        chainlenght_dict[lenght_o] = (r-1, c)
                    #Prüfen, ob diagonal unten rechts Platz ist
                    if r + 1 < self.game.board.m and c + 1 < self.game.board.n and self.game.get_symbol(r + 1, c + 1) == "":
                        lenght_ur = len(self.calculate_chain_length( r + 1, c + 1, self.symbol))
                        chainlenght_dict[lenght_ur] = (r+1, c+1)
                    #Prüfen, ob diagonal oben links Platz ist
                    if r - 1 >= 0 and c - 1 >= 0 and self.game.get_symbol(r - 1, c - 1) == "":
                        lenght_ol = len(self.calculate_chain_length( r - 1, c - 1, self.symbol))
                        chainlenght_dict[lenght_ol] = (r-1, c-1)
                    #Prüfen, ob diagonal unten links Platz ist
                    if r + 1 < self.game.board.m and c - 1 >= 0 and self.game.get_symbol(r + 1, c - 1) == "":
                        lenght_ul = len(self.calculate_chain_length( r + 1, c - 1, self.symbol))
                        chainlenght_dict[lenght_ul] = (r+1, c-1)
                    #Prüfen, ob diagonal oben rechts Platz ist
                    if r - 1 >= 0 and c + 1 < self.game.board.n and self.game.get_symbol(r - 1, c + 1) == "":
                        lenght_or = len(self.calculate_chain_length( r - 1, c + 1, self.symbol))
                        chainlenght_dict[lenght_or] = (r-1, c+1)
                
        if chainlenght_dict:                               # geht das dictionary durch
            best_length = max(chainlenght_dict)            # speichert die maximale länge als best_lenght
            best_move = chainlenght_dict[best_length]      # speichert den best_move als best lenght(eig unnötig aber dsachte wir lasse best move einfach mal drinnen)
            return best_move                               # gibt best_move wieder

    
    def make_winning_move(self):
            for i in range(self.game.board.m):
                for j in range(self.game.board.n):
                        if self.game.get_symbol(i, j) == self.symbol:    #wenn das symbol an der stelle r,c das symbol der KI ist:
                            chain = self.calculate_chain_length(i, j, self.symbol)
                            if chain is not None and len(chain) >= self.game.board.k - 1:
                                direction = self.richtung_herausfinden(i, j, self.symbol, chain)
                                move = self.find_empty_spot(chain, direction)
                                if move is not None:
                                    return move
                                else:
                                    return None  
    
    def kurz_vor_zwickmuehle(self):
        ki_positionen = []
        zwickmuehle_liste = self.zwichmuehlen_liste()
        for i in range(self.game.board.m):
            for j in range(self.game.board.n):
                if self.game.get_symbol(i, j) == self.symbol:
                    ki_positionen.append((i,j))
                    
        differences = self.get_difference_coordinates(zwickmuehle_liste, ki_positionen)
        if differences is not None:
            move = random.choice(differences)
            return move
        
                    
    def get_difference_coordinates(self, zwickmuhle_coords, board_coords):
        differences = [coord for coord in zwickmuhle_coords if coord not in board_coords]
        if differences is not None:
            if len(differences) <= 3:
                return differences
        else:
            return None
        



    
    def zwichmuehlen_liste(self):
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
         zwickmuehlen_liste = self.zwichmuehlen_liste()
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
         
    
    
                    
    def make_blocking_move(self):
            opponent_symbol = self.get_opponent_symbol()
            for i in range(self.game.board.m):
                for j in range(self.game.board.n):
                        if self.game.get_symbol(i, j) == opponent_symbol:    #wenn das symbol an der stelle r,c das symbol der KI ist:
                            chain = self.calculate_chain_length(i, j, opponent_symbol) 
                            if chain is not None and len(chain)>= self.game.board.k - 1:
                                direction = self.richtung_herausfinden(i, j, opponent_symbol, chain)
                                print(f"direction:{direction}")
                                already_blocked = self.bereits_geblockt(chain, direction)
                                if already_blocked: 
                                    print("Ich bin so schlau")
                                    pass
                                else:
                                    move = self.find_empty_spot(chain, direction)
                                    if move is not None:
                                        print("RDJLOVE")
                                        return move
                                    else:
                                        return None 
                                
                            
        
    def richtung_herausfinden(self, row, col, symbol, coordinates_list):
    # Richtung der Kette herausfinden
    # Prüfen, ob rechts das Symbol in der Liste ist
        if col + 1 < self.game.board.n and (row, col + 1) in coordinates_list and self.game.get_symbol(row, col + 1) == symbol:
            return "Waagerecht, rechts"
        # Prüfen, ob links das Symbol in der Liste ist
        elif col - 1 >= 0 and (row, col - 1) in coordinates_list and self.game.get_symbol(row, col - 1) == symbol:
            return "Waagerecht, links"
        # Prüfen, ob unten das Symbol in der Liste ist
        elif row + 1 < self.game.board.m and (row + 1, col) in coordinates_list and self.game.get_symbol(row + 1, col) == symbol:
            return "Senkrecht, unten"
        # Prüfen, ob oben das Symbol in der Liste ist
        elif row - 1 >= 0 and (row - 1, col) in coordinates_list and self.game.get_symbol(row - 1, col) == symbol:
            return "Senkrecht, oben"
        # Prüfen, ob diagonal unten rechts das Symbol in der Liste ist
        elif row + 1 < self.game.board.m and col + 1 < self.game.board.n and (row + 1, col + 1) in coordinates_list and self.game.get_symbol(row + 1, col + 1) == symbol:
            return "Diagonal, rechts unten"
        # Prüfen, ob diagonal oben links das Symbol in der Liste ist
        elif row - 1 >= 0 and col - 1 >= 0 and (row - 1, col - 1) in coordinates_list and self.game.get_symbol(row - 1, col - 1) == symbol:
            return "Diagonal, links oben"
        # Prüfen, ob diagonal unten links das Symbol in der Liste ist
        elif row + 1 < self.game.board.m and col - 1 >= 0 and (row + 1, col - 1) in coordinates_list and self.game.get_symbol(row + 1, col - 1) == symbol:
            return "Diagonal, links unten"
        # Prüfen, ob diagonal oben rechts das Symbol in der Liste ist
        elif row - 1 >= 0 and col + 1 < self.game.board.n and (row - 1, col + 1) in coordinates_list and self.game.get_symbol(row - 1, col + 1) == symbol:
            return "Diagonal, rechts oben"
        else:
            return None

    

    
    def find_empty_spot(self, list, direction):
        if not list:
            return None  # Return None if the list is empty

        if len(list) < 2:
            return None  # Not enough elements in the list
        print(list)
        #da Abstand zwischen zwei Punkten immer k ist die Summe aller (Row/Col - Row/Col+1 (pro Objekt +1) = k
        consecutive = self.are_coordinates_consecutive(list)
        #bei waagerechter Kette. die alle in einer Reihe sind
        if consecutive == True and (direction == "Waagerecht, rechts" or direction == "Waagerecht, links"):
            #Prüfen, ob rechts Platz ist
            if list[-1][1] + 1 < self.game.board.n and self.game.get_symbol(list[-1][0], list[-1][1] + 1) == "":  
                return list[-1][0], list[-1][1] + 1
            #Prüfen, ob links Platz ist
            if list[0][1] - 1 >= 0 and self.game.get_symbol(list[0][0], list[0][1] - 1) == "":
                return list[0][0], list[0][1] - 1
        elif consecutive is not None and (direction == "Waagerecht, rechts" or direction == "Waagerecht, links"):
            row, col = consecutive
            if col + 1 < self.game.board.n and self.game.get_symbol(row, col + 1) == "":  
                return row, col + 1
            #Prüfen, ob links Platz ist
            if col - 1 >= 0 and self.game.get_symbol(row, col - 1) == "":
                return row, col - 1
        #bei senkrechter Kette, die alle in einer Reihe sind
        elif consecutive == True and (direction == "Senkrecht, unten" or direction == "Senkrecht, oben"):
            #Prüfen, ob unten Platz ist
            if list[-1][0] + 1 < self.game.board.m and self.game.get_symbol(list[-1][0] + 1, list[-1][1]) == "":
                return list[-1][0] + 1, list[-1][1]
            #Prüfen, ob oben Platz ist
            if list[0][0] - 1 >= 0 and self.game.get_symbol(list[0][0] - 1, list[0][1]) == "":
                return list[0][0] - 1, list[0][1]
        elif consecutive is not None and (direction == "Senkrecht, unten" or direction == "Senkrecht, oben"):
            row, col = consecutive
            #Prüfen, ob unten Platz ist
            if row + 1 < self.game.board.m and self.game.get_symbol(row + 1, col) == "":
                return row + 1, col
            #Prüfen, ob oben Platz ist
            if row - 1 >= 0 and self.game.get_symbol(row - 1, col) == "":
                return row - 1, col
        elif consecutive == True and (direction == "Diagonal, links oben" or direction == "Diagonal, rechts unten"):
            # Prüfen, ob diagonal unten rechts kein Platz ist
            if list[-1][0] + 1 < self.game.board.m and list[-1][1] + 1 < self.game.board.n and self.game.get_symbol(list[-1][0] + 1, list[-1][1] + 1) == "":
                return list[-1][0] + 1, list[-1][1] + 1
            # Prüfen, ob diagonal oben links kein Platz ist
            if list[0][0] - 1 >= 0 and list[0][1] - 1 >= 0 and self.game.get_symbol(list[0][0] - 1, list[0][1] - 1) == "":
                return list[0][0] - 1, list[0][1] - 1
        elif consecutive is not None and (direction == "Diagonal, links oben" or direction == "Diagonal, rechts unten"):
            row, col = consecutive
            #Prüfen, ob diagonal unten rechts Platz ist
            if row + 1 < self.game.board.m and col + 1 < self.game.board.n and self.game.get_symbol(row + 1, col + 1) == "":
                return row + 1, col + 1
            #Prüfen, ob diagonal oben links Platz ist
            if row - 1 >= 0 and col - 1 >= 0 and self.game.get_symbol(row - 1, col - 1) == "":
                return row - 1, col - 1
        elif consecutive == True and (direction == "Diagonal, links unten" or direction == "Diagonal, rechts oben"):
            if list[-1][0] + 1 < self.game.board.m and list[-1][1] - 1 >= 0 and  self.game.get_symbol(list[-1][0] + 1, list[-1][1] - 1) == "":
                return list[-1][0] + 1, list[-1][1] - 1
        # Prüfen, ob diagonal oben rechts das Symbol in der Liste ist
            if list[0][0] - 1 >= 0 and list[0][1] + 1 < self.game.board.n and self.game.get_symbol(list[0][0] - 1, list[0][1] + 1) == "":
                return list[0][0] - 1, list[0][1] + 1
        elif consecutive is not None and (direction == "Diagonal, links unten" or direction == "Diagonal, rechts oben"):
            row, col = consecutive
            #Prüfen, ob diagonal unten links Platz ist
            if row + 1 < self.game.board.m and col - 1 >= 0 and self.game.get_symbol(row + 1, col - 1) == "":
                return row + 1, col - 1
            #Prüfen, ob diagonal oben rechts Platz ist
            if row - 1 >= 0 and col + 1 < self.game.board.n and self.game.get_symbol(row - 1, col + 1) == "":
                return row - 1, col + 1
        else:
            return None
                
    def bereits_geblockt(self, list, direction):
        #bei waagerechter Kette. die alle in einer Reihe sind
        consecutive = self.are_coordinates_consecutive(list)
        #if (summe_rows_plus1 - summe_rows) == self.game.board.k-1:#and direction == "Waagerecht, rechts" or direction == "Waagerecht, links":
        #Prüfen, ob rechts Platz ist
        if list and consecutive == True and list[-1][1] + 1 < self.game.board.n and list[0][0] - 1 >= 0 and (direction == "Waagerecht, rechts" or direction == "Waagerecht, links"):     
            if self.game.get_symbol(list[-1][0], list[-1][1] + 1) != "" and self.game.get_symbol(list[0][0], list[0][1] - 1) != "" :  
                return True
        # bei senkrechter Kette, die alle in einer Reihe sind
        elif list and consecutive == True and list[-1][0] + 1 < self.game.board.m and list[0][0] - 1 >= 0 and (direction == "Senkrecht, unten" or direction == "Senkrecht, oben"): 
            if self.game.get_symbol(list[-1][0] + 1, list[-1][1]) != "" and self.game.get_symbol(list[0][0] - 1, list[0][1]) != "":
                return True
        elif list and consecutive == True and list[-1][0] + 1 < self.game.board.m and list[-1][1] + 1 < self.game.board.n and list[0][0] - 1 >= 0 and list[0][1] - 1 >= 0 and (direction == "Diagonal, links oben" or direction == "Diagonal, rechts unten"):
            if list and self.game.get_symbol(list[0][0] + 1, list[0][1] + 1) != "" and self.game.get_symbol(list[-1][0] - 1, list[-1][1] - 1) != "" :
                return True
        elif consecutive is not None  and (direction == "Waagerecht, rechts" or direction == "Waagerecht, links"):
            row, col = consecutive
            if self.game.get_symbol(row, col + 1) != "" and self.game.get_symbol(row, col - 1) != "":
                return True
        else:
            return False
        
        
        
    def are_coordinates_consecutive(self, coord_list):
        if not coord_list:
            return False

        for i in range(len(coord_list) - 1):
            current_coord = coord_list[i]
            next_coord = coord_list[i + 1]

            # Check if both parts of the coordinates are completely next to each other in any direction
            if (
                (abs(current_coord[0] - next_coord[0]) == 1 and abs(current_coord[1] - next_coord[1]) == 0) or  # Vertical
                (abs(current_coord[0] - next_coord[0]) == 0 and abs(current_coord[1] - next_coord[1]) == 1) or  # Horizontal
                (abs(current_coord[0] - next_coord[0]) == 1 and abs(current_coord[1] - next_coord[1]) == 1)     # Diagonal
            ):
                continue
            else:
                row, col = current_coord
                return (row, col)
                

        return True