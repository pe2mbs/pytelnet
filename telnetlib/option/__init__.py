"""
    Telnet library for Python

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

from telnetlib import IAC, SB, SE
import logging

class TelnetOption:
    def __init__( self ):
        self.log = logging.getLogger()
        return
    # end def

    def Do( self, telnet, sock ):
        return
    # end def

    def Dont( self, telnet, sock ):
        return
    # end def

    def Will( self, telnet, sock ):
        return
    # end def

    def Wont( self, telnet, sock ):
        return
    # end def

    def Execute( self, telnet, sock, sbdataq ):
        return
    # end def

    def _SendIacSbSe( self, sock, block ):
        sock.sendall( IAC + SB + block + IAC + SE )
        return
    # end def
# end class