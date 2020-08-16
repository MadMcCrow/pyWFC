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
from numpy      import ndarray
from numpy      import asarray
from numpy      import array
from numpy      import array_equal

# error class for when it fails to be coherent
class Math2DError(Exception):
        pass


# 2D int vector
class IVec2D (tuple):

    x = property(itemgetter(0))
    y = property(itemgetter(1))

    def __new__(self, x, y):
        return tuple.__new__(IVec2D, (round(x), round(y)))

    def __repr__(self):
        return "{" + str("{X},{Y}").format(X=self[0], Y=self[0]) + "}"

    def __truediv__(self, other) :
        if isinstance(other, float) or isinstance(other, int) :
            return IVec2D(self.x / other, self.y / other)
        else:
            raise Math2DError("cannot divide {a} by {b}".format(a = self, b = other))

    def __mul__(self, other) :
        if isinstance(other, float) or isinstance(other, int) :
            return IVec2D(self.x * other, self.y * other)
        elif isinstance(other,IVec2D ):
            return IVec2D(self.x * other.x, self.y * other.y)
        else:
            raise Math2DError("cannot multiply {a} by {b}".format(a = self, b = other))

    def __add__(self, other) :
        if isinstance(other, float) or isinstance(other, int) :
            return IVec2D(self.x + other, self.y + other)
        elif isinstance(other,IVec2D ):
            return IVec2D(self.x + other.x, self.y + other.y)
        else:
            raise Math2DError("cannot add {a} by {b}".format(a = self, b = other))

    def __sub__(self, other) :
        if isinstance(other, float) or isinstance(other, int) :
            return IVec2D(self.x - other, self.y - other)
        elif isinstance(other,IVec2D ):
            return IVec2D(self.x - other.x, self.y - other.y)
        else:
            raise Math2DError("cannot add {a} by {b}".format(a = self, b = other))



# turn index into array position
def PositionFromIndexAndSize(idx : int , size : IVec2D) -> IVec2D:
        return  IVec2D( idx % size.x, (idx // size.x) % size.y )
        

# 2D array class for readability
class Array2D(ndarray):

    def dim(self) -> IVec2D:
        try :
            dimension = IVec2D(self.shape[0], self.shape[1])
            return dimension
        except IndexError : 
            pass 
            return IVec2D(self.shape[0], 0)

    # get a smaller portion of the array 
    def sub(self, begin : IVec2D, end : IVec2D):
        (bx,by) = begin[:2]
        bx %= self.dim().x
        by %= self.dim().y
        (ex,ey) = end[:2]
        ex %= self.dim().x
        ey %= self.dim().y
        raise ValueError("{}\n with begin = \n{}\n and end = \n{}\n".format(self[bx:ex ,by:ey], bx, ex))
        return self[bx :ex ,by :ey]


    def __new__(cls, in_list):
        data_type   = type((in_list[0])[0]) if type(in_list[0]) == list else  type(in_list[0]) 
        array_shape = (len(in_list), len(in_list[0]))
        input_array = asarray(in_list)
        obj = super(Array2D, cls).__new__(cls, shape = input_array.shape, dtype = input_array.dtype, buffer = input_array)
        return obj

        
    def __eq__ (self, other) :
        return array_equal(self,other)

    
    def __getitem__(self, index):
        new_index= [None ]* 2
        try :
            if isinstance(index, IVec2D):
                (x,y) = index[:2]
                raise TypeError
                return super(Array2D, self).__getitem__([x,y])
            elif isinstance(index, tuple):
                if isinstance(index[0], slice):
                    new_index[0]   = slice(index[0].start % self.dim().x, index[0].stop % self.dim().x, index[0].step )
                    new_index[1]   = slice(index[1].start % self.dim().y, index[1].stop % self.dim().y, index[1].step )
                    return super(Array2D, self).__getitem__(tuple(new_index))
                elif isinstance(index[0], int):
                    new_index[0]   = index[0] % self.dim().x
                    new_index[1]   = index[1] % self.dim().y
                    return super(Array2D, self).__getitem__(tuple(new_index))
        finally:
            return super(Array2D, self).__getitem__(index)
            
            
    

    

    @staticmethod
    def arrayFromFile(file_url : str, elem_cls : type):
        f = open(file_url,"rt")
        input_text =  f.read()
        f.close()
        items = []
        row   = []
        for char in input_text :
            if char == '\n' and len(row) > 0 :
                items.append(row)
                row   = []
            else :
                row.append(elem_cls(char))
        # "cast" to Array2D
        arr = Array2D(items)
        return arr

