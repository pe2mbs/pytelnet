import telnetlib.emulation

class VT220( telnetlib.emulation.TerminalEmulation ):
    def __init__( self ):
        telnetlib.emulation.TerminalEmulation.__init__( self )
        self.__statusRow    = ''
        self.__currentMode  = 0
        self.__m_display    = None
        self.__m_keys       = None
        return
    # end def

    def OnReceive( self, buffer ):
        return buffer
    # end def

    def BeforeTransmit( self, buffer ):
        return buffer
    # end def
# end class