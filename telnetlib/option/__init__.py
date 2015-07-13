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

from telnetlib import *
import logging

OPTION_DICT = { BINARY:             "8-bit data path",
                ECHO:               "echo",
                RCP:                "prepare to reconnect",
                SGA:                "suppress go ahead",
                NAMS:               "approximate message size",
                STATUS:             "give status",
                TM:                 "timing mark",
                RCTE:               "remote controlled transmission and echo",
                NAOL:               "negotiate about output line width",
                NAOP:               "negotiate about output page size",
                NAOCRD:             "negotiate about CR disposition",
                NAOHTS:             "negotiate about horizontal tabstops",
                NAOHTD:             "negotiate about horizontal tab disposition",
                NAOFFD:             "negotiate about formfeed disposition",
                NAOVTS:             "negotiate about vertical tab stops",
                NAOVTD:             "negotiate about vertical tab disposition",
                NAOLFD:             "negotiate about output LF disposition",
                XASCII:             "extended ascii character set",
                LOGOUT:             "force logout",
                BM:                 "byte macro",
                DET:                "data entry terminal",
                SUPDUP:             "supdup protocol",
                SUPDUPOUTPUT:       "supdup output",
                SNDLOC:             "send location",
                TTYPE:              "terminal type",
                EOR:                "end or record",
                TUID:               "TACACS user identification",
                OUTMRK:             "output marking",
                TTYLOC:             "terminal location number",
                VT3270REGIME:       "3270 regime",
                X3PAD:              "X.3 PAD",
                NAWS:               "window size",
                TSPEED:             "terminal speed",
                LFLOW:              "remote flow control",
                LINEMODE:           "Linemode option",
                XDISPLOC:           "X Display Location",
                OLD_ENVIRON:        "Old - Environment variables",
                AUTHENTICATION:     "Authenticate",
                ENCRYPT:            "Encryption option",
                NEW_ENVIRON:        "New - Environment variables",
                # the following ones come from
                # http://www.iana.org/assignments/telnet-options
                # Unfortunately, that document does not assign identifiers
                # to all of them, so we are making them up
                TN3270E:            "TN3270E",
                XAUTH:              "XAUTH",
                CHARSET:            "CHARSET",
                RSP:                "Telnet Remote Serial Port",
                COM_PORT_OPTION:    "Com Port Control Option",
                SUPPRESS_LOCAL_ECHO:"Telnet Suppress Local Echo",
                TLS:                "Telnet Start TLS",
                KERMIT:             "KERMIT",
                SEND_URL:           "SEND-URL",
                FORWARD_X:          "FORWARD_X",
                PRAGMA_LOGON:       "TELOPT PRAGMA LOGON",
                SSPI_LOGON:         "TELOPT SSPI LOGON",
                PRAGMA_HEARTBEAT:   "TELOPT PRAGMA HEARTBEAT",
                EXOPL:              "Extended-Options-List" }

def Option2String( val ):
    try:
        return OPTION_DICT[ val ]
    except Exception, exc:
        logging.getLogger().error( "Option didn't exists: %s" % ( repr( exc ) ) )
        pass
    # end if
    return "Option_0x%02X" % ( ord( val ) )

def IAC_Option( val ):
    # log.debug( "IAC_Option: %i - %X - %c" % ( ord( val ), ord( val ), val ) )
    try:
        return "%s(0x%02X)" % ( OPTION_DICT[ val ], ord( val ) )
    except Exception, exc:
        logging.getLogger().error( "Option didn't exists: %s" % ( repr( exc ) ) )
    # end if
    return "%d (0x%02X)" % ( ord( val ), ord( val ) )
# end def

class TelnetOption:
    def __init__( self ):
        self.log = logging.getLogger()
        return
    # end def

    def Do( self, telnet ):
        return
    # end def

    def Dont( self, telnet ):
        return
    # end def

    def Will( self, telnet ):
        return
    # end def

    def Wont( self, telnet ):
        return
    # end def

    def Execute( self, telnet, sbdataq ):
        return
    # end def

    def _SendIacSbSe( self, sock, block ):
        sock.sendall( IAC + SB + block + IAC + SE )
        return
    # end def
# end class