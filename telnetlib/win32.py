import sys
import threading
import logging

class Win32stdioThread( threading.Thread ):
    """
        Helper class for win32_interact() -- this thread handles the stdin handling.
    """
    def __init__( self, telnet ):
        self.telnet     = telnet
        threading.Thread.__init__( self, target=self.run )
        return
    # end def

    def run( self ):
        while 1:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                # end if
                logging.getLogger().info( "write text in mt_interact" )
                # Need LF to CR LF translation
                if self.telnet.TranslateLF2CRLF:
                    line = line.replace( '\n', '\r\n' )
                # end if
                self.telnet.write( line )
            except:
                break
            # end try
        # end while
        self.telnet.quit()
        return
    # end def

    def quit( self ):
        self._Thread__stop()
        return
    # end def
# end class

class Win32readHostThread( threading.Thread ):
    """
        Helper class for win32_interact() -- this thread handles the host handling.
    """
    def __init__( self, telnet ):
        self.telnet     = telnet
        threading.Thread.__init__( self, target = self.run )
        return
    # end def

    def run( self ):
        while 1:
            try:
                data = self.telnet.read_eager()
            except EOFError:
                print '*** Connection closed by remote host ***'
                logging.getLogger().info( '*** Connection closed by remote host ***' )
                break
            # end try
            if data:
                sys.stdout.write( data )
            else:
                sys.stdout.flush()
            # end if
        # end while
        self.telnet.quit()
        return
    # end def

    def quit( self ):
        self._Thread__stop()
        return
    # end def
# end class
