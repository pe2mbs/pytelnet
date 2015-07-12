"""
    Telnet library for Python - local eho implementation.

    Copyright (C) 2015  Marc Bertens-Nguyen

    This library is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    This library is based on idea of Abhilash Meesala <abhilash929@gmail.com>
    his basic implementation is heavily extended to make a complete library.

"""

from telnetlib import *
from telnetlib.option import TelnetOption

class TelnetOptionLocalEcho( TelnetOption ):
    """
        RFC 857, TELNET echo option
    """
    def __init__( self ):
        TelnetOption.__init__( self )
        self.__echo = True
        return
    # end def

    @property
    def Echo( self ):
        return self.__echo

    def Do( self, telnet, sock ):
        """
            IAC DO ECHO

            The sender of this command REQUESTS that the receiver of this
            command begin echoing, or confirms that the receiver of this
            command is expected to echo, data characters it receives over the
            TELNET connection back to the sender.

            :param telnet:
            :param sock:
            :return:
        """
        self.log.debug( "IAC DO ECHO" )
        sock.sendall( IAC + DO + ECHO )
        return
    # end def

    def Dont( self, telnet, sock ):
        """
            IAC DON'T ECHO

            The sender of this command DEMANDS the receiver of this command
            stop, or not start, echoing data characters it receives over the
            TELNET connection.

            :param telnet:
            :param sock:
            :return:
        """
        self.log.debug( "IAC DONT ECHO" )
        sock.sendall( IAC + DONT + ECHO )
        return
    # end def

    def Will( self, telnet, sock ):
        """
            IAC WILL ECHO

            The sender of this command REQUESTS to begin, or confirms that it
            will now begin, echoing data characters it receives over the
            TELNET connection back to the sender of the data characters.

            :param telnet:
            :param sock:
            :return:
        """
        self.log.debug( "IAC WILL ECHO" )
        sock.sendall( IAC + WILL + ECHO )
        return
    # end def

    def Wont( self, telnet, sock ):
        """
            IAC WON'T ECHO

            The sender of this command DEMANDS to stop, or refuses to start,
            echoing the data characters it receives over the TELNET connection
            back to the sender of the data characters.

            :param telnet:
            :param sock:
            :return:
        """
        self.log.debug( "IAC WONT ECHO" )
        sock.sendall( IAC + WONT + ECHO )
        return
    # end def

    def Execute( self, telnet, sock, sbdataq ):
        self.log.debug( "enter TelnetOptionLocalEcho.Execute()" )
        self.log.info( "sbdataq = [%s]" % ( sbdataq.encode( 'hex' ) ) )
        self.log.debug( "leave TelnetOptionLocalEcho.Execute()" )
        pass
    # end def
# end class
