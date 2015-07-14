class StatusLine( object ):
    def __init__( self, blockMode = False, protMode = False ):
        self.__message      = ''    # max 64 characters
        self.__status       = ''    # 13 - 5
        self.__error        = ''
        # blockMode = False     CONV    = Conversational
        #             True      BLOCK   = Block
        self.__blockMode        = blockMode
        self.__protectedMode    = protMode
        return
    # end def

    def setConvMode( self, value ):
        self.__blockMode = not alue
        return
    # end def

    def getConvMode( self ):
        return not self.__blockMode
    # end def

    ConvMode = property( setConvMode, getConvMode )

    def IsBlockMode(self):
        return self.__blockMode or self.__protectedMode
    # end def

    def IsConvMode( self ):
        return not self.IsBlockMode()

    def setBlockMode( self, value ):
        self.__blockMode = value
        return
    # end def

    def getBlockMode( self ):
        return self.__blockMode
    # end def

    BlockMode = property( getBlockMode, setBlockMode )

    def setProtectedMode( self, value ):
        self.__protectedMode = value
        return
    # end def

    def getProtectedMode( self ):
        return self.__protectedMode
    # end def

    ProtectedMode = property( getProtectedMode, setProtectedMode )


    def setMode( self, value ):
        self.__mode = value
        return
    # end def

    def getMode( self ):
        return self.__mode
    # end def

    def setError( self, value ):
        self.__error = value
        return
    # end def

    def clearError( self ):
        self.__error = ''
        return
    # end def

    def setMessage( self, value ):
        if len(value) > 64:
            self.__message = value[:64]
        else:
            self.__message = value
        # end if
        return
    # end def

    def clearMessage( self ):
        self.__message = ''
        return
    # end def

    def setStatus( self, value ):
        if len(value) > 8:
            self.__status = value[:8]
        else:
            self.__status = value
        # end if
        return
    # end def

    def clearStatus( self ):
        self.__status   = ''
        return
    # end def

    def getStatus( self ):
        """
            The bottom row of the screen contains the message/status line, which has
            the following format:

            Column
            1 2            66 67            80
            b Message Area b  Status Area

            Columns 1 and 66 always contain a blank space.
            The message area occupies columns 2 through 65. It can contain any
            character string sent through an escape sequence from either your
            application program or the keyboard in conversational mode.Text in the
            message area remains visible until it is cleared or reset by another escape
            sequence.
            The status area, occupying columns 67 through 80, contains terminal
            status information such as the current mode of operation. Only the 6530
            can write into this area; your application cannot address this area. The
            user can enable and disable the display of the status area by pressing the
            Ctrl-Next Page and Ctrl-Prev Page keys, respectively.
        """
        return " %s %s %s %s" % ( self.__message,
                               "CONV" if not self.__blockMode else "BLOCK",
                               "PROT" if not self.__protectedMode else "",
                               self.__status )
    # end def

    def getError( self ):
        """
            When the 6530 detects an error, it temporarily replaces the message/
            status line with an error line. The error line has the following format:

            Column
            1 2                              80
            b Error Message Area

            These types of error can occur:
            *   General errors. Operator errors, device errors, and other errors
                detected by the operating system or by the 6530.
            *   Communications errors. Invalid commands to the 6530 (detected
                and reported by the Command errors).
            While the error line is displayed, any keypress removes the error line and
            restores the message/status line.
        """
        return " %s" % ( self.__error )
    # end def
# end class
