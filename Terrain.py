## includes
from array2D import IVec2D
from array2D import Array2D

# basic class for terrain colors 
class Color: 
    LAND     = '\x1b[6;30;42m'
    SEA      = '\x1b[6;30;44m'
    BEACH    = '\x1b[1;36;43m'
    MOUNTAIN = '\x1b[6;7;70m'
    NONE     = '\x1b[0;1;0m'

# helps transform an element into a nicer representation
class Tile (str):

    Index = 0
    Value = None

    def __init__(self , index : int, letter : str, color = Colors.NONE : Color) :  
        self += letter
        self.Index = index
        self.Value = color

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


LAND      = TileType('L', Colors.LAND       )     
SEA       = TileType('W', Colors.SEA        )      
BEACH     = TileType('B', Colors.BEACH      )    
MOUNTAIN  = TileType('M', Colors.MOUNTAIN   ) 

TILESET = [LAND, SEA, BEACH, MOUNTAIN]

# nicely print a Land Array
def strLand(array : Array2D) :
   if len(array) == 0 :
            print("empty array")
            return
        retstr = str()
        # find longest of str and then make every element a str of that length and then return as multilines   
        import re
        lda = lambda k : len(re.sub("[^a-z0-9]+","", repr(k), flags=re.IGNORECASE))
        maxlen = len(repr(max(array, key= lda )))
        for idx in range((array._Size.X * array._Size.Y))    :

            elem = array[idx]
            if elem in TILESET:
                elemstr = TILESET.index 
            else:
                elemstr = str(elem)
            retstr += str(elemstr).center(maxlen + len(str(elemstr)) - len(repr(elemstr)) )

            if idx % array._Size.X == array._Size.X - 1         :
                retstr += '\n'
                
        return retstr

