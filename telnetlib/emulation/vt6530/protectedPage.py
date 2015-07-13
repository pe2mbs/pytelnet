from telnetlib.emulation.vt6530.sharedProtocol import SharedProtocol
from telnetlib.emulation.vt6530.page import Page

class ProtectPage( SharedProtocol ):
    def __init__( self ):
        SharedProtocol.__init__( self )
        return
    # end def

    def Home( self, Page_page ):
        return
    # end def

    def End( self, Page_page ):
        return
    # end def

    """
        0x09
        PROTECT
        Move to the first position of the next
        unprotected field.
    """
    def Tab( self, Page_page, inc ):
        return
    # end def

    def ClearToEOL( self, Page_page ):
        return
    # end def

    def ClearToEOP( self, Page_page ):
        return
    # end def

    def CursorLeft( self, Page_page ):
        return
    # end def

    def ReadBuffer( self, StringBuffer_accum, Page_page, iReqMask, iForbidMask,
                    iStartRow, iStartCol, iEndRow, iEndCol):
        return
    # end def

    def WriteChar( self, Page_page, Cursor_bufferPos, c ):
        return
    # end def

    def Linefeed( self, Page_page ):
        return
    # end def

    def ValidateCursorPos( self, Page_page ):
        return
    # end def

    def SetCursor( self, Page_page, row, col):
        return
    # end def

    def ClearBlock( self, Page_page, iStartRow, iStartCol, iEndRow, iEndCol ):
        return
    # end def

    def ArrowDown( self, Page_page, Cursor_cursor):
        return
    # end def

    def ArrowUp( self, Page_page, Cursor_cursor ):
        return
    # end def

    def ArrowLeft( self, Page_page, Cursor_cursor ):
        return
    # end def

    def ArrowRight( self, Page_page, Cursor_cursor ):
        return
    # end def
# end class
