import telnetlib.emulation
from telnetlib.emulation.vt6530.page  import Page

class UnprotectPage( SharedProtocol )
    def __init__( self ):
        SharedProtocol.__init__( self )
        return
    # end def

    def Tab( self, inc ):
        return
    # end def

    def ClearToEOL( Page_page ):
        return
    # end def

    def ReadBuffer( self, StringBuffer_accum, Page_page, iReqMask, iForbidMask,
                    iStartRow, iStartCol, iEndRow, iEndCol):
        return
    # end def
# end class


class StatusLine( object ):
    def __init__( self, blockMode = False ):
        self.__message      = ''    # max 64 characters
        self.__status       = ''    # 13 - 5
        self.__error        = ''
        # blockMode = False     CONV    = Conversational
        #             True      BLOCK   = Block
        self.__blockMode    = blockMode
        return
    # end def

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
        return " %s %s %s" % ( self.__message,
                               "CONV" if not self.__blockMode else "BLOCK",
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

class TextDisplay( object ):
    def __init__( self, pages, rows, cols ):
        """
            Constructor
        """
        self.__echoOn           = True
        self.__blockMode        = False
        self.__protectMode      = False
        self.__requiresRepaint  = True
        self.__ppprotectMode    = ProtectPage()
        self.__ppunProtectMode  = UnprotectPage()
        self.__ppconvMode       = UnprotectPage()
        self.__numPages         = pages
        self.__numRows          = rows
        self.__numColumns       = cols
        self.__ppRemote         = self.__ppconvMode
        self.__pages            = None
        self._Init()
        self.__statusLine       = StatusLine( self.__blockMode )

        return
    # end def

    def __del__( self ):
        """
            Destructor
        """
        return
    # end def

    def _Init( self ):
        return
    # end def

    def WriteLocal( self, text ):
        self.__displayPage.WriteCursorLocal( self.__ppRemote, text );
        self.__ppRemote.ValidateCursorPos( self.__displayPage );
        self.__requiresRepaint = True
        return
    # end def

    def EchoDisplay( self, text ):
        if self.__echoOn:
            self.__displayPage.WriteCursor( self.__ppRemote, text )
            self.__requiresRepaint = True
            return
        # end def
        if text[ 0 ] == 13:
            self.__displayPage.WriteCursor( self.__ppRemote, '\r\n' )
            self.__requiresRepaint = True
        # end if
        return
    # end def




class VT6530( telnetlib.emulation.TerminalEmulation ):
    def __init__( self ):
        telnetlib.emulation.TerminalEmulation.__init__( self )
        self.__statusRow    = ''
        self.__currentMode  = 0
        self.__m_display    = None
        self.__m_keys       = None
        return
    # end def

    def OnReceive( self, buffer ):



        return buffer
    # end def

    def BeforeTransmit( self, buffer ):
        return buffer.replace( '\n', '\r\n' )
    # end def
# end class