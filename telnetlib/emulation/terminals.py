import logging
import traceback
from telnetlib.emulation.vt6530 import VT6530
from telnetlib.emulation.vt100  import VT100
from telnetlib.emulation        import TerminalEmulation

TERMINAL_OBJECTS = { 'vt6530': VT6530, 'vt100': VT100 }

def getTerminalObject( terminal, telnet, display = None, keys = None ):
    try:
        obj = TERMINAL_OBJECTS[ terminal ]
        return obj( telnet = telnet, display = display, keys = keys )
    except Exception, exc:
        logging.getLogger().error( "Could not locate emulator for %s => %s" % ( terminal, repr( exc ) ) )
        logging.getLogger().exception( 'Exception' )
        try:
            return VT100( telnet = telnet, display = display, keys = keys )
        except Exception, exc:
            logging.getLogger().error( "Could not create VT100 default emulator => %s" % ( repr( exc ) ) )
            logging.getLogger().exception( 'Exception' )
        # end try
    # end try
    return TerminalEmulation( telnet, display = display, keys = keys )
# end if
