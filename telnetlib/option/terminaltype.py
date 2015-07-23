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
from telnetlib.option import *

ALLOWED_TERMINAL_TYPES = [ "ADDS-CONSUL-980",
                           "ADDS-REGENT-100",
                           "ADDS-REGENT-20",
                           "ADDS-REGENT-200",
                           "ADDS-REGENT-25",
                           "ADDS-REGENT-40",
                           "ADDS-REGENT-60",
                           "AMPEX-DIALOGUE-80",
                           "ANDERSON-JACOBSON-630",
                           "ANDERSON-JACOBSON-832",
                           "ANDERSON-JACOBSON-841",
                           "ANN-ARBOR-AMBASSADOR",
                           "ARDS",
                           "BITGRAPH",
                           "BUSSIPLEXER",
                           "CALCOMP-565",
                           "CDC-456",
                           "CDI-1030",
                           "CDI-1203",
                           "CLNZ",
                           "COMPUCOLOR-II",
                           "CONCEPT-100",
                           "CONCEPT-104",
                           "CONCEPT-108",
                           "DATA-100",
                           "DATA-GENERAL-6053",
                           "DATAGRAPHIX-132A",
                           "DATAMEDIA-1520",
                           "DATAMEDIA-1521",
                           "DATAMEDIA-2500",
                           "DATAMEDIA-3025",
                           "DATAMEDIA-3025A",
                           "DATAMEDIA-3045",
                           "DATAMEDIA-3045A",
                           "DATAMEDIA-DT80/1",
                           "DATAPOINT-2200",
                           "DATAPOINT-3000",
                           "DATAPOINT-3300",
                           "DATAPOINT-3360",
                           "DEC-DECWRITER-I",
                           "DEC-DECWRITER-II",
                           "DEC-GT40",
                           "DEC-GT40A",
                           "DEC-GT42",
                           "DEC-LA120",
                           "DEC-LA30",
                           "DEC-LA36",
                           "DEC-LA38",
                           "DEC-VT05",
                           "DEC-VT100",
                           "DEC-VT132",
                           "DEC-VT50",
                           "DEC-VT50H",
                           "DEC-VT52",
                           "DELTA-DATA-5000",
                           "DELTA-TELTERM-2",
                           "DIABLO-1620",
                           "DIABLO-1640",
                           "DIGILOG-333",
                           "DTC-300S",
                           "EDT-1200",
                           "EXECUPORT-4000",
                           "EXECUPORT-4080",
                           "GENERAL-TERMINAL-100A",
                           "GSI",
                           "HAZELTINE-1500",
                           "HAZELTINE-1510",
                           "HAZELTINE-1520",
                           "HAZELTINE-2000",
                           "HP-2621",
                           "HP-2621A",
                           "HP-2621P",
                           "HP-2626",
                           "HP-2626A",
                           "HP-2626P",
                           "HP-2640",
                           "HP-2640A",
                           "HP-2640B",
                           "HP-2645",
                           "HP-2645A",
                           "HP-2648",
                           "HP-2648A",
                           "HP-2649",
                           "HP-2649A",
                           "IBM-3101",
                           "IBM-3101-10",
                           "IBM-3275-2",
                           "IBM-3276-2",
                           "IBM-3276-3",
                           "IBM-3276-4",
                           "IBM-3277-2",
                           "IBM-3278-2",
                           "IBM-3278-3",
                           "IBM-3278-4",
                           "IBM-3278-5",
                           "IBM-3279-2",
                           "IBM-3279-3",
                           "IMLAC",
                           "INFOTON-100",
                           "INFOTONKAS",
                           "ISC-8001",
                           "LSI-ADM-3",
                           "LSI-ADM-31",
                           "LSI-ADM-3A",
                           "LSI-ADM-42",
                           "MEMOREX-1240",
                           "MICROBEE",
                           "MICROTERM-ACT-IV",
                           "MICROTERM-ACT-V",
                           "MICROTERM-MIME-1",
                           "MICROTERM-MIME-2",
                           "NETRONICS",
                           "NETWORK-VIRTUAL-TERMINAL",
                           "OMRON-8025AG",
                           "PERKIN-ELMER-1100",
                           "PERKIN-ELMER-1200",
                           "PERQ",
                           "PLASMA-PANEL",
                           "QUME-SPRINT-5",
                           "SOROC",
                           "SOROC-120",
                           "SOUTHWEST-TECHNICAL-PRODUCTS-CT82",
                           "SUPERBEE",
                           "SUPERBEE-III-M",
                           "TEC",
                           "TEKTRONIX-4010",
                           "TEKTRONIX-4012",
                           "TEKTRONIX-4013",
                           "TEKTRONIX-4014",
                           "TEKTRONIX-4023",
                           "TEKTRONIX-4024",
                           "TEKTRONIX-4025",
                           "TEKTRONIX-4027",
                           "TELERAY-1061",
                           "TELERAY-3700",
                           "TELERAY-3800",
                           "TELETEC-DATASCREEN",
                           "TELETERM-1030",
                           "TELETYPE-33",
                           "TELETYPE-35",
                           "TELETYPE-37",
                           "TELETYPE-38",
                           "TELETYPE-43",
                           "TELEVIDEO-912",
                           "TELEVIDEO-920",
                           "TELEVIDEO-920B",
                           "TELEVIDEO-920C",
                           "TELEVIDEO-950",
                           "TERMINET-1200",
                           "TERMINET-300",
                           "TI-700",
                           "TI-733",
                           "TI-735",
                           "TI-743",
                           "TI-745",
                           "TYCOM",
                           "UNIVAC-DCT-500",
                           "VIDEO-SYSTEMS-1200",
                           "VIDEO-SYSTEMS-5000",
                           "VISUAL-200",
                           "XEROX-1720",
                           "ZENITH-H19",
                           "ZENTEC-30" ]

class TelnetOptionTerminalType( TelnetOption ):

    """
        RFC 1091, Telnet terminal-type option
    """
    def __init__( self, terminal_name = 'DEC-VT100' ):
        TelnetOption.__init__( self )
        if ALLOWED_TERMINAL_TYPES.index( terminal_name ) == -1:
            trm = terminal_name.upper()
            for trmtype in ALLOWED_TERMINAL_TYPES:
                if trm in trmtype:
                    self.__terminal = terminal_name
                    return
                # end if
            # next
            self.__terminal = None
        else:
            self.__terminal = terminal_name
        return
    # end def

    def Do( self, telnet ):
        self.log.debug( "IAC DO TTYPE" )
        if self.__terminal is None:
            self.log.debug( "IAC DONT TTYPE" )
            telnet._sock.sendall( IAC + DONT + TTYPE )
        else:
            self.log.debug( "IAC WILL TTYPE" )
            telnet._sock.sendall( IAC + WILL + TTYPE )
        # end if
        return
    # end def
    """
        Server: IAC SB TERMINAL-TYPE SEND IAC SE

        Client: IAC SB TERMINAL-TYPE IS <terminal-string> IAC SE
    """
    def Execute( self, telnet, sbdataq ):
        self.log.debug( "enter TelnetOptionTerminalType.Execute()" )
        self.log.info( "sbdataq = [%s]" % ( sbdataq.encode( 'hex' ) ) )
        if sbdataq[ 0 ] == TTYPE:
            if sbdataq[ 1 ] == OPTION_SEND:
                self.log.debug( "IAC SB TTYPE IS %s IAC SB" % ( self.__terminal ) )
                telnet.write( IAC + SB + TTYPE + OPTION_IS + self.__terminal + IAC + SB )
            # end if
        # end if
        self.log.debug( "leave TelnetOptionTerminalType.Execute()" )
        return
    # end def

    def getTerminal( self ):
        return self.__terminal
    # end def

    def setTerminal( self, terminal ):
        self.log.info( "Set TERMINAL = %s" % ( terminal ) )
        self.__terminal     = terminal
        return
    # end def

    Terminal = property( getTerminal, setTerminal )

# end class
