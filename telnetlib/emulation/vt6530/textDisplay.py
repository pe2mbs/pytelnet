import sys
from telnetlib.emulation.vt6530.page            import *
from telnetlib.emulation.vt6530.sharedProtocol  import *
from telnetlib.emulation.vt6530.protectedPage   import *
from telnetlib.emulation.vt6530.statusLine      import *
from telnetlib.emulation.color                  import *

class TextDisplay( object ):
    def __init__( self, pages, rows, cols ):
        """
            Constructor
        """
        self.__echoOn           = True
        self.__requiresRepaint  = True
        self.__ppprotectMode    = ProtectPage()
        self.__ppunProtectMode  = UnprotectPage()
        self.__ppconvMode       = UnprotectPage()
        self.__numPages         = pages
        self.__numRows          = rows
        self.__numColumns       = cols
        self.__ppRemote         = self.__ppconvMode
        self.__pages            = []                    # [ Page ]
        self.Init()
        self.__writePage        = None                  # Page
        self.__displayPage      = None                  # Page
        self.__keysLocked       = False
        self.__foreground       = Color()
        self.__background       = Color()
        self.__statusLine       = StatusLine( self.__blockMode )

        return
    # end def

    def __del__( self ):
        """
            Destructor
        """
        return
    # end def

    def SetForeGroundColor( self, Color_color ):
        self.__foreground = Color_color
        return
    # end def

    def SetBackGroundColor( self, Color_color ):
        self.__background = Color_color
        return
    # end def

    def GetForeGroundColor( self ):
        return self.__foreground
    # end def

    def GetBackGroundColor( self ):
        return self.__background
    # end def

    def NeedsRepaint( self ):
        return self.__requiresRepaint
    # end def

    def SetRePaint( self, val ):
        self.__requiresRepaint = val
        return
    # end def

    def WriteBuffer( self, text ):
        self.__writePage.WriteBuffer( self.__ppRemote, text )
        return
    # end def

    def WriteDisplay( self, text ):
        self.__displayPage.WriteCursor( self.__ppRemote, text )
        self.__requiresRepaint = True
        return
    # end def

    def WriteLocal( self, text ):
        self.__displayPage.WriteCursorLocal( self.__ppRemote, text )
        self.__ppRemote.ValidateCursorPos( self.__displayPage )
        self.__requiresRepaint = True
        return
    # end def


    def EchoDisplay( self, text ):
        if self.__echoOn:
            self.__displayPage.WriteCursor( self.__ppRemote, text )
            self.__requiresRepaint = True
            return
        # end if
        if text[0] == 13:
            self.__displayPage.WriteCursor( self.__ppRemote, '\r\n' )
            self.__requiresRepaint = True
        # end if
        return
    # end def

    """ ESC W
    *  1.  Clear all pages to blanks
    *  2.  Set video prior condition to NORMAL for all pages
    *  3.  Select page 1
    *  4.  Display page 1
    *  5.  Set the buffer addess to (1,1) for all pages
    *  6.  Set the cursor address to (1,1) for all pages
    *  7.  Lock the keyboard
    *  8.  Clear the status line display
    *  9.  Reset insert mode
    * 10.  Initialize datatype table
    * 11.  Disable local line editing
    """
    def SetProtectMode( self ):
        self.__displayPage  = self.__pages[ 1 ]
        self.__writePage    = self.__pages[ 1 ]
        self.__ppRemote     = self.__ppprotectMode
        self.ClearAll()
        self.SetVideoPriorCondition( VID_NORMAL )
        self.SetInsertMode( INSERT_INSERT )
        self.InitDataTypeTable()
        self.SetKeysLocked()
        self.__statusLine.BlockMode = True
        self.__statusLine.ProtectedMode = True
        self.__requiresRepaint = True
        return
    # end def


    """ ESC X
    *  1.  Clear all pages to blanks
    *  2.  Set the video prior conditiion registers to NORMAL for all pages
    *  3.  Select page 1
    *  4.  Display page 1
    *  5.  Set the buffer address to (1,1) for all pages
    *  6.  Set the cursor address to (1,1) for all pages
    *  7.  Lock the keyboard
    *  8.  Clear the status line
    *  9.  Reset insert mode
    * 10.  Enable local line editing
    * 11.  Clear all horizontal tab stops
    """
    def ExitProtectMode( self ):
        self.__displayPage = self.__pages[ 1 ]
        self.__writePage = self.__pages[ 1 ]
        self.__ppRemote = self.__ppunProtectMode
        self.ClearAll()
        self.SetInsertMode( INSERT_INSERT )
        self.ClearAllTabs()
        self.SetKeysLocked()
        self.__statusLine.BlockMode = True
        self.__statusLine.ProtectedMode = False
        return
    # end def

    def SetKeysLocked( self ):
        self.__keysLocked = True
        return
    # end def

    def SetKeysUnlocked( self ):
        self.__keysLocked = False
        return
    # end def

    """ ESC :
    """
    def SetPage( self, page ):
        # if ( page >= numPages )
        #   return
        # # end if
        self.__writePage = self.__pages[ page ]
        return
    # end def

    """ 0x07
    """
    def Bell( self ):
        # ding, ding, ding
        return
    # end def

    """ 0x08
     """
    def Backspace( self ):
        self.__writePage.Backspace( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ 0x09
     """
    def Tab( self ):
        self.__writePage.Tab( self.__ppRemote, 1 )
        self.__requiresRepaint = True
        return
    # end def

    """ 0x0A
     """
    def Linefeed( self ):
        self.__writePage.CursorDown( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ 0x0D
     """
    def CarageReturn( self ):
        self.__writePage.CarageReturn( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    def CursorUp( self, value = 1 ):
        return
    # end def

    def CursorDown( self, value = 1 ):
        return
    # end def

    def CursorRight( self, value = 1 ):
        return
    # end def

    def CursorLeft( self, value = 1 ):
        return
    # end def

    """ ESC J
     """
    def SetCursorRowCol( self, row, col ):
        self.__writePage.SetCursor( self.__ppRemote, row, col )
        self.__requiresRepaint = True
        return
    # end def

    def SetBufferRowCol( self, row, col ):
        self.__writePage.SetBuffer( row, col )
        self.__requiresRepaint = True
        return
    # end def

    def SetVideoPriorCondition( self, attr ):
        self.__writePage.SetVideoPriorCondition( attr )
        return
    # end def

    def SetInsertMode( self, mode ):
        self.__writePage.SetInsertMode( mode )
        return
    # end def

    """ ESC 0
    """
    def PrintScreen( self ):
        return
    # end def

    """ ESC 1
    *
    *  Set a tab at the current cursor location
    """
    def SetTab( self ):
        return
    # end def

    """ ESC 2
    *
    *  Clear the tab at the current cursor location
    """
    def ClearTab( self ):
        return
    # end def

    """ ESC 3
    """
    def ClearAllTabs( self ):
        return
    # end def

    """ ESC i
    """
    def Backtab( self ):
        self.__displayPage.Tab( self.__ppRemote, -1 )
        self.__requiresRepaint = True
        return
    # end def

    """ ESC 6
    *
    *  All subsuquent writes use this attribute
    """
    def SetWriteAttribute( self, attr ):
        self.__writePage.SetWriteAttribute( attr )
        return
    # end def

    """ ESC 7
    *  Not sure what this is supposed to do
    """
    def SetPriorWriteAttribute( self, attr ):
        self.__writePage.SetWriteAttribute( attr )
        return
    # end def

    """ ESC ! or ESC ' '
    """
    def SetDisplayPage( self, page ):
        # if page >= numPages:
        #	return
        # end if
        self.__displayPage = self.__pages[ page ]
        self.__displayPage.ForceDirty()
        self.__requiresRepaint = True
        return
    # end def

    """ ESC A
    """
    def MoveCursorUp( self ):
        self.__writePage.CursorUp( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ ESC C
    """
    def MoveCursorRight( self ):
        self.__writePage.CursorRight( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ ESC H
    """
    def Home( self ):
        self.__writePage.SetCursor( self.__ppRemote, 0, 0 )
        self.__requiresRepaint = True
        return
    # end def

    """ ESC F
    """
    def End( self ):
        self.__writePage.SetCursor( self.__ppRemote, self.__numRows - 1, 0 )
        self.__requiresRepaint = True
        return
    # end def

    """ ESC I
    """
    def ClearPage( self ):
        self.__writePage.SetWriteAttribute( VID_NORMAL )
        self.__writePage.SetVideoPriorCondition( VID_NORMAL )
        self.__writePage.ClearPage()
        self.__requiresRepaint = True
        return
    # end def

    """ ESC J
    """
    def ClearToEnd( self ):
        self.__writePage.ClearToEOP( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ ESC I
     """
    def ClearBlock( self, iStartRow, iStartCol, iEndRow, iEndCol ):
        self.__writePage.ClearBlock( self.__ppRemote, iStartCol, iEndRow, iEndCol )
        self.__requiresRepaint = True
        return
    # end def

    """ ESC K
    *  In block mode, erase the field.  In
    *  conversation mode, clear to end of line
    """
    def ClearEOL( self ):
        self.__writePage.ClearToEOL( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ 0x1D
    """
    """ ESC [
    """
    def StartField( self, videoAttr, dataAttr,  keyAttr = 0 ):
        attr = self.DecodeVideoAttrs( videoAttr ) | self.DecodeDataAttrs( dataAttr ) | 0x20
        if keyAttr != 0:
            attr |= self.DecodeVideoAttrs( keyAttr )
        # end if
        self.WriteField( attr )
        return
    # end def

    def ReadBufferAllMdt( self, StringBuffer_out, iStartRow, iStartCol, iEndRow, iEndCol ):
        return self.ReadBuffer( StringBuffer_out, DAT_MDT, 0, iStartRow, iStartCol, iEndRow, iEndCol )
    # end def

    def ReadBufferAllIgnoreMdt( self, StringBuffer_out, iStartRow, iStartCol, iEndRow, iEndCol ):
        return self.ReadBuffer( StringBuffer_out, 0, 0, iStartRow, iStartCol, iEndRow, iEndCol )
    # end def

    """ ESC - <
    *
    * PROTECT MODE
    *  Read all the unprotected fields in the block
    *
    * UNPROTECT MODE
    *  Return raw characters in the block
    """
    def ReadBufferUnprotectIgnoreMdt( self, StringBuffer_out, iStartRow, iStartCol, iEndRow, iEndCol ):
        return self.ReadBuffer( StringBuffer_out, DAT_UNPROTECT, 0, iStartRow, iStartCol, iEndRow, iEndCol )
    # end def

    def ReadBufferUnprotect( self, StringBuffer_out, iStartRow, iStartCol, iEndRow, iEndCol ):
        return self.ReadBuffer( StringBuffer_out, DAT_UNPROTECT | DAT_MDT, 0, iStartRow, iStartCol, iEndRow, iEndCol )
    # end def

    """ ESC ]
    *
    *  Read all the fields in the block (protected and unprotected)
    """
    def ReadFieldsAll( self, StringBuffer_out, iStartRow, iStartCol, iEndRow, iEndCol ):
        return self.ReadBuffer( StringBuffer_out, 0, 0, iStartRow, iStartCol, iEndRow, iEndCol )
    # end def

    """ ESC >
    *  reset all modified data tags for unprotected fields
    """
    def ResetMdt( self ):
        self.__writePage.ResetMDTs()
        return
    # end def

    """ ESC O
    """
    def InsertChar( self ):
        self.__writePage.InsertChar( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ ESC M
    """
    def SetModeBlock( self ):
        self.__statusLine.BlockMode = True
        self.ExitProtectMode()
        self.__ppRemote = self.__ppunProtectMode
        return
    # end def

    def SetModeConv( self ):
        self.__displayPage  = self.__pages[ 1 ]
        self.__writePage    = self.__pages[ 1 ]
        self.__ppRemote     = self.__ppunProtectMode
        self.SetInsertMode( INSERT_INSERT )
        self.ClearAllTabs()
        self.SetKeysLocked()
        self.__statusLine.ConvMode      = True
        self.__statusLine.ProtectedMode = False
        self.__ppRemote         = self.__ppconvMode
        self.__requiresRepaint  = True
        return
    # end def

    def IsBlockMode( self ):
        return self.__statusLine.IsBlockMode()
    # end def

    """ ESC p
    """
    def SetPageCount( self, value ):
        self.__numPages = value
        return
    # end def

    """ ESC q
     """
    def Init( self ):
        if self.__pages is not None:
            x = 0
            while self.__pages[ x ] is not None:
                del self.__pages[ x ]
                x += 1
            # end while
            del self.__pages
        # end if
        self.__pages = [ Page( self.__numRows, self.__numColumns ) ] * self.__numPages + 2
        self.__pages[ self.__numPages + 1 ] = None
        self.__displayPage = self.__pages[ 0 ]
        self.__writePage = self.__pages[ 0 ]
        self.__requiresRepaint = True
        return
    # end def

    def WriteStatus( self, msg ):
        self.__statusLine.setStatus( msg )
        return
    # end def

    """ ESC o
     *
     """
    def WriteMessage( self, msg ):
        self.__statusLine.setMessage( msg )
        return
    # end def

    def InitDataTypeTable( self ):
        return
    # end def

    def GetNumColumns( self ):
        return self.__numColumns
    # end def

    def GetNumRows( self ):
        return self.__numRows
    # end def

    def GetCurrentPage( self ):
        for x in range( 0, self.__numPages + 1):
            if self.__pages[ x ] == self.__writePage:
                return x
            # end if
        # next
        raise Exception( "Unable to find the Current page" )
    # end def

    def GetDisplayPage( self ):
        return self.__displayPage
    # end def

    def GetCursorCol( self ):
        return self.__writePage.CursorPos.Column + 1
    # end def

    def GetCursorRow( self ):
        return self.__writePage.CursorPos.Row + 1
    # end def

    def GetBufferCol( self ):
        return self.__writePage.BufferPos.Column + 1
    # end def

    def GetBufferRow( self ):
        return self.__writePage.BufferPos.Row + 1
    # end def

    def GetProtectMode( self ):
        return self.__statusLine.ProtectedMode
    # end def

    def GetBlockMode( self ):
        return self.__statusLine.BlockMode
    # end def

    def SetEchoOn( self ):
        self.__echoOn = True
        return
    # end def

    def SetEchoOff( self ):
        self.__echoOn = False
        return
    # end def

    """ ESC A
    """
    def CursorUp( self ):
        self.__writePage.CursorUp( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ 0x0A
    """
    def CursorDown( self ):
        self.__writePage.CursorDown( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ ESC C
    """
    def CursorRight( self ):
        self.__writePage.CursorRight( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ ESC L
    """
    def LineDown( self ):
        self.__requiresRepaint = True
        return
    # end def

    """ ESC M
     """
    def DeleteLine( self ):
        self.__requiresRepaint = True
        return
    # end def

    """ ESC O
     *
     *  Insert a space
     """
    def Insert( self ):
        self.__requiresRepaint = True
        return
    # end def

    def GetStartFieldASCII( self, StringBuffer_sb ):
        return self.__displayPage.GetStartFieldASCII( StringBuffer_sb )
    # end def

    """ ESC P
    * Delete a character at a given position on the screen.
    * All characters right to the position will be moved one to the left.
    """
    def DeleteChar( self ):
        self.__writePage.DeleteChar( self.__ppRemote )
        self.__requiresRepaint = True
        return
    # end def

    """ def paint( self, PaintSurface_ps )
        self.__displayPage->paint( ps, *statusLine )
        self.__requiresRepaint = False
    """

    def DumpScreen( self, StringBuffer_pw ):
        for r in range( 0, self.__displayPage.GetNumRows() ):
            for c in range( 0, self.__displayPage.GetNumColumns() ):
                StringBuffer_pw += self.__displayPage.GetCell( c, r ).Get()
            # next
            StringBuffer_pw += chr( 13 )
            StringBuffer_pw += chr( 10 )
        # next
        StringBuffer_pw += chr( 13 )
        StringBuffer_pw += chr( 10 )
        return StringBuffer_pw
    # end def

    def DumpAttibutes( self, StringBuffer_pw ):
        for r in range( 0, self.__displayPage.GetNumRows() ):
            for c in range( 0, self.__displayPage.GetNumColumns() ):
                cell = self.__displayPage.GetCell( c, r ).GetAttributes()
                StringBuffer_pw += self.__displayPage.GetCell( c, r ).Get()
                if (cell & VID_NORMAL) != 0:
                    StringBuffer_pw += "N"
                else:
                    StringBuffer_pw += '0'
                # end if
                if (cell & VID_BLINKING) != 0:
                    StringBuffer_pw += "B"
                else:
                    StringBuffer_pw += '0'
                # end if
                if (cell & VID_REVERSE) != 0:
                    StringBuffer_pw += "R"
                else:
                    StringBuffer_pw += '0'
                # end if
                if (cell & VID_INVIS) != 0:
                    StringBuffer_pw += "I"
                else:
                    StringBuffer_pw += '0'
                # end if
                if ( cell & VID_UNDERLINE ) != 0:
                    StringBuffer_pw += "U"
                else:
                    StringBuffer_pw += '0'
                # end if
                if ( cell & DAT_MDT ) != 0:
                    StringBuffer_pw += "M"
                else:
                    StringBuffer_pw += '0'
                # end if
                if ( cell & DAT_TYPE ) != 0:
                    StringBuffer_pw += chr( ( ord( c ) >> SHIFT_DAT_TYPE ) & 7 )
                else:
                    StringBuffer_pw += '0'
                # end if
                if ( cell & DAT_AUTOTAB ) != 0:
                    StringBuffer_pw += "A"
                else:
                    StringBuffer_pw += '0'
                # end if
                if ( cell & DAT_UNPROTECT ) != 0:
                    StringBuffer_pw += "0"
                else:
                    StringBuffer_pw += "P"
                # end if
                if ( cell & KEY_UPSHIFT ) != 0:
                    StringBuffer_pw += "S"
                else:
                    StringBuffer_pw += '0'
                # end if
                if ( cell & KEY_KB_ONLY ) != 0:
                    StringBuffer_pw += "K"
                else:
                    StringBuffer_pw += '0'
                # end if
                if ( cell & KEY_AID_ONLY ) != 0:
                    StringBuffer_pw += ""
                else:
                    StringBuffer_pw += ""
                # end if
                if ( cell & KEY_EITHER ) != 0:
                    StringBuffer_pw += ""
                else:
                    StringBuffer_pw += ""
                # end if
                if ( cell & CHAR_START_FIELD ) != 0:
                    StringBuffer_pw += "F"
                else:
                    StringBuffer_pw += '0'
                # end if
                StringBuffer_pw += ','
            # next
            StringBuffer_pw += chr( 13 )
            StringBuffer_pw += chr( 10 )
        # next
        StringBuffer_pw += chr( 13 )
        StringBuffer_pw += chr( 10 )
        return StringBuffer_pw
    # end def

    """
    *  Get the 'index'nth field on the screen.
    *  The first field is index ZERO.  If the
    *  index is larger than the number of field,
    *  an empty string is returned.
    """
    def GetField( self, index, StringBuffer_accum ):
        count = 0
        cap = False
        for r in range( 0, self.__numRows ):
            for c in range( 0, self.__numColumns ):
                if self.__displayPage.GetCell( c, r ).IsStartField():
                    if cap:
                        return
                    # end if
                    if ( count == index ):
                        cap = True
                    # end if
                    count += 1
                # end if
                if cap:
                    StringBuffer_accum += self.__displayPage.GetCell( c, r ).Get()
                # end if
            # next
        # next
        return StringBuffer_accum
    # end def

    """
    *  Get the video, data, and key attributes for a
    *  field.
    """
    def GetFieldAttributes( self, index ):
        count = 0
        for r in range( 0, self.__numRows ):
            for c in range( 0, self.__numColumns ):
                if self.__displayPage.GetCell( c, r ).IsStartField():
                    if count == index:
                        r2 = r
                        c2 = c + 1
                        if c2 >= self.__numColumns:
                            r2 += 1
                            c2 = 0
                        # end if
                        return self.__displayPage.GetCell( c2, r2 ).GetAttributes()
                    # end if
                    count += 1
                # end if
            # next
        # next
        return 0
    # end def

    """
    *  Get the text in the field at the cursor
    *  position.
    """
    def GetCurrentField( self, StringBuffer_accum ):
        count = 0
        cap = False
        r = self.__displayPage.CursorPos.Row
        c = self.__displayPage.CursorPos.Column
        while c > 0:
            if not self.__displayPage.GetCell( c, r ).IsStartField():
                break
            # end if
            c -= 1
        # end while
        c += 1
        while c < self.__numColumns:
            if self.__displayPage.GetCell( c, r ).IsStartField():
                break
            # end if
            StringBuffer_accum += self.__displayPage.GetCell( c, r ).Get()
            c += 1
        # end while
        return StringBuffer_accum
    # end def

    """
    *  Get the 'index'nth unprotected field on
    *  the screen.  The first field is index
    *  ZERO.  If the index is larger than the
    *  number of field, an empty string is
    *  returned.
    """
    def GetUnprotectField( self, index, StringBuffer_accum = "" ):
        count = 0
        cap = False
        for r in range( 0, self.__numRows ):
            for c in range( 0, self.__numColumns ):
                if self.__displayPage.GetCell( c, r ).IsStartField():
                    if cap:
                        return
                    # end if
                    r2 = r
                    c2 = c + 1
                    if c2 >= self.__numColumns:
                        c2 = 0
                        r2 += 1
                    # end if
                    if self.__displayPage.GetCell( c2, r2 ).IsUnprotect():
                        if count == index:
                            cap = True
                        # end if
                        count += 1
                    # end if
                # end if
                if cap:
                    StringBuffer_accum += self.__displayPage.GetCell( c, r ).Get()
                # end if
            # next
        # next
        return StringBuffer_accum
    # end def

    """
    *   Write text into the 'index'nth unprotected field on the screen.
    *   The first field is index ZERO.  If the index is larger than the
    *   number of field, the request is ignored.
    """
    def SetField( self, index, text ):
        count = 0
        for r in range( 0, self.__numRows ):
            for c in range( 0, self.__numColumns ):
                if self.__displayPage.GetCell( c, r ).IsStartField():
                    r2 = r
                    c2 = c + 1
                    if c2 >= self.__numColumns:
                        c2 = 0
                        r2 += 1
                    # end if
                    if self.__displayPage.GetCell( c2, r2 ).IsUnprotect():
                        if count == index:
                            self.SetCursorRowCol( r2, c2 )
                            self.WriteDisplay( text )
                            self.__requiresRepaint = True
                            return
                        # end if
                    # end if
                    count += 1
                # end if
            # next
        # next
        return
    # end def

    """
    *   Returns true if the 'index'nth unprotected field has its MDT set.
    *   The first field is index ZERO.  If the index is larger than the
    *   number of fields, false is returned.
    """
    def IsFieldChanged( self, index ):
        count = 0
        for r in range( 0, self.__numRows ):
            for c in range( 0, self.__numColumns ):
                if self.__displayPage.GetCell( c, r ).IsStartField():
                    r2 = r
                    c2 = c + 1
                    if c2 >= self.__numColumns:
                        c2 = 0
                        r2 += 1
                    # end if
                    if self.__displayPage.GetCell( c2, r2 ).IsUnprotect():
                        if count == index:
                            return self.__displayPage.GetCell( c2, r2 ).IsMDT()
                        # end if
                        count += 1
                    # end if
                # end if
            # next
        # next
        return False
    # end def

    """
    *  Get a full line of display text.
    """
    def GetLine( self, lineNumber, StringBuffer_line = "" ):
        for c in range( 0, self.__numColumns ):
            StringBuffer_line += self.__displayPage.GetCell( c, lineNumber ).Get()
        # next
        return StringBuffer_line
    # end def

    """
     *  Set the cursor at the start if the
     *  'index'nth unprotected field on the screen.
     *  The first field is index ZERO.  If the
     *  index is larger than the number of field,
     *  the request is ignored.
     """
    def CursorToField( self, index ):
        count = 0
        for r in range( 0, self.__numRows ):
            for c in range( 0, self.__numColumns ):
                if self.__displayPage.GetCell( c, r ).IsStartField():
                    r2 = r
                    c2 = c + 1
                    if c2 >= self.__numColumns:
                        c2 = 0
                        r2 += 1
                    # end if
                    if r2 >= self.__numRows:
                        r2 = 0
                    # end if
                    if self.__displayPage.GetCell( c2, r2 ).IsUnprotect():
                        if count == index:
                            self.SetCursorRowCol( r2, c2 )
                            self.__requiresRepaint = True
                            return
                        # end if
                        count += 1
                    # end if
                # end if
            # next
        # next
        return
    # end def

    def ToHTML( self, Color_fg, Color_bg, StringBuffer_buf = '' ):
        fgRGB = Color_fg.AsHexString()
        bgRGB = Color_bg.AsHexString()

        fieldCount  = 0
        inUnprot    = False
        accum       = ''

        # write the script and style
        StringBuffer_buf += """<html>"
    <script language='javascript'>
function keys()
{
    if ( event.keyCode < 112 || event.keyCode > 123 )
    {
        event.returnValue = true;
        return;
    }
    event.cancelBubble = true;
    event.returnValue = false;
    var k = document.forms('screen')('hdnKey');
    switch( event.keyCode )
    {
    case 112:
        k.value = 'F1';
        break;
    case 10:
        k.value = 'ENTER';
        break;
    }
    document.forms('screen').submit();
}

function canxIt()
{
    event.cancelBubble = true;
    event.returnValue = false;
}

function loaded()
{
    document.onkeydown=keys;
    document.onhelp=canxIt;
    var f = document.forms('screen')('F0');
    if (f != null)
        f.focus();
}

function tabcheck( field )
{
    var f = document.forms('screen')('F'+field);
    if (f.value.length == f.maxLength())
    {
        field++;
        if (document.forms('screen')('F'+field) != null)
        {
            document.forms('screen')('F'+field).focus();
        }
        else
        {
            document.forms('screen')('F0').focus();
        }
    }
}
    </script>
    <body onload='loaded()' style='color: green; background: #3F3F3F'>"""

        StringBuffer_buf += """
    <style type='text/css' >"
.normal
{
    color: #{fg};
    background: #{bg};
    text-decoration: none;
}

.reverse
{
    color: #{bg};
    background: #{fg};
    text-decoration: none;
}

.underline
{
    color: #{fg};
    background: #{bg};
    text-decoration: underline;
}

.reverseunderline
{
    color: #{bg};
    background: #{fg};
    text-decoration: underline;
}

.blink
{
    color: #{fg};
    background: #{bg};
    text-decoration: blink;
}

.blinkreverse {
    color: #{bg};
    background: #{fg};
    text-decoration: blink;
}
        </style>""".format( fg = fgRGB, bg = bgRGB )

        # write the table header
        StringBuffer_buf += "<form id='screen' method='post'><input type='hidden' id='hdnKey' value='' /><table cols='80' width='100%' >"

        for r in range( 0, self.__numRows ):
            StringBuffer_buf += "<tr>"
            for c in range( 0, self.__numColumns ):
                cell = self.__displayPage.GetCell( c, r )
                ch = cell.GetAttributes()
                if not inUnprot:
                    StringBuffer_buf += "<td class="
                    if (ch & MASK_COLOR) == 0:
                        pass
                    else:
                        pass

                    if ( ch & ( VID_UNDERLINE | VID_REVERSE ) == VID_UNDERLINE | VID_REVERSE ):
                        StringBuffer_buf += "reverseunderline"
                    elif ( ch & ( VID_BLINKING | VID_REVERSE ) == VID_BLINKING | VID_REVERSE ):
                        StringBuffer_buf += "blinkreverse"
                    elif ( ch & VID_BLINKING ) != 0:
                        StringBuffer_buf += "blink"
                    elif ( ch & VID_REVERSE ) != 0:
                        StringBuffer_buf += "reverse"
                    elif ( ch & VID_UNDERLINE ) != 0:
                        StringBuffer_buf += "underline"
                    else:
                        StringBuffer_buf += "normal"
                    # end if
                    if ( ch & CHAR_START_FIELD) == 0:
                        StringBuffer_buf += ">"
                        StringBuffer_buf += cell.Get()
                        StringBuffer_buf += "</td>"
                    # end if
                # end if
                if ( ch & CHAR_START_FIELD ) != 0:
                    if inUnprot:
                        # end the input tag
                        accum += "' maxlength='%i' />" % ( len( accum ) )
                        inUnprot = False
                        StringBuffer_buf += " colspan=%i>"% ( len( accum ) )
                        StringBuffer_buf += accum
                        StringBuffer_buf += "</td>"
                        accum = ''
                    # end if
                    # is the new field unprotected?
                    c2 = c + 1
                    if c2 >= self.__numColumns:
                        c2 = 0
                        r += 1
                        cell = self.__displayPage.GetCell( c2, r )
                    # end if
                    if cell.IsUnprotect():
                        inUnprot = True
                        accum += "<input type='text' id='F%i' onkeypress='tabcheck( %i)' value='" % ( fieldCount, fieldCount, cell.Get() )
                        fieldCount += 1
                    # end if
                elif inUnprot:
                    accum += chr( ord( ch ) & MASK_CHAR )
                # end if
            # next
            StringBuffer_buf += "</tr>\r\n"
        # next
        StringBuffer_buf += "</table></form><p/><center><a href='mailto:marc.bertens@nl.equens.com'>Got Bugs?</a></center></body></html>"
        return
    # end def

    def GetSubString( self, row, col, l, sb = "" ):
        for c in range( col, col+l ):
            sb += self.__displayPage.GetCell( c, row ).Get()
        # next
        return sb
    # end def

    def GetText( self, sb = "" ):
        for row in range( 0, self.GetNumRows() ):
            for col in range( 0, self.GetNumColumns() ):
                sb += self.__displayPage.GetCell( col, row ).Get()
            # next
        # next
        return sb
    # end def

    """
        Private section
    """
    def ReadBuffer( self, out, reqMask, forbidMask, startRow, startCol, endRow, endCol ):
        return self.__writePage.ReadBuffer( out, self.__ppRemote, reqMask, forbidMask, startRow, startCol, endRow, endCol )
    # end def

    """ 0x08
    * PROTECT MODE
    *  Move to the start of the field.  If the cursor
    *  is already at the start, move the first position
    *  of the previous unprotected field.
    *
    * If the new cursor position is protected,
    * move to the last position of the previous
    * unprotected field.
    *
    * UNPROTECT MODE
    *  Move to previous tab.  If no prev tab exists
    *  on the current row, move to first column.  If
    *  already on first column, move to last tab on
    *  previous row.  If the cursor is in (1,1), move
    *  to the right most tab of the last row
    """
    def CursorLeft( self ):
        self.__writePage.CursorLeft( self.__ppRemote )
        self.__requiresRepaint = True
    # end def

    def WriteField( self, c ):
        self.__writePage.WriteField( c )
    # end def

    def ClearAll( self ):
        for x in range( 0, self.__numPages + 1 ):
            if self.__pages[ x ] is None:
                break
            # end if
            self.__pages[ x ].ClearPage()
            self.__pages[ x ].BufferPos.Clear()
            self.__pages[ x ].CursorPos.Clear()
            self.__pages[ x ].SetWriteAttribute( VID_NORMAL )
            self.__pages[ x ].SetVideoPriorCondition( VID_NORMAL )
        # next
        self.__requiresRepaint = True
        return
    # end def

    def DecodeKeyAttrs( self, attr ):
        ret = 0
        if attr == 0:
            return 0
        # end if
        if ( attr & ( 1 << 0 ) ) != 0:
            ret |= KEY_UPSHIFT
        # end if
        if ( attr & ( 1 <<  1 ) ) != 0:
            ret |= KEY_KB_ONLY
        # end if
        if ( attr & ( 1 << 2 ) ) != 0:
            ret |= KEY_AID_ONLY
        # end if
        if ( attr & ( 1 << 3 ) ) != 0:
            ret |= KEY_EITHER
        # end if
        if ret == 0 and ( ret & ~( 1 << 6 ) ) != 0:
            # System.out.println("Unknown video attr " + attr);
            pass
        # end if
        return ret
    # end def

    def DecodeDataAttrs( self, attr ):
        ret = 0
        if attr == 0:
            return 0
        # end if
        if ( attr & ( 1 << 0 ) ) != 0:
            ret |= DAT_MDT
        # end if
        if ( attr & ( 1 << 4 ) ) != 0:
            ret |= DAT_AUTOTAB
        # end if
        if ( attr & ( 1 << 5 ) ) != 0:
            ret |= DAT_UNPROTECT
        # end if
        type = attr & ( ( 1 << 1 ) | ( 1 << 2 ) | ( 1 <<3 ) )
        ret |= type << SHIFT_DAT_TYPE
        return ret
    # end def

    def DecodeVideoAttrs( self, attr ):
        ret = 0
        if attr == 0 or attr == 32:
            return 0
        # end if
        if ( attr & ( 1 << 0 ) ) != 0:
            ret |= VID_NORMAL
        # end if
        if ( attr & ( 1 << 1 ) ) != 0:
            ret |= VID_BLINKING
        # end if
        if ( attr & ( 1 << 2 ) ) != 0:
            ret |= VID_REVERSE
        # end if
        if ( attr & ( 1 << 3 ) ) != 0:
            ret |= VID_INVIS
        # end if
        if ( attr & ( 1 << 4 ) ) != 0:
            ret |= VID_UNDERLINE
        # end if
        if ( attr & ~( ( 1 << 5 ) | ( 1 << 0 ) | ( 1 << 1 ) | ( 1<< 2 ) | ( 1 << 3 ) | ( 1 << 4 ) ) ) != 0:
            # System.out.println("Unknown video attr " + attr);
            pass
        # end if
        return ret
    # end def
# end class
