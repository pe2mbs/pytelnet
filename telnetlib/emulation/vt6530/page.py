from telnetlib.emulation.vt6530.cursor import Cursor
from telnetlib.setbits          import SetBits

MASK_CHAR           = 0xFF

"""
*   VIDEO attributes
"""
VID_NORMAL          = 1 << 8
VID_BLINKING	    = 1 << 9
VID_REVERSE	        = 1 << 10
VID_INVIS		    = 1 << 11
VID_UNDERLINE	    = 1 << 12
MASK_VID		    = VID_NORMAL | VID_BLINKING | VID_REVERSE | VID_INVIS | VID_UNDERLINE

"""
*   DATA attributes
"""
DAT_MDT	            = 1 << 13
DAT_TYPE	        = ( 1 << 14 ) | ( 1 << 15 ) | ( 1 << 16 )
DAT_AUTOTAB         = 1 << 17
DAT_UNPROTECT       = 1 << 18
SHIFT_DAT_TYPE      = 14

"""
*   KEY attributes
"""
KEY_UPSHIFT	        = 1 << 19
KEY_KB_ONLY	        = 1 << 20
KEY_AID_ONLY	    = 1 << 21
KEY_EITHER		    = 1 << 22

"""
*   SPECIAL attributes
"""
CHAR_START_FIELD    = 1 << 23
CHAR_CELL_DIRTY     = 1 << 24
MASK_FIELD          = ( ( 1 << 8 ) | ( 1 << 9 ) | ( 1 << 10 ) | ( 1 << 11 ) | ( 1 << 12 ) |
                        ( 1 << 13 ) | ( 1 << 14 ) | ( 1 << 15 ) | ( 1 << 16 ) | ( 1 << 17 ) |
                        ( 1 << 18 ) | ( 1 << 19 ) | ( 1 << 20 ) | ( 1 << 21 ) | ( 1 << 22 ) |
                        ( 1 << 23 ) | ( 1 << 25 ) | ( 1 << 26 ) | ( 1 << 27 ) )
"""
*   Color bits
"""
MASK_COLOR          = ( 1 << 25 ) | ( 1 << 26 ) | ( 1 << 27 )
SHIFT_COLOR         = 25

"""
*   Insert mode
"""
INSERT_INSERT       = 0
INSERT_OVERWRITE    = 1



m_vidNormal         = 0
m_vidBlinking       = 1
m_vidReverse        = 2
m_vidInvis          = 3
m_vidUnderline      = 4
m_datMdt            = 5
m_datAutotab        = 6
m_datUnprotect      = 7
m_keyUpshift        = 8
m_keyKbOnly         = 9
m_keyAidOnly        = 10
m_keyEither         = 11
m_charStartField    = 12
m_charDirtyCell     = 13
m_datDataType       = 14
m_charColor         = 17

class PageCell( object ):
    def __init__( self ):
        self.__attribs  = SetBits()
        self.__ch       = ' '
        return
    # end def

    def __del__( self ):
        return
    # end def


    def Get( self ):
        return self.__ch
    # end def

    def getAttr( self ):
        return self.__attribs
    # end def

    def Set( self, value, attrs = None ):
        if type( value ) in [ str, unicode ]:
            self.__ch = value
            self.__attribs.setBit( m_charDirtyCell )
            if attrs is not None:
                 self.SetAttributes( attrs )
            # end def
        elif type( value ) is PageCell:
            self.__ch = value.Get()
            self.__attribs.Set( value.GetAttr() )
            self.__attribs.setBit( m_charDirtyCell )
        # end def
        return
    # end def

    def SetAttributes( self, iAttribs ):
        self.__attribs.setInteger( iAttribs >> 8 )
        return
    # end def

    def GetAttributes( self ):
        return self.__attribs.getInteger() << 8
    # end def

    def AsInt( self ):
        return self.GetAttributes() | ord( self.__ch )
    # end def

    def Clear( self, attributes = None ):
        self.__ch = ' '
        if attributes is None:
            self.__attribs.Clear()
            self.__attribs.setBit( m_vidNormal )
        else:
            self.SetAttributes( attributes )
        # end if
        return
    # end def

    def ClearVideoAttribs( self ):
        self.__attribs.setBit( m_vidNormal )
        self.__attribs.clearBit( m_vidBlinking )
        self.__attribs.clearBit( m_vidReverse )
        self.__attribs.clearBit( m_vidInvis )
        self.__attribs.clearBit( m_vidUnderline )
        self.__attribs.setBit( m_charDirtyCell )
        return
    # end def


    def ClearTo( self, ch ):
        """
            ClearTo doesn't set the dirty flag
        """
        self.__ch = ch
        self.__attribs.Clear()
        self.__attribs.setBit( m_vidNormal )
        return
    # end def

    def SetDirty( self, val ):
        if val:
            self.__attribs.setBit( m_charDirtyCell )
        else:
            self.__attribs.clearBit( m_charDirtyCell )
        # end if
        return
    # end def

    def IsDirty( self ):
        return self.__attribs.testBit( m_charDirtyCell )
    # end def

    def SetNormal( self, val ):
        if val:
            self.__attribs.setBit( m_vidNormal )
        else:
            self.__attribs.clearBit( m_vidNormal )
        # end if
        return
    # end def

    def IsNormal( self ):
        return self.__attribs.testBit( m_vidNormal )
    # end def

    def SetBlinking( self, val ):
        if val:
            self.__attribs.setBit( m_vidBlinking )
        else:
            self.__attribs.clearBit( m_vidBlinking )
        # end if
        return
    # end def

    def IsBlinking( self ):
        return self.__attribs.testBit( m_vidBlinking )
    # end def

    def SetReverse( self, val ):
        if val:
            self.__attribs.setBit( m_vidReverse )
        else:
            self.__attribs.clearBit( m_vidReverse )
        # end if
        return
    # end def

    def IsReverse( self ):
        return self.__attribs.testBit( m_vidReverse )
    # end def

    def SetInvis( self, val ):
        if val:
            self.__attribs.setBit( m_vidInvis )
        else:
            self.__attribs.clearBit( m_vidInvis )
        # end if
        return
    # end def

    def IsInvis( self ):
        return self.__attribs.testBit( m_vidInvis )
    # end def

    def SetUnderline( self, val ):
        if val:
            self.__attribs.setBit( m_vidUnderline )
        else:
            self.__attribs.clearBit( m_vidUnderline )
        # end if
        return
    # end def

    def IsUnderline( self ):
        return self.__attribs.testBit( m_vidUnderline )
    # end def

    def SetUnprotect( self, val ):
        if val:
            self.__attribs.setBit( m_datUnprotect )
        else:
            self.__attribs.clearBit( m_datUnprotect )
        # end if
        return
    # end def

    def IsUnprotect( self ):
        return self.__attribs.testBit( m_datUnprotect )
    # end def

    def SetStartField( self, val ):
        if val:
            self.__attribs.setBit( m_charStartField )
        else:
            self.__attribs.clearBit( m_charStartField )
        # end if
        return
    # end def

    def IsStartField( self ):
        return self.__attribs.testBit( m_charStartField )
    # end def

    def SetMDT( self, val ):
        if val:
            self.__attribs.setBit( m_datMdt )
        else:
            self.__attribs.clearBit( m_datMdt )
        # end if
        return
    # end def

    def IsMDT( self ):
        return self.__attribs.testBit( m_datMdt )
    # end def

    def SetKeyUpshift( self, val ):
        if val:
            self.__attribs.setBit( m_keyUpshift )
        else:
            self.__attribs.clearBit( m_keyUpshift )
        # end def
        return
    # end def

    def IsKeyUpshift( self ):
        return self.__attribs.testBit( m_keyUpshift )
    # end def
# end class


class Page( object ):
    def __init__( self, iNumRows, iNumCols ):
        self.__chbuf            = '  '
        self.__numRows          = iNumRows
        self.__numColumns       = iNumCols
        self.__writeAttr        = 0         # These attributes can be set and then effect
        self.__priorAttr        = 0         # all subsequent writes.
        self.__insertMode       = 0
        self.__cursorBlock      = False
        self.__cursorPos        = Cursor()
        self.__bufferPos        = Cursor()
        self.__cells            = [ PageCell() ] * self.__numRows * self.__numColumns
        self.__fields           = []        # PageCell()
        self.__unprotectFields  = []        # PageCell()

        return
    # end def

    def getCursorPos( self ):
        return self.__cursorPos
    # end def

    CursorPos = property( getCursorPos )

    def getBufferPos( self ):
        return self.__bufferPos
    # end def

    BufferPos = property( getBufferPos )


    def Init( self ):
        self.__writeAttr = VID_NORMAL
        self.__priorAttr = VID_NORMAL
        self.__cursorPos.Clear()
        self.__bufferPos.Clear()
        self.__fields = []
        self.__unprotectFields = []
        for x in range( 0, self.__numRows ):
            for q in range( 0, self.__numColumns ):
                cell = self.GetCell( q, x )
                cell.ClearTo( ' ' ) # = (int)' ' | CHAR_CELL_DIRTY | m_writeAttr
                cell.SetDirty( True )
                cell.SetNormal( True )
            # next
        # next
        return
    # end def

    def GetNumRows( self ):
        return self.__numRows
    # end def

    def GetNumColumns( self ):
        return self.__numColumns
    # end def

    def GetCell( self, x, y = None ):
        if type( x ) is Cursor:
            return self.GetCell( x.Col(), x.Row() )
        # end if
        return self.__cells[ y * self.__numColumns + x ]
    # end def


    def WriteBuffer( self, PageProtocol_mode, text ):
        PageProtocol_mode.WriteBuffer( self, text )
        return
    # end def

    def WriteCursor( self, PageProtocol_mode, text ):
        PageProtocol_mode.WriteCursor( self, text)
        return
    # end def

    def WriteCursorLocal( self, PageProtocol_mode, text ):
        for x in text:
            PageProtocol_mode.WriteChar( self, self.__cursorPos, x | DAT_MDT )
        # next
        return
    # end def

    def CarageReturn( self, PageProtocol_mode ):
        PageProtocol_mode.CarageReturn( self )
        return
    # end def

    def SetCursor( self, PageProtocol_mode, row, col ):
        PageProtocol_mode.SetCursor( self, row, col )
        return
    # end def

    def SetBuffer( self, row, col ):
        self.__bufferPos.Row = row
        self.__bufferPos.Col = col
        return
    # end def

    def SetVideoPriorCondition( self, attr ):
        self.__priorAttr = attr
    # end def

    def SetWriteAttribute( self, attr ):
        self.__writeAttr = attr
        return
    # end def

    def GetWriteAttr( self ):
        return self.__writeAttr
    # end def

    def GetPriorAttr( self ):
        return self.__priorAttr
    # end def

    def InsertChar( self, PageProtocol_mode ):
        PageProtocol_mode.InsertChar( self )
        return
    # end def

    def SetInsertMode( self, mode ):
        self.__insertMode = mode
        return
    # end def

    def DeleteChar( self, PageProtocol_mode ):
        PageProtocol_mode.DeleteChar( self )
        return
    # end def

    def Tab( self, PageProtocol_mode, inc ):
        PageProtocol_mode.Tab( self, inc )
        return
    # end def

    def Backspace( self, PageProtocol_mode ):
        PageProtocol_mode.Backspace( self )
        return
    # end def

    def CursorUp( self, PageProtocol_mode ):
        PageProtocol_mode.CursorUp( self )
        return
    # end def

    def CursorDown( self, PageProtocol_mode ):
        PageProtocol_mode.CursorDown( self )
        return
    # end def

    def CursorLeft( self, PageProtocol_mode ):
        PageProtocol_mode.CursorLeft( self )
        return
    # end def

    def CursorRight( self, PageProtocol_mode ):
        PageProtocol_mode.CursorRight( self )
        return
    # end def

    def ClearPage( self ):
        for r in range( 0, self.__numRows * self.__numColumns ):
            self.__cells[ r ].Clear()
            self.__cells[ r ].SetAttributes( self.__writeAttr | self.__priorAttr )
        # next
        return
    # end def

    def ClearToEOP( self, PageProtocol_mode ):
        PageProtocol_mode.ClearToEOP( self )
        return
    # end def

    def ClearToEOL( self, PageProtocol_mode ):
        PageProtocol_mode.ClearToEOL( self )
        return
    # end def

    def ClearBlock( self, PageProtocol_mode, iStartRow, iStartCol, iEndRow, iEndCol ):
        PageProtocol_mode.ClearBlock( self, iStartRow, iStartCol, iEndRow, iEndCol )
        return
    # end def

    def WriteField( self, c ):
        """
            mark the field

        """
        cell = self.GetCell( self.__bufferPos )
        self.__fields.append( cell )
        cell.Set( c & MASK_CHAR )
        cell.SetAttributes( (c & MASK_FIELD) | CHAR_START_FIELD | CHAR_CELL_DIRTY | self.__writeAttr | self.__priorAttr )
        if cell.IsUnprotect():
            self.__unprotectFields.append( cell )
        # end if
        # The field start char is not updatable.  For unprotect fields, the char to the
        # right is the first updatable char.
        cell.SetUnprotect( False )

        self.__bufferPos.Column += 1
        self.__bufferPos.AdjustCol()

        # detect any previous field on the line and extend
        # its attributes upto this one
        for col in range( self.__bufferPos.Column, self.__numColumns ):
            if self.GetCell( col, self.__bufferPos.Row ).IsStartField():
                return
            # end if
            self.GetCell( col, self.__bufferPos.Row ).SetAttributes( (c & MASK_FIELD) | CHAR_CELL_DIRTY | self.__writeAttr | self.__priorAttr )
        # next
        for y in range( self.__bufferPos.Row + 1, self.__numRows ):
            for x in range( 0, self.__numColumns ):
                cell = self.GetCell( x, y )
                if cell.IsStartField():
                    return
                # end  def
                cell.SetAttributes( (c & MASK_FIELD) | CHAR_CELL_DIRTY | self.__writeAttr | self.__priorAttr )
            # next
        # next
        return
    # end def

    def ReadBuffer( self, StringBuffer_out, PageProtocol_mode, iReqMask, iForbidMask, iStartRow, iStartCol, iEndRow, iEndCol ):
        PageProtocol_mode.ReadBuffer( StringBuffer_out, self, iReqMask, iForbidMask, iStartRow, iStartCol, iEndRow, iEndCol )
        return
    # end def

    def ResetMDTs( self ):
        for r in range( 0, self.__numRows * self.__numColumns ):
            self.__cells[ r ].SetMDT( False )
        # next
    # end def

    def GetStartFieldASCII( self, StringBuffer_buf ):
        for r in range( 0, self.__numRows ):
            for c in range( 0, self.__numColumns ):
                c2 = c + 1
                r2 = r
                if c2 >= self.__numColumns:
                    c2 = 0
                    r2 += 1
                    if r2 >= self.__numRows:
                        r2 = 0
                    # end if
                # end if
                if self.GetCell( c, r ).IsStartField() and self.GetCell( c2, r2 ).IsUnprotect():
                    StringBuffer_buf.append( chr(r + 0x20 ) )
                    StringBuffer_buf.append( chr(c + 0x21 ) )
                    return
                # end if
            # next
        # next
        StringBuffer_buf.append( "  " )
        # self.paint( PaintSurface *ps, statusLine )/
        return
    # end def

    def ForceDirty( self ):
        for r in range( 0, self.__numRows * self.__numColumns ):
            self.__cells[ r ].SetDirty( True )
        # next
        return
    # end def

    def ScrollPageUp( self ):
        for r in range( 0, self.__numRows - 1 ):
            for c in range( 0, self.__numColumns ):
                self.GetCell( c, r ).Set( self.GetCell( c, r + 1 ) )
            # next
        # next
        for c in range( 0, self.__numColumns ):
            self.GetCell( c, self.__numRows - 1 ).Set( ' ' )
            self.GetCell( c, self.__numRows - 1 ).SetAttributes( self.__writeAttr | self.__priorAttr )
        # next
        return
    # end def

    def ScanForNextField( self, c, r, inc ):
        if inc > 0:
            for x in range( c, self.__numColumns ):
                if self.GetCell( x, r ).IsStartField():
                    return x
                # end if
            # next
        else:
            if c == 0:
                c = self.__numColumns - 1
                if r == 0:
                    r = self.__numRows - 1
                else:
                    r -= 1
                # end if
            # end if
            for x in range( c + 1, 0 ):
                if self.GetCell( x - 1, r ).IsStartField():
                    return x
                # end if
            # next
        # end if
	    return -1
    # end def

    def ScanForUnprotectField( self, c, r, inc ):
        if inc > 0:
            for x in range( c, self.__numColumns ):
                if self.GetCell( x, r ).IsUnprotect():
                    return x
                # enx if
            # next
        else:
            if c == 0:
                c = self.__numColumns - 1
                if r == 0:
                    r = self.__numRows - 1
                else:
                    r -= 1
                # end if
            # end if
            for x in range( c, 0 ):
                if self.GetCell( x - 1, r ).IsUnprotect():
                    return x
                # end if
            # next
        # end if
        return -1
    # end def

    def GetFieldCount( self ):
        return len( self.__fields )
    # end def

    def GetUnprotectFieldCount( self ):
        return len( self.__unprotectFields )
    # end def

    def GetFieldStart( self, x ):
        return None if x >= len( self.__fields ) else self.__fields.ElementAt( x )
    # end def

    def GetUnprotectFieldStart( self, x ):
        return None if x >= len( self.__unprotectFields ) else self.__unprotectFields.ElementAt( x )
    # end def
# end class

