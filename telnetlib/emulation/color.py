
class TerminalForeColors:
    BLACK = AnsiTerm::FORE_BLACK,
    RED = AnsiTerm::FORE_RED,
    GREEN = AnsiTerm::FORE_GREEN,
    YELLOW = AnsiTerm::FORE_YELLOW,
    BLUE = AnsiTerm::FORE_BLUE,
    MAGENTA = AnsiTerm::FORE_MAG,
    CYAN = AnsiTerm::FORE_CYAN,
    GREY = AnsiTerm::FORE_GREY
# end class

class TerminalBackColors:
    BLACK = AnsiTerm::BACK_BLACK,
    RED = AnsiTerm::BACK_RED,
    GREEN = AnsiTerm::BACK_GREEN,
    YELLOW = AnsiTerm::BACK_YELLOW,
    BLUE = AnsiTerm::BACK_BLUE,
    MAGENTA = AnsiTerm::BACK_MAG,
    CYAN = AnsiTerm::BACK_CYAN,
    GREY = AnsiTerm::BACK_GREY
# end class

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
        AnsiTerm::TermForeColor rettermcolor;
        int64 retdiff = 0xFFFFFFFFL;
        int diff = 0;

        int64 argb = UIntToLongNoSignExt(AsRGBA32());

        if ( (diff = abs((int)(argb - m_black))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermForeColor)TerminalForeColors::BLACK;
        }
        if ( (diff = abs((int)(argb - m_red))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermForeColor)TerminalForeColors::RED;
        }
        if ( (diff = abs((int)(argb - m_green))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermForeColor)TerminalForeColors::GREEN;
        }
        if ( (diff = abs((int)(argb - m_yellow))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermForeColor)TerminalForeColors::YELLOW;
        }
        if ( (diff = abs((int)(argb - m_blue))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermForeColor)TerminalForeColors::BLUE;
        }
        if ( (diff = abs((int)(argb - m_magenta))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermForeColor)TerminalForeColors::MAGENTA;
        }
        if ( (diff = abs((int)(argb - m_cyan))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermForeColor)TerminalForeColors::CYAN;
        }
        if ( (diff = abs((int)(argb - m_grey))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermForeColor)TerminalForeColors::GREY;
        }
        return rettermcolor;
    # end def

    def AsTerminalBackColor( self ):
        AnsiTerm::TermBackColor rettermcolor;
        int64 retdiff = 0xFFFFFFFFL;
        int diff = 0;

        int64 argb = UIntToLongNoSignExt(AsRGBA32());

        if ( (diff = abs((int)(argb - m_black))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermBackColor)TerminalBackColors::BLACK;
        }
        if ( (diff = abs((int)(argb - m_red))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermBackColor)TerminalBackColors::RED;
        }
        if ( (diff = abs((int)(argb - m_green))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermBackColor)TerminalBackColors::GREEN;
        }
        if ( (diff = abs((int)(argb - m_yellow))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermBackColor)TerminalBackColors::YELLOW;
        }
        if ( (diff = abs((int)(argb - m_blue))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermBackColor)TerminalBackColors::BLUE;
        }
        if ( (diff = abs((int)(argb - m_magenta))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermBackColor)TerminalBackColors::MAGENTA;
        }
        if ( (diff = abs((int)(argb - m_cyan))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermBackColor)TerminalBackColors::CYAN;
        }
        if ( (diff = abs((int)(argb - m_grey))) < retdiff )
        {
            retdiff = diff;
            rettermcolor = (AnsiTerm::TermBackColor)TerminalBackColors::GREY;
        }
        return rettermcolor;
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
