#!python 
# Terrain.py
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
class Tile :

    Color = None
    Value = None

    def __init__(self , letter, color  ) :  
        self.Value = letter
        self.Color = color

    def __str__(self)       :
        return str( self.Color  + repr(self) + '\x1b[0m')  

    def __repr__(self)      :
        return self.Value

    def __eq__(self, other) :
        if isinstance(other, Tile) :
            return self == other
        else :
            return str(other) == self.Value 



    def __hash__(self) :
        return hash(self.Value)

LAND      = Tile( 'L', str(Color.LAND       ) )     
SEA       = Tile( 'W', str(Color.SEA        ) )      
BEACH     = Tile( 'B', str(Color.BEACH      ) )    
MOUNTAIN  = Tile( 'M', str(Color.MOUNTAIN   ) ) 

TILESET = set([LAND, SEA, BEACH, MOUNTAIN])

# nicely print a Land Array
def strLand(array : Array2D) :
    if len(array) == 0 :
            print("empty array")
            return
    retstr = ""
    import re
    #lda = lambda k : len(re.sub("[^a-z0-9]+","", repr(k), flags=re.IGNORECASE))
    #maxlen = len(repr(max(array, key= lda )))
    maxlen = 1
    for idx in range((array.dim().X * array.dim().Y))    :
        elemstr = "-"
        elem = array[idx]
        if len(elem) <= 1 :
            for t in TILESET :
                if t == list(elem)[0] :
                    elemstr = str(t)

        retstr += str(elemstr).center(maxlen + len(str(elemstr)) - len(repr(elemstr)) )
        if idx % array.dim().X == array.dim().X - 1         :
            retstr += '\n'
            
    return retstr
