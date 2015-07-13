"""
    Telnet library for Python - client implementation

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

# imported modules
import errno
# import os
# import stat
import sys
import socket
import select
import logging

from telnetlib import *
from telnetlib.option.authentication import TelnetOptionAuthentication
from telnetlib.option.localecho import TelnetOptionLocalEcho
from telnetlib.option import IAC_Option
from telnetlib.win32 import Win32stdioThread, Win32readHostThread
from telnetlib.emulation.vt6530 import VT6530


__all__ = [ "Telnet" ]
"""
    RFC 137, TELNET protocol specification
    RFC 139, TELNET protocol specification
    RFC 854, TELNET protocol specification
    RFC 855, TELNET option specifications
    RFC 856, TELNET binary transmission
    RFC 858, TELNET suppress Go Ahead option
    RFC 859, TELNET status option
    RFC 860, TELNET timing mark option
    RFC 861, TELNET extended options - list option
    RFC 885, Telnet end of record option
    RFC 1041, Telnet 3270 regime option
    RFC 1073, Telnet Window Size Option
    RFC 1079, Telnet terminal speed option
    RFC 1091, Telnet terminal-type option
    RFC 1096, Telnet X display location option
    RFC 1116, Telnet Linemode Option
    RFC 1123, Requirements for Internet Hosts - Application and Support
    RFC 1143, The Q Method of Implementing TELNET Option Negotiation
    RFC 1184, Telnet linemode option
    RFC 1205, 5250 Telnet interface
    RFC 1372, Telnet remote flow control option
    RFC 1572, Telnet Environment Option
    RFC 2217, Telnet Com Port Control Option
    RFC 2941, Telnet Authentication Option
    RFC 2942, Telnet Authentication: Kerberos Version 5
    RFC 2943, TELNET Authentication Using DSA
    RFC 2944, Telnet Authentication: SRP
    RFC 2946, Telnet Data Encryption Option
    RFC 4248, The telnet URI Scheme
    RFC 4777, IBM's iSeries Telnet Enhancements
"""

log = logging.getLogger()

class Telnet( object ):

    """Telnet interface class.

    An instance of this class represents a connection to a telnet
    server.  The instance is initially not connected; the open()
    method must be used to establish a connection.  Alternatively, the
    host name and optional port number can be passed to the
    constructor, too.

    Don't try to reopen an already connected instance.

    This class has many read_*() methods.  Note that some of them
    raise EOFError when the end of the connection is read, because
    they can return an empty string for other reasons.  See the
    individual doc strings.

    read_until(expected, [timeout])
        Read until the expected string has been seen, or a timeout is
        hit (default is no timeout); may block.

    read_all()
        Read all data until EOF; may block.

    read_some()
        Read at least one byte or EOF; may block.

    read_very_eager()
        Read all data available already queued or on the socket,
        without blocking.

    read_eager()
        Read either data already queued or some data available on the
        socket, without blocking.

    read_lazy()
        Read all data in the raw queue (processing it first), without
        doing any socket I/O.

    read_very_lazy()
        Reads all data in the cooked queue, without doing any socket
        I/O.

    read_sb_data()
        Reads available data between SB ... SE sequence. Don't block.

    set_option_negotiation_callback(callback)
        Each time a telnet option is read on the input flow, this callback
        (if set) is called with the following parameters :
        callback(telnet socket, command, option)
            option will be chr(0) when there is no option.
        No other action is done afterwards by telnetlib.

    """

    def __init__(self, host=None, port = 23,
                 timeout=socket._GLOBAL_DEFAULT_TIMEOUT, terminal = "vt200"):
        """Constructor.

        When called without arguments, create an unconnected instance.
        With a hostname argument, it connects the instance; port number
        and timeout are optional.
        """
        # Standard variable
        self.__host                     = host
        self.__port                     = port
        self.__timeout                  = timeout
        self._sock                      = None
        self._sslsock                   = None
        self.__rawq                     = ''
        self.__irawq                    = 0
        self.__cookedq                  = ''
        self.__eof                      = 0
        self.__iacseq                   = ''        # Buffer for IAC sequence.
        self.__sb                       = 0         # flag for SB and SE sequence.
        self.__sbdataq                  = ''
        self.__has_poll                 = hasattr( select, 'poll' )
        self.__username                 = None
        self.__password                 = None
        self.__terminal                 = None
        self.__terminalObj              = None
        self.__options                  = [ None ] * 256
        self.__options[ ord( ECHO ) ]   = TelnetOptionLocalEcho()
        self.__options[ ord( AUTHENTICATION ) ] = TelnetOptionAuthentication()
        # self.__options[ ord( TTYPE ) ] = TelnetOptionTerminalType()
        Terminal                        = terminal
        if host is not None:
            self.open( host, port, timeout )
        # end if
        return
    # end def

    def __del__( self ):
        """
            Destructor -- close the connection.
        """
        self.close()
        return
    # end def

    def setUserPassword( self, username, password ):
        self.__username           = username
        self.__password           = password
        return
    # end def

    @property
    def Username( self ):
        return self.__username
    # end def

    @Username.setter
    def Username( self, value ):
        self.__username = value
        return
    # end def

    @property
    def Password( self ):
        return self.__password
    # end def

    @Password.setter
    def Password( self, value ):
        self.__password = value
        return
    # end def

    def getTerminal( self ):
        return self.__terminal
    # end def

    def setTerminal( self, terminal ):
        log.info( "Set TERMINAL = %s" % ( terminal ) )
        self.__terminal = terminal
        if self.__terminal == 'vt6530':
            self.__terminalObj      = VT6530()
        # end if
        return
    # end def

    Terminal = property( getTerminal, setTerminal )

    def Option( self, option, Object ):
        self.__options[ option ] = Object
        return
    # end def

    def open( self, host, port = 23, timeout = socket._GLOBAL_DEFAULT_TIMEOUT ):
        """
            Connect to a host.

            The optional second argument is the port number, which
            defaults to the standard telnet port (23).

            Don't try to reopen an already connected instance.
        """
        self.setHost( host, port, timeout )
        self._sock      = socket.create_connection( ( self.__host, self.__port ), self.__timeout )
        return
    # end def

    def setHost( self, host, port, timeout ):
        self.__eof      = 0
        self.__host     = host
        self.__port     = port
        self.__timeout  = timeout
        return
    # end def

    @property
    def Host( self ):
        return self.__host
    # end def

    @property
    def Port( self ):
        return self.__port
    # end def

    def close( self ):
        """
            Close the connection.
        """
        if self._sslsock:
            self._sslsock.close()
        else:
            if self._sock and self._sock:
                self._sock.close()
            # end if
        # end if
        self._sock = 0
        self.__eof = 1
        self.__iacseq = ''
        self.__sb = 0
        return
    # end def

    def get_socket( self ):
        """
            Return the socket object used internally.
        """
        return self._sock
    # end def

    def fileno( self ):
        """
            Return the fileno() of the socket object used internally.
        """
        return self._sock.fileno()
    # end def

    def getSocket(self):
        """
            Return the socket object used internally.
        """
        return self._sock
    # end def

    def write( self, buffer ):
        """
            Write a string to the socket, doubling any IAC characters.

            Can block if the connection is blocked.  May raise
            socket.error if the connection is closed.
        """
        if self.__terminalObj is not None:
            buffer = self.__terminalObj.BeforeTransmit( buffer )
        # end if
        if IAC in buffer:
            buffer = buffer.replace( IAC, IAC + IAC )
        # end if
        log.debug( "send %r", buffer )
        self._sock.sendall( buffer )
        return
    # end def

    def read_until(self, match, timeout=None):
        """
            Read until a given string is encountered or until timeout.

            When no match is found, return whatever is available instead,
            possibly the empty string.  Raise EOFError if the connection
            is closed and no cooked data is available.
        """
        if self.__has_poll:
            return self._read_until_with_poll( match, timeout )
        # end if
        return self._read_until_with_select( match, timeout )
    # end def

    def _read_until_with_poll( self, match, timeout ):
        """
            Read until a given string is encountered or until timeout.

            This method uses select.poll() to implement the timeout.
        """
        n = len(match)
        call_timeout = timeout
        if timeout is not None:
            from time import time
            time_start = time()
        # end if
        self.process_rawq()
        i = self.__cookedq.find(match)
        if i < 0:
            poller = select.poll()
            poll_in_or_priority_flags = select.POLLIN | select.POLLPRI
            poller.register(self, poll_in_or_priority_flags)
            while i < 0 and not self.__eof:
                try:
                    ready = poller.poll(call_timeout)
                except select.error as e:
                    if e.errno == errno.EINTR:
                        if timeout is not None:
                            elapsed = time() - time_start
                            call_timeout = timeout-elapsed
                        # end if
                        continue
                    # end if
                    raise
                # end try
                for fd, mode in ready:
                    if mode & poll_in_or_priority_flags:
                        i = max(0, len(self.__cookedq)-n)
                        self.fill_rawq()
                        self.process_rawq()
                        i = self.__cookedq.find( match, i )
                    # end if
                # next
                if timeout is not None:
                    elapsed = time() - time_start
                    if elapsed >= timeout:
                        break
                    # end if
                    call_timeout = timeout-elapsed
                # end if
            # end while
            poller.unregister(self)
        # end if
        if i >= 0:
            i = i + n
            buf = self.__cookedq[:i]
            self.__cookedq = self.__cookedq[ i: ]
            return buf
        # end if
        return self.read_very_lazy()
    # end def

    def _read_until_with_select(self, match, timeout=None):
        """
            Read until a given string is encountered or until timeout.

            The timeout is implemented using select.select().
        """
        n = len(match)
        self.process_rawq()
        i = self.__cookedq.find( match )
        if i >= 0:
            i = i+n
            buf = self.__cookedq[:i]
            self.__cookedq = self.__cookedq[i:]
            return buf
        # end if
        s_reply = ([self], [], [])
        s_args = s_reply
        if timeout is not None:
            s_args = s_args + (timeout,)
            from time import time
            time_start = time()
        # end if
        while not self.__eof and select.select( *s_args ) == s_reply:
            i = max( 0, len( self.__cookedq ) - n )
            self.fill_rawq()
            self.process_rawq()
            i = self.__cookedq.find( match, i )
            if i >= 0:
                i = i + n
                buf = self.__cookedq[ : i ]
                self.__cookedq = self.__cookedq[ i : ]
                return buf
            # end if
            if timeout is not None:
                elapsed = time() - time_start
                if elapsed >= timeout:
                    break
                # end if
                s_args = s_reply + ( timeout - elapsed,)
            # end if
        # end while
        return self.read_very_lazy()

    def read_all( self ):
        """
            Read all data until EOF; block until connection closed.
        """
        self.process_rawq()
        while not self.__eof:
            self.fill_rawq()
            self.process_rawq()
        # end while
        buf = self.__cookedq
        self.__cookedq = ''
        return buf
    # end def

    def read_some( self ):
        """
            Read at least one byte of cooked data unless EOF is hit.

            Return '' if EOF is hit.  Block if no data is immediately
            available.
        """
        self.process_rawq()
        while not self.__cookedq and not self.__eof:
            self.fill_rawq()
            self.process_rawq()
        # end while
        buf = self.__cookedq
        self.__cookedq = ''
        return buf
    # end def

    def read_very_eager( self ):
        """
            Read everything that's possible without blocking in I/O (eager).

            Raise EOFError if connection closed and no cooked data
            available.  Return '' if no cooked data available otherwise.
            Don't block unless in the midst of an IAC sequence.
        """
        self.process_rawq()
        while not self.__eof and self.sock_avail():
            self.fill_rawq()
            self.process_rawq()
        # end while
        return self.read_very_lazy()
    # end def

    def read_eager( self ):
        """
            Read readily available data.

            Raise EOFError if connection closed and no cooked data
            available.  Return '' if no cooked data available otherwise.
            Don't block unless in the midst of an IAC sequence.

        """
        self.process_rawq()
        while not self.__cookedq and not self.__eof and self.sock_avail():
            self.fill_rawq()
            self.process_rawq()
        # end while
        return self.read_very_lazy()
    # end def

    def read_lazy( self ):
        """
            Process and return data that's already in the queues (lazy).

            Raise EOFError if connection closed and no data available.
            Return '' if no cooked data available otherwise.  Don't block
            unless in the midst of an IAC sequence.
        """
        self.process_rawq()
        return self.read_very_lazy()
    # end def

    def read_very_lazy( self ):
        """
            Return any data available in the cooked queue (very lazy).

            Raise EOFError if connection closed and no data available.
            Return '' if no cooked data available otherwise.  Don't block.
        """
        buf = self.__cookedq
        self.__cookedq = ''
        if not buf and self.__eof and not self.__rawq:
            raise EOFError, 'telnet connection closed'
        # end if
        """
            Here the TERMINAL implementation must be called.
        """
        if self.__terminalObj is not None:
            buf = self.__terminalObj.OnReceive( buf )
        # end if
        return buf
    # end def

    def read_sb_data( self ):
        """
            Return any data available in the SB ... SE queue.

            Return '' if no SB ... SE available. Should only be called
            after seeing a SB or SE command. When a new SB command is
            found, old unread SB data will be discarded. Don't block.
        """
        buf = self.__sbdataq
        self.__sbdataq = ''
        return buf
    # end def

    def process_rawq( self ):
        """
            Transfer from raw queue to cooked queue.

            Set self.__eof when connection is closed.  Don't block unless in
            the midst of an IAC sequence.
        """
        buf = ['', '']
        try:
            while self.__rawq:
                c = self.rawq_getchar()
                if not self.__iacseq:
                    if c == theNULL:
                        continue
                    # end if
                    if c == "\021":
                        continue
                    # end if
                    if c != IAC:
                        buf[ self.__sb ] = buf[ self.__sb ] + c
                        continue
                    else:
                        self.__iacseq += c
                    # end if
                elif len( self.__iacseq ) == 1:
                    # 'IAC: IAC CMD [OPTION only for WILL/WONT/DO/DONT]'
                    if c in ( DO, DONT, WILL, WONT ):
                        self.__iacseq += c
                        continue
                    # end if
                    self.__iacseq = ''
                    if c == IAC:
                        buf[ self.__sb ] = buf[ self.__sb ] + c
                    else:
                        optionObj   = None
                        if c == SB: # SB ... SE start.
                            self.__sb = 1
                            self.__sbdataq = ''
                        elif c == SE:
                            self.__sb = 0
                            self.__sbdataq = self.__sbdataq + buf[ 1 ]
                            buf[1] = ''
                            optionObj   = self.__options[ ord( self.__sbdataq[ 0 ] ) ]
                        # end if
                        if optionObj is not None:
                            optionObj.Execute( self, self.__sbdataq )
                        elif c == SB:
                            pass
                        else:
                            # We can't offer automatic processing of
                            # suboptions. Alas, we should not get any
                            # unless we did a WILL/DO before.
                            log.warn( 'IAC %s not recognized' % IAC_Option( c ) )
                        # end if
                    # end if
                elif len( self.__iacseq ) == 2:
                    cmd         = self.__iacseq[ 1 ]
                    self.__iacseq = ''
                    opt         = c
                    log.info( 'recv IAC %s %s', IAC_Command( cmd ), IAC_Option( opt ) )
                    optionObj   = self.__options[ ord( opt ) ]
                    log.info( "IAC option %i -> %s" % ( ord( opt ), optionObj ) )
                    if optionObj is None:
                        # Do default behaviour when the option is not supported
                        if cmd in ( WILL, WONT ):
                            log.info( 'send IAC DONT %s', IAC_Option( opt ) )
                            self._sock.sendall( IAC + DONT + opt )
                        else:
                            log.info( 'send IAC WONT %s', IAC_Option( opt ) )
                            self._sock.sendall( IAC + WONT + opt )
                        # end if
                    else:
                        if cmd == DO:
                            optionObj.Do( self )
                        elif cmd == DONT:
                            optionObj.Dont( self )
                        elif cmd == WILL:
                            optionObj.Will( self )
                        elif cmd == WONT:
                            optionObj.Wont( self )
                        # end if
                    # end if
                # end if
            # end while
        except EOFError: # raised by self.rawq_getchar()
            self.__iacseq = '' # Reset on EOF
            self.__sb = 0
            pass
        # end try
        self.__cookedq = self.__cookedq + buf[ 0 ]
        self.__sbdataq = self.__sbdataq + buf[ 1 ]
        return
    # end def

    def rawq_getchar( self ):
        """
            Get next char from raw queue.

            Block if no data is immediately available.  Raise EOFError
            when connection is closed.
        """
        if not self.__rawq:
            self.fill_rawq()
            if self.__eof:
                raise EOFError
            # end if
        # end if
        c = self.__rawq[ self.__irawq ]
        self.__irawq += 1
        if self.__irawq >= len( self.__rawq ):
            self.__rawq = ''
            self.__irawq = 0
        # end if
        return c
    # end def

    def fill_rawq( self ):
        """
            Fill raw queue from exactly one recv() system call.

            Block if no data is immediately available.  Set self.__eof when
            connection is closed.
        """
        if self.__irawq >= len( self.__rawq ):
            self.__rawq = ''
            self.__irawq = 0
        # end if
        # The buffer size should be fairly small so as to avoid quadratic
        # behavior in process_rawq() above
        buf = self._sock.recv( 50 )
        log.debug( "recv %r", buf )
        self.__eof    = (not buf)
        self.__rawq   = self.__rawq + buf
        return
    # end def

    def sock_avail( self ):
        """
            Test whether data is available on the socket.
        """
        return select.select( [ self ], [], [], 0 ) == ( [ self ], [], [] )
    # end def

    def interact( self ):
        """
            Interaction function, emulates a very dumb telnet client.
        """
        if sys.platform == "win32":
            self.win32_interact()
            return
        # end if
        self.unix_interact()
        return
    # end def

    def unix_interact( self ):
        while 1:
            rfd, wfd, xfd = select.select( [ self, sys.stdin ], [], [] )
            if self in rfd:
                try:
                    text = self.read_eager()
                except EOFError:
                    print '*** Connection closed by remote host ***'
                    log.info( '*** Connection closed by remote host ***' )
                    break
                # end try
                if text:
                    log.info( "write #1 text in interact" )
                    sys.stdout.write( text )
                    sys.stdout.flush()
                # end if
            # end if
            if sys.stdin in rfd:
                line = sys.stdin.readline()
                if not line:
                    break
                # end if
                optionObj = self.__options[ ord( ECHO ) ]
                if optionObj is not None:
                    if optionObj.Echo:
                        log.info( "write #2 text in interact" )
                        self.write( line )
                    # end if
                else:
                    log.info( "write #3 text in interact" )
                    self.write( line )
                # end if
            # end if
        # end while
        return
    # end def

    def quit( self ):
        if self.reader.is_alive():
            self.reader.quit()
        # end if
        if self.console.is_alive():
            self.console.quit()
        # end if
        return
    # end def

    def win32_interact( self ):
        """
            Win32 - Multi threaded WIN32 version of interact().
        """
        self.reader     = Win32readHostThread( self )
        self.console    = Win32stdioThread( self )
        self.reader.start()
        self.console.start()
        # Wait for all threads to complete
        self.reader.join()
        self.console.join()
        return
    # end def

    def expect( self, list, timeout = None ):
        """
            Read until one from a list of a regular expressions matches.

            The first argument is a list of regular expressions, either
            compiled (re.RegexObject instances) or uncompiled (strings).
            The optional second argument is a timeout, in seconds; default
            is no timeout.

            Return a tuple of three items: the index in the list of the
            first regular expression that matches; the match object
            returned; and the text read up till and including the match.

            If EOF is read and no text was read, raise EOFError.
            Otherwise, when nothing matches, return (-1, None, text) where
            text is the text received so far (may be the empty string if a
            timeout happened).

            If a regular expression ends with a greedy match (e.g. '.*')
            or if more than one expression can match the same input, the
            results are undeterministic, and may depend on the I/O timing.
        """
        if self.__has_poll:
            return self._expect_with_poll( list, timeout )
        # end if
        return self._expect_with_select( list, timeout )
    # end def

    def _expect_with_poll( self, expect_list, timeout = None ):
        """
            Read until one from a list of a regular expressions matches.

            This method uses select.poll() to implement the timeout.
        """
        re = None
        expect_list = expect_list[ : ]
        indices = range( len( expect_list ) )
        for i in indices:
            if not hasattr( expect_list[ i ], "search" ):
                if not re: import re
                expect_list[ i ] = re.compile( expect_list[ i ] )
            # end if
        # next
        call_timeout = timeout
        if timeout is not None:
            from time import time
            time_start = time()
        # end if
        self.process_rawq()
        m = None
        for i in indices:
            m = expect_list[ i ].search( self.__cookedq )
            if m:
                e = m.end()
                text = self.__cookedq[ : e ]
                self.__cookedq = self.__cookedq[ e : ]
                break
            # end if
        # next
        if not m:
            poller = select.poll()
            poll_in_or_priority_flags = select.POLLIN | select.POLLPRI
            poller.register( self, poll_in_or_priority_flags )
            while not m and not self.__eof:
                try:
                    ready = poller.poll( call_timeout )
                except select.error as e:
                    if e.errno == errno.EINTR:
                        if timeout is not None:
                            elapsed = time() - time_start
                            call_timeout = timeout - elapsed
                        # end if
                        continue
                    # end if
                    raise
                # end try
                for fd, mode in ready:
                    if mode & poll_in_or_priority_flags:
                        self.fill_rawq()
                        self.process_rawq()
                        for i in indices:
                            m = expect_list[ i ].search( self.__cookedq )
                            if m:
                                e = m.end()
                                text = self.__cookedq[ : e ]
                                self.__cookedq = self.__cookedq[ e : ]
                                break
                            # end if
                        # next
                    # end if
                # next
                if timeout is not None:
                    elapsed = time() - time_start
                    if elapsed >= timeout:
                        break
                    # end if
                    call_timeout = timeout - elapsed
                # end if
            # end while
            poller.unregister(self)
        # end if
        if m:
            return ( i, m, text )
        # end if
        text = self.read_very_lazy()
        if not text and self.__eof:
            raise EOFError
        # end if
        return ( -1, None, text )
    # end def

    def _expect_with_select( self, list, timeout = None ):
        """
            Read until one from a list of a regular expressions matches.

            The timeout is implemented using select.select().
        """
        re = None
        list = list[:]
        indices = range( len( list ) )
        for i in indices:
            if not hasattr( list[ i ], "search"):
                if not re: import re
                list[ i ] = re.compile( list[ i ] )
            # end if
        # next
        if timeout is not None:
            from time import time
            time_start = time()
        # end if
        while 1:
            self.process_rawq()
            for i in indices:
                m = list[ i ].search( self.__cookedq )
                if m:
                    e = m.end()
                    text = self.__cookedq[ : e ]
                    self.__cookedq = self.__cookedq[ e : ]
                    return ( i, m, text )
                # end if
            # next
            if self.__eof:
                break
            # end if
            if timeout is not None:
                elapsed = time() - time_start
                if elapsed >= timeout:
                    break
                # end if
                s_args = ( [ self.fileno() ], [], [], timeout - elapsed )
                r, w, x = select.select( *s_args )
                if not r:
                    break
                # end if
            # end if
            self.fill_rawq()
        # end while
        text = self.read_very_lazy()
        if not text and self.__eof:
            raise EOFError
        # end if
        return ( -1, None, text )
    # end def
# end class

