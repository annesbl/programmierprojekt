def calculate_chain_length(self, row, col, symbol):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertikal, diagonal absteigend, diagonal aufsteigend, dargestellt durch (dr, dc)

        max_chain = []  # List to store the coordinates of the longest chain
        for dr, dc in directions:
            chain_coordinates = []  # List to store the coordinates of the current chain

            # Check in positive direction
            while True:
                r, c = row + dr, col +  dc
                try:
                    self.game.get_symbol(r, c)
                except:
                    break
                else:
                    if 0 <= r < self.game.board.m and 0 <= c < self.game.board.n and self.game.get_symbol(r, c) == symbol:
                        chain_coordinates.append((r, c))
                    else:
                        break


            if chain_coordinates and len(chain_coordinates) >= self.game.board.k - 1:
                print(f"Chain:{chain_coordinates}")
                return chain_coordinates  # If the chain is long enough, return its coordinates

            if len(chain_coordinates) > len(max_chain):
                max_chain = chain_coordinates  # Update the longest chain

        return max_chain or None # Return the coordinates of the longest chain
            #längste gefundene Kette wird zurück gegeben
            
            
            
def finde_koordinaten_in_richtung(self, punkt, direction, symbol):
        gefundenen_koordinaten = []
        row, col = punkt 
        counter = 1
        
        if direction == "Waagerecht, rechts" or direction == "Waagerecht, links":
            for i in range(self.game.board.n):
                if self.game.get_symbol(row, i) == symbol:
                    gefundenen_koordinaten.append((row, i))
        elif direction == "Senkrecht, unten" or direction == "Senkrecht, oben":
            for i in range(self.game.board.m):
                if self.game.get_symbol(i, col) == symbol:
                    gefundenen_koordinaten.append((i, col))
        elif direction == "Diagonal, links oben":
            i = row
            j = col 
            while True:
                try: 
                    self.game.get_symbol(i, j)
                except:
                    break
                else:
                    if self.game.get_symbol(i, j)== symbol:
                        gefundenen_koordinaten.append((i, j))
                    i += 1
                    j += 1
        elif direction == "Diagonal, rechts unten":
            i = row
            j = col 
            while True:
                try: 
                    self.game.get_symbol(i, j)
                except:
                    break
                else:
                    if self.game.get_symbol(i, j)== symbol:
                        gefundenen_koordinaten.append((i, j))
                    i -= 1
                    j -= 1
        elif direction == "Diagonal, links unten":
            i = row
            j = col
            while True:
                try: 
                    self.game.get_symbol(i, j)
                except:
                    break
                else:
                    if self.game.get_symbol(i, j)== symbol:
                        gefundenen_koordinaten.append((i, j))
                    i -= 1
                    j += 1
        elif direction == "Diagonal, rechts oben":
            i = row
            j = col
            while True:
                try: 
                    self.game.get_symbol(i, j)
                except:
                    break
                else:
                    if self.game.get_symbol(i, j)== symbol:
                        gefundenen_koordinaten.append((i, j))
                    i += 1
                    j -= 1                  
        print(gefundenen_koordinaten)
        return gefundenen_koordinaten