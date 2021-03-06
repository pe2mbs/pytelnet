import sys
import os
import telnetlib.emulation
import curses
import logging
from telnetlib.emulation.display import CursesDisplay


VT52_CUR_UP     = ( 27, 65 )
VT52_CUR_DOWN   = ( 27, 66 )
VT52_CUR_RIGHT  = ( 27, 67 )
VT52_CUR_LEFT   = ( 27, 68 )

VT52_NUM_0      = ( 27, '?', 'p' )
VT52_NUM_1      = ( 27, '?', 'q' )
VT52_NUM_2      = ( 27, '?', 'r' )
VT52_NUM_3      = ( 27, '?', 's' )
VT52_NUM_4      = ( 27, '?', 't' )
VT52_NUM_5      = ( 27, '?', 'u' )
VT52_NUM_6      = ( 27, '?', 'v' )
VT52_NUM_7      = ( 27, '?', 'w' )
VT52_NUM_8      = ( 27, '?', 'x' )
VT52_NUM_9      = ( 27, '?', 'y' )

VT52_NUM_DOT    = ( 27, '?', 'n' )
VT52_NUM_DASH   = ( 27, '?', 'm' )
VT52_NUM_COMMA  = ( 27, '?', 'l' )
VT52_NUM_ENTER  = ( 27, '?', 'M' )
VT52_NUM_FP1    = ( 27, 'P' )
VT52_NUM_FP2    = ( 27, 'Q' )
VT52_NUM_FP3    = ( 27, 'R' )
VT52_NUM_FP4    = ( 27, 'S' )


VT100_CUR_UP     = ( 27, 'O', 65 )
VT100_CUR_DOWN   = ( 27, 'O', 66 )
VT100_CUR_RIGHT  = ( 27, 'O', 67 )
VT100_CUR_LEFT   = ( 27, 'O', 68 )

VT100_NUM_0      = ( 27, 'O', 'p' )
VT100_NUM_1      = ( 27, 'O', 'q' )
VT100_NUM_2      = ( 27, 'O', 'r' )
VT100_NUM_3      = ( 27, 'O', 's' )
VT100_NUM_4      = ( 27, 'O', 't' )
VT100_NUM_5      = ( 27, 'O', 'u' )
VT100_NUM_6      = ( 27, 'O', 'v' )
VT100_NUM_7      = ( 27, 'O', 'w' )
VT100_NUM_8      = ( 27, 'O', 'x' )
VT100_NUM_9      = ( 27, 'O', 'y' )

VT100_NUM_DOT    = ( 27, 'O', 'n' )
VT100_NUM_DASH   = ( 27, 'O', 'm' )
VT100_NUM_COMMA  = ( 27, 'O', 'l' )
VT100_NUM_ENTER  = ( 27, 'O', 'M' )
VT100_NUM_FP1    = ( 27, 'O', 'P' )
VT100_NUM_FP2    = ( 27, 'O', 'Q' )
VT100_NUM_FP3    = ( 27, 'O', 'R' )
VT100_NUM_FP4    = ( 27, 'O', 'S' )

log = logging.getLogger()


class VT100( telnetlib.emulation.TerminalEmulation,
             telnetlib.emulation.MappedKeyListener,
             CursesDisplay ):
    def __init__( self, telnet, display = None, keys = None ):
        CursesDisplay.__init__( self, telnet, display )
        self.__telnet           = telnet
        self.__state            = 0
        self.__lastState        = 0
        self.__justConnected    = True
        self.__lastLine         = ''
        return
    # end def

    def __del__( self ):
        return
    # end def

    def OnReceive( self, data ):
        for cCh in data:
            iCh = ord( cCh )
            if self.__lastState != self.__state:
                log.debug( "state change from %i to %i" % ( self.__lastState, self.__state ) )
                self.__lastState = self.__state
            # end if
            if self.__state == 0:
                if iCh == 0x1B:
                    log.debug( "ESC mode" )
                    self.__state = 27
                elif iCh == 7:
                    self.bell()
                elif iCh == 8:
                    self.Print( '\x08 \x08' )
                elif iCh == 9:
                    self.Print( '\t' )
                elif iCh == 0x0A:
                    self.newline()
                elif iCh == 0x0C:
                    self.carragereturn()
                elif iCh == 0x0f: # Invoke G0 character set into GL. G0 is designated by a select-character-set sequence (SCS).
                    pass
                else:
                    self.__lastLine += cCh
                    self.Print( cCh )
                # end if
                if self.__justConnected:
                    if self.__telnet.Username is not None and 'login:' in self.__lastLine.lower():
                        log.info( "send username" )
                        self.__telnet.write( self.__telnet.Username + "\n" )
                        self.Print( self.__telnet.Username + "\n" )
                        self.__lastLine = ''
                    elif self.__telnet.Password is not None and 'password:' in self.__lastLine.lower():
                        log.info( "send password" )
                        self.__telnet.write( self.__telnet.Password + "\n" )
                        self.Print( "*" * len( self.__telnet.Password ) + "\n" )
                        self.__lastLine = ''
                    elif "last login" in self.__lastLine.lower():
                        self.__justConnected = False
                        log.info( "connected" )
                        self.__telnet.write( 'export TERM=vt100\n' )
                        self.__lastLine = ''
                    # end if
                else:
                    self.__lastLine = ''
                # end if
            elif self.__state == 27:    # ESC mode
                if cCh == '7':          # Save cursor and attributes
                    pass
                elif cCh == '8':        # Restore cursor and attributes
                    pass
                elif cCh == 'A':        # Cursor UP
                    self.cursorup()
                elif cCh == 'B':        # Cursor DOWN
                    self.cursordown()
                elif cCh == 'C':        # Cursor RIGHT
                    self.cursorright()
                elif cCh == 'D':        # Cursor LEFT
                    self.cursorleft()
                elif cCh == 'F':        # Select Special Graphics character set
                    pass
                elif cCh == 'G':        # Select ASCII character set
                    pass
                elif cCh == 'H':        # Cursor Home
                    self.cursorpos( 0, 0 )
                elif cCh == 'I':        # Reverse line feed
                    pass
                elif cCh == 'J':        # Erase to end of screen
                    self.clrtobot()
                elif cCh == 'K':        # Erase to end of line
                    self.clrtoeol()
                elif cCh == '=':        # Enter alternate keypad mode
                    pass
                elif cCh == '>':        # Exit alternate keypad mode
                    pass
                elif cCh == '1':        # Graphics processor on
                    pass
                elif cCh == '2':        # Graphics processor off
                    pass
                elif cCh == '<':        # Enter ANSI mode
                    pass
                elif cCh == 'Z':        # Identify
                    id = ( 27, '/', 'K' )
                    self.__telnet.SendRaw( id )
                elif cCh == 'Y':        # Direct Cursor Address
                    self.__state = 28
                elif cCh == 'D':        # Index
                    pass
                elif cCh == 'M':    # Reverse Index
                    pass
                elif cCh == '[':
                    log.debug( "CSI mode" )
                    self.__state    = 2700
                    self.__lastLine = ''
                    self.__params   = []
                    continue
                elif cCh == '#':
                    self.__state = 29
                elif cCh == '(':     # Character set G0
                    self.__state = 30
                elif cCh == ')':     # Character set G1
                    self.__state = 31
                # end if
                self.__state = 0
            elif self.__state == 28:
                self.__params.append( cCh )
                self.__state = 29
            elif self.__state == 29:
                self.__params.append( cCh )
                self.cursorpos( ord( self.__params[ 0 ] ) - 0x20, ord( self.__params[ 0 ] ) - 0x20 )
                self.__params = []
                self.__state = 0
            elif self.__state == 29:
                if iCh == 0x33:         # Change this line to double-height top half
                    pass
                elif iCh == 0x34:       # Change this line to double-height bottom half
                    pass
                elif iCh == 0x35:       # Change this line to single-width single-height
                    pass
                elif iCh == 0x36:       # Change this line to double-width single-height
                    pass
                else:
                    pass
                # end if
                self.__state = 0
            elif self.__state == 2700:  # State CSI
                if cCh == 'K':   # Erase from cursor to end of line
                    if len( self.__params ) > 0:
                        if self.__params[ 0 ] == '1':
                            log.debug( "delete to beginning of line" )
                            # self.__display.EraseToBOL()
                            pass
                        elif self.__params[ 0 ] == '2':
                            self.deleteln()
                            log.debug( "delete line" )
                        # end if
                    else:
                        log.debug( "delete to end of line" )
                        self.clrtoeol()
                    # end if
                elif cCh == 'J':   # Erase from cursor to end of screen
                    if len( self.__params ) > 0:
                        if self.__params[ 0 ] == '1':
                            # self.__display.EraseFromBOA()
                            log.debug( "erase from beginning of screen" )
                            pass
                        elif self.__params[ 0 ] == '2':
                            self.clear()
                            log.debug( "erase screen" )
                        # end if
                    else:
                        self.clrtobot()
                        log.debug( "erase to end of screen" )
                    # end if
                elif cCh == 'H':
                    if len( self.__lastLine ) > 0:
                        self.__params.append( self.__lastLine )
                        self.__lastLine = ''
                    # end if
                    if len( self.__params ):
                        log.debug( "set cursor pos to %i, %i" % ( int( self.__params[ 0 ] ), int( self.__params[ 1 ] ) ) )
                        self.cursorpos( int( self.__params[ 0 ] ) - 1, int( self.__params[ 1 ] ) - 1  )
                    else:
                        log.debug( "set cursor pos to HOME" )
                        self.cursorpos( 0, 0 )
                    # end if
                elif cCh == 'm':
                    if len( self.__lastLine ) > 0:
                        self.__params.append( self.__lastLine )
                        self.__lastLine = ''
                    # end if
                    self._doAttrs( self.__params )
                elif cCh == ';':   # Cursor direct addressing / Set attributes
                    self.__params.append( self.__lastLine )
                    self.__lastLine = ''
                    continue
                elif cCh in '1234567890':
                    self.__lastLine += cCh
                    continue
                elif cCh == '?':
                    self.__lastLine += cCh
                    continue
                elif cCh == 'h':    # set
                    if self.__lastLine == "?1": # Causes the cursor keys to send application control functions.
                        log.debug( "Causes the cursor keys to send application control functions." )
                    # end if
                elif cCh == 'l':    # reset
                    if self.__lastLine == "?1": # Causes the cursor keys to generate ANSI cursor control sequences.
                        log.debug( "Causes the cursor keys to generate ANSI cursor control sequences." )
                    # end if
                else:
                    log.debug( "unknown chr %c %i in state CSI" % ( cCh, iCh ) )
                # end if
                self.__state = 0
            elif self.__state == 2701:

                if iCh == 0x65:   # Cursor UP
                    for x in range( ord( self.__params[ 0 ] ) ):
                        self.cursorup()
                    # end if
                elif iCh == 0x66:   # Cursor DOWN
                    for x in range( ord( self.__params[ 0 ] ) ):
                        self.cursordown()
                    # end if
                    pass
                elif iCh == 0x67:   # Cursor RIGHT
                    for x in range( ord( self.__params[ 0 ] ) ):
                        self.cursorright()
                    # end if
                    pass
                elif iCh == 0x68:   # Cursor LEFT
                    for x in range( ord( self.__params[ 0 ] ) ):
                        self.cursorleft()
                    # end if
                    pass

                else:
                    self.__state    = 0
                # end if
            elif self.__state == 2703:
                self.__params.append( cCh )
                self.__state = 2704
            elif self.__state == 2704:
                if cCh == 'H' or cCh == 'f':   # Direct Cursor Addressing
                    self.__display.cursorpos( int( self.__params[ 0 ] ), int( self.__params[ 1 ] ) )
                elif cCh == 'm':   # Attributes
                    self._doAttrs()
                elif cCh == 'p': # Programmeble LEDs
                    self._doLeds()
                elif cCh == 'r':     # Scrolling region
                    pass
                elif cCh == ';':
                    self.__params.append( cCh )
                    self.__state    = 2703
                    continue
                # end if
                self.__state    = 0
            elif self.__state == 30:        # Character set G0
                if cCh == 'A':              # UK
                    pass
                elif cCh == 'B':            # US ASCII
                    pass
                elif cCh == '0':            # Special graphics characters and line drawing set
                    pass
                elif cCh == '1':            # Alternate character ROM
                    pass
                elif cCh == '2':            # Alternate character ROM special graphics characters
                    pass
                # end if
                self.__state    = 0
            elif self.__state == 31:        # Character set G1
                if cCh == 'A':              # UK
                    pass
                elif cCh == 'B':            # US ASCII
                    pass
                elif cCh == '0':            # Special graphics characters and line drawing set
                    pass
                elif cCh == '1':            # Alternate character ROM
                    pass
                elif cCh == '2':            # Alternate character ROM special graphics characters
                    pass
                # end if
                self.__state    = 0
            # end if
        # next
        return
    # end def

    def HandleKeyboard( self ):
        return CursesDisplay.HandleKeyboard( self )
    # end def

    def Transmit( self, key ):
        CursesDisplay.Transmit( self, key )
        if key == curses.KEY_UP:
            self.__telnet.write( VT100_CUR_UP )
        elif key == curses.KEY_DOWN:
            self.__telnet.write( VT100_CUR_DOWN )
        elif key == curses.KEY_LEFT:
            self.__telnet.write( VT100_CUR_LEFT )
        elif key == curses.KEY_RIGHT:
            self.__telnet.write( VT100_CUR_RIGHT )
        # end if
        return
    # end def
# end class

class VTxterm( telnetlib.emulation.TerminalEmulation, telnetlib.emulation.MappedKeyListener,
               CursesDisplay ):
    def __init__( self, telnet, display = None, keys = None ):
        CursesDisplay.__init__( self, telnet, display )
        self.__state        = 0
        self.__lastState    = 0
        self.__justConnected= True
        self.__lastLine     = ''
        return
    # end def

    def __del__( self ):
        return
    # end def

    def OnTelnetRecv( self, data ):
        for cCh in data:
            iCh = ord( cCh )
            if self.__lastState != self.__state:
                log.debug( "state change from %i to %i" % ( self.__lastState, self.__state ) )
                self.__lastState = self.__state
            # end if
            if self.__state == 0:
                if iCh == 27:
                    self.__state = 27
                elif iCh == 7:
                    self.__display.addch( '\x07', color_attr( self.__fgattr, self.__bgattr ) | self.__attr )
                elif iCh == 8:
                    self.__display.addstr( '\x08 \x08', color_attr( self.__fgattr, self.__bgattr ) | self.__attr )
                elif iCh == 9:
                    self.__display.addch( '\t', color_attr( self.__fgattr, self.__bgattr ) | self.__attr )
                elif iCh == 10:
                    try:
                        self.__display.addch( '\n', color_attr( self.__fgattr, self.__bgattr ) | self.__attr )
                    except Exception, exc:
                        log.error( "self.__display.addch( '\n' ) raises ans error: %s" % ( exc ) )
                    # end try
                elif iCh == 13:
                    pass
                else:
                    self.__display.addch( cCh, color_attr( self.__fgattr, self.__bgattr ) | self.__attr )
                # end if
                if self.__justConnected:
                    self.__lastLine += cCh
                    if self.__telnet.Username is not None and 'login:' in self.__lastLine.lower():
                        log.debug( "send username" )
                        self.__telnet.write( self.__telnet.Username + '\n' )
                        # self.__telnet.write( '\n' )
                        self.__lastLine = ''
                    elif self.__telnet.Password is not None and 'password:' in self.__lastLine.lower():
                        log.debug( "send password" )
                        self.__telnet.write( self.__telnet.Password + "\n" )
                        # self.__telnet.write( '\n' )
                        self.__lastLine = ''
                    elif "last login" in self.__lastLine.lower():
                        self.__justConnected = False
                        log.debug( "connected" )
                        self.__telnet.write( 'export TERM=xterm\n' )
                        self.__lastLine = ''
                    # end if
                else:
                    self.__lastLine = ''
                # end if
            elif self.__state == 27:
                if cCh == '7':         # Save cursor and attributes
                    log.debug( "Missing: Save cursor and attributes" )
                elif cCh == '8':       # Restore cursor and attributes
                    log.debug( "Missing: Restore cursor and attributes" )
                elif cCh == 'A':     # Cursor UP
                    log.debug( "Cursor UP" )
                    self.__display.do_command( curses.KEY_UP )
                elif cCh == 'B':     # Cursor DOWN
                    log.debug( "Cursor DOWN" )
                    self.__display.do_command( curses.KEY_DOWN )
                elif cCh == 'C':     # Cursor RIGHT
                    log.debug( "Cursor RIGHT" )
                    self.__display.do_command( curses.KEY_RIGHT )
                elif cCh == 'D':     # Cursor LEFT
                    log.debug( "Cursor LEFT" )
                    self.__display.do_command( curses.KEY_LEFT )
                elif cCh == 'F':     # Select Special Graphics character set
                    log.debug( "Missing: Select Special Graphics character set" )
                elif cCh == 'G':     # Select ASCII character set
                    log.debug( "Missing: Select ASCII character set" )
                elif cCh == 'H':     # Cursor Home
                    log.debug( "CURSOR.HOME" )
                    self.__display.move( 0, 0 )
                elif cCh == 'I':     # Reverse line feed
                    log.debug( "Reverse line feed" )
                elif cCh == 'J':     # Erase to end of screen
                    log.debug( "Erase to end of screen" )
                    self.__display.clrtobot()
                elif cCh == 'K':     # Erase to end of line
                    log.debug( "Erase to end of line" )
                    self.__display.clrtoeol()
                elif cCh == '=':     # Enter alternate keypad mode
                    log.debug( "Missing: Enter alternate keypad mode" )
                elif cCh == '>':     # Exit alternate keypad mode
                    log.debug( "Missing: Exit alternate keypad mode" )
                elif cCh == '1':     # Graphics processor on
                    log.debug( "Missing: Graphics processor on" )
                elif cCh == '2':     # Graphics processor off
                    log.debug( "Missing: Graphics processor off" )
                elif cCh == '<':     # Enter ANSI mode
                    log.debug( "Missing: Enter ANSI mode" )
                elif cCh == 'Z':     # Identify
                    id = ( 27, '/', 'K' )
                    self.__telnet.SendRaw( id )
                elif cCh == 'Y':     # Direct Cursor Address
                    self.__state = 28
                elif cCh == 'D':   # Index
                    log.debug( "Missing: Index" )
                elif cCh == 'M':   # Reverse Index
                    log.debug( "Missing: Reverse Index" )
                elif cCh == '[':
                    log.debug( "CSI" )
                    self.__params = []
                    self.__lastLine = ''
                    self.__state = 2700
                elif cCh == '#':
                    self.__state = 29
                elif cCh == '(':     # Character set G0
                    self.__state = 30
                elif cCh == ')':     # Character set G1
                    self.__state = 31
                else:
                    log.debug( "unknown command %i in state 27" % ( iCh ) )
                    self.__state = 0
                # end if
            elif self.__state == 28:
                self.__params.append( cCh )
                self.__state = 29
            elif self.__state == 29:
                self.__params.append( cCh )
                log.debug( "state 29: params: %s" % ( repr( self.__params ) ) )
                l = int( self.__params[ 0 ] )
                c = int( self.__params[ 1 ] )
                self.__display.move( l, c )
                log.debug( "Cursor move to line: %s column: %s" % ( l, c ) )
                self.__display.move( ord( self.__params[ 0 ] ) - 0x20, ord( self.__params[ 0 ] ) - 0x20 )
                self.__params = []
                self.__state = 0
            elif self.__state == 29:
                if iCh == 0x33:         # Change this line to double-height top half
                    pass
                elif iCh == 0x34:       # Change this line to double-height bottom half
                    pass
                elif iCh == 0x35:       # Change this line to single-width single-height
                    pass
                elif iCh == 0x36:       # Change this line to double-width single-height
                    pass
                else:
                    log.debug( "unknown command %i in state 29" % ( iCh ) )
                # end if
                self.__state = 0
            elif self.__state == 2700:  # State CSI  "ESC["
                if cCh in "0123456789":
                    self.__lastLine += cCh
                    continue
                elif cCh == '?':
                    self.__state = 2710
                    continue
                elif cCh == ';':
                    self.__params.append( self.__lastLine )
                    self.__lastLine = ''
                    continue
                elif cCh == 'm':
                    if self.__lastLine != '':
                        self.__params.append( self.__lastLine )
                    # end if
                    self._DoAttrs()
                    self.__lastLine = ''
                elif cCh == 'H':
                    if self.__lastLine != '':
                        self.__params.append( self.__lastLine )
                    # end if
                    log.debug( "state 2700: params: %s" % ( repr( self.__params ) ) )
                    if len( self.__params ) == 2:
                        l = int( self.__params[ 0 ] ) - 1
                        c = int( self.__params[ 1 ] ) - 1
                        self.__display.move( l, c )
                        log.debug( "Cursor move to line: %s column: %s" % ( l, c ) )
                    else:
                        self.__display.move( 0, 0 )
                    # end if
                    self.__params = []
                elif cCh == 'K':   # Erase from cursor to end of line
                    if self.__lastLine != '':
                        self.__params.append( self.__lastLine )
                    # end if
                    if len( self.__params ) > 0:
                        if self.__params[ 0 ] == '1':
                            # self.__display.EraseToBOL()
                            log.debug( "Erase from cursor to beginning of line" )
                        elif self.__params[ 0 ] == '2':
                            log.debug( "Erase line under cursor" )
                            self.__display.deleteln()
                        # end if
                    else:
                        log.debug( "Erase from cursor to end of line" )
                        self.__display.clrtoeol()
                    # end if
                elif cCh == 'J':   # Erase from cursor to end of screen
                    if self.__lastLine != '':
                        self.__params.append( self.__lastLine )
                    # end if
                    if len( self.__params ) > 0:
                        if self.__params[ 0 ] == '1':
                            # self.__display.EraseFromBOA()
                            log.debug( "Erase from cursor to beginning of screen" )
                            pass
                        elif self.__params[ 0 ] == '2':
                            self.__display.clear()
                            log.debug( "Erase screen" )
                        # end if
                    else:
                        self.__display.clrtobot()
                        log.debug( "Erase from cursor to end of screen" )
                    # end if
                elif cCh == ';':
                    self.__params.append( cCh )
                    self.__state = 2701
                else:
                    log.debug( "unknown command %i %c in state 2700" % ( iCh, cCh ) )
                    self.__state    = 0
                    continue
                # end if
                self.__state = 0
            elif self.__state == 2710:
                if cCh in "0123456789":
                    self.__lastLine += cCh
                    continue
                # Text cursor enable	On          ESC [?25h	Off       ESC [?25l
                elif cCh == 'l':    # DISABLE
                    log.debug( "command l: params: %s" % ( self.__lastLine ) )
                    if self.__lastLine == "25":
                        # Text cursor enable	Off         ESC [?25l
                        curses.curs_set( 0 )
                        pass
                    elif self.__lastLine == "12": # blinking cursor (att610)
                        curses.curs_set( 2 )
                    # end if
                elif cCh == 'h':    # ENABLE
                    log.debug( "command h: params: %s" % ( self.__lastLine ) )
                    if self.__lastLine == "25":
                        # Text cursor enable	On          ESC [?25h
                        curses.curs_set( 1 )
                else:
                    log.debug( "unknown command %i %c in state 2710" % ( iCh, cCh ) )
                    self.__state    = 0
                self.__lastLine
                self.__state    = 0
            elif self.__state == 2701:
                if cCh in "0123456789":
                    self.__lastLine += cCh
                    continue
                elif iCh == 0x65:   # Cursor UP
                    for x in range( ord( self.__params[ 0 ] ) ):
                        self.__display.do_command( curses.KEY_UP )
                    # end if
                elif iCh == 0x66:   # Cursor DOWN
                    for x in range( ord( self.__params[ 0 ] ) ):
                        self.__display.do_command( curses.KEY_DOWN )
                    # end if
                elif iCh == 0x67:   # Cursor RIGHT
                    for x in range( ord( self.__params[ 0 ] ) ):
                        self.__display.do_command( curses.KEY_RIGHT )
                    # end if
                elif iCh == 0x68:   # Cursor LEFT
                    for x in range( ord( self.__params[ 0 ] ) ):
                        self.__display.do_command( curses.KEY_LEFT )
                    # end if
                elif cCh == 'H':    # Cursor direct addressing
                    self.__display.move( int( self.__params[ 0 ] ), int( self.__params[ 1 ] ) )
                elif cCh == ';':   # Cursor direct addressing / Set attributes
                    self.__params.append( cCh )
                    self.__state    = 2703
                else:
                    log.debug( "unknown command %i %c in state 2701" % ( iCh, cCh ) )
                    self.__state    = 0
                # end if
            elif self.__state == 2703:
                self.__params.append( cCh )
                self.__state = 2704
            elif self.__state == 2704:
                if cCh == 'H' or cCh == 'f':   # Direct Cursor Addressing
                    self.__display.move( int( self.__params[ 0 ] ), int( self.__params[ 1 ] ) )
                elif cCh == 'm':   # Attributes
                    self._DoAttrs()
                elif cCh == 'p': # Programmeble LEDs
                    for attr in self.__params:
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
                elif cCh == 'r':     # Scrolling region
                    pass
                elif cCh == ';':
                    self.__params.append( cCh )
                    self.__state    = 2703
                    continue
                else:
                    log.debug( "unknown command %i in state 2704" % ( iCh ) )
                # end if
                self.__state    = 0
            elif self.__state == 30:        # Character set G0
                if cCh == 'A':              # UK
                    log.debug( "Character set G0 - UK" )
                elif cCh == 'B':            # US ASCII
                    log.debug( "Character set G0 - US ASCII" )
                elif cCh == '0':            # Special graphics characters and line drawing set
                    log.debug( "Character set G0 - Special graphics characters and line drawing set" )
                elif cCh == '1':            # Alternate character ROM
                    log.debug( "Character set G0 - Alternate character ROM" )
                elif cCh == '2':            # Alternate character ROM special graphics characters
                    log.debug( "Character set G0 - Alternate character ROM special graphics characters" )
                else:
                    log.debug( "unknown command %i in state 30" % ( iCh ) )
                # end if
                self.__state    = 0
            elif self.__state == 31:        # Character set G1
                if cCh == 'A':              # UK
                    log.debug( "Character set G1 - UK" )
                elif cCh == 'B':            # US ASCII
                    log.debug( "Character set G1 - US ASCII" )
                elif cCh == '0':            # Special graphics characters and line drawing set
                    log.debug( "Character set G1 - Special graphics characters and line drawing set" )
                elif cCh == '1':            # Alternate character ROM
                    log.debug( "Character set G1 - Alternate character ROM" )
                elif cCh == '2':            # Alternate character ROM special graphics characters
                    log.debug( "Character set G1 - Alternate character ROM special graphics characters" )
                else:
                    log.debug( "unknown command %i in state 31" % ( iCh ) )
                # end if
                self.__state    = 0
            # end if
        # next
        self.__display.refresh()
        return
    # end def

    def HandleKeyboard( self ):
        return CursesDisplay.HandleKeyboard( self )
    # end def

    def Transmit( self, key ):
        CursesDisplay.Transmit( self, key )
        if key == curses.KEY_UP:
            pass
        elif key == curses.KEY_DOWN:
            pass
        elif key == curses.KEY_LEFT:
            pass
        elif key == curses.KEY_RIGHT:
            pass
        elif key == curses.KEY_BACKSPACE:
            pass
        elif key == curses.KEY_BTAB:
            pass
        # end if
        return
    # end def
# end class
