## includes
from array2D import IVec2D
from array2D import Array2D
from math import ceil
from math import floor
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

class Colors: 
    LAND     = '\x1b[6;30;42m'
    SEA      = '\x1b[6;30;44m'
    BEACH    = '\x1b[1;36;43m'
    MOUNTAIN = '\x1b[6;7;70m'
    NONE     = '\x1b[0;1;0m'

# the type of tiles available
class TileType :

    # The Actual representation of that type
    Value = None
    Color = None

    def __init__(self ,letter, color = Colors.NONE) :  
        self.Color = color
        self.Value = letter

    def __str__(self)       :
        return str( self.Color  + self.Value + '\x1b[0m') 
        
     

    def __repr__(self)      :
        return str(self.Value)
        
         
    def __eq__(self, other) :
        if isinstance(other, TileType) :
            return self.Value == other.Value
        elif isinstance(other, str) :
            return other == self.Value 
        else :
            return False





class Element(list):


    LAND      = TileType('L', Colors.LAND       )     
    SEA       = TileType('W', Colors.SEA        )      
    BEACH     = TileType('B', Colors.BEACH      )    
    MOUNTAIN  = TileType('M', Colors.MOUNTAIN   ) 

    # List of possibilities :
    Tileset = [LAND,SEA, BEACH,MOUNTAIN]

    # entropy Value, stored
    Entropy = 0 


    # Remove possibilities of this tile
    def collapse(self, tiles : list) : 
        for t in tiles :
            if t in self :
                self.remove(t)
        if len(self) == 0  :
            raise ImpossibleError("no possibilites left")

    def __init__(self, val = None) :
        if isinstance(val,str)  :
            self += [Element.Tileset[x] for x in range(len(Element.Tileset)) if Element.Tileset[x] == val]
        elif isinstance(val, TileType) and val in Element.Tileset :
            self = val
        elif isinstance(val, list) :
            for itr in val :
                if isinstance(itr, TileType) and itr in Element.Tileset :
                    self.append(itr)
        else :
            raise ValueError("could not make input a value")

    def __repr__(self):
        if len(self) == 1 :
            return self[0].__repr__()
        else :
            retval = "|"
            for type_itr in self :
                retval += type_itr.__repr__()
            retval += ""
            return retval

    def __str__(self):
        if len(self) == 1 :
            return self[0].__str__()
        else :
            retval = "|"
            for type_itr in self :
                retval += type_itr.__str__()
            retval += ""
            return retval

    
    def __eq__(self, other) :
        if isinstance(other, Element) :
            return list.__eq__(self,other)
        elif isinstance(other, str) :
            if TileType(other) in self.Value :
                return True
            else : 
                return False



class Pattern(Array2D)  :



    def __init__(self, array) :
        size = IVec2D(*array.Size) # make sure its a IVec2D
        # populate with none
        super(Pattern,self).__init__(size, array)

    @staticmethod
    def findPatternInGrid(input_grid: Array2D, pattern_size : IVec2D) -> list:
        #lets get all patterns for every
        pattern_size = IVec2D(*pattern_size)
        all_patterns = []
        for i in range(input_grid.Size.X)     :
            for j in range(input_grid.Size.Y) :
                top_left     = [ i - floor(pattern_size.X / 2.0), j - floor(pattern_size.Y/2.0) ]
                bottom_right = [ i + floor(pattern_size.X / 2.0),  j + floor(pattern_size.Y/2.0)  ]
                new_pattern = Pattern(input_grid.sub(top_left, bottom_right))
                all_patterns.append(new_pattern)

        weighted_pattern_list = []
        for pattern in all_patterns :
            stored = False
            for weighted in weighted_pattern_list:
                if pattern == weighted[0] :
                    weighted[1] += 1
                    stored = True
                    break
            if not stored :
                weighted_pattern_list.append([pattern,1])
        # we have the info we want
        return weighted_pattern_list


# a cell is an array2D pointing to a part the underlying grid.
class cell (Array2D):

    Entropy = 0

    def calculateEntropy(self) :
        return 0

    @staticmethod
    def makeCells() :
        return 



  

patternsize = [3,3]
outputsize  = [20,20]
output_len = outputsize[1] * outputsize[0]

grid = Array2D.arrayFromFile('input', Element)
print(grid)

weight_patternlist = Pattern.findPatternInGrid(grid, patternsize)

patternlist = [pat[0] for pat in weight_patternlist]
print(len(patternlist))
#for pattern in patternlist :
#    print(pattern)



output = Array2D(outputsize, [Element(Element.Tileset)] * output_len )
firstcoord =[randrange(0, outputsize[0]), randrange(0, outputsize[1])]
print(firstcoord)
first_type =  Element.Tileset
first_type.remove(Element.LAND)

output[firstcoord].collapse(first_type)

#for neighbourg in 


print(output)


