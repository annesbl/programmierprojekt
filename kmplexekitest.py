class KomplexeKI_test(Player):
    def __init__(self, name, symbol, game):
         super().__init__(name, symbol)
         self.game = game
         self.is_komplexeki = True
         
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
        
        for row in range (game.board.m):
            result_row = EinfacheKI.check_row(row, self.player.symbol)
            
    

    def make_move_for_row(self, player_symbol):
        for row in range(self.board.m):
            move = self.check_row(row, player_symbol)
            if move is not None:
                return move
        return None

    def make_move_for_column(self, player_symbol):
        for col in range(self.board.n):
            move = self.check_column(col, player_symbol)
            if move is not None:
                return move
        return None
        
        
        
    

    def check_row(self, row, player_symbol):
        for col in range(self.board.n - self.board.k + 1):
            symbols_in_row = [self.board.get_symbol(row, col + i) for i in range(self.board.k)]
            if (symbols_in_row.count(player_symbol) == self.board.k - 1 and '' not in symbols_in_row) or \
                    (col > 0 and col < self.board.n - self.board.k and
                    symbols_in_row[self.board.k // 2] == player_symbol and
                    symbols_in_row[self.board.k - 1] == player_symbol and
                    symbols_in_row[0] == ''):
                empty_index = symbols_in_row.index('')  
                return row, col + empty_index
        return None

    def check_column(self, col, player_symbol):
        for row in range(self.board.m - self.board.k + 1):
            symbols_in_column = [self.board.get_symbol(row + i, col) for i in range(self.board.k)]
            if (symbols_in_column.count(player_symbol) == self.board.k - 1 and '' not in symbols_in_column) or \
                    (row > 0 and row < self.board.m - self.board.k and
                    symbols_in_column[self.board.k // 2] == player_symbol and
                    symbols_in_column[self.board.k - 1] == player_symbol and
                    symbols_in_column[0] == ''):
                empty_index = symbols_in_column.index('')  
                return row + empty_index, col
        return None
        
        
        
        
                
        
    def find_optimal_placement_defense(self):
         pass
    def make_einfacheki_move (self):
        move = self.game.make_move_for_column(self.symbol) or self.game.make_move_for_row(self.symbol)
        if move is not None:
            row, col = move
            self.game.place_symbol(row, col)

'''
# Beispiel für die Verwendung der KI in Ihrer Game-Klasse
if self.current_player.is_zufallski:
    self.current_player.make_zufallski_move()
    '''
 