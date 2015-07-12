"""
    Telnet library for Python - terminal type implementation.

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

class TelnetOptionTerminalType( TelnetOption ):
    """
        RFC 1091, Telnet terminal-type option
    """
    def __init__( self ):
        TelnetOption.__init__( self )
        return
    # end def

# end class
