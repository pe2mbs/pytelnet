class MappedKeyListener( object ):
    def KeyMappedKey( self, s ):
        return
    # end def

    def KeyCommand( self, c ):
        return
    # end def

    def KeyGetPage( self ):
        return 0
    # end def

    def KeyGetCursorX( self ):
        return 0
    # end def

    def KeyGetCursorY( self ):
        return
    # end def

    def KeyGetStartFieldASCII( self, sb ):
        return
    # end def
# end class

class TerminalEmulation( object ):
    def __init__( self, telnet, display = None, keys = None ):
        return
    # end def

    def __del__( self ):
        return
    # end def

    def OnTelnetRecv( self, data ):
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
