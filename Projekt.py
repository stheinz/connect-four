#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 16:05:07 2021

@author: steven
"""

#| # Vier Gewinnt
#| Steven Heinz
#|
#| # Vorwort
#| Bei Vier Gewinnt spielt man mit zwei Spielern. Das Ziel ist es, dass ein Spieler entweder horizontal, vertikal, oder diagonal 
#| vier Spielsteine in eine Reihe zu bekommen um zu gewinnen. Falls keiner der beiden Spieler es schafft dies zu erreichen bevor das Spielbrett gefüllt ist,
#| dann wird das Spiel als Unentschieden gewertet. Im Folgenden wird ein Brett mit sechs Zeilen und sieben Spalten verwendet.
#| 
#| Es beginnt Spieler 1(hier: AI1) gefolgt von Spieler 2(hier: AI2).
#| 
#| 
#| # Vermutung 
#| 
#| Wir vermuten, dass Vier Gewinnt ein faires Spiel ist und das die Gewinnchance bei jedem Spieler bei 50% ist.
#| 
#| # Imports

import numpy as np
import random
import matplotlib.pyplot as plt

#| # Globale Variablen

ROW_COUNT = 6
COLUMN_COUNT = 7
REPETITION = 1000

AI1 = 0
AI2 = 1

EMPTY = 0
AI1_PIECE = 1
AI2_PIECE = 2


#| # Vorbereitungen für das Spiel
#| 
#| * Spielbrett 

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


#| * Setzen eines Spielsteins
def drop_piece(board, row, selection, piece):
    board[row][selection] = piece


#| * Prüfen ob die gewünschte Stelle eine gültige ist
def is_valid_location(board, selection):
    # If the last row(here 5) is empty then the selection is valid
    return board[ROW_COUNT - 1][selection] == 0


#| * Nächtse freie Zeile
def get_next_open_row(board, selection):
    # Which row will the piece fall on?
    for r in range(ROW_COUNT):
        if board[r][selection] == 0:
            return r


#| * Ausgabe des Spielbretts in der gewünschten Art zur Überprüfung
# Print the board as we expect it with this game
def print_board(board):
    print(np.flip(board, 0))


#|
#| # Verarbeitung der gesetzten Steine
#| 
#| * Wie können wir festellen wann ein Spieler gewonnen hat?
#| * Wie können wir prüfen ob vier Spielsteine in einer Reihe liegen?
#| * Wie können wir die horizontale, die vertikale und die diagonale überprüfen ?
#| * Was machen wir wenn keiner der beiden Spieler mehr gewinnen kann?
#|
#| In dieser Methode werden all diese Fragen behandelt
# How can the Game know if we won?
# We need the Board and the last piece 
def winning_move(board, piece):
    # We manually Check 
    # 1. Check the horizontal locations for winning
    for columns in range(COLUMN_COUNT - 3):
        for rows in range(ROW_COUNT):
            if board[rows][columns] == piece and board[rows][columns + 1] == piece and board[rows][
                columns + 2] == piece and board[rows][columns + 3] == piece:
                return True

    # 2. Check the vertical locations for winning
    for columns in range(COLUMN_COUNT):
        for rows in range(ROW_COUNT - 3):
            if board[rows][columns] == piece and board[rows + 1][columns] == piece and board[rows + 2][
                columns] == piece and board[rows + 3][columns] == piece:
                return True

                # 3. Check Diaganols
    for columns in range(COLUMN_COUNT - 3):
        for rows in range(ROW_COUNT - 3):
            if board[rows][columns] == piece and board[rows + 1][columns + 1] == piece and board[rows + 2][
                columns + 2] == piece and board[rows + 3][columns + 3] == piece:
                return True

    for columns in range(COLUMN_COUNT - 3):
        for rows in range(3, ROW_COUNT):
            if board[rows][columns] == piece and board[rows - 1][columns + 1] == piece and board[rows - 2][
                columns + 2] == piece and board[rows - 3][columns + 3] == piece:
                return True

            #| # Monte-Carlo Simulation


#| Hier wird der oben beschriebene Code ohne visuelle Ausgaben weiterverwendet, damit eine Monte-Carlo Simulation durchgeführt werden kann.
#| Das Spiel wird so lange gespielt bis entweder ein Spieler die Runde gewonnen hat oder ein Unentschieden eingetreten ist.      
def monte_Carlo():
    game_over = False
    ROUND_COUNT = 0
    turn = 0
    board = create_board()
    AI1_COUNTER = 0
    AI2_COUNTER = 0

    while not game_over:
        # Ask Player One for Input
        if turn == AI1 and not game_over:
            selection = random.randint(0, 6)

            if is_valid_location(board, selection):
                row = get_next_open_row(board, selection)
                drop_piece(board, row, selection, AI1_PIECE)

                if winning_move(board, AI1_PIECE):
                    # print ('AI1 won in ' + str(ROUND_COUNT) + 'Rounds')
                    game_over = True
                    AI1_COUNTER += 1
            else:
                game_over = True

            # Ask Player Two for Input
        else:
            selection = random.randint(0, 6)

            if is_valid_location(board, selection):
                row = get_next_open_row(board, selection)
                drop_piece(board, row, selection, AI2_PIECE)

                if winning_move(board, AI2_PIECE):
                    # print ('AI2 won in ' + str(ROUND_COUNT) + 'Rounds')
                    game_over = True
                    AI2_COUNTER += 1

            else:
                game_over = True

        ROUND_COUNT += 1
        # print_board(board)
        # Player One and Two (Odd Even)
        turn += 1
        turn = turn % 2

    return ROUND_COUNT, AI1_COUNTER, AI2_COUNTER


#| # Ausführen eines Beispiels
#| Da wir nun den Grundstein gesetzt haben führen wir eine beliebige Anzahl an gespielten Runden durch und sammeln die Daten.
# Array with Data
res = []
for i in range(REPETITION):
    res.append(monte_Carlo())
# print(res)

#| # Vorbereitung für die Separierung der Daten in eigene Variablen mit Analyse
#| Die gesammelten Daten müssen nun so separiert werden, dass wir sie besser analysieren und auswerten können.
# Preparation of the variables for Separation of the results 
rounds = []
ai1_win = []
ai2_win = []
tie_game = []

# Array of Triple with 1. Number of Rounds, 2. Win AI1 1(Yes)/0(No), 3. Win AI2 1(Yes)/0(No)
for i in range(REPETITION):
    rounds.append(res[i][0])
    ai1_win.append(res[i][1])
    ai2_win.append(res[i][2])

tie_game.append((REPETITION - sum(ai1_win) - sum(ai2_win)))

# print('Rounds to a win per Game: ' + str(rounds))
# print('Rounds to win per Game mean: ' + str(np.mean(rounds)))
# print('AI1 win' + str(ai1_win))
# print('AI2 win' + str(ai2_win))
print('AI1 has ' + str(sum(ai1_win)) + 'wins')
print('AI2 has ' + str(sum(ai2_win)) + 'wins')

# Winningchance for REPETITION Games
win_rateAI1 = sum(ai1_win) / REPETITION
win_rateAI2 = sum(ai2_win) / REPETITION
# print('Winrate AI1 for ' + str(REPETITION) + 'played Rounds: ' + str(win_rateAI1) + '%')
# print('Winrate AI2 for ' + str(REPETITION) + 'played Rounds: ' + str(win_rateAI2) + '%')

# Played Games
x_dev = []
for i in range(REPETITION):
    x_dev.append(i)
#| # 1. Wie viele Runden werden benötigt um einen Gewinner zu bekommen?
# 1. Plot
plt.title(str(REPETITION) + ' gespielte Runden')
plt.xlabel('Gespielte Runde')
plt.ylabel('Anzahl Spielzüge zum Gewinn eines Spielers')
# Axis
plt.axis([0, REPETITION, 0, 100])

# Needed Rounds to win per Game
plt.plot(x_dev, rounds)
plt.show()
#| # 2. Wie viele Spiele hat Spieler 1 oder Spieler 2 gewonnen und wieviele waren unentschieden?
# 2. Plot
spieler = np.array(["AI1", "AI2", "Tie_Game"])
spieler_ticks = np.array([1.0, 2.0, 3.0])
colors = np.array(['green', 'orange', 'y'])
plt.title('Gewinne pro Spieler bei ' + str(REPETITION) + ' Runden')
plt.xlabel('Spieler')
plt.xticks(spieler_ticks, spieler)
plt.ylabel('Gewinne pro Spieler')
# Axis
plt.axis([0, 4, 0, REPETITION])

# Gewonnene Spiele pro Spieler
gewinne = [sum(ai1_win), sum(ai2_win), tie_game[0]]
bars = plt.bar(spieler_ticks, gewinne, color=colors)
plt.show()
#| # 3. Wo liegt die Gewinnchance der Spieler und wieviele Spiele sind Prozentual unentschieden?
# 3. Plot
# Winningchance per player and Round
ai1_cum = []
ai2_cum = []
summe_ai1 = 0
summe_ai2 = 0

for i in range(REPETITION):
    summe_ai1 = summe_ai1 + ai1_win[i]
    ai1_cum.append(summe_ai1)
    summe_ai2 = summe_ai2 + ai2_win[i]
    ai2_cum.append(summe_ai2)

win_chanceAI1 = []
win_chanceAI2 = []
tieGame = []

for i in range(REPETITION):
    win_chanceAI1.append(ai1_cum[i] / (1 + i))
    win_chanceAI2.append(ai2_cum[i] / (1 + i))
    tieGame.append((1.0 - win_chanceAI1[i] - win_chanceAI2[i]))

# print('AI 1 winchance: ' + str(win_chanceAI1))
# print('AI 2 winchance: ' + str(win_chanceAI2))

plt.title('Kumulierte Häufigkeiten bei ' + str(REPETITION) + ' Runden')
plt.xlabel('Gespielte Runde')
plt.ylabel('Durchschnittliche Wahrscheinlichkeit zu gewinnen')
# Axis
plt.axis([0, REPETITION, 0, 1])

# Needed Rounds to win per Game
plt.plot(x_dev, win_chanceAI1, 'C2', label='AI1')
plt.plot(x_dev, win_chanceAI2, 'C1', label='AI2')
plt.plot(x_dev, tieGame, 'y', label='Tie_Game')
plt.legend(loc="upper left")
plt.show()

#| # Zusammenfassung
#|
#| Im Laufe des Projekts wurde die Vermutung, dass das Spiel Vier Gewinnt ein faires Spiel ist immer fragwürdiger.
#| Als die ersten 1000 Runden gespielt wurden kamen bereits erste Zweifel. 
#| Hier wurde bereits eine Tendenz zum Gewinn eines Spieles auf Seiten des Spieler 1 beobachtet.
#| Im Folgenden wurde die Rundenanzahl auf 100.000 erhöht.
#| Spätestens nach einer Million gespielter Runden wurde klar, 
#| dass die Gewinnwahrscheinlichkeit für Spieler 1 bei ca. 40% liegt, während sie bei Spieler 2 bei ca. 31% liegt.
#| Verblüfend hierbei ist, dass die Chance ein Unentschieden zu bekommen bei ca. 29% liegt.
#|
#| # Fututre Work
#| Für die weitere Arbeit an dem Projekt wären einige Themen interessant.
#| Hierbei können die Richtungen vielseitig sein.
#| Beispiele wären:
#|
#| * Verbesserung der Intelligenz der Spieler, sodass die Anzahl der Runden eines Unentschiedens verringert werden
#| * Veränderungen an der Menge der benötigten Spielsteine die zum Gewinn führen
#| * Veränderung an der größe des Spielbretts
