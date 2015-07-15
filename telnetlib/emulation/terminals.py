from telnetlib.emulation.vt6530 import VT6530
from telnetlib.emulation        import TerminalEmulation

TERMINAL_OBJECTS = { 'vt6530': VT6530, 'vt100': None }

def getTerminalObject( terminal, telnet, display = None, keys = None ):

    try:
        return TERMINAL_OBJECTS[ terminal ]( telnet = telnet, display = display, keys = keys )
    except:
        pass
    # end try
    return TerminalEmulation( telnet, display = display, keys = keys )
# end if
