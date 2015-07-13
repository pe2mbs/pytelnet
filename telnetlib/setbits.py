
class SetBits( object ):
    def __init__( self ):
        self.__bitset = 0
        return
    # end def

    def Clear( self ):
        self.__bitset = 0
        return
    # end def

    def Set( self, value ):
        self.__bitset = value.GetInteger()
    # end def

    def testBit( self, offset ):
        """
            testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.

            :param offset:
            :return:
        """
        mask = 1 << offset
        return self.__bitset & mask
    # end def

    def setBit( self, offset ):
        """
            setBit() returns an integer with the bit at 'offset' set to 1.

            :param offset:
            :return:
        """
        mask = 1 << offset
        return self.__bitset | mask

    #
    def clearBit( self, offset ):
        """
            clearBit() returns an integer with the bit at 'offset' cleared.

            :param offset:
            :return:
        """
        mask = ~(1 << offset)
        return self.__bitset & mask
    # end def

    def toggleBit( self, offset ):
        """
            toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.

            :param offset:
            :return:
        """
        mask = 1 << offset
        return self.__bitset ^ mask
    # end def

    def setValue( self, offset, width, value ):
        maskw = 0
        for w in range( 0, width ):
            maskw <<= 1
            maskw |= 1
        # next
        mask = ( value & maskw ) << offset
        return self.__bitset | mask
    # end def

    def getValue( self, offset, width ):
        maskw = 0
        for w in range( 0, width ):
            maskw <<= 1
            maskw |= 1
        # next
        return self.__bitset >> offset & maskw
    # end def

    def getInteger( self ):
        return self.__bitset
    # end def

    def setInteger( self, value ):
        self.__bitset = value
        return
    # end def
# end class
