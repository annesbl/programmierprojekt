# def andere_punkte_kette(self, punkt, direction):
    #     andere_punkte_dict = {}
    #     opponent_symbol = self.get_opponent_symbol()
    #     row, col = punkt 
    #     counter = 1
    #     if direction == "Waagerecht, rechts" or direction == "Waagerecht, links":
    #         for i in col:
    #             if self.game.get_symbol(row, i) == opponent_symbol:
    #                 andere_punkte_dict[counter] = (row, i)
    #                 counter += 1
    #     elif direction == "Senkrecht, unten" or direction == "Senkrecht, oben":
    #         for i in row:
    #              for i in col:
    #             if self.game.get_symbol(i, col) == opponent_symbol:
    #                 andere_punkte_dict[counter] = (i, col)
    #                 counter += 1   
    #     return andere_punkte_dict