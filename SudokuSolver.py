############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Christian Picofazzi"

############################################################
# Imports
############################################################

# Include your imports here, if any are used
import copy
import random
import os

############################################################
# Section 1: Sudoku
############################################################

def sudoku_cells():
    cells = [(x,y) for x in range(9) for y in range(9)]
    return cells

def sudoku_arcs():
    allArcs = []
    for x in range(9):
        
        for y in range(9):
            rowsArcs = [((x,y),(x,t))for t in range(9) if y != t]
            colsArcs = [((x,y),(t,y))for t in range(9) if x != t]
            allArcs += rowsArcs
            allArcs += colsArcs
            #BOX ARC BOUNDS
                #(0,0) - (2,2)    (0,3) - (2,5)     (0,6) - (2,8)
                #(3,0) - (3,2)    (3,3) - (5,5)     (3,6) - (5,8)
                #(5,0) - (5,2)    (5,3) - (8,5)     (5,6) - (8,8)
            
            if x < 3:
                if y < 3:
                    boxArcs = [((x,y),(a,b))for a in range(3) for b in range(3) if y != b or x != a]
                elif y < 6:
                    boxArcs = [((x,y),(a,b))for a in range(3) for b in range(3,6) if y != b or x != a]
                else:
                    boxArcs = [((x,y),(a,b))for a in range(3) for b in range(6,9) if y != b or x != a]
            elif x < 6:
                if y < 3:
                    boxArcs = [((x,y),(a,b))for a in range(3,6) for b in range(3) if y != b or x != a]
                elif y < 6:
                    boxArcs = [((x,y),(a,b))for a in range(3,6) for b in range(3,6) if y != b or x != a]
                else:
                    boxArcs = [((x,y),(a,b))for a in range(3,6) for b in range(6,9) if y != b or x != a]
            else:
                if y < 3:
                    boxArcs = [((x,y),(a,b))for a in range(6,9) for b in range(3) if y != b or x != a]
                elif y < 6:
                    boxArcs = [((x,y),(a,b))for a in range(6,9) for b in range(3,6) if y != b or x != a]
                else:
                    boxArcs = [((x,y),(a,b))for a in range(6,9) for b in range(6,9) if y != b or x != a]
            allArcs += boxArcs
    return allArcs
                    

def valid_arc_cell(cell):
    #print((x,y))
    allArcs = []
    x = cell[0]
    y = cell[1]
    rowsArcs = [((x,t),(x,y))for t in range(9) if y != t]
    colsArcs = [((t,y),(x,y))for t in range(9) if x != t]
    allArcs += rowsArcs
    allArcs += colsArcs
    #BOX ARC BOUNDS
        #(0,0) - (2,2)    (0,3) - (2,5)     (0,6) - (2,8)
        #(3,0) - (3,2)    (3,3) - (5,5)     (3,6) - (5,8)
        #(5,0) - (5,2)    (5,3) - (8,5)     (5,6) - (8,8)
    
    if x < 3:
        if y < 3:
            boxArcs = [((a,b),(x,y))for a in range(3)  for b in range(3) if y != b or x != a]
        elif y < 6:
            boxArcs = [((a,b),(x,y))for a in range(3)  for b in range(3,6) if y != b or x != a]
        else:
            boxArcs = [((a,b),(x,y))for a in range(3)  for b in range(6,9) if y != b or x != a]
    elif x < 6:
        if y < 3:
            boxArcs = [((a,b),(x,y))for a in range(3,6)  for b in range(3) if y != b or x != a]
        elif y < 6:
            boxArcs = [((a,b),(x,y))for a in range(3,6)  for b in range(3,6) if y != b or x != a]
        else:
            boxArcs = [((a,b),(x,y))for a in range(3,6)  for b in range(6,9) if y != b or x != a]
    else:
        if y < 3:
            boxArcs = [((a,b),(x,y))for a in range(6,9)  for b in range(3) if y != b or x != a]
        elif y < 6:
            boxArcs = [((a,b),(x,y))for a in range(6,9)  for b in range(3,6) if y != b or x != a]
        else:
            boxArcs = [((a,b),(x,y))for a in range(6,9)  for b in range(6,9) if y != b or x != a]
    allArcs += boxArcs
    return allArcs

def read_board(path):
    maxSet = set([1,2,3,4,5,6,7,8,9])
    
    x = 0
    y = 0
    board  = {}
    with open(path,'Ur') as myFile:
        for chunk in myFile:
            y = 0
            #print(chunk)
            for char in chunk:
                if char == '\n':
                    pass
                elif char == '*':
                    board[(x,y)] = maxSet
                else:
                    #print(x,y  , "  ",   int(char)) 
                    board.update({(x,y): set([int(char)])})
                y +=1
            x +=1
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    maxSet = set([1,2,3,4,5,6,7,8,9])

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]
    def get_row_arcs(self, cell):
        x = cell[0]
        y = cell[1]
        rowsArcs = [(x,t)for t in range(9) if y != t]
        return set(rowsArcs)
    def get_col_arcs(self, cell):
        x = cell[0]
        y = cell[1]
        colsArcs = [(t,y)for t in range(9) if x != t]
        return set(colsArcs)
    
    def get_box_arcs(self, cell):
        x = cell[0]
        y = cell[1]

        if x < 3:
            if y < 3:
                boxArcs = [(a,b)for a in range(3)  for b in range(3) if y != b or x != a]
            elif y < 6:
                boxArcs = [(a,b)for a in range(3)  for b in range(3,6) if y != b or x != a]
            else:
                boxArcs = [(a,b)for a in range(3)  for b in range(6,9) if y != b or x != a]
        elif x < 6:
            if y < 3:
                boxArcs = [(a,b)for a in range(3,6)  for b in range(3) if y != b or x != a]
            elif y < 6:
                boxArcs = [(a,b)for a in range(3,6)  for b in range(3,6) if y != b or x != a]
            else:
                boxArcs = [(a,b)for a in range(3,6)  for b in range(6,9) if y != b or x != a]
        else:
            if y < 3:
                boxArcs = [(a,b)for a in range(6,9)  for b in range(3) if y != b or x != a]
            elif y < 6:
                boxArcs = [(a,b)for a in range(6,9)  for b in range(3,6) if y != b or x != a]
            else:
                boxArcs = [(a,b)for a in range(6,9)  for b in range(6,9) if y != b or x != a]

        return set(boxArcs)
    def remove_inconsistent_values(self, cell1, cell2):
        maxSet = set([1,2,3,4,5,6,7,8,9])
        cell_1_Set = self.get_values(cell1)
        cell_2_Set = self.get_values(cell2)
        
        if len(cell_1_Set) == 1:
            if cell_1_Set.issubset(cell_2_Set):
                #print ("", cell2, " ",cell_2_Set, "    ", cell1, " ",cell_1_Set)
                #print("cell_2_SET =  :" ,self.get_values(cell2) - self.get_values(cell1))
                self.board[cell2] = self.get_values(cell2) - self.get_values(cell1)
                return True
            else:
                return False
        elif len(cell_2_Set) == 1:
            if cell_2_Set.issubset(cell_1_Set):
                self.board[cell1] = self.get_values(cell1) - self.get_values(cell2)
                return True 
            else:
                return False
        else:
            return False


    def infer_ac3(self):
        #print("DOING INFER")
        arcQueue = copy.copy(Sudoku.ARCS)
        #print(arcQueue)

        while len(arcQueue) > 0:
            #if len(arcQueue) < 10:
                #print(arcQueue)
            cell1,cell2 = arcQueue.pop(0)
            #print(cell1,"  ", cell2)
            if self.remove_inconsistent_values(cell1,cell2):
                #print("\t\t\t\t Cell ", cell1, "  Length ", len(self.board[cell1]) )
                if len(self.board[cell1]) <1 or len(self.board[cell2]) < 1 :
                    #print("\t\t\t\t\t CELL IS INCONSISTENT ")
                    return False
                for cell3 in set(valid_arc_cell(cell1)) - set([cell2]) :
                    #print(cell3,"  ", cell1)
                    if cell3 not in arcQueue:
                        arcQueue.append(cell3)
        #print (arcQueue)
        return True

    def collective_Union(self, cellSet):
        totalUnion = set([])
        for cell in cellSet:
            totalUnion = totalUnion.union(self.board[cell])
        return totalUnion

    def is_solved(self):
        allCELLS = self.CELLS
        for cell in allCELLS:
            #print("check")
            if len(self.board[cell]) > 1:   
                return False
        return True


    def infer_improved(self):
        stopped = False
        while not stopped: 
            allCELLS = Sudoku.CELLS
           
            boardCpy = copy.copy(self.board)
            success = Sudoku.infer_ac3(self)
            if not success:
                return False
            for cell in allCELLS:
                currSet = self.board[cell]
                if len(currSet) > 1:
                    rowArcCells = self.get_row_arcs(cell)
                    rowUnion = self.collective_Union(rowArcCells)
                    
                    colArcCells = self.get_col_arcs(cell)
                    colUnion = self.collective_Union(colArcCells)

                    boxArcCells = self.get_box_arcs(cell)
                    boxUnion = self.collective_Union(boxArcCells)

                    threeIntsect = rowUnion.intersection(colUnion)
                    threeIntsect = threeIntsect.intersection(boxUnion)

                
                    if len(self.maxSet - threeIntsect)==1:
                        self.board[cell] = self.maxSet - threeIntsect
            if boardCpy == self.board:
                stopped = True
        if not success:
            return False
        return True
            
            
            #print("after sovle")
    def check_consistency(self, cell1, value):
        #check row
        for cell2 in self.get_row_arcs(cell1):
            if self.board[cell2] == set([value]):
                return False
        #check col
        for cell2 in self.get_col_arcs(cell1):
            if self.board[cell2] == set([value]):
                return False

        #check box
        for cell2 in self.get_box_arcs(cell1):
            if self.board[cell2] == set([value]):
                return False
        return True
    
    def random_cell(self):
        while True:
            cell = random.choice(self.CELLS)
            if len(self.board[cell]) >1:
                return cell
            
    def infer_with_guessing(self):
        
        self.infer_improved()
        #if problem is solved
        if  self.is_solved():
            return True
        #set cell = random cell with a set > 1
        cell = self.random_cell()
        #print("Random CELL :", cell, "  CELL SET :", self.board[cell])
        #for value = each possible answer in cell's Set
        for value in self.board[cell]:
            #print("\tVALUE: ", value, "CELL : ", cell)
            #if value make the board consistent -> check the row and colm and box of the cell to see if that answer was already picked
            if self.check_consistency(cell, value):
                #make a copy of the Sudoku game
                gameCopy = copy.deepcopy(self)
                #set that copy cell = value
                gameCopy.board[cell] = set([value])
                #Success= improved inferencc()
                success = gameCopy.infer_improved()
                #print ("\t\t\t SUCCESS ", success)
                #if success is True:
                if success:
                    
                    #result = self.backtrack
                    result = gameCopy.infer_with_guessing()

                    #print("\t\t\t",result)
                    if result:
                        self.board = copy.deepcopy(gameCopy.board)
                        return True
            #remove value from the cell's set
            #print("REMOVING :", self.board[cell] - set([value]), ' = ', self.board[cell], " - ", set([value]))
            self.board[cell] = self.board[cell] - set([value])
        return False

                


############################################################
# Section 2: Feedback
############################################################
feedback_question_1 = """
20
"""

feedback_question_2 = """
The backtracking was most difficult, trying to figure out when to backtrack and how far
"""

feedback_question_3 = """
I like the progression up to the hardest problem. It made the entire homework manageable and easier to understand 
"""
