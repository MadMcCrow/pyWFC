#!python 
# WFC.py
'''
MIT License

Copyright (c) 2020 PERARD-G N.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
'''
## WFC stands for wave function collapse
## this is my attempt of making it work in python
 

## includes
from operator   import itemgetter

from math import ceil
from math import floor
from math import log

from random import randrange
from random import random

from array2D import IVec2D
from array2D import Array2D

from Terrain import strLand

from numpy      import array

# error class for when it fails to be coherent
class ImpossibleError(Exception):
        pass


# the most basic stored info we have on a grid
class Element(set):

    # Class Properties : 
    _ElemList = []

    ##Instance Properties : 

    #Functions :
    def __init__(self, *args) :
        for E in list(args) :
            self.add(E)
   
    def collapse(self, to_remove : list) : 
        """  Remove possibilities of this element """
        for t in to_remove :
            if t in self :
                self.remove(t)
        if len(self) == 0  :
            raise ImpossibleError("no possibilites left")

    def __repr__(self):
        if len(self) == 1 :
            return repr(list(self)[0])
        else :
            retval = "{"
            for item in self :
                retval += repr(item)
            retval += "}"
            return retval

    def __str__(self)   :
        if len(self) == 1 :
            return str(list(self)[0])
        else :
            retval = "{"
            for item in self :
                retval += str(item)
            retval += "}"
            return retval


    def __eq__(self, other) :
        A = set(list(self))
        B = set(list(other))
        return len(A.intersection(B)) > 0 

    def __ne__(self, other) :
        return not self.__eq__(other)


    def __hash__(self)  :
        return hash("".join([str(c) for c in self]))






# a simple grid containing a unique combination of elements
class Pattern(Array2D)  : pass


# Tuple to hold a pattern and a weight/probability for easy storage
class WeightedPattern (tuple):

    Pattern = property(itemgetter(0))
    Weight = property(itemgetter(1))

    def __new__(self, pattern, weight):
        return tuple.__new__(WeightedPattern, (pattern, weight))


def findPatternPatternsInGrid(input_grid: Array2D, pattern_size : IVec2D) -> list:
    '''
    lets get all patterns contained
    in every 'pattern_size' block
    '''
    pattern_size = IVec2D(*pattern_size)
    all_patterns = []
    for i in range(input_grid.dim().x)     :
        for j in range(input_grid.dim().y) :
            top_left     = [ i - floor(pattern_size.x / 2.0) , j - floor(pattern_size.y /2.0) ]
            bottom_right = [ i + floor(pattern_size.x / 2.0) , j + floor(pattern_size.y /2.0) ]
            new_pattern = input_grid.sub(top_left, bottom_right).view(Pattern)
            all_patterns.append(new_pattern)

    '''  
    Parse list and remove every pattern 
    found multiple time, and count the number
    of appearance of every pattern
    '''
    patlist = []
    for pattern in all_patterns :
        stored = False
        for weighted in patlist:
            if pattern == weighted[0] :
                weighted[1] += 1
                stored = True
                break
        if not stored :
            patlist.append([pattern,1])

    '''  
    normalise by the total number of patterns
    and write as tuples (WeightedPattern)
    '''
    weighted_pattern_list = [WeightedPattern(p,w / len(patlist)) for (p,w) in  patlist ]

    return weighted_pattern_list





# a cell is part of a bigger grid and helps to find 
class Cell :

    # class properties
    _PatternLists = []
    _Dimension = None
    _CenterPos = None
    _LogBase   = 2

    # instance Properties
    Coord = None
    PossiblePatterns = []
    Entropy = 1
    Collapsed = False

    def __init__(self, coord : IVec2D)  :
        self.Coord = coord
        self.PossiblePatterns = Cell._PatternLists
        if not isinstance(Cell._PatternLists[0], WeightedPattern) :
            raise TypeError 
        

    def checkPatterns(self, subgrid : Array2D ) :
        self.PossiblePatterns = []
        pattern_grid = Pattern(subgrid)
        for wp in Cell._PatternLists :
            if wp.Pattern ==  pattern_grid  :
                self.PossiblePatterns.append(wp)
        
        if self.Collapsed == False and len(self.PossiblePatterns) < 1:
            raise ImpossibleError

    def calculateEntropy(self) :
        self.Entropy = 0
        for wp in self.PossiblePatterns : 
             self.Entropy -= wp.Weight * log(wp.Weight, Cell._LogBase)

    def getElements(self, grid : Array2D) -> Array2D :
        #(i,j) = self.Coord
        top_left     = self.Coord - Cell._CenterPos
        bottom_right = self.Coord + ((Cell._Dimension -1 ) - Cell._CenterPos)
        return grid.sub(top_left, bottom_right)

    def setElements(self, grid : Array2D, pattern) :
        (bx,by)  = self.Coord - Cell._CenterPos
        (ex,ey)  = self.Coord + ((Cell._Dimension -1 ) - Cell._CenterPos)
        for y in range(by, ey + 1)  :
            for x in range(bx,ex + 1)   :
                grid[IVec2D(x,y)] = Element(pattern[x - bx, y - by]) 

        
class Solver :
    
    # class properties
    _PatternSize = IVec2D(3,3)
    _OutputSize  = IVec2D(20,20)

    # instance properties
    Input  = None
    Output = None
    Cells  = None
    LastChangedCell = None
    LowestEntropy = None
    End = False

    def readInput(self, input_file : str) :
        self.Input = Array2D.arrayFromFile(input_file, Element)
        Cell._PatternLists = findPatternPatternsInGrid( self.Input, self._PatternSize)
        Element._ElemList = tuple(set(self.Input.tobytes()))

    def createGrid(self) :  
        elem_list = list([[Element(*Element._ElemList)]*self._OutputSize[0] ] * self._OutputSize[1] )
        self.Output = Array2D(elem_list)

    def createCells(self):
        Cell._Dimension = self._PatternSize
        Cell._CenterPos = self._PatternSize / 2.0
        cells_list = [[Cell(IVec2D(x,y)) for x in range(self._OutputSize.x)] for y in range(self._OutputSize.y)]
        self.Cells = Array2D(cells_list)
        raise ValueError( "{}".format(self.Cells))

    #step 1
    def observe(self) :
        '''  
        "observe" is check for all the possibly modified slots 
        we only need to check in the region of the previously changed cell
        to do so, we get the grid of cell "centered" on the last changed cell
        and check to remove.
        we also take time to consider
        ''' 
        min_entropy = 1
        min_entropy_coord = IVec2D(0,0) 
        no_entropy = True

        top_left     = self.LastChangedCell - Cell._CenterPos
        bottom_right = self.LastChangedCell + ((Cell._Dimension -1 ) - Cell._CenterPos)
        toChangeCell = self.Cells.sub(top_left, bottom_right)

        for cell in toChangeCell :
            cell.checkPatterns(cell.getElements(self.Output))
            if cell.Collapsed == False :
                cell.calculateEntropy()
                no_entropy = False # we saw some entropy left
                if cell.Entropy <= min_entropy :
                    min_entropy = cell.Entropy
                    min_entropy_coord = cell.Coord

        if no_entropy == True :
            self.End = True
        else :
            self.LowestEntropy = min_entropy_coord

    #step 2
    def collapse(self)  :
        '''  
        "collapse" is forcing a state on the lowest entropy 
        this means throwing a dice and using weigted probabilities 
        to force the cell to only have one pattern,
        thus limiting the possibilities of the underlying pixels
        We could chose to be less violent and only remove the least possible pattern.
        ''' 
        if self.End == True : 
            return

        random_value = random()
        to_collapse = self.Cells[self.LowestEntropy]
        pats = to_collapse.PossiblePatterns
        sum_weights = sum([el.Weight for el in to_collapse.PossiblePatterns])
        patterns = [WeightedPattern(el[0] ,sum( [ wei / sum_weights for (pat,wei) in pats[:pats.index(el)+1] ] )) for el in pats]
        select = [t for (t, w) in reversed(patterns) if w >= random_value][0]
        # apply :
        self.Cells[self.LowestEntropy].PossiblePatterns = [select]
        self.Cells[self.LowestEntropy].Collapsed = True
        self.Cells[self.LowestEntropy].setElements(self.Output, select)
        # save our modification
        self.LastChangedCell = self.LowestEntropy



    def run(self) :
        count = 0
        try :

            self.LowestEntropy = IVec2D(randrange(self.Output.dim().x), randrange(self.Output.dim().y))
            self.collapse()
            while self.End == False :
                count +=1
                self.observe()
                self.collapse()
                
        except ImpossibleError:
            print("stopped at loop number {c}".format(c=count))
            print(strLand(self.Output))
            self.createGrid()
            self.createCells()
            self.run()
            pass

        


    def __init__(self, input_file : str) :
        self.readInput(input_file)
        self.createGrid()
        self.createCells()
        



'''  
Now we only have to use our solver to actually produce a result :
''' 
Solver._PatternSize = IVec2D(3,3)
Solver._OutputSize  = IVec2D(10,10)
solver = Solver("input")
solver.run()



        



    





