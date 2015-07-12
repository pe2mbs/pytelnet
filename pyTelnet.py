#!/usr/bin/python
"""
    Telnet program for Python

    Copyright (C) 2015  Marc Bertens-Nguyen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    This library is based on idea of Abhilash Meesala <abhilash929@gmail.com>
    his basic implementation is heavily extended to make a complete library.

"""
# imported modules
import sys
import socket
import logging
import getopt
import traceback
import telnetlib.client

VERSION = "0.1.0"

log = logging.getLogger()

def usage():
    print( """pyTelnet.py, version %s, 2015 Copyright by Marc Bertens.

Usage: pyTelnet [ options ] ... [host [port]]

    Options:

    -d/--debug <level>      Set debug level for the application, DEBUG, INFO, WARN, ERROR, CRITICAL.
    -v/--verbose            Set verbose mode.
    -u/--user <username>    Set user name.
    -p/--pass <passwd>      Set password for user.
    -t/--timeout <real>     Set timeout value, default is 0.5 second
    -h/--help               Shows this help page.

Default host is localhost; default port is 23.

    """ % ( VERSION ) )
    return

def TelnetConsole():
    """

    Usage: python pyTelnet.py [-d] ... [host [port]]

    Default host is localhost; default port is 23.

    """
    debuglevel      = 0
    verboselevel    = 0
    try:
        opts, myargs = getopt.getopt( sys.argv[1:], 'd:vu:p:i:t:h',
                                    ['debug=', 'verbose', 'user=', 'pass=', 'terminal=', 'timeout=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    # end try
    port        = 23
    timeout     = 0.5
    username    = None
    password    = None
    terminal    = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-v', '--verbose'):
            verboselevel = logging.INFO
        elif opt in ('-d', '--debug'):
            try:
                debuglevel = int( arg )
            except:
                try:
                    levels = [ "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL" ]
                    debuglevel = levels.index( arg.upper() ) * 10
                except:
                    print( "Invalid --debug value" )
                    usage()
                    sys.exit( 3 )
                # end try
            # end try
        elif opt in ('-u', '--user'):
            username = arg
        elif opt in ('-p', '--pass'):
            password = arg
        elif opt in ('-i', '--terminal'):
            terminal = arg
        elif opt in ('-t', '--timeout'):
            try:
                timeout = float( arg )
            except:
                print( "-t/--timeout must be a real number, using default timeout value." )
                timeout = 0.5
            # end try
        else:
            usage()
            sys.exit( 2 )
        # end if
    # next
    while len( myargs ) > 0 and myargs[ 0 ][ 0 ] == '-':
        del myargs[ 0 ]
    # end if
    if len( myargs ) < 1:
        host = 'localhost'
    else:
        host = myargs[ 0 ]
        if len( myargs ) < 2:
            port = 23
        else:
            try:
                port = int( myargs[ 1 ] )
            except ValueError:
                port = socket.getservbyname( myargs[ 1 ], 'tcp' )
            # end if
        # end if
    # end if
    log.setLevel( logging.CRITICAL )
    if verboselevel> 0:
        ch = logging.StreamHandler()
        ch.setLevel( verboselevel )
        formatter = logging.Formatter('%(levelname)s::%(message)s')
        ch.setFormatter( formatter )
        log.addHandler( ch )
    # end if
    ch = logging.FileHandler( './telnet.log' )
    ch.setLevel( debuglevel )
    formatter = logging.Formatter('%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s')
    ch.setFormatter( formatter )
    log.addHandler( ch )
    if debuglevel > 0:
        log.setLevel( debuglevel )
    # end if
    tn = telnetlib.client.Telnet()
    if username is not None:
        tn.SetUser( username, password )
    # end if
    if terminal is not None:
        tn.SetTerminal( terminal )
    # end if
    try:
        tn.open( host, port, timeout = timeout )
    except Exception, exc:
        print( "Could not connect to %s:%i - %s" % ( host, port, exc ) )
        sys.exit( -1 )
    # end def
    try:
        tn.interact()
    except KeyboardInterrupt, exc:
        pass
    except Exception, exc:
        log.error( exc )
        log.error( traceback.format_exc() )
    # end try
    tn.close()
    return
# end def

if __name__ == '__main__':
    TelnetConsole()
# end if
