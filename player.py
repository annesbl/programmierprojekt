#player class
#imports
import sys
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QColor


class Player:
    def __init__(self, name, player_number):
        self.name = name
        self.player_number = player_number

    def make_move(self, button):
        if self.player_number == 1:
            button.setText("X")
        else:
            button.setText("O")