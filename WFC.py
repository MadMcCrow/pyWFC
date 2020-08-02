## includes
from array2D import IVec2D
from array2D import Array2D
from math import ceil
from math import floor
from math import log
from random import randrange
 
 #  FindPattern
 ## setup indices
 ## extend the grid (make it loopable)

## find pattern neighbourgs
#  Multi Element pattern

## inputs 
# PatternSize
# OutputSize
# NumberOfIterations

# error class for when it fails to be coherent
class ImpossibleError(Exception):
        pass


# the most basic stored info we have on a grid
class Element(list):

    # Class Properties : 
    _ElemList = []

    ##Instance Properties : 

    #Functions :
    def __init__(self, *args) :
            self +=  args
   
    def collapse(self, to_remove : list) : 
        """  Remove possibilities of this element """
        for t in self.to_remove :
            if t in self :
                self.remove(t)
        if len(self) == 0  :
            raise ImpossibleError("no possibilites left")

    def __repr__(self):
        if len(self) == 1 :
            return self[0].__repr__()
        else :
            retval = "{"
            for item in self :
                retval += item.__repr__()
            retval += "}"
            return retval


# a simple grid containing a unique combination of elements
class Pattern(Array2D)  :

    def __init__(self, array) :
        size = IVec2D(*array._Size) # make sure its a IVec2D
        # populate with none
        super(Pattern,self).__init__(size, array)



# Tuple to hold a pattern and a weight/probability for easy storage
class WeightedPattern (tuple):

    Pattern = property(itemgetter(0))
    Weight = property(itemgetter(1))

    def __new__(self, pattern, weight):
        return tuple.__new__(WeightedPattern, (pattern, weight))


def findPatternsInGrid(input_grid: Array2D, pattern_size : IVec2D) -> list:
    '''
    lets get all patterns contained
    in every 'pattern_size' block
    '''
    pattern_size = IVec2D(*pattern_size)
    all_patterns = []
    for i in range(input_grid._Size.X)     :
        for j in range(input_grid._Size.Y) :
            top_left     = [ i - floor(pattern_size.X / 2.0), j - floor(pattern_size.Y/2.0) ]
            bottom_right = [ i + floor(pattern_size.X / 2.0),  j + floor(pattern_size.Y/2.0)  ]
            new_pattern = Pattern(input_grid.sub(top_left, bottom_right))
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
    _Dimension = None
    _CenterPos = None
    _LogBase   = 2

    # instance Properties
    Coord = None
    PossiblePatterns = []
    Entropy = 0

    def calculateEntropy(self) :
        self.Entropy = 0
        for wp in PossiblePatterns : 
             self.Entropy -= wp.Weight * log(wp.Weight, Cell._LogBase)

    def getElements(self, grid : Array2D) -> Array2D :
        (i,j) = Coord
        top_left     = Coord - Cell._CenterPos
        bottom_right = Coord + ((Cell._Dimension -1 ) - Cell._CenterPos)
        return grid.sub(top_left, bottom_right)
        
class Solver :
    
    # class properties
    _PatternSize = IVec2D(3,3)
    _OutputSize  = IVec2D(20,20)

    # instance properties
    Patterns = []
    Output = None
    Cells  = None

    def readInput( input_file : str) :
        input_grid = Array2D.arrayFromFile(input_file, Element)
        Patterns = Pattern.findPatternInGrid(grid, patternsize)

    def CreateGrid() : 
        output_len = outputsize[1] * outputsize[0]
        Output = Array2D(outputsize, [Element(Element.Tileset)] * output_len )

    def CreateCells():
        Cell._Dimension = self._PatternSize()
        Cell._CenterPos = _PatternSize / 2.0
        Cells = (outputsize, [Element(Element.Tileset)] * output_len )





