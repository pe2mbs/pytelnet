
class Cursor( object ):
    def __init__( self, rows = 0, cols = 0 ):
        self.__row          = 0
        self.__column       = 0
        self.__numColumns   = cols
        self.__numRows      = rows
        return
    # end def

    def __del__( self ):
        return
    # end def

    def getRow( self ):
        return self.__row
    # end def

    def setRow( self, value ):
        self.__row = value
        return
    # end def

    Row = property( getRow, setRow )

    def getCol( self ):
        return self.__col
    # end def

    def setCol( self, value ):
        self.__col  = value
        return
    # end def

    Col = property( getCol, setCol )
    Column = property( getCol, setCol )


    def MaxRows( self ):
        return self.__numRows
    # end def

    def MaxCols( self ):
        return self.__numColumns
    # end def

    def Clear( self ):
        self.__row          = 0
        self.__column       = 0
        return
    # end def

    def AdjustCol( self ):
        if self.__column >= self.__numColumns:
            self.__column = 0
            self.__row += 1
            self.AdjustRow()
        # end if
        if self.__column < 0:

            self.__column = 0
            self.__row -= 1
            self.AdjustRow()
        # end if
        return
    # end def

    def AdjustRow( self ):
        if self.__row >= self.__numRows:
            self.__row = 0
        # end if
        if self.__row < 0:
            self.__row = self.__numRows - 1;
        # end if
        return
    # end def
# end class
