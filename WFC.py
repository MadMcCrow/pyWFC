 #  FindPattern
 ## setup indices
 ## extend the grid (make it loopable)

## find pattern neighbourgs
#  Multi Tile pattern

## inputs 
# PatternSize
# OutputSize
# NumberOfIterations

class Colors: 
    LAND     = '\x1b[6;30;42m'
    SEA      = '\x1b[6;30;44m'
    BEACH    = '\x1b[1;36;43m'
    MOUNTAIN = '\x1b[6;7;70m'

# the type of tiles available
class Types :

    # The Actual representation of that type
    Value = None
    Color = None

    def __init__(self , color, letter) :  
        self.Color = color
        self.Value = letter

    def __repr__(self):
         return str( self.Color  + self.Value + '\x1b[0m') 
         



class IVec2D:
    X = 0
    Y = 0

    def __init__(self, x : int, y : int) :
        self.X = x
        self.Y = y

    def __repr__(self):
        return "{" + str("{X},{Y}").format(X=self.X, Y=self.Y) + "}"

def randomIVec2D(MaxSize : IVec2D) -> IVec2D :
    return IVec2D(randrange(MaxSize.X), randrange(MaxSize.Y))


class Tile :

    LAND      = Types(Colors.LAND,     'L')
    SEA       = Types(Colors.SEA,      'W')
    BEACH     = Types(Colors.BEACH,    'B')
    MOUNTAIN  = Types(Colors.MOUNTAIN, 'M')


    # List of possibilities :
    Tileset = [LAND,SEA, BEACH,MOUNTAIN]


    # the types of tile this could be 
    TypeList = None

    def collapse(self, idx : int) : 
        self.TypeList = list(filter(lambda x: ( self.TypeList[idx] == x),  self.TypeList))
    
    def __init__(self) :
        self.TypeList = Tile.Tileset

    def __repr__(self):
        if len(self.TypeList) == 1 :
            return self.TypeList[0].__repr__()
        else :
            retval = "{"
            for type_itr in self.TypeList :
                retval += type_itr.__repr__()
            retval += "}"
            return retval

    def fixedValue(self) :
        if len(self.TypeList) != 1 :
            raise ValueError('this tile is not collapsed, or not set this is wrong')
        return self.TypeList[0]

class Grid :

    Values = None
    Size = None

    def __init__(self, size : IVec2D): 
        print(range(size.X))
        self.Size = size
        rows=[] 
        for i in range(size.X):
            columns=[] 
            for j in range(size.Y):
                tile = Tile()
                tile.collapse(0)
                columns.append(tile)
            rows.append(columns)
        self.Values =rows

    def at(self, pos : IVec2D)  -> Tile:
        return self.Values[pos.X][pos.Y]

    def __repr__(self):
        retval = str()
        for row in self.Values: 
            for col in row :
                 retval = retval + col.__repr__()
            retval = retval +'\n' 
        return retval


class OutputGrid(Grid) :

    def __init__(self, output_size : IVec2D): 
        self.Size = output_size
        rows=[] 
        for i in range(output_size.X):
            columns=[] 
            for j in range(output_size.Y):
                columns.append(Tile())
            rows.append(columns)
        self.Values =rows



class Pattern(Grid):

    # the tile the pattern resolve around
    Center = None


def findPatternInGrid(input: Grid) -> list:
    #lets get all patterns for every
    for i in range(Grid.Size.X):
        for j in range(Grid.Size.Y):
            print (Grid.at(IVec2(i,j)))

        

    


       


Output = OutputGrid(IVec2D(4,4))
print(Output)
Output.at(IVec2D(0,0)).collapse(0)
print(Output)
