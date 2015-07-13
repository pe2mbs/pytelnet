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
import logging

# Telnet protocol characters (don't change)
IAC                 = chr( 255 )    # 0xFF  - Interpret As Command
DONT                = chr( 254 )    # 0xFE
DO                  = chr( 253 )    # 0xFD
WONT                = chr( 252 )    # 0xFC
WILL                = chr( 251 )    # 0xFB
theNULL             = chr( 0 )

SE                  = chr( 240 )    # 0xF0  - Subnegotiation End
NOP                 = chr( 241 )    # 0xF1  - No Operation
DM                  = chr( 242 )    # 0xF2  - Data Mark
BRK                 = chr( 243 )    # 0xF3  - Break
IP                  = chr( 244 )    # 0xF4  - Interrupt process
AO                  = chr( 245 )    # 0xF5  - Abort output
AYT                 = chr( 246 )    # 0xF6  - Are You There
EC                  = chr( 247 )    # 0xF7  - Erase Character
EL                  = chr( 248 )    # 0xF8  - Erase Line
GA                  = chr( 249 )    # 0xF9  - Go Ahead
SB                  = chr( 250 )    # 0xFA  - Subnegotiation Begin

# Telnet protocol options code (don't change)
# These ones all come from arpa/telnet.h
BINARY              = chr( 0 )      # 8-bit data path
ECHO                = chr( 1 )      # echo
RCP                 = chr( 2 )      # prepare to reconnect
SGA                 = chr( 3 )      # suppress go ahead
NAMS                = chr( 4 )      # approximate message size
STATUS              = chr( 5 )      # give status
TM                  = chr( 6 )      # timing mark
RCTE                = chr( 7 )      # remote controlled transmission and echo
NAOL                = chr( 8 )      # negotiate about output line width
NAOP                = chr( 9 )      # negotiate about output page size
NAOCRD              = chr( 10 )     # negotiate about CR disposition
NAOHTS              = chr( 11 )     # negotiate about horizontal tabstops
NAOHTD              = chr( 12 )     # negotiate about horizontal tab disposition
NAOFFD              = chr( 13 )     # negotiate about formfeed disposition
NAOVTS              = chr( 14 )     # negotiate about vertical tab stops
NAOVTD              = chr( 15 )     # negotiate about vertical tab disposition
NAOLFD              = chr( 16 )     # negotiate about output LF disposition
XASCII              = chr( 17 )     # extended ascii character set
LOGOUT              = chr( 18 )     # force logout
BM                  = chr( 19 )     # byte macro
DET                 = chr( 20 )     # data entry terminal
SUPDUP              = chr( 21 )     # supdup protocol
SUPDUPOUTPUT        = chr( 22 )     # supdup output
SNDLOC              = chr( 23 )     # send location
TTYPE               = chr( 24 )     # terminal type
EOR                 = chr( 25 )     # end or record
TUID                = chr( 26 )     # TACACS user identification
OUTMRK              = chr( 27 )     # output marking
TTYLOC              = chr( 28 )     # terminal location number
VT3270REGIME        = chr( 29 )     # 3270 regime
X3PAD               = chr( 30 )     # X.3 PAD
NAWS                = chr( 31 )     # window size
TSPEED              = chr( 32 )     # terminal speed
LFLOW               = chr( 33 )     # remote flow control
LINEMODE            = chr( 34 )     # Linemode option
XDISPLOC            = chr( 35 )     # X Display Location
OLD_ENVIRON         = chr( 36 )     # Old - Environment variables
AUTHENTICATION      = chr( 37 )     # Authenticate
ENCRYPT             = chr( 38 )     # Encryption option
NEW_ENVIRON         = chr( 39 )     # New - Environment variables
# the following ones come from
# http://www.iana.org/assignments/telnet-options
# Unfortunately, that document does not assign identifiers
# to all of them, so we are making them up
TN3270E             = chr( 40 )     # TN3270E
XAUTH               = chr( 41 )     # XAUTH
CHARSET             = chr( 42 )     # CHARSET
RSP                 = chr( 43 )     # Telnet Remote Serial Port
COM_PORT_OPTION     = chr( 44 )     # Com Port Control Option
SUPPRESS_LOCAL_ECHO = chr( 45 )     # Telnet Suppress Local Echo
TLS                 = chr( 46 )     # Telnet Start TLS
KERMIT              = chr( 47 )     # KERMIT
SEND_URL            = chr( 48 )     # SEND-URL
FORWARD_X           = chr( 49 )     # FORWARD_X
PRAGMA_LOGON        = chr( 138 )    # TELOPT PRAGMA LOGON
SSPI_LOGON          = chr( 139 )    # TELOPT SSPI LOGON
PRAGMA_HEARTBEAT    = chr( 140 )    # TELOPT PRAGMA HEARTBEAT
EXOPL               = chr( 255 )    # Extended-Options-List
NOOPT               = chr( 0 )

def IAC_Command( cmd ):
    Command = { DONT:   'DONT',
                DO:     'DO',
                WONT:   'WONT',
                WILL:   'WILL',
                SB:     'SB',
                GA:     'GA',
                EL:     'EL',
                EC:     'EC',
                AYT:    'AYT',
                AO:     'AO',
                IP:     'IP',
                BRK:    'BRK',
                DM:     'DM',
                NOP:    'NOP',
                SE:     'SE' }
    # log.debug( "IAC_Command: %i - %X - %s" % ( ord( cmd ), ord( cmd ), cmd ) )
    try:
        return "%s(0x%02X)" % ( Command[ cmd ], ord( cmd ) )
    except Exception, exc:
        logging.getLogger().error( exc )
    return "%d(0x%02X)" % ( ord( cmd ), ord( cmd ) )
# end def

class TelnetConnectionClosed( Exception ):
    pass
# end class
