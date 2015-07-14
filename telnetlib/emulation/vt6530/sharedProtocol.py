from telnetlib.emulation.vt6530.keys import *
from telnetlib.emulation.vt6530.page import *
from telnetlib.emulation.vt6530.cursor import *

MODE_DISPLAY        = 0
MODE_PROTECT        = 1
MODE_UNPROTECT      = 2

class PageProtocol( object ):
    """
        Interface class
    """
    def __init__( self ):
        return
    # end def

    def WriteBuffer( self, Page_page, text ):
        return
    # end def
    
    def WriteCursor( self, Page_page, text ):
        return
    # end def

    def WriteChar( self, Page_page, Cursor_cursor, iCh ):
        return
    # end def

    def InsertChar( self, Page_page ):
        return
    # end def

    def DeleteChar( self, Page_page ):
        return
    # end def

    def Backspace( self, Page_page ):
        return
    # end def

    def Tab( self, Page_page, iInc ):
        return
    # end def

    def CarageReturn( self, Page_page ):
        return
    # end def

    def Linefeed( self, Page_page ):
        return
    # end def

    def Home( self, Page_page ):
        return
    # end def

    def End( self, Page_page ):
        return
    # end def

    def ValidateCursorPos( self, Page_page ):
        return
    # end def

    def SetCursor( self, Page_page, iRow, iCol ):
        return
    # end def

    def CursorLeft( self, Page_page ):
        return
    # end def

    def CursorRight( self, Page_page ):
        return
    # end def

    def CursorDown( self, Page_page ):
        return
    # end def

    def CursorUp( self, Page_page ):
        return
    # end def

    def ClearToEOL( self, Page_page ):
        return
    # end def

    def ClearToEOP( self, Page_page ):
        return
    # end def

    def ClearBlock( self, Page_page, iStartRow, iStartCol, iEndRow, iEndCol ):
        return
    # end def

    def ReadBuffer( self, StringBuffer_out, Page_page, iReqMask, iForbidMask, iStartRow, iStartCol, iEndRow, iEndCol ):
        return
    # end def
# end class

class SharedProtocol( PageProtocol ):
    def __init__( self ):
        return
    # end def

    def Write( self, Cursor_pos, Page_page, iAttribute, text ):
        for x in text:
            # Page_page.mem[pos.row][pos.column] = text.charAt(x) | attribute | CHAR_CELL_DIRTY
            # c = text.charAt( x )
            # System.out.print((char)(c & MASK_CHAR))
            # c |= attribute
            # System.out.print((char)(c & MASK_CHAR))
            self.WriteChar( Page_page, Cursor_pos, x | iAttribute )
            if Cursor_pos.Column == Page_page.GetNumColumns() - 1:
                return
            # end if
        # next
        return
    # end def
    
    
    def WriteBuffer( self, Page_page, text):
        self.Write( Page_page.BufferPos, Page_page, Page_page.GetWriteAttr() | Page_page.GetPriorAttr(), text )
        return
    # end def

    def WriteCursor( self, Page_page, text ):
        self.Write( Page_page.CursorPos, Page_page, Page_page.GetWriteAttr() | Page_page.GetPriorAttr(), text )
        return
    # end def

    def WriteChar ( self, Page_page, Cursor_cursor, cCh ):
        c =  chr( ord( cCh ) & MASK_CHAR )
        if c == '\t':
            self.Tab( Page_page, 1 )
        elif c == '\r':
            self.Linefeed( Page_page )
        elif c == '\n':
            self.CarageReturn( Page_page )
        elif c == '\b':
            self.Backspace( Page_page )
        elif c == chr( 11 ):
            self.CursorUp( Page_page )
        elif c == SPC_DEL:
            self.DeleteChar( Page_page )
        elif c == SPC_DOWN:
            self.ArrowDown( Page_page, Cursor_cursor )
        elif c == SPC_END:
            self.End( Page_page )
        elif c == SPC_HOME:
            self.Home( Page_page )
        elif c == SPC_INS:
            self.InsertChar( Page_page )
        elif c == SPC_LEFT:
            self.ArrowLeft( Page_page, Cursor_cursor )
        elif c == SPC_PGDN:
            pass
        elif c == SPC_PGUP:
            pass
        elif c == SPC_PRINTSCR:
            pass
        elif c == SPC_RIGHT:
            self.ArrowRight( Page_page, Cursor_cursor )
        elif c == SPC_UP:
            self.ArrowUp( Page_page, Cursor_cursor )
        else:
            if Page_page.GetCell( Cursor_cursor ).IsKeyUpshift():
                Page_page.GetCell( Cursor_cursor ).Set( c, ( ord( c ) & ~MASK_CHAR ) | Page_page.GetWriteAttr() | Page_page.GetPriorAttr() | Page_page.GetCell( Cursor_cursor ).GetAttributes() )
            else:
                Page_page.GetCell( Cursor_cursor ).Set( cCh, Page_page.GetCell( Cursor_cursor ).GetAttributes() | CHAR_CELL_DIRTY | Page_page.GetPriorAttr() )
            # end if
            Cursor_cursor.Column += 1
            Cursor_cursor.AdjustCol()
            Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        # end if
        self.ValidateCursorPos( Page_page )
        return
    # end def

    def ArrowDown( self, Page_page, Cursor_cursor ):
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        Cursor_cursor.Row += 1
        Cursor_cursor.AdjustRow()
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        return
    # end def

    def ArrowUp( self, Page_page, Cursor_cursor ):
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        Cursor_cursor.Row -= 1
        Cursor_cursor.AdjustRow()
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        return
    # end def

    def ArrowLeft( self, Page_page, Cursor_cursor ):
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        Cursor_cursor.Column -= 1
        Cursor_cursor.AdjustCol()
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        return
    # end def

    def ArrowRight( self, Page_page, Cursor_cursor ):
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        Cursor_cursor.Column += 1
        Cursor_cursor.AdjustCol()
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        return
    # end def

    def Home( self, Page_page ):
        return
    # end def

    def End( self, Page_page ):
        return
    # end def

    def ValidateCursorPos( self, Page_page ):
        return
    # end def

    def InsertChar( self, Page_page ):
        return
    # end def

    def DeleteChar( self, Page_page ):
        return
    # end def

    def Backspace( self, Page_page ):
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        Page_page.CursorPos.Column -= 1
        Page_page.CursorPos.AdjustCol()
        Page_page.GetCell( Page_page.CursorPos ).Set( ' ' )
        return
    # end def

    def Tab( self, Page_page, iInc ):
        return
    # end def

    def CarageReturn( self, Page_page ):
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        Page_page.m_cursorPos.m_column = 0
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        return
    # end def

    def Linefeed( self, Page_page ):
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        if Page_page.CursorPos.Row == Page_page.GetNumRows() - 1:
            Page_page.ScrollPageUp()
        else:
            Page_page.CursorPos.m_row += 1
        # end if
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        return
    # end def

    def CursorRight( self, Page_page ):
        Page_page.GetCell( Page_page.BufferPos ).SetDirty( True )
        Page_page.m_cursorPos.Column += 1
        if Page_page.CursorPos.Column >= Page_page.GetNumColumns():
            Page_page.CursorPos.Column = 0
            if Page_page.CursorPos.Row == Page_page.GetNumRows() - 1:
                Page_page.ScrollPageUp()
            else:
                Page_page.CursorPos.Row += 1
                Page_page.CursorPos.AdjustRow()
            # end if
        # end if
        return
    # end def

    def CursorLeft( self, Page_page ):
        Page_page.CursorPos.m_column -= 1
        if Page_page.CursorPos.Column < 0:
            Page_page.CursorPos.Column = 0
            if Page_page.CursorPos.m_row == 0:
                Page_page.CursorPos.Row = Page_page.GetNumRows() -1
            else:
                Page_page.CursorPos.Row -= 1
            # end if
        # end if
        return
    # end def

    def CursorUp( self, Page_page ):
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        Page_page.m_cursorPos.m_row += 1
        Page_page.m_cursorPos.AdjustRow()
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        return
    # end def

    def CursorDown( self, Page_page ):
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        if Page_page.CursorPos.Row == Page_page.GetNumRows() - 1:
            Page_page.ScrollPageUp()
        else:
            Page_page.CursorPos.Row += 1
            Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        # end if
        return
    # end def

    def ClearToEOL( self, Page_page ):
        return
    # end def

    def ClearBlock( self, Page_page, iStartRow, iStartCol, iEndRow, iEndCol ):
        return
    # end def

    def ClearToEOP( self, Page_page ):
        for c in range( Page_page.CursorPos.Column, Page_page.GetNumColumns() ):
            Page_page.GetCell( c, Page_page.CursorPos.Row ).Clear( CHAR_CELL_DIRTY | Page_page.GetWriteAttr() | Page_page.GetPriorAttr() )
        # next
        for r in range( Page_page.CursorPos.Row + 1, Page_page.GetNumRows() ):
            for c in range( 0, Page_page.GetNumColumns() ):
                Page_page.GetCell( c, r ).Clear( CHAR_CELL_DIRTY | Page_page.GetWriteAttr() | Page_page.GetPriorAttr() )
            # next
        # next
        return
    # end def

    def ReadBuffer( StringBuffer_sb, Page_page, iReqMask, iForbidMask, iStartRow, iStartCol, iEndRow, iEndCol ):
        return
    # end def

    def SetCursor( self, Page_page, iRow, iCol ):
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        Page_page.CursorPos.Row = iRow
        Page_page.CursorPos.Column = iCol
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        return
    # end def
# end class
