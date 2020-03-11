#!/usr/bin/env python3
import sys
import time
from queue import Queue
from copy import deepcopy

winCond = False
cornerPos = 0

#-------------------------gameBoard class definition-----------------------------
class gameBoard:

    #Constructor
    def __init__(self, x, y, z, spawnArr):
        self.spawns = spawnArr
        self.goal = z
        self.moves = ""
        self.numMoves = 0
        self.board = [[0 for i in range(x)] for j in range(y)]

    #prettyPrint function
    def printBoard(self, timer):
        print("%d" % ((time.time() - timer) * 1000000))
        print(self.numMoves)
        print(self.moves)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                content = print(self.board[i][j], end = " ")
            print("")

    #Check for finish condition, iterative. End on self.goal
    def checkFinish(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == self.goal:
                    return True

    #Using a spawn array, spawn new tiles in specific order
    def spawnNewTile(self):
        #assign new value to spawned tile; replace the spawned tile to back of spawn list
        newTile = self.spawns[0]
        self.spawns.append(self.spawns.pop(0))
        #set to corner 0 (Top Left)
        self.currentPos = 0

        if self.board[0][0] == 0:
            self.board[0][0] = newTile
            return
        elif self.board[0][len(self.board[0])-1] == 0:
            self.board[0][len(self.board[0])-1] = newTile
            return
        elif self.board[len(self.board)-1][len(self.board[0])-1] == 0:
            self.board[len(self.board)-1][len(self.board[0])-1] = newTile
            return
        elif self.board[len(self.board)-1][0] == 0:
            self.board[len(self.board)-1][0] = newTile
        else:
            return

    #Following functions are for movement on board, tile collapsing
    def mvUp(self):
        self.moves += "U"
        self.numMoves += 1
        # Condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1, 0, -1):
                    if self.board[j-1][i] == 0:
                        self.board[j-1][i] = self.board[j][i]
                        self.board[j][i] = 0
        # Add tiles
        for i in range(len(self.board)):
            for j in range(len(self.board[i]) - 1):
                if self.board[j+1][i] == self.board[j][i]:
                    self.board[j][i] = self.board[j][i] + self.board[j+1][i]
                    self.board[j+1][i] = 0
        # Re-condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i]) - 1, 0, -1):
                    if self.board[j-1][i] == 0:
                        self.board[j-1][i] = self.board[j][i]
                        self.board[j][i] = 0
        return self

    def mvDown(self):
        self.moves += "D"
        self.numMoves += 1
        # Condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1):
                    if self.board[j+1][i] == 0:
                        self.board[j+1][i] = self.board[j][i]
                        self.board[j][i] = 0
        # Add tiles
        for i in range(len(self.board)):
            for j in range(len(self.board[i])-1, 0, -1):
                if self.board[j-1][i] == self.board[j][i]:
                    self.board[j][i] = self.board[j][i] + self.board[j-1][i]
                    self.board[j-1][i] = 0
        # Condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1):
                    if self.board[j+1][i] == 0:
                        self.board[j+1][i] = self.board[j][i]
                        self.board[j][i] = 0
        return self

    def mvLeft(self):
        self.moves += "L"
        self.numMoves += 1
        #Condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1, 0, -1):
                    if self.board[i][j-1] == 0:
                        self.board[i][j-1] = self.board[i][j]
                        self.board[i][j] = 0
        #Add tiles
        for i in range(len(self.board)):
            for j in range(len(self.board[i])-1):
                if self.board[i][j+1] == self.board[i][j]:
                    self.board[i][j] = self.board[i][j] + self.board[i][j+1]
                    self.board[i][j+1] = 0
        #Re-condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i]) - 1, 0, -1):
                    if self.board[i][j - 1] == 0:
                        self.board[i][j - 1] = self.board[i][j]
                        self.board[i][j] = 0
        return self

    def mvRight(self):
        self.moves += "R"
        self.numMoves += 1
        #Condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1):
                    if self.board[i][j+1] == 0:
                        self.board[i][j+1] = self.board[i][j]
                        self.board[i][j] = 0
        # Add tiles
        for i in range(len(self.board)):
            for j in range(len(self.board[i])-1, 0, -1):
                if self.board[i][j] == self.board[i][j-1]:
                    self.board[i][j] = self.board[i][j-1] + self.board[i][j]
                    self.board[i][j-1] = 0
        #Re-condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1):
                    if self.board[i][j+1] == 0:
                        self.board[i][j+1] = self.board[i][j]
                        self.board[i][j] = 0
        return self

#----------------------- end of gameBoard class ---------------------------------
#Read input.txt, or test cases
goal = int(input())
width, height = map(int, input().split())
spawnList = list(map(int, input().split()))

#instantiate a new gameBoard, then fill board with input
x = gameBoard(width, height, goal, spawnList)
for i in range(len(x.board)):
    x.board[i] = list(map(int, input().split()))

#--------------------------- Problem Solving ------------------------------------
#set timer
start_time = time.time()
q = Queue()

#enqueue the initial state as a deep copy
q.put(x)
while(not(winCond) and not(q.empty())):
    #Pop queue
    a = q.get()
    #evaluate children of a, 4 states created
    stU = deepcopy(a)
    stD = deepcopy(a)
    stL = deepcopy(a)
    stR = deepcopy(a)
    #generate move states
    stU = stU.mvUp()
    stD = stD.mvDown()
    stL = stL.mvLeft()
    stR = stR.mvRight()
    #determine if redundant move
    #enqueue states to be checked on next iteration
    if stU.board != a.board:
        stU.spawnNewTile()
        q.put(stU)
    if stD.board != a.board:
        stD.spawnNewTile()
        q.put(stD)
    if stL.board != a.board:
        stL.spawnNewTile()
        q.put(stL)
    if stR.board != a.board:
        stR.spawnNewTile()
        q.put(stR)
    #check for win condition
    if stU.checkFinish():
        x = stU
        winCond = True
    if stD.checkFinish():
        x = stD
        winCond = True
    if stL.checkFinish():
        x = stL
        winCond = True
    if stR.checkFinish():
        x = stR
        winCond = True

#finish state
#time converted to microsenconds
x.printBoard(start_time)
