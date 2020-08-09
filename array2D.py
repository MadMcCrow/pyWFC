#!python 
# array2D.py
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

from operator   import itemgetter
from copy       import copy
from random     import randrange

# error class for when it fails to be coherent
class Math2DError(Exception):
        pass


# 2D int vector
class IVec2D (tuple):

    X = property(itemgetter(0))
    Y = property(itemgetter(1))

    def __new__(self, x, y):
        return tuple.__new__(IVec2D, (round(x), round(y)))

    def __repr__(self):
        return "{" + str("{X},{Y}").format(X=self[0], Y=self[0]) + "}"

    def __truediv__(self, other) :
        if isinstance(other, float) or isinstance(other, int) :
            return IVec2D(self.X / other, self.Y / other)
        elif isinstance(other,IVec2D ):
            return IVec2D(self.X / other.X, self.Y / other.Y)
        else:
            raise Math2DError("cannot divide {a} by {b}".format(a = self, b = other))

    def __mul__(self, other) :
        if isinstance(other, float) or isinstance(other, int) :
            return IVec2D(self.X * other, self.Y * other)
        elif isinstance(other,IVec2D ):
            return IVec2D(self.X * other.X, self.Y * other.Y)
        else:
            raise Math2DError("cannot multiply {a} by {b}".format(a = self, b = other))

    def __add__(self, other) :
        if isinstance(other, float) or isinstance(other, int) :
            return IVec2D(self.X + other, self.Y + other)
        elif isinstance(other,IVec2D ):
            return IVec2D(self.X + other.X, self.Y + other.Y)
        else:
            raise Math2DError("cannot add {a} by {b}".format(a = self, b = other))

    def __sub__(self, other) :
        if isinstance(other, float) or isinstance(other, int) :
            return IVec2D(self.X - other, self.Y - other)
        elif isinstance(other,IVec2D ):
            return IVec2D(self.X - other.X, self.Y - other.Y)
        else:
            raise Math2DError("cannot add {a} by {b}".format(a = self, b = other))



# turn index into array position
def PositionFromIndexAndSize(idx : int , size : IVec2D) -> IVec2D:
        return  IVec2D( idx % size.X, (idx // size.X) % size.Y )
        

# 2D array class for readability
class Array2D(list):


    # dimension of the array
    _Size  = None

    # list of items there should be _Size.X * _Size.Y

    def mod(self, x : int, y : int ) -> IVec2D  :
        col = x % self._Size.X
        row = y % self._Size.Y
        return IVec2D(col, row)

    def idx(self, x : int, y : int) -> int      :
        (col, row) = self.mod(x,y)
        return col + (row * self._Size.X)

    def end(self) -> IVec2D   :
        col = self._Size.X -1
        row = self._Size.Y -1
        return IVec2D(col,row)

    # get the value of the items stored at a certain location
    def at(self, x : int ,y : int) :
        return list.__getitem__(self, self.idx(x,y))        

    # init with a IVec2D, but that's just a tuple
    def __init__(self, size : IVec2D, input_list = None) :  
        size = IVec2D(*size) # make sure its a IVec2
        super(Array2D, self).__init__(input_list)
        # if input_list is not None :
        #    for idx in range(len(input_list)) :
        #        self[idx] = copy(input_list[idx])
        self._Size = size

    def __setitem__(self, key : IVec2D, value):
        if isinstance(key, IVec2D) :
            list.__setitem__(self, self.idx(key[0],key[1]), value)
        else    :
            list.__setitem__(self, key, value)

    def __getitem__(self, key : IVec2D ):
        if isinstance(key, list)  or isinstance(key, tuple):
            return self.at(key[0],key[1])
        else :
            return list.__getitem__(self, key)
        
    # get a smaller portion of the array 
    def sub(self, begin : IVec2D, end : IVec2D):
        (bx,by) = begin[:2]
        (ex,ey) = end[:2]
        #s = copy(self)
        indices = []   
        for y in range(by, ey + 1)  :
            for x in range(bx,ex + 1)   :
                indices.append(self.idx(x,y))
        s = Array2D([ex + 1 - bx, ey + 1 - by],  [self[index] for index in indices])
        return s

    def __repr__(self):
        return  super(Array2D, self).__repr__() + " of size " + str(self._Size)

    def __str__(self):
        if len(self) == 0 :
            print("empty array")
            return
        retstr = str()
        # find longest of str and then make every element a str of that length and then return as multilines   
        import re
        lda = lambda k : len(re.sub("[^a-z0-9]+","", repr(k), flags=re.IGNORECASE))
        maxlen = len(repr(max(self, key= lda )))
        for idx in range((self._Size.X * self._Size.Y))    :
            elem = self[idx]
            retstr += str(elem).center(maxlen + len(str(elem)) - len(repr(elem)) )
            if idx % self._Size.X == self._Size.X - 1         :
                retstr += '\n'
        return retstr

    def randomPosition(self) -> IVec2D :
        col =  randrange(self._Size.X)
        row =  randrange(self._Size.Y)
        return IVec2D(col, row)

    #def __eq__(self, other) :
    #    return set(self).intersection(other) == set(self)


    @staticmethod
    def arrayFromFile(file_url : str, elem_cls : type):
        f = open(file_url,"rt")
        input_text =  f.read()

        f.close()
        items = []
        row_c   = 1 # because the last one is not counted by the loop
        col_c   = 0
        prev_col_c = 0 # will be used for sanity check
        for char in input_text :
            if char == '\n' and len(items) > 0 :
                if prev_col_c < col_c :
                    raise IndexError("too many character in col, prev is {prev} and current is {curr}".format(prev = prev_col_c, curr = col_c))
                row_c += 1
                col_c = 0
            else :
                col_c += 1
                prev_col_c = col_c
                items.append(elem_cls(char))
        retval = Array2D([col_c, row_c], items)
        return retval

    def PositionFromIndex(self, idx : int ) -> IVec2D:
        return  IVec2D( idx % self._Size.X, (idx //self._Size.X) % self._Size.Y )
