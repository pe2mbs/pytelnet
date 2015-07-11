#!/usr/bin/python

# imported modules
import sys
import socket
import logging
import getopt
import traceback
import telnetlib

VERSION = "0.1.0"

log = logging.getLogger()

def usage():
    print( """pyTelnet.py, version %s, 2015 Copyright by Marc Bertens.

Usage: pyTelnet [-d] ... [host [port]]

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
    log.setLevel( logging.DEBUG )
    if verboselevel> 0:
        ch = logging.StreamHandler()
        ch.setLevel( verboselevel )
        formatter = logging.Formatter('%(levelname)s::%(message)s')
        ch.setFormatter( formatter )
        log.addHandler( ch )
    # end if
    if debuglevel > 0:
        ch = logging.FileHandler( './telnet.log' )
        ch.setLevel( debuglevel )
        formatter = logging.Formatter('%(asctime)s - %(module)s:%(lineno)d - %(levelname)s - %(message)s')
        ch.setFormatter( formatter )
        log.addHandler( ch )
    # end if
    tn = telnetlib.Telnet()
    #tn = SslTelnet()
    tn.SetDebugLevel( debuglevel )
    tn.SetVerboseLevel( debuglevel )
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
