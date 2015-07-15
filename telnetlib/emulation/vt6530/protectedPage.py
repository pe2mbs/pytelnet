from telnetlib.emulation.vt6530.sharedProtocol import SharedProtocol
from telnetlib.emulation.vt6530.page import *

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
        PageCursorPos = Page_page.CursorPos
        newX = Page_page.ScanForNextField( PageCursorPos.Column, PageCursorPos.Row, inc )
        if newX >= 0:
            newX = Page_page.ScanForUnprotectField( newX, PageCursorPos.Row, inc )
            if newX >= 0:
                Page_page.CursorPos.Column = newX
                return
            # # end if
        # end if
        y = Page_page.CursorPos.Row + inc
        for qpr in range( 0, Page_page.GetNumRows(), inc ):
            if inc > 0:
                if y >= Page_page.GetNumRows():
                    y = 0
                # end if
            else:
                if y < 0:
                    y = Page_page.GetNumRows() - 1
                # end if
            # end if
            newX = Page_page.ScanForUnprotectField( 0, y, inc )
            if newX >= 0:
                Page_page.CursorPos.Column  = newX
                Page_page.CursorPos.Row     = y
                return
            # end if
            # y += 1
            y += inc
        # next
        return
    # end def

    def ClearToEOL( self, Page_page ):
        x = Page_page.BufferPos.Column
        y = Page_page.BufferPos.Row
        attr = Page_page.GetCell( x, y ).GetAttributes()
        if Page_page.GetCell( x, y ).IsStartField():
            # clear the video attributes for the field
            attr = VID_NORMAL
            Page_page.GetCell( x, y ).ClearVideoAttribs()
            x += 1
        # end if
        attr |= CHAR_CELL_DIRTY   # | 0x20
        while x < Page_page.GetNumColumns() and not Page_page.GetCell( x, y ).IsStartField():
            Page_page.GetCell( x, y ).Clear( attr )
            x += 1
        # end while
        if x != Page_page.GetNumColumns():  # Page_page.mem[ y ][ x ] & CHAR_START_FIELD ) != 0:
            return
        # end if
        for y in range( y + 1, Page_page.GetNumRows() ):
            x = 0
            while x < Page_page.GetNumColumns() and not Page_page.GetCell( x, y ).IsStartField():
                Page_page.GetCell( x, y ).Clear( attr )
                x += 1
            # end while
            if x < Page_page.GetNumColumns():
                if Page_page.GetCell( x, y ).IsStartField():
                    break
                # end if
            # end if
        # next
        return
    # end def

    def ClearToEOP( self, Page_page ):
        cursor = Page_page.BufferPos
        attr = Page_page.GetWriteAttr() | Page_page.GetPriorAttr()
        for c in range( cursor.Column, Page_page.GetNumColumns() ):
            cell = Page_page.GetCell( c, cursor.Row )
            if cell.IsUnprotect():
                cell.Clear( CHAR_CELL_DIRTY | attr | DAT_UNPROTECT )
            # end if
        # next
        for r in range( cursor.Row + 1, Page_page.GetNumRows() ):
            for c in range( 0, Page_page.GetNumColumns() ):
                cell = Page_page.GetCell( c, r )
                if cell.IsUnprotect():
                    cell.Clear( CHAR_CELL_DIRTY | attr | DAT_UNPROTECT )
                # end if
            # next
        # next
        return
    # end def

    def CursorLeft( self, Page_page ):
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        if Page_page.CursorPos.Column == 0:
            if Page_page.CursorPos.Row == 0:
                Page_page.CursorPos.Row = Page_page.GetNumRows() - 1
            else:
                Page_page.CursorPos.Row -= 1
                Page_page.CursorPos.AdjustRow()
            # end if
            Page_page.CursorPos.Column = Page_page.GetNumColumns() - 1
        else:
            Page_page.CursorPos.Column -= 1
            Page_page.CursorPos.AdjustCol()
        # end if
        if not Page_page.GetCell( Page_page.CursorPos ).IsUnprotect():
            self.Tab( Page_page, -1 )
        # end if
        return
    # end def

    def ReadBuffer( self, StringBuffer_accum, Page_page, iReqMask, iForbidMask,
                    iStartRow, iStartCol, iEndRow, iEndCol):
        writeCr = False
        sb  = ''
        accum = ''
        for y in range( iStartRow, iEndRow ):
            fieldStarted = False
            for x in range( iStartCol, iEndCol ):
                if Page_page.GetCell( x, y ).IsStartField():
                    if fieldStarted:
                        sb = sb.strip( ' ' )
                        if len( sb ) > 0:
                            accum.append ( sb )
                        # end if
                        sb = ''
                        writeCr = False
                    # end if
                    if ( Page_page.GetCell( x + 1, y ).AsInt() & iReqMask ) != 0:
                        fieldStarted = True
                        accum += chr( 17 )
                        accum += chr( y + 0x20 )
                        accum += chr( x + 0x21 )
                    else:
                        fieldStarted = False
                    # end if
                # end if
                elif ( Page_page.GetCell( x, y ).AsInt() & iReqMask ) != 0 and fieldStarted:
                    sb += Page_page.GetCell( x, y ).Get()
                    writeCr = True
                elif fieldStarted:
                    sb = sb.strip( ' ' )
                    if len( sb ) > 0:
                        accum += sb
                    # end if
                    sb = ''
                    writeCr = False
                    fieldStarted = False
                # end if
            # next
            if writeCr:
                sb = sb.strip( ' ' )
                if len( sb ) > 0:
                    accum += sb
                # end if
                writeCr = False
                sb = ''
            # enx if
        # next
        accum += chr( 4 )
        return accum
    # end def

    def WriteChar( self, Page_page, Cursor_bufferPos, c ):
        if ( ord( c ) & 0xFF ) < 32:

            SharedProtocol.WriteChar( self, Page_page, Cursor_bufferPos, c )
            return
        # end if
        cell = Page_page.GetCell( Cursor_bufferPos )
        cell.Set( 0xFF & c )
        cell.SetAttributes( (c & ~0xFF) | cell.GetAttributes() | Page_page.GetWriteAttr() | CHAR_CELL_DIRTY | Page_page.GetPriorAttr() )
        Cursor_bufferPos.Column += 1
        Cursor_bufferPos.AdjustCol();
        Page_page.GetCell( Cursor_bufferPos ).SetDirty( True )
        return
    # end def

    def Linefeed( self, Page_page ):
        self.Tab( Page_page, 1 )
        return
    # end def

    def ValidateCursorPos( self, Page_page ):
        if not Page_page.GetCell( Page_page.CursorPos ).IsUnprotect():
            self.Tab( Page_page, 1 )
        # end if
        return
    # end def

    def SetCursor( self, Page_page, row, col):
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        Page_page.CursorPos.Row = row
        Page_page.CursorPos.Column = col
        self.ValidateCursorPos( Page_page )
        Page_page.GetCell( Page_page.CursorPos ).SetDirty( True )
        return
    # end def

    def ClearBlock( self, Page_page, iStartRow, iStartCol, iEndRow, iEndCol ):
        value = CHAR_CELL_DIRTY | 0x20
        mask = MASK_FIELD ^ CHAR_START_FIELD
        for y in range( iStartRow, iEndRow ):
            for x in range( iStartCol, iEndCol ):
                cell = Page_page.GetCell( x, y )
                cell.Clear( cell.GetAttributes() & mask | CHAR_CELL_DIRTY )
            # next
        # next
        self.ValidateCursorPos( Page_page )
        return
    # end def

    def ArrowDown( self, Page_page, Cursor_cursor):
        self.Tab( Page_page, 1 )
        return
    # end def

    def ArrowUp( self, Page_page, Cursor_cursor ):
        self.Tab( Page_page, -1 )
        return
    # end def

    def ArrowLeft( self, Page_page, Cursor_cursor ):
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        Cursor_cursor.Column -= 1
        Cursor_cursor.AdjustCol()
        if not Page_page.GetCell( Cursor_cursor ).IsUnprotect():
            self.Tab( Page_page, -1 )
        # end if
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        return
    # end def

    def ArrowRight( self, Page_page, Cursor_cursor ):
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        Cursor_cursor.Column += 1
        Cursor_cursor.AdjustCol()
        if not Page_page.GetCell( Cursor_cursor ).IsUnprotect():
            self.Tab( Page_page, 1 )
        # end if
        Page_page.GetCell( Cursor_cursor ).SetDirty( True )
        return
    # end def
# end class

class UnprotectPage( SharedProtocol ):
    def __init__( self ):
        SharedProtocol.__init__( self )
        return
    # end def

    def Tab( self, inc ):
        return
    # end def

    def ClearToEOL( self, Page_page ):
        for x in range( Page_page.CursorPos.Column, Page_page.GetNumColumns() ):
            Page_page.GetCell( x, Page_page.CursorPos.Row ).ClearTo( ' ' )
        # next
        return
    # end def

    def ReadBuffer( self, StringBuffer_accum, Page_page, iReqMask, iForbidMask,
                    iStartRow, iStartCol, iEndRow, iEndCol):
        for y in range( iStartRow - 1, iEndRow - 1 ):
            for x in range( iStartCol - 1, iEndCol - 1 ):
                StringBuffer_accum += Page_page.GetCell( x, y ).Get()
            # next
            StringBuffer_accum += chr( 13 )
        # next
        return StringBuffer_accum
    # end def
# end class