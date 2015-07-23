import logging

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
        self.__log = logging.getLogger()
        return
    # end def

    def __del__( self ):
        return
    # end def

    def OnRecveive( self, data ):
        return
    # end def

    """
    *  The terminal has successfully connected to the host.
    """
    def OnConnect( self ):
        return
    # end def

    """
    *  The connection to the host was lost or closed.
    """
    def OnClose( self ):
        return
    # end def

    """
    *  There has been an internal error.
    """
    def OnError( self, message ):
        self.__log.error( message )
        return
    # end def

    def OnUnmappedOption( self, command, option ):
        return
    # end if

    def OnSetWindowSize( self, minx, maxx, miny, maxy ):
        return
    # end if

    def GetWindowSize( self ):
        return ( 24, 80 )
    # end if

    def OnTermName( self, termname ):
        return
    # end if

    def GetTeminalName( self ):
        return
    # end if

    def OnStateChange( self, command, option ):
        return
    # end if

    def OnResetLine( self ):
        return
    # end if

    """
    *  The host has completed rendering the screen and is now waiting for input.
    """
    def OnEnquire( self ):
        return
    # end if

    """
    *  Changes in the display require the container to repaint.
    """
    def OnDisplayChanged( self ):
        return
    # end if

    """
    *  Debuging output -- may be ignored
    """
    def OnDebug( self, message ):
        self.__log.debug( message )
        return
    # end if

    def OnRecv34( self, op, params, paramLen = 0 ):
        return
    # end if

    def OnTextWatch( self, txt, iCommandCode ):
        return
    # end if

    def BeforeTransmit( self, buffer ):
        return buffer
    # end def
# end class
