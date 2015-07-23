import curses
import logging

def color_attr( fg, bg ):
    return ( fg << 3 | bg ) << 8
# end if

class CursesDisplay( object ):
    def __init__( self, telnet, display = None ):
        self.__log          = logging.getLogger()
        self.__display      = display
        self.__telnet       = telnet
        self.__fgattr       = curses.COLOR_WHITE
        self.__bgattr       = curses.COLOR_BLACK
        self.__attr         = curses.A_NORMAL
        self.__display.scrollok( True )
        self.__colorList    = [ curses.COLOR_BLACK, curses.COLOR_RED,
                                curses.COLOR_GREEN, curses.COLOR_YELLOW,
                                curses.COLOR_BLUE, curses.COLOR_MAGENTA,
                                curses.COLOR_CYAN, curses.COLOR_WHITE ]
        self.__colorNames   = [ 'BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE' ]
        curses.start_color()
        curses.use_default_colors()
        for fg in range( curses.COLORS ):
            for bg in range( curses.COLORS ):
                curses.init_pair( fg << 3 | bg, fg, bg )
             # next
        # next
        return
    # end def

    def _doAttrs( self, params ):
        if len( params ) == 0:
            self.__attr         = curses.A_NORMAL
            self.__fgattr       = curses.COLOR_WHITE
            self.__bgattr       = curses.COLOR_BLACK
            self.__display.attrset( color_attr( self.__fgattr, self.__bgattr ) | self.__attr )
            self.__log.debug( "Set default fore- and back-ground colors" )
            return
        # end if
        log.debug( "ATTR.params: %s" % ( repr( params ) ) )
        for attr in params:
            """
                0	Reset all attributes
                1	Bright
                2	Dim
                4	Underscore
                5	Blink
                7	Reverse
                8	Hidden

            """
            if attr.isdigit():
                attr = int( attr )
                if attr == 0:    # A_NORMAL	Normal attribute.
                    # self.__display.attrset( curses.A_NORMAL )
                    self.__attr     = curses.A_NORMAL
                    self.__fgattr   = curses.COLOR_WHITE
                    self.__bgattr   = curses.COLOR_BLACK
                    self.__log.debug( "set color A_NORMAL    %X" % ( self.__attr ) )
                elif attr == 1:    # A_BOLD	Bold mode.
                    self.__attr &= ~curses.A_DIM
                    self.__attr |= curses.A_BOLD
                    self.__log.debug( "set color A_BOLD      %X" % ( self.__attr ) )
                elif attr == 2:    # A_DIM	Dim mode.
                    self.__attr &= ~curses.A_BOLD
                    self.__attr |= curses.A_DIM
                    self.__log.debug( "set color A_DIM       %X" % ( self.__attr ) )
                elif attr == 4:    # A_UNDERLINE	Underline mode.
                    self.__attr |= curses.A_UNDERLINE
                    self.__log.debug( "set color A_UNDERLINE %X" % ( self.__attr ) )
                elif attr == 5:    # A_BLINK	Blink mode.
                    self.__attr |= curses.A_BLINK
                    self.__log.debug( "set color A_BLINK     %X" % ( self.__attr ) )
                elif attr == 7:    # A_REVERSE	Reverse background and foreground colors.
                    self.__attr |= curses.A_REVERSE
                    self.__log.debug( "set color A_REVERSE   %X" % ( self.__attr ) )
                elif attr >= 30 and attr <= 37:
                    """
                        Foreground Colours
                        30	Black
                        31	Red
                        32	Green
                        33	Yellow
                        34	Blue
                        35	Magenta
                        36	Cyan
                        37	White

                        39  Default
                    """
                    self.__fgattr = attr - 30
                    self.__log.debug( "set foreground color attr:%i color:%X label:%s" % ( attr, self.__fgattr, self.__colorNames[ self.__fgattr ] ) )
                elif attr == 39:
                    self.__log.debug( "Set default foreground color" )
                    self.__fgattr       = curses.COLOR_WHITE
                elif attr >= 40 and attr <= 47:
                    """
                        background Colours
                        40	Black
                        41	Red
                        42	Green
                        43	Yellow
                        44	Blue
                        45	Magenta
                        46	Cyan
                        47	White

                        49  Default
                    """
                    self.__bgattr = attr - 40
                    self.__display.attrset( color_attr( self.__fgattr, self.__bgattr ) | self.__attr )
                    self.__log.debug( "set background color attr:%i color:%i label:%s" % ( attr, self.__bgattr, self.__colorNames[ self.__bgattr ] ) )
                elif attr == 49:
                    self.__log.debug( "Set default background color" )
                    self.__bgattr       = curses.COLOR_BLACK
                    self.__display.attrset( color_attr( self.__fgattr, self.__bgattr ) | self.__attr )
                # end if
            elif attr == "":
                self.__log.debug( "Set default fore- and back-ground colors" )
                self.__attr         = curses.A_NORMAL
                self.__bgattr       = curses.COLOR_BLACK
                self.__fgattr       = curses.COLOR_WHITE
                self.__display.attrset( color_attr( self.__fgattr, self.__bgattr ) | self.__attr )
            else:
                self.__log.debug( "unknown attr for ESC[%sm" % ( attr ) )
        # next
        self.__params = []
        return
    # end def

    def _doLeds( self, params ):
        for attr in params:
            """
                0   All LEDs off
                1   LED #1 on
                2   LED #2 on
                3   LED #3 on
                4   LED #4 on
            """
            if attr == '0':
                for led in self.__display.Leds:
                    led.Off()
                # next
            else:
                self.__display.Leds[ ord( attr ) - 0x30 ].On()
            # end if
        # next
        return
    # end def

    def HandleKeyboard( self ):
        key = self.__display.getch()
        if key != -1:
            self.Transmit( key )
        # end if
        return key
    # end def

    def Transmit( self, key ):
        self.__log.debug( "Transmit( %i )" % ( key ) )
        if key >= 0x20 and key < 256:
            self.__telnet.write( chr( key ) )
            echo = False
            opt = self.__telnet.getOption(1)
            if opt is not None:
                echo = opt.Echo
            # end if
            echo = False
            if echo:
                self.Print( chr( key ) )
            # end if
        elif key == 0x0A:   # Linefeed
            self.__telnet.write( '\r\n' )
            self.Print( '\n' )
        elif key == 0x0C:   # Carrage return
            # screen.addch( cKey )
            self.__telnet.write( '\r' )
        elif key == 0x09:   # Tab
            # screen.addch( cKey )
            self.__telnet.write( '\t' )
        # end if
        self.__display.refresh()
        return
    # end def

    def Print( self, pstr ):
        try:
            clr = color_attr( self.__fgattr, self.__bgattr )
            self.__log.debug( "fg:%i(%s)  bg:%i(%s)  color: %X  attr: %X  combined: %X" %
                       ( self.__fgattr, self.__colorNames[ self.__fgattr ],
                         self.__bgattr, self.__colorNames[ self.__bgattr ],
                         clr, self.__attr, clr | self.__attr ) )
            self.__display.addstr( pstr, clr | self.__attr )
        except Exception, exc:
            self.__log.error( "self.__display.addstr( %s ) raises ans error: %s" % ( pstr, exc ) )
        # end try
        self.__display.refresh()
        return
    # end def

    def Row( self ):
        l, c = curses.getsyx()
        return l
    # end def

    def Col( self ):
        l, c = curses.getsyx()
        return c
    # end def

    def maxRow( self ):
        l, c = self.__display.getmaxyx()
        return l
    # end def

    def maxCol( self ):
        l, c = self.__display.getmaxyx()
        return c
    # end def

    def clrtobot( self ):
        self.__display.clrtobot()
        return
    # end def

    def clrtoeol( self ):
        self.__display.clrtoeol()
        return
    # end def

    def deleteln( self ):
        self.__display.deleteln()
        return
    # end def

    def clear( self ):
        self.__display.clear()
        return
    # end def

    def cursorpos( self, l, c ):
        try:
            self.__display.move( l, c )
            self.__display.refresh()
        except Exception, exc:
            self.__log.error( "cursorpos( %s, %s ) => %s" % ( l, c, repr( exc ) ) )
        # end try
        return
    # end def

    def setcursor( self, set ):
        return
    # end def

    def cursorup( self ):
        self.__display.do_command( curses.KEY_UP )
        return
    # end def

    def cursordown( self ):
        self.__display.do_command( curses.KEY_DOWN )
        return
    # end def

    def cursorleft( self ):
        self.__display.do_command( curses.KEY_RIGHT )
        return
    # end def

    def cursorright( self ):
        self.__display.do_command( curses.KEY_LEFT )
        return
    # end def

    def newline( self ):
        if self.Row() + 1 == self.maxRow():
            self.__display.scroll( 1 )
            self.__display.refresh()
            #lines = self.Row() - self.maxRow()
            #self.__display.addch( '\n' )
        else:
            self.cursorpos( self.Row() + 1, self.Col() )
        # end if
        return
    # end def

    def carragereturn( self ):
        self.cursorpos( self.Row(), 0 )
        #self.__display.addch( '\r' )
        #self.__display.refresh()
        return
    # end def

    def bell( self ):
        try:
            import winsound
            import time
            import sys
            winsound.Beep(440, 250) # frequency, duration
            time.sleep(0.25)        # in seconds (0.25 is 250ms)
            winsound.Beep(600, 250)
            time.sleep(0.25)
        except:
            sys.stdout.write( '\x07' )
        # end try
        return
    # end def
# end class
