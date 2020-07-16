 #  FindPattern
 ## setup indices
 ## extend the grid (make it loopable)

## find pattern neighbourgs
#  Multi Tile pattern

## inputs 
# PatternSize
# OutputSize
# NumberOfIterations


# List of possibilities :
Tileset = ['L','W','B','M']


class IVec2D:
    X = 0
    Y = 0

    def __init__(self, x : int, y : int) :
        self.X = x
        self.Y = y

def randomIVec2D(MaxSize : IVec2D) :
    return IVec2D(randrange(MaxSize.X), randrange(MaxSize.Y))


class Tile :
    Value = None

    def collapse(self, idx) : 
        self.Value = list(filter(lambda remainder: (remainder%Tile.Tileset.size() == idx) , Tile.Tileset))
    
    def __init__(self) :
        self.Value = Tile.Tileset

    def __repr__(self):
         return self.Value.__repr__()

class Grid :

    Values = None
    Size = None

    def __init__(self, output_size : IVec2D): 
        self.Size = output_size
        rows=[] 
        columns=[] 
        for i in range(output_size.X):
            for j in range(output_size.Y):
                columns.append(Tile())
        rows.append(columns)
        self.Values =rows

    def at(self, pos : IVec2D)  :
        return Values[pos.X][pos.Y]

    def __repr__(self):
         return self.Values.__repr__()
       


Output = Grid(IVec2D(10,10))
print(Output)
