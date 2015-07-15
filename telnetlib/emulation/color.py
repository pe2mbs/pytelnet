
class TerminalForeColors:
    BLACK               = 30
    RED                 = 31
    GREEN               = 32
    YELLOW              = 33
    BLUE                = 34
    MAGENTA             = 35
    CYAN                = 36
    GREY                = 37
# end class

class TerminalBackColors:
    BLACK               = 40
    RED                 = 41
    GREEN               = 42
    YELLOW              = 43
    BLUE                = 44
    MAGENTA             = 45
    CYAN                = 46
    GREY                = 47
# end class

class TerminalTextAttribute:
    TEXTATRR_OFF        = 0 	#	All attributes off
    EXTATRR_BOLD        = 1	    #	Bold on
    TEXTATRR_DIM        = 2	    #	Dim
    TEXTATRR_UNDERSCORE = 4     #   Underscore (on monochrome display adapter only)
    TEXTATRR_BLINK      = 5	    #   Blink on
    TEXTATRR_REV        = 7	    #   Reverse video on
    TEXTATRR_INVIS      = 8		#   Concealed on

class Color( object ):
    _black      = (0xFF <<24) | (0x00 << 16) | (0x00 << 8) | (0x00)
    _red        = (0xFF <<24) | (0xFF << 16) | (0x00 << 8) | (0x00)
    _green      = (0xFF <<24) | (0x00 << 16) | (0xFF << 8) | (0x00)
    _yellow     = (0xFF <<24) | (0xFF << 16) | (0xFF << 8) | (0x00)
    _blue       = (0xFF <<24) | (0x00 << 16) | (0x00 << 8) | (0xFF)
    _magenta    = (0xFF <<24) | (0xFF << 16) | (0x00 << 8) | (0xFF)
    _cyan       = (0xFF <<24) | (0x00 << 16) | (0xFF << 8) | (0xFF)
    _grey       = (0xFF <<24) | (0xF0 << 16) | (0xF0 << 8) | (0xF0)

    def __init__( self, alpha = 255, red = 0, green = 0, blue = 0, colorref = 0 ):
        self._a = alpha
        self._r = red
        self._g = green
        self._b = blue
        if colorref != 0:
            self._r = ( colorref & 0xFF0000 ) >> 16
            self._g = ( colorref & 0xFF00 ) >> 8
            self._b = colorref & 0xFF
        # end if
    # end def

    def __del__( self ):
        return
    # end def

    def GetAlpha( self ):
        return self._a
    # end def

    def GetRed( self ):
        return self._r
    # end def

    def GetGreen( self ):
        return self._g
    # end def

    def GetBlue( self ):
        return self._b
    # end def

    def AsInt( self ):
        return self._a << 24 | self._r << 16 | self._g << 8 | self._b
    # end def

    def AsRGB24( self ):
        return self._r << 16 | self._g << 8 | self._b
    # end def

    def AsRGBA32( self ):
        return self._a << 24 | self._r << 16 | self._g << 8 | self._b
    # end def

    def AsHexString( self ):
        return "%X" % ( self.AsInt() )
    # end def

    def Brighter( self ):
        rr = self._r + (self._r * .1)
        gg = self._g + (self._g * .1)
        bb = self._b + (self._b * .1)
        return Color( self._a,  0xFF if rr > 0xFF else rr,
                                0xFF if gg > 0xFF else gg,
                                0xFF if bb > 0xFF else bb )
    # end def

    def __eq__( self, color ):
        return self._b == color._b and self._g == color._g and self.r == color._r and self._a == color._a
    # end def

    def __ne__( self, color ):
        return self._b != color._b or self._g != color.m_g or self._r != color._r or self._a != color._a
    # end def

    def AsTerminalForeColor( self ):
        colorList = [   ( self._black,      TerminalForeColors.BLACK ),
                        ( self._red,        TerminalForeColors.RED ),
                        ( self._green,      TerminalForeColors.GREEN ),
                        ( self._yellow,     TerminalForeColors.YELLOW ),
                        ( self._blue,       TerminalForeColors.BLUE ),
                        ( self._magenta,    TerminalForeColors.MAGENTA ),
                        ( self._cyan,       TerminalForeColors.CYAN ),
                        ( self._grey,       TerminalForeColors.GREY ) ]
        rettermcolor    = 0
        retdiff         = 0xFFFFFFFFL
        diff            = 0
        argb            = self._a << 24 | self._r << 16 | self._g << 8 | self._b
        for rbgColor, TermColor in colorList:
            diff = abs( argb - rbgColor )
            if diff < retdiff:
                retdiff         = diff
                rettermcolor    = TermColor
            # end if
        # next
        return rettermcolor
    # end def

    def AsTerminalBackColor( self ):
        colorList = [   ( self._black,      TerminalBackColors.BLACK ),
                        ( self._red,        TerminalBackColors.RED ),
                        ( self._green,      TerminalBackColors.GREEN ),
                        ( self._yellow,     TerminalBackColors.YELLOW ),
                        ( self._blue,       TerminalBackColors.BLUE ),
                        ( self._magenta,    TerminalBackColors.MAGENTA ),
                        ( self._cyan,       TerminalBackColors.CYAN ),
                        ( self._grey,       TerminalBackColors.GREY ) ]
        rettermcolor    = 0
        retdiff         = 0xFFFFFFFFL
        diff            = 0
        argb            = self._a << 24 | self._r << 16 | self._g << 8 | self._b
        for rbgColor, TermColor in colorList:
            diff = abs( argb - rbgColor )
            if diff < retdiff:
                retdiff         = diff
                rettermcolor    = TermColor
            # end if
        # next
        return rettermcolor
    # end def

    def Parse( self, str_color ):
        if "GREEN" == str_color:
            return Color(0, 240, 0)
        elif "BLACK" == str_color:
            return Color(0,0,0)
        elif "BLUE" == str_color:
            return Color(0, 0, 240)
        elif "LTGRAY" == str_color:
            return Color(200, 200, 200)
        elif "GRAY" == str_color:
            return Color(140, 140, 140)
        elif "WHITE" == str_color:
            return Color(255, 255, 255)
        elif "YELLOW" == str_color:
            return Color(0, 255, 255)
        elif "RED" == str_color:
            return Color(255, 0, 0)
        elif "PINK" == str_color:
            return Color(230, 100, 100)
        elif "MAGENTA" == str_color:
            return Color(230, 0, 230)
        elif "ORANGE" == str_color:
            return Color(255, 200, 0)
        # end if
        return Color( 80, 80, 80 )
    # end def
# end class

Black   = Color( 0x00, 0x00, 0x00 )
Red     = Color( 0xFF, 0x00, 0x00 )
Green   = Color( 0x00, 0xFF, 0x00 )
Yellow  = Color( 0xFF, 0xFF, 0x00 )
Blue    = Color( 0x00, 0x00, 0xFF )
Magenta = Color( 0xFF, 0x00, 0xFF )
Cyan    = Color( 0x00, 0xFF, 0xFF )
Grey    = Color( 0xF0, 0xF0, 0xF0 )
