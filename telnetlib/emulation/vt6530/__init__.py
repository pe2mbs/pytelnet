import telnetlib.emulation
from telnetlib.emulation.vt6530.page  import Page
from telnetlib.emulation.vt6530.keys  import *
from telnetlib.emulation.vt6530.textDisplay import TextDisplay
import logging

CHAR_ESC    = 27
CHAR_BELL   = 7
CHAR_BKSPACE= 8
CHAR_HTAB   = 9
CHAR_LF     = 10
CHAR_CR     = 13

SIZE_ELEM   = 100

log = logging.getLogger()

class VT6530( telnetlib.emulation.TerminalEmulation, telnetlib.emulation.MappedKeyListener ):
    def __init__( self, telnet, display = None, keys = None ):
        telnetlib.emulation.TerminalEmulation.__init__( self, telnet, display, keys )
        self.__strStack     = []
        # accumulate characters for sending to the display
        self.__accum        = ''
        self.__keyBuffer    = ''
        self.__blockBuf     = ''

        # the keyboard handler
        self.__keys         = keys

        # the socket IO and telnet line protocol handler
        self.__telnet       = telnet

        """
            the abstract display.  characters are stored here,
            but doesn't actually render the text on-screen
        """
        self.__display      = display

        # The command interpreter is a state machine -- this is the state
        self.__state        = 0
        # from Vt6530
        self.__listeners    = []
        return
    # end def

    def OnTelnetConnect( self ):
        return
    # end def

    def OnTelnetError( self, message ):
        return
    # end def

    def OnTelnetUnmappedOption( self, command, option ):
        return
    # end def

    def TelnetGetTeminalName( self ):
        return "tn6530-8"
    # end def

    def OnTelnetSetWindowSize( self, iMinx, iMaxx, iMiny, iMaxy ):
        return
    # end def

    def OnTelnetTermName( self, termname ):
        return
    # end def

    def OnTelnetStateChange( self, command, option ):
        return
    # end def

    def KeyMappedKey( self, key ):
        return
    # end def

    def KeyCommand( self, c ):
        return
    # end def

    def FakeKeys( self, keystrokes ):
        return
    # end def

    def AddOnText( self, text, iCommand, bIgnoreCase ):
        return
    # end def

    def DispatchTextWatch( self, text = None, iCommand = None ):
        return
    # end def

    def DispatchConnect( self ):
        return
    # end def

    def DispatchDisconnect( self ):
        return
    # end def

    def DispatchDisplayChanged( self ):
        return
    # end def

    def DispatchError( self, text ):
        return
    # end def

    def DispatchDebug( self, text ):
        return
    # end def

    def Close( self ):
        return
    # end def

    """
    *  Process incoming text from the host.
    """
    def OnTelnetRecv( self, inp ):
        pos = 0
        dataTypeTableCount = 0
        while pos < len( inp ):
            cCh = inp[ pos ]
            iCh = ord( cCh )
            pos += 1
            if self.__state == 0:
                if iCh > 31:
                    self.__accum += chr( ch )
                    continue
                # end if
                if len( self.__accum ) > 0:
                    if self.__display.GetProtectMode():
                        self.__display.WriteBuffer( self.__accum )
                    # end if
                else:
                    self.__display.WriteDisplay( self.__accum )
                    self.__accum = ''
                # end if
                if iCh == 0x00:
                    pass
                elif iCh == 0x01:
                    # SOH
                    self.__state = 5000
                elif iCh == 0x04:
                    # reset the line
                    self.__display.ResetMdt()
                    self.DispatchResetLine()
                elif iCh == 0x05:
                    # ENQ
                    self.DispatchEnquire()
                elif iCh == 0x07:
                    # BELL
                    self.__display.Bell()
                elif iCh == 0x08:
                    # Backspace
                    self.__display.Backspace()
                elif iCh == 0x09:
                    # HTab
                    self.__display.Tab()
                elif iCh == 0x0A:
                    # NL
                    self.__display.Linefeed()
                elif iCh == 0x0D:
                    # CR
                    self.__display.CarageReturn()
                elif iCh == 0x0E:
                    # shift out to G1 character set
                    log.info("G1 char set")
                elif iCh == 0x0F:
                    # Shift in to G0 character set
                    log.info("G0 char set")
                elif iCh == 0x13:
                    # set cursor address
                    self.__state = 42
                elif iCh == 0x1B:
                    # ESC
                    self.__state = 1
                elif iCh == 0x11:
                    # set buffer address (block mode)
                    self.__state = 56
                elif iCh == 0x1D:
                    # start field
                    self.__state = 59
                else:
                    log.error( "Unknown command char %d" % ( ch ) )
                # end if
                continue
            elif self.__state == 1:
                # ESC
                if cCh == '0':
                    # print screen
                    self.__state = 0
                    self.__display.PrintScreen()
                elif cCh == '1':
                    # Set tab at cursor location
                    self.__state = 0
                    self.__display.SetTab()
                elif cCh == '2':
                    # Clear tab
                    self.__display.ClearTab()
                    self.__state = 0
                elif cCh == '3':
                    # Clear all tabs
                    self.__display.ClearAllTabs()
                    self.__state = 0
                elif cCh == '6':
                    # Set video attributes
                    self.__state = 44
                elif cCh == '7':
                    # Set video prior condition register
                    self.__state = 46
                elif iCh == 0x00:
                    # Display page
                    self.__state = 48
                elif cCh == '?':
                    # Read terminal configuration
                    if self.__display.GetBlockMode():
                        bp = "\1!A 2B72C 0D 0E 0F 0G 0H15I 3J 0L 0M 1N 0O 0P 0X 6S 0T 0U 1V 1W 1e 1f 0i 1h10\3\0"
                    else:
                        bp = "\1!A 2B72C 0D 0E 0F 0G 0H15I 3J 0L 0M 1N 0O 0P 0X 6S 0T 0U 1V 1W 1e 1f 0i 1h10\13"
                    # end if
                    self.__telnet.SendRaw( bp )
                    self.__state = 0
                elif cCh == '@':
                    # Delay one second
                    self.__state = 0
                elif cCh == 'A':
                    # Cursor up
                    self.__display.MoveCursorUp()
                    self.__state = 0
                elif cCh == 'C':
                    # Cursor right
                    self.__display.MoveCursorRight()
                    self.__state = 0
                elif cCh == 'F':
                    # Cursor home down
                    self.__display.End()
                    self.__state = 0
                elif cCh == 'H':
                    # Cursor home
                    self.__display.Home()
                    self.__state = 0
                elif cCh == 'I':
                    # Clear memory to spaces
                    # NOTE: in protect mode, this gets a block arg
                    if self.__display.GetProtectMode():
                        self.__state = 15000
                        continue
                    # end if
                    self.__display.ClearPage()
                    self.__state = 0
                elif cCh == 'J':
                    # Erase to end of page/memory
                    self.__display.ClearToEnd()
                    self.__state = 0
                elif cCh == 'K':
                    # Erase to end of line/field
                    self.__display.ClearEOL()
                    self.__state = 0
                elif cCh == '^':
                    # Read terminal status
                    if self.__display.GetBlockMode():
                        status = ( 1, 63, 66, 70, 67, 67, 94, 64, 3, 0, 4 )
                    else:
                        status = ( 1, 63, 67, 70, 67, 13 ) #67, 94, 64, 3, 0 )
                    # end if
                    self.__telnet.SendRaw( status )
                    self.__state = 0
                elif cCh == '_':
                    # Read firmware revision level
                    if self.__display.GetBlockMode():
                        log.info( "Read firmware revision level" )
                    else:
                        status = ( 1, 35, 67, 48, 48, 84, 79, 67, 48, 48, 13 )
                        self.__telnet.SendRaw( status )
                    # end if
                    self.__state = 0
                elif cCh == 'a':
                    # Read cursor address
                    cursorPos = ( 1, '_', '!', self.__display.GetCursorRow(), self.__display.GetCursorCol(), 13 )
                    self.__telnet.SendRaw( cursorPos )
                    self.__state = 0
                elif cCh == 'b':
                    # Unlock keyboard
                    self.__keys.UnlockKeyboard()
                    self.__display.SetKeysUnlocked()
                    self.__state = 10000
                elif cCh == 'c':
                    # Lock keyboard
                    self.__keys.LockKeyboard()
                    self.__display.SetKeysLocked()
                    self.__state = 0
                elif cCh == 'd':
                    # Simulate function key
                    self.__keys.LockKeyboard()
                    self.__state = 50
                elif cCh == 'f':
                    # Disconnect modem
                    log.info("Disconnect modem")
                    self.__state = 0
                elif cCh == 'o':
                    # Write to message field
                    self.__state = 52
                elif cCh == 'v':
                    # set terminal configuration
                    self.__state = 54
                elif cCh == 'x':
                    #Set IO device configuration
                    log.info("Set IO device configuration")
                    self.__state = 0
                elif cCh == 'y':
                    # Read IO device configuration
                    log.info("Read IO device configuration")
                    self.__state = 0
                elif cCh == '{':
                    # Write to file or device driver
                    log.info("Write to file or device driver")
                    self.__state = 0
                elif cCh == '}':
                    # Write/read to file or device driver
                    log.info("Write/read to file or device driver")
                    self.__state = 0
                elif cCh == '-':
                    # extended CSI sequence
                    self.__state = 3
                elif cCh == ':':
                    # select page
                    self.__state = 66
                elif cCh == '<':
                    # read buffer
                    #if (ASSERT.debug > 0)
                    #	display.dumpScreen(Logger.out)
                    self.__blockBuf = ''
                    self.__blockBuf = self.__display.ReadBufferUnprotectIgnoreMdt( self.__blockBuf, 0, 0, self.__display.GetNumRows() - 1, self.__display.GetNumColumns() - 1 )
                    self.__telnet.SendRaw( self.__blockBuf )
                    self.__blockBuf = ''
                    self.__state    = 0
                elif cCh == '=':
                    # Read with address
                    self.__state = 67
                elif cCh == '>':
                    # Reset modified data tags
                    self.__display.ResetMdt()
                    self.__state = 0
                elif cCh == 'L':
                    self.__display.LineDown()
                    self.__state = 0
                elif cCh == 'M':
                    self.__display.DeleteLine()
                    self.__state = 0
                elif cCh == 'N':
                    # disable local line editing until
                    # 1. ESC q
                    # 2. Exit block mode
                    # 3. protect to nonprotect submode
                    log.info("Disable local line editing")
                    self.__state = 0
                elif cCh == 'O':
                    # insert char
                    self.__display.InsertChar()
                    self.__state = 0
                elif cCh == 'P':
                    # delete char
                    self.__display.DeleteChar()
                    self.__state = 0
                elif cCh == 'S':
                    # roll up
                    log.info("Roll up")
                    self.__state = 0
                elif cCh == 'T':
                    # roll down
                    self.__state = 0
                    self.__display.LineDown()
                elif cCh == 'U':
                    # page down
                    log.info("Page down")
                    self.__state = 0
                elif cCh == 'V':
                    # page up
                    log.info("Page up")
                    self.__state = 0
                elif cCh == 'W':
                    #  Enter protect mode
                    self.__display.SetProtectMode()
                    self.__keys.SetProtectMode()
                    self.__state = 0
                elif cCh == 'X':
                    # exit protect mode
                    self.__display.ExitProtectMode()
                    self.__keys.ExitProtectMode()
                    self.__state = 0
                elif cCh == '[':
                    # start field extended
                    self.__state = 71
                elif cCh == ']':
                    # Read with address all
                    if self.__display.GetProtectMode():
                        # same as ESC =
                        self.__state = 67
                        continue
                    # end if
                    self.__state = 75
                elif cCh == 'i':
                    # back tab
                    self.__display.Backtab()
                    self.__state = 0
                elif cCh == 'p':
                    # set max page num
                    self.__state = 81
                elif cCh == 'q':
                    # reinitialize
                    self.__display.Init()
                    self.__display.SetProtectMode()
                    self.__display.ExitProtectMode()
                    self.__state = 10000
                elif cCh == 'r':
                    # Define data type table
                    self.__state = 84
                elif cCh == 'u':
                    # define enter key function
                    self.__state = 82
                else:
                    log.info( "Unknown ESC %d" % ( iCh ) )
                    self.__state = 0
                # end if
                continue
            elif self.__state == 3:
                if cCh in "0123456789":
                    self.__state = 24
                    self.__accum += cCh
                    continue
                # end if
                if cCh == 'c':
                    self.__strStack.append( "7" )
                    self.__state = 30
                elif cCh == 'e':
                    # Get machine name 3-28
                    name = ( 1, '&', 'j', 'o', 'h', 'n', 13 )
                    self.__telnet.SendRaw( name )
                    self.__state = 0
                elif cCh == 'V':
                    self.__state = 39
                elif cCh == 'W':
                    # Report Exec code 3-34
                    code = ( 1, '?', (1<<6) | 1, 'F', 'D', 13 )
                    # self.__telnet.SendRaw( name )
                    self.__state = 0
                elif cCh == 'J':
                    self.__blockBuf = ''
                    self.__blockBuf = self.__display.ReadBufferUnprotect( self.__blockBuf, 0, 0, self.__display.GetNumRows()-1, self.__display.GetNumColumns()-1)
                    self.__telnet.SendRaw( self.__blockBuf )
                    self.__state = 0
                else:
                    log.info( "Unknown ESC - %d" % ( iCh ) )
                # end if
            elif self.__state == 39:
                if iCh == CHAR_CR:
                    # Execute local program
                    log.info( "Execute local program %s" % ( self.__accum ) )
                    self.__accum = ''
                    self.__state = 0
                    continue
                # end if
                self.__accum += cCh
            elif self.__state == 24:
                if cCh in "0123456789":
                    self.__accum += cCh
                    self.__state = 25
                    continue
                # end if
                if cCh == '':
                    self.__strStack.append( self.__accum )
                    self.__accum = ''
                    self.__state = 34
                elif cCh == 'd':
                    # Read string configuration param
                    log.info( "Read string config param %s" % ( self.__accum ) )
                    self.__accum = ''
                    self.__state = 0
                elif cCh == 'c':
                    self.__state = 30
                else:
                    log.info( "Unknown ESC-%s %d" % ( self.__accum, iCh ) )
                # end if
            elif self.__state == 34:
                if cCh in "0123456789":
                    self.__accum += cCh
                    continue
                # end if
                if iCh != 0x00:
                    log.info("Expected '' in state 34 Got %d" % ( iCh ) )
                # end if
                self.__strStack.append( self.__accum )
                self.__accum = ''
                self.__state = 35
            elif self.__state == 35:
                if cCh in "0123456789":
                    self.__accum += cCh
                    continue
                # end if
                if cCh == 'C':
                    # set buffer address extended
                    self.__display.SetBufferRowCol( int( self.__strStack[ 0 ] ), int( self.__accum ) )
                    self.__strStack = []
                    self.__accum = ''
                    self.__state = 0

                elif cCh == 'q':
                    self.__strStack.append( self.__accum )
                    self.__strStack.append( "q" )
                    self.__accum = ''
                    self.__state = 36

                elif cCh == 'I':
                    # Clear memory to spaces extended
                    sr = int( self.__strStack[ 0 ][ 0 ] )
                    sc = int( self.__strStack[ 0 ][ 1 ] )
                    er = int( self.__accum[ 0 ] )
                    ec = int( self.__accum[ 1 ] )
                    self.__accum = ''
                    self.__strStack = []
                    self.__display.ClearBlock( sr, sc, er, ec )
                    self.__state = 0

                elif iCh == 0x00:
                    self.__strStack.append( self.__accum )
                    self.__state = 64
                else:
                    log.info("Unexpected char in 35: %d" % ( iCh ) )
                # end if
            elif self.__state == 36:
                if cCh in "0123456789ABCDEF":
                    self.__strStack.append( cCh )
                    self.__state = 37
                    continue
                # end if
                self.__strStack.append( self.__accum )
                self.__accum = ''
                p1 = self.__strStack[ 0 ]
                if p1[ 0 ] == '0':
                    # reset color map
                    log.info( "Reset color map" )
                else:
                    log.info("Set color map")
                    p2 = int( self.__strStack[ 1 ] )
                    p3 = int( self.__strStack[ 2 ] )
                    if self.__strStack[ 3 ][ 0 ] != 'q':
                        log.info( "State 36 Error" )
                    # end if
                    for x in range( 0, p3-p2 ):
                        # setColorMap( p2 + x, Integer.parseInt( (String)strStack[ x*2+4 ], 16),
                        #                       Integer.parseInt((String)strStack[ x*2+5 ], 16) )
                        log.info("SetColorMap(%d, %s, %s)" % ( p2 + x, self.__strStack[ x*2+4 ], self.__strStack[ x*2+5 ] ) )
                    # next
                # end if
                self.__strStack = []
            elif self.__state == 37:
                if cCh in "0123456789ABCDEF":
                    self.__strStack.append( cCh )
                    self.__state = 36
                    continue
                # end if
                log.info( "Bad hex in state 37: %d" % ( iCh ) )
            elif self.__state == 30:
                if iCh > 31:
                    self.__accum += cCh
                    continue
                # end if
                if iCh == 0x12:
                    self.__strStack.append( self.__accum )
                    self.__accum = ''
                    continue
                # end if
                if iCh != CHAR_CR:
                    log.info("Expected CR in 30 Got %d" % ( iCh ) )
                # end if
                self.__accum = ''
                # count = int( self.__strStack[ 0 ] )
                for x in self.__strStack:
                    log.info( "Parameter recived: %s" % ( x ) )
                # next
                self.__strStack = []
            elif self.__state == 25:
                if cCh in "0123456789":
                    self.__accum += cCh
                    continue
                # end if
                if iCh == ';':
                    self.__strStack.append( self.__accum )
                    self.__accum = ''
                    self.__state = 27
                    continue
                # end if
                log.info("Unexpected char in 25: %d" % ( iCh ) )
            elif self.__state == 27:
                if cCh in "0123456789":
                    self.__accum += cCh
                    continue
                # end if
                if cCh == 'D':
                    # set cursor position
                    self.__display.SetCursorRowCol( ord( self.__strStack[ 0 ][ 0 ] ) - 32,
                                                    ord( self.__strStack[ 1 ][ 0 ] ) - 32 )
                elif cCh == 'O':
                    # write to AUX
                    log.info("Write to AUX")
                else:
                    log.info( "Unexpcted char in 27: %d" % ( ch ) )
                # end if
            elif self.__state == 42:
                self.__strStack.append( cCh )
                self.__state = 43
            elif self.__state == 43:
                self.__display.SetCursorRowCol( ord( self.__strStack[ 0 ][ 0 ] ) - 0x20, iCh - 0x20 )
                self.__strStack = []
                self.__state = 0
            elif self.__state == 44:
                self.__display.SetWriteAttribute( iCh & ~( 1 << 5 ) )
                self.__state = 0
            elif self.__state == 46:
                self.__display.SetPriorWriteAttribute( iCh & ~( 1 << 5 ) )
                self.__state = 0
            elif self.__state == 48:
                self.__display.SetDisplayPage( iCh - 0x20 )
                self.__state = 0
            elif self.__state == 50:
                fnKey = ( 1, ch, self.__display.GetCursorRow(), self.__display.GetCursorCol(), 13 )
                self.__telnet.SendRaw( fnKey )
                self.__state = 0
            elif self.__state == 52:
                if iCh == 13:
                    self.__display.WriteMessage( self.__accum )
                    self.__accum = ''
                    self.__state = 0
                    continue
                # end if
                self.__accum += cCh
            elif self.__state == 54:
                if iCh == 13:
                    if self.__accum[ 0 ] == 'A':
                        # cursor type
                        pass
                    elif self.__accum[ 0 ] == 'F':
                        # language
                        pass
                    elif self.__accum[ 0 ] == 'G':
                        # mode
                        pass
                    elif self.__accum[ 0 ] == 'M':
                        # enter key mode
                        if self.__accum[1] == '0':
                            self.__keys.SetEnterKeyOff()
                        else:
                            self.__keys.SetEnterKeyOn()
                        # end if
                    elif self.__accum[ 0 ] == 'T':
                        # normal intensity
                        pass
                    elif self.__accum[ 0 ] == 'V':
                        # character size
                        pass
                    else:
                        log.info("State 54: %s" % ( self.__accum ) )
                    # end if
                    self.__accum = ''
                    self.__state = 0
                    continue
                # end if
                self.__accum += cCh
            elif self.__state == 56:
                self.__strStack.append( cCh )
                self.__state = 57
            elif self.__state == 57:
                self.__display.SetBufferRowCol( ord( self.__strStack[ 0 ][0] ) - 0x20, iCh - 0x20)
                self.__strStack = []
                self.__state = 0
            elif self.__state == 59:
                self.__strStack.append( cCh )
                self.__state = 60

            elif self.__state == 60:
                self.__display.StartField( ord( self.__strStack[ 0 ][ 0 ] ) - 0x20, iCh - 0x20 )
                self.__strStack = []
                self.__state = 0

            elif self.__state == 64:
                if cCh in "0123456789":
                    self.__accum += cCh
                    continue
                # end if
                if cCh in [ 'J', 'K' ]:
                    sr = int( self.__strStack[ 0 ] )
                    sc = int( self.__strStack[ 1 ] )
                    er = int( self.__strStack[ 2 ] )
                    ec = int( self.__accum )
                    self.__strStack = []
                    self.__accum = ''
                    self.__blockBuf = self.__display.ReadBufferAllIgnoreMdt( '', sr, sc, er, ec )
                    self.__telnet.SendRaw( self.__blockBuf )
                    self.__blockBuf = ''
                else:
                    log.info("Unexpected char in 64: %d" % ( iCh ) )
                # end if
            elif self.__state == 66:
                self.__display.SetPage( iCh - 0x20 )
                self.__state = 0
            elif self.__state == 67:
                if len( self.__strStack ) == 3:
                    sr = ord( self.__strStack[ 0 ][ 0 ] ) - 0x20
                    sc = ord( self.__strStack[ 1 ][ 0 ] ) - 0x20
                    er = ord( self.__strStack[ 2 ][ 0 ] ) - 0x20
                    ec = iCh - 0x20
                    self.__blockBuf = self.__display.ReadBufferAllMdt( '', sr, sc, er, ec )
                    self.__telnet.SendRaw( self.__blockBuf )
                    self.__blockBuf = ''
                    self.__strStack = []
                    self.__state = 0
                    continue
                # end if
                self.__strStack.append( cCh )
            elif self.__state == 71:
                self.__strStack.append( cCh )
                self.__state = 72
            elif self.__state == 72:
                self.__strStack.append( cCh )
                self.__state = 73
            elif self.__state == 73:
                vidAttr     = ord( self.__strStack[ 0 ][ 0 ] ) - 0x20
                dataAttr    = ord( self.__strStack[ 1 ][ 0 ] ) - 0x20
                self.__display.StartField( vidAttr, dataAttr, iCh - 0x20 )
                self.__strStack = []
                self.__state = 0
            elif self.__state == 75:
                self.__strStack.append( cCh )
                self.__state = 76
            elif self.__state == 76:
                self.__strStack.append( cCh )
                self.__state = 77
            elif self.__state == 77:
                if cCh != ';':
                    log.info("Expected  in 77: %d" % ( iCh ) )
                # end if
                self.__state = 78
            elif self.__state == 78:
                self.__strStack.append( cCh )
                self.__state = 79
            elif self.__state == 79:
                sr = ord( self.__strStack[ 0 ][ 0 ] ) - 0x20
                sc = ord( self.__strStack[ 1 ][ 0 ] ) - 0x20
                er = ord( self.__strStack[ 2 ][ 0 ] ) - 0x20
                ec = iCh - 0x20
                self.__blockBuf = self.__display.ReadFieldsAll( '', sr, sc, er, ec )
                self.__telnet.SendRaw( self.__blockBuf )
                m_blockBuf = ''
                self.__strStack = []
                self.__state = 0
            elif self.__state == 81:
                self.__display.SetPageCount( chr( iCh - 0x30 ) )
                self.__state = 10000
            elif self.__state == 82:
                self.__strStack.append( chr( iCh - 0x20 ) )
                self.__state = 83
            elif self.__state == 83:
                self.__accum += cCh
                ch = ord( self.__strStack[ 0 ][ 0 ] ) - 1
                self.__strStack = []
                if ch == 0:
                    #keys.setMap(13, 0, accum)
                    log.info( "keys.setMap(13, 0, accum)" )
                    self.__accum = ''
                    self.__state = 0
                else:
                    self.__strStack.append( chr( ch ) )
                # end if
            elif self.__state == 84:
                # datatype table add ch
                dataTypeTableCount += 1
                if dataTypeTableCount == 96:
                    # set data type table
                    self.__state = 0
                    log.info("Set data type table")
                # end if
            elif self.__state == 10000:
                if iCh == 4:
                    self.__state = 0
                    continue
                # end if
                if iCh != 13:
                    log.info( "Guardian Expected 13 in 10000: %d" % ( iCh ) )
                # end if
                self.__state = 10001
            elif self.__state == 10001:
                if iCh == 4:
                    self.__state = 0
                    continue
                # end if
                if iCh != 13:
                    log.info( "Guardian Expected 13 in 10001: %d" % ( iCh ) )
                # end if
                self.__state = 0
            elif self.__state == 5000:
                if cCh == 'A':
                    # ANSI terminal mode
                    #telnet.setBufferingOff()
                    log.info( "ANSI MODE" )
                elif cCh == 'B':
                    # BLOCK mode
                    self.__display.SetModeBlock()
                    self.__keys.SetKeySet( KEYS_BLOCK )
                    #telnet.setBufferingOn()
                    log.info( "BLOCK MODE" )
                elif cCh == 'C':
                    # Conversational mode
                    self.__display.SetModeConv()
                    self.__keys.SetKeySet( KEYS_CONV )
                    #telnet.setBufferingOff()
                    log.info( "CONVERSATIONAL MODE" )
                elif cCh == '!':
                    # send term config?
                    self.__state = 5050
                    log.info( "send term config?" )
                else:
                    log.info("Unexpected char in 5000: %d" % ( iCh ) )
                # end if
                self.__state = 5001
            elif self.__state == 5001:
                if iCh != 3:
                    log.info("Expected 3 in 5000: %d" % ( iCh ) )
                # end if
                self.__state = 0
            elif self.__state == 5050:
                # accept chars until 3
                if iCh != 3:
                    log.info( "Send term config? %s" % ( self.__accum ) )
                    self.__accum = ''
                    self.__state = 0
                    continue
                # end if
                self.__accum += cCh
            elif self.__state == 15000:
                # ESC I (Clear Block)
                if len( self.__strStack ) == 3:
                    self.__display.ClearBlock( ord( self.__strStack[ 0 ][ 0 ] ) - 0x20,
                                               ord( self.__strStack[ 1 ][ 0 ] ) - 0x20,
                                               ord( self.__strStack[ 2 ][ 0 ] ) - 0x20, iCh - 0x20 )
                    self.__strStack = []
                    self.__state = 0
                    continue
                # end if
                self.__strStack.append( cCh )
            else:
                log.info( "Unknown state %d" % ( self.__state ) )
            # end if
        # end while
        if len( self.__accum ) > 0:
            if self.__display.GetProtectMode():
                self.__display.WriteBuffer( self.__accum )
            else:
                self.__display.WriteDisplay( self.__accum )
            # end if
            self.__accum = ''
        # end if
        return
    # end def

    def BeforeTransmit( self, buffer ):
        return buffer.replace( '\n', '\r\n' )
    # end def

    """
    *  Process text in local edit mode.
    """
    def ExecLocalCommand( self, cmd ):
        self.__display.WriteLocal( cmd )
        if  not self.__display.GetBlockMode():
            if cmd == chr( 13 ) or cmd == chr( 10 ):
                self.__display.WriteLocal( '\10' )
                self.__keyBuffer += chr( 13 )
                self.__telnet.SendRaw( self.__keyBuffer )
                self.__keyBuffer = ''
            elif cmd == '\b' and len( self.__keyBuffer ) > 0:
                self.__keyBuffer = self.__keyBuffer[ : len( self.__keyBuffer ) - 1 ]
            else:
                self.__keyBuffer += cmd
            # end if
        # end if
        self.__display.SetRePaint( True )
        return
    # end def

    def IsConvMode( self ):
        return not self.__display.IsBlockMode()
    # end def

    def DispatchResetLine( self ):
        for listener in self.__listeners:
            listener.Vt6530_OnResetLine()
        # next
        return
    # end def

    """
    *  The host has completed transmision and is
    *  now waiting for input.  This can be used
    *  to buffer keystrokes until the screen is
    *  fully m_displayed.
    """
    def DispatchEnquire( self ):
        for listener in self.__listeners:
            listener.Vt6530_OnEnquire()
        # next
        return
    # end def
# end class
