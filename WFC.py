## includes
from math import ceil
from math import floor
 
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
class TileType :

    # The Actual representation of that type
    Value = None
    Color = None

    def __init__(self , color, letter) :  
        self.Color = color
        self.Value = letter

    def __repr__(self)      :
        return str( self.Color  + self.Value + '\x1b[0m') 
         
    def __eq__(self, other) :
        return self.Value == other.Value



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

    LAND      = TileType(Colors.LAND,     'L')
    SEA       = TileType(Colors.SEA,      'W')
    BEACH     = TileType(Colors.BEACH,    'B')
    MOUNTAIN  = TileType(Colors.MOUNTAIN, 'M')


    # List of possibilities :
    Tileset = [LAND,SEA, BEACH,MOUNTAIN]

    # the types of tile this could be 
    TypeList = None

    def collapse(self, idx : int) : 
        self.TypeList = list(filter(lambda x: ( self.TypeList[idx] == x),  self.TypeList))
    
    def __init__(self) :
        self.TypeList = Tile.Tileset

    def __init__(self, val : TileType) :
        self.TypeList = [val]

    def __repr__(self):
        if len(self.TypeList) == 1 :
            return self.TypeList[0].__repr__()
        else :
            retval = "{"
            for type_itr in self.TypeList :
                retval += type_itr.__repr__()
            retval += "}"
            return retval

    
    def __eq__(self, other) :
        return self.TypeList == other.TypeList


    def fixedValue(self) :
        if len(self.TypeList) != 1 :
            raise ValueError('this tile is not collapsed, or not set this is wrong')
        return self.TypeList[0]

    
def findTypeFromChar(char : str) -> TileType :
    matches = [x for x in Tile.Tileset if  x.Value == char[0]]
    if len(matches) == 1    :
        return matches[0]
    else                    :
        raise ValueError('there was no type with this Char')

    

class Grid :

    Values = None
    Size = None

    def __init__(self, size : IVec2D): 
        self.Size = size

    def at(self, pos : IVec2D)  -> Tile:
        return self.Values[pos.X % self.Size.X][pos.Y % self.Size.Y]

    def __repr__(self):
        retval = str()
        for row in self.Values: 
            for col in row :
                 retval = retval + col.__repr__()
            retval = retval +'\n' 
        return retval

    def __eq__(self, other) :
        return self.Values == other.Values
         



def subGrid(grid : Grid, begin :IVec2D, end : IVec2D) -> Grid:
    Size = IVec2D(end.X - begin.X, end.Y - begin.Y)
    retval = Grid(Size)
    row = []
    columns =[] 
    for i in range(begin.X, end.X):
            columns = []
            for j in range(begin.Y, end.Y):
                columns.append(grid.at(IVec2D(i,j)))
            row.append(columns)
    retval.Values = row
    return retval
    

def gridFromFile(file_url : str) -> Grid:
    f = open(file_url,"rt")
    input_text =  f.read()
    f.close()
    columns=[]
    rows   =[]
    line_count   = 0
    column_count = 0
    for char in input_text :
        if char == '\n' and len(columns) > 0 :
            line_count  += 1
            column_count = 0
            rows.append(columns)
            columns=[]
        else :
            column_count+= 1
            columns.append(Tile(findTypeFromChar(char)))
    retval = Grid(IVec2D(column_count,line_count ))
    retval.Values = rows
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

    def __init__(self, grid : Grid, center : Tile) :
        Grid.__init__(self, grid.Size)
        self.Values = grid.Values
        self.Center = center

    def __eq__(self, other):
        if  self.Values == other.Values :
            return True
        return False

def findPatternInGrid(input_grid: Grid, pattern_size : IVec2D) -> list:
    #lets get all patterns for every
    all_patterns = []
    for i in range(input_grid.Size.X)     :
        for j in range(input_grid.Size.Y) :
            top_left     = IVec2D( i - floor(pattern_size.X / 2.0), j - floor(pattern_size.Y/2.0))
            bottom_right = IVec2D( i + ceil(pattern_size.X / 2.0),  j + ceil(pattern_size.Y/2.0))
            new_pattern = Pattern(subGrid(input_grid, top_left, bottom_right), input_grid.at(IVec2D(i,j)))
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

def findPatternsInList(input_list : list, input_type : TileType ) -> list :
    retval = []
    for pattern in input_list :
        if not isinstance(pattern, Pattern) :
            raise ValueError("not a pattern")
        if pattern.Center.fixedValue() == input_type :
            retval.append(pattern)
    return retval

    

patternsize = IVec2D(3,3)
grid = gridFromFile('input')
print(grid)
weight_patternlist = findPatternInGrid(grid, patternsize)
patternlist = [pat[0] for pat in weight_patternlist]
print(patternlist)
land_only = findPatternsInList(patternlist, Tile.LAND)
for pattern in land_only :
    print(pattern)

