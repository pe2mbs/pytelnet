import telnetlib.emulation

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


class VT52( telnetlib.emulation.TerminalEmulation, telnetlib.emulation.MappedKeyListener ):
    def __init__( self, telnet, display = None, keys = None ):
        self.__state = 0
        self.__params = []
        self.__display = display
        self.__telnet   = telnet
        return
    # end def

    def __del__( self ):
        return
    # end def

    def OnTelnetRecv( self, data ):
        for cCh in data:
            iCh = ord( cCh )
            if self.__state == 0:
                if iCh == 27:
                    self.__state = 27
                elif iCh == 7:
                    self.__display.Bell()
                elif iCh == 8:
                    self.__display.Backspace()
                elif iCh == 9:
                    self.__display.Tab()
                elif iCh == 10:
                    self.__display.Linefeed()
                elif iCh == 13:
                    self.__display.CarrageReturn()
                else:
                    self.__display.EchoDisplay( cCh )
                # end if
            elif self.__state == 27:
                if iCh == 0x37:         # Save cursor and attributes
                    self.__display.SaveCursorAttributes()
                elif iCh == 0x38:       # Restore cursor and attributes
                    self.__display.RestoreCursorAttributes()
                elif iCh == chr( 'A' ):     # Cursor UP
                    self.__display.CursorUp( 1 )
                elif iCh == chr( 'B' ):     # Cursor DOWN
                    self.__display.CursorDown( 1 )
                elif iCh == chr( 'C' ):     # Cursor RIGHT
                    self.__display.CursorRight( 1 )
                elif iCh == chr( 'D' ):     # Cursor LEFT
                    self.__display.CursorLeft( 1 )
                elif iCh == chr( 'F' ):     # Select Special Graphics character set
                    pass
                elif iCh == chr( 'G' ):     # Select ASCII character set
                    pass
                elif iCh == chr( 'H' ):     # Cursor Home
                    self.__display.Home( 0, 0 )
                elif iCh == chr( 'I' ):     # Reverse line feed
                    pass
                elif iCh == chr( 'J' ):     # Erase to end of screen
                    self.__display.ClearEnd()
                elif iCh == chr( 'K' ):     # Erase to end of line
                    self.__display.ClearEOL()
                elif iCh == chr( '=' ):     # Enter alternate keypad mode
                    pass
                elif iCh == chr( '>' ):     # Exit alternate keypad mode
                    pass
                elif iCh == chr( '1' ):     # Graphics processor on
                    pass
                elif iCh == chr( '2' ):     # Graphics processor off
                    pass
                elif iCh == chr( '<' ):     # Enter ANSI mode
                    pass
                elif iCh == chr( 'Z' ):     # Identify
                    id = ( 27, '/', 'K' )
                    self.__telnet.SendRaw( id )
                elif iCh == chr( 'Y' ):     # Direct Cursor Address
                    self.__state = 28
                elif iCh == chr( 'D' ):   # Index
                    pass
                elif iCh == chr( 'M' ):   # Reverse Index
                    pass
                elif iCh == chr( '[' ):
                    self.__state = 2700
                elif iCh == chr( '#' ):
                    self.__state = 29
                elif iCh == chr( '(' ):     # Character set G0
                    self.__state = 30
                elif iCh == chr( ')' ):     # Character set G1
                    self.__state = 31
                # end if
                self.__state = 0
            elif self.__state == 28:
                self.__params.append( cCh )
                self.__state = 29
            elif self.__state == 29:
                self.__params.append( cCh )
                self.__display.SetCursorRowCol( ord( self.__params[ 0 ] ) - 0x20, ord( self.__params[ 0 ] ) - 0x20 )
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
            elif self.__state == 2700:
                if cCh == 'K':   # Erase from cursor to end of line
                    if len( self.__params[] ) > 0:
                        if self.__params[ 0 ] == '1':
                            self.__display.EraseToBOL()
                        elif self.__params[ 0 ] == '2':
                            self.__display.DeleteLine()
                        # end if
                    else:
                        self.__display.ClearEOL()
                    # end if
                elif cCh == 'J':   # Erase from cursor to end of screen
                    if len( self.__params[] ) > 0:
                        if self.__params[ 0 ] == '1':
                            self.__display.EraseFromBOA()
                        elif self.__params[ 0 ] == '2':
                            self.__display.ClearPage()
                        # end if
                    else:
                        self.__display.ClearEnd()
                    # end if
                elif cCh in [ '1', '2' ]:   # Erase from cursor to end of line
                    self.__params.append( cCh )
                    continue
                else:
                    self.__params.append( cCh )
                    self.__state = 2701
                    continue
                # end if
                self.__state = 0
            elif self.__state == 2701:
                if iCh == 0x65:   # Cursor UP
                    self.__display.CursorUp( ord( self.__params[ 0 ] ) )
                    pass
                elif iCh == 0x66:   # Cursor DOWN
                    self.__display.CursorDown( ord( self.__params[ 0 ] ) )
                    pass
                elif iCh == 0x67:   # Cursor RIGHT
                    self.__display.CursorRight( ord( self.__params[ 0 ] ) )
                    pass
                elif iCh == 0x68:   # Cursor LEFT
                    self.__display.CursorLeft( ord( self.__params[ 0 ] ) )
                    pass
                elif iCh == chr( ';' ):   # Cursor direct addressing / Set attributes
                    self.__params.append( cCh )
                    self.__state    = 2703
                else:
                    self.__state    = 0
                # end if
            elif self.__state == 2703:
                self.__params.append( cCh )
                self.__state = 2704
            elif self.__state == 2704:
                if iCh == chr( 'H' ) or iCh == chr( 'f' ):   # Direct Cursor Addressing
                    self.__display.SetCursor( int( self.__params[ 0 ] ), int( self.__params[ 1 ] ) )
                elif iCh == chr( 'm' ):   # Attributes
                    for attr in self.__params:
                        """
                            0   All attributes off
                            1   Bold on
                            4   Underscore on
                            5   Blink on
                            7   Reverse video
                        """
                        self.__display.SetAttribute( ord( attr ) - 0x30 )
                    # next
                elif iCh == chr( 'p' ): # Programmeble LEDs
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
                elif iCh == chr( 'r' ):     # Scrolling region

                elif iCh == chr( ';' ):
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

    def OnTelnetConnect( self ):
        return
    # end def

    def OnTelnetClose( self ):
        return
    # end def

    def OnTelnetError( self, message ):
        return
    # end def

    def OnTelnetUnmappedOption( self, command, option ):
        return
    # end if

    def OnTelnetSetWindowSize( self, minx, maxx, miny, maxy ):
        return
    # end if

    def TelnetGetWindowSize( self ):
        return ( 24, 80 )
    # end if

    def OnTelnetTermName( self, termname ):
        return
    # end if

    def TelnetGetTeminalName( self ):
        return
    # end if

    def OnTelnetStateChange( self, command, option ):
        return
    # end if

    """
    *  The terminal has successfully connected to the host.
    """
    def Vt6530_OnConnect( self ):
        return
    # end if

    """
    *  The connection to the host was lost or closed.
    """
    def Vt6530_OnDisconnect( self ):
        return
    # end if

    def Vt6530_OnResetLine( self ):
        return
    # end if

    """
    *  The host has completed rendering the screen and is now waiting for input.
    """
    def Vt6530_OnEnquire( self ):
        return
    # end if

    """
    *  Changes in the display require the container to repaint.
    """
    def Vt6530_OnDisplayChanged( self ):
        return
    # end if

    """
    *  There has been an internal error.
    """
    def Vt6530_OnError( self, message ):
        return
    # end if

    """
    *  Debuging output -- may be ignored
    """
    def Vt6530_OnDebug( self, message ):
        return
    # end if

    def Vt6530_OnRecv34( self, op, params, paramLen = 0 ):
        return
    # end if

    def Vt6530_OnTextWatch( self, txt, iCommandCode ):
        return
    # end if

    def BeforeTransmit( self, buffer ):
        return buffer
    # end def
# end class

class VT100( VT52 ):
    pass
# end class