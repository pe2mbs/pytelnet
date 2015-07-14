"""
*   Tandem key definitions and mappings.
"""
KEYS_ANSI       = 0
KEYS_CONV       = 1
KEYS_BLOCK      = 2

TDM_SOH         = chr( 1 )
TDM_ENQUIRY     = chr( 5 )
TDM_ACK         = chr( 6 )
TDM_BELL        = chr( 7 )
TDM_BACKSPACE   = chr( 9 )
TDM_NAK         = chr( 21 )
TDM_ESC         = chr( 27 )
TDM_CR          = chr( 13 )

SPC_F1          = 0
SPC_F2          = 1
SPC_F3          = 2
SPC_F4          = 3
SPC_F5          = 4
SPC_F6          = 5
SPC_F7          = 6
SPC_F8          = 7
SPC_F9          = 11
SPC_F10         = 12
SPC_F11         = 14
SPC_F12         = 15
SPC_BREAK       = 16
SPC_PGUP        = 17
SPC_PGDN        = 18
SPC_HOME        = 19
SPC_END         = 20
SPC_INS         = 21
SPC_DEL         = 22
SPC_SCROLLOCK   = 23
SPC_UP          = 24
SPC_DOWN        = 25
SPC_LEFT        = 26
SPC_RIGHT       = 28
SPC_PRINTSCR    = 29
LAST_SPC        = 30


class Keys( object ):
    def __init__( self ):
        self.SetKeySet( KEYS_CONV )
        self.__sendCursorWithFn = False
        self.__pressedKey   = 0
        self.__pressedWhen  = 0

        self.__plain        = []    # str
        self.__crtl         = []    # str
        self.__alt          = []    # str
        self.__shift        = []    # str
        self.__localCmd     = []    # int
        self.__localCmdCtl  = []    # int
        self.__localCmdAlt  = []    # int

        self.__ignoreKeys   = False
        self.__protectMode  = False
        self.__enterKeyOn   = True
        self.__listener     = None    # MappedKeyListener
        return
    # end def

    def __del__( self ):
        return
    # end def

    def SetProtectMode( self ):
        self.LockKeyboard()
        self.__protectMode = True
        return
    # end def

    def ExitProtectMode( self ):
        self.UnlockKeyboard()
        self.__protectMode = False
        return
    # end def

    def SetEnterKeyOn( self ):
        self.__enterKeyOn = True
        return
    # end def

    def SetEnterKeyOff( self ):
        self.__enterKeyOn = False
        return
    # end def

    def SetListener( self, MappedKeyListener_listener ):
        self.__listener = MappedKeyListener_listener
        return
    # end def

    def SetKeySet( self, iKeySet ):
        if iKeySet == KEYS_ANSI:
            self.__plain        = self.ansiChar
            self.__crtl         = self.ansiCharCtl
            self.__alt          = self.ansiCharAlt
            self.__shift        = self.ansiCharShift
            self.__localCmd     = self.ansiLocal
            self.__localCmdCtl  = self.ansiLocalCtl
            self.__localCmdAlt  = self.ansiLocalAlt
            self.__sendCursorWithFn = False
            self.__protectMode  = False
            self.__enterKeyOn   = True
        elif iKeySet == KEYS_CONV:
            self.__plain        = self.convChar
            self.__crtl         = self.convCharCtl
            self.__alt          = self.convCharAlt
            self.__shift        = self.convCharShift
            self.__localCmd     = self.convLocal
            self.__localCmdCtl  = self.convLocalCtl
            self.__localCmdAlt  = self.convLocalAlt
            self.__sendCursorWithFn = True
            self.__protectMode  = False
            self.__enterKeyOn   = True
        elif iKeySet == KEYS_BLOCK:
            self.__plain        = self.blockChar
            self.__crtl         = self.blockCharCtl
            self.__alt          = self.blockCharAlt
            self.__shift        = self.blockCharShift
            self.__localCmd     = self.blockLocal
            self.__localCmdCtl  = self.blockLocalCtl
            self.__localCmdAlt  = self.blockLocalAlt
            self.__sendCursorWithFn = True
            self.__protectMode  = False
            self.__enterKeyOn   = True
        # end if
        return
    # end def

    # def setMap( self, iCh, iModifier, out_str ):

    def KeyPressed( self, iKeycode, bShift, bCtrl, bAlt ):
        return
    # end def

    def KeyReleased( self, iKeycode, bShift, bCtrl, bAlt ):
        fn = False
        if iKeycode == SPC_F1:
            self.__pressedKey = SPC_F1
            fn = True
        elif iKeycode == SPC_F2:
            self.__pressedKey = SPC_F2
            fn = True
        elif iKeycode == SPC_F3:
            self.__pressedKey = SPC_F3
            fn = True
        elif iKeycode == SPC_F4:
            self.__pressedKey = SPC_F4
            fn = True
        elif iKeycode == SPC_F5:
            self.__pressedKey = SPC_F5
            fn = True
        elif iKeycode == SPC_F6:
            self.__pressedKey = SPC_F6
            fn = True
        elif iKeycode == SPC_F7:
            self.__pressedKey = SPC_F7
            fn = True
        elif iKeycode == SPC_F8:
            self.__pressedKey = SPC_F8
            fn = True
        elif iKeycode == SPC_F9:
            self.__pressedKey = SPC_F9
            fn = True
        elif iKeycode == SPC_F10:
            self.__pressedKey = SPC_F10
            fn = True
        elif iKeycode == SPC_F11:
            self.__pressedKey = SPC_F11
            fn = True
        elif iKeycode == SPC_F12:
            self.__pressedKey = SPC_F12
            fn = True
        elif iKeycode == SPC_HOME:
            # iKeycode = SPC_HOME
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_INS:
            # iKeycode = SPC_INS
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_DEL:
            # iKeycode = SPC_DEL
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_DOWN:
            # iKeycode = SPC_DOWN
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_END:
            # iKeycode = SPC_END
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_LEFT:
            # iKeycode = SPC_LEFT
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_PGDN:
            # iKeycode = SPC_PGDN
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_PGUP:
            # iKeycode = SPC_PGUP
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_PRINTSCR:
            # iKeycode = SPC_PRINTSCR
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_RIGHT:
            # iKeycode = SPC_RIGHT
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_UP:
            # iKeycode = SPC_UP
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        elif iKeycode == SPC_SCROLLOCK:
            # iKeycode = SPC_SCROLLOCK
            self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        # end if
        if fn:
            self.KeyAction( fn, iKeycode, bShift, bCtrl, bAlt )
        # end if
        return
    # end def


    def KeyTyped( self, iKeycode, bShift, bCtrl, bAlt ):
        self.__pressedKey = iKeycode
        self.KeyAction( False, iKeycode, bShift, bCtrl, bAlt )
        return
    # end def

    def KeyAction( self, bFn, iKeycode, bShift, bCtrl, bAlt ):
        sb  = ''
        if bCtrl:
            if bFn:
                if self.__sendCursorWithFn:
                    if self.__protectMode:
                        return
                    else:
                        return
                    # end if
                # end if
            # end if
            if self.__localCmdCtl[ self.__pressedKey ] != 0:
                self.NotifyListener( self.__localCmdCtl[ self.__pressedKey ] )
                return
            # end if
            self.NotifyListener( self.__crtl[ self.__pressedKey ] )
        elif bShift:
            if bFn:
                if self.__sendCursorWithFn:
                    if self.__protectMode:
                        sb += chr( 1 )
                        sb += self.shiftFn[ self.__pressedKey ]
                        sb += chr( self.__listener.KeyGetPage() + 0x20 )
                        sb = self.__listener.KeyGetStartFieldASCII( sb )
                        sb += chr( 3 )
                        sb += chr( 0 )
                        self.NotifyListener( sb )
                        return
                    else:
                        sb += chr( 1 )
                        sb += self.shiftFn[ self.__pressedKey ]
                        sb += chr( self.__listener.KeyGetCursorX() + 0x20 )
                        sb += chr( self.__listener.KeyGetCursorY() + 0x20 )
                        sb += chr( 13 )
                        self.NotifyListener( sb )
                        return
                    # end if
                # end if
            # end if
            if self.__localCmd[ self.__pressedKey ] != 0:
                self.NotifyListener( self.__localCmd[ self.__pressedKey ] )
                return
            # end if
            self.NotifyListener( self.__shift[ self.__pressedKey ] )
        elif bAlt:
            if bFn:
                if self.__sendCursorWithFn:
                    if self.__protectMode:
                        return
                    else:
                        return
                    # end if
                # end if
            # end if
            if self.__localCmdAlt[ self.__pressedKey ] != 0:
                self.NotifyListener( self.__localCmdAlt[ self.__pressedKey ] )
                return
            # end if
            self.NotifyListener( self.__alt[ self.__pressedKey ] )
        else:
            if bFn:
                if self.__sendCursorWithFn:
                    if self.__protectMode:
                        #	notifyListener((char)1 + plainFn[pressedKey] + (char)(listener.getPage() + 0x20) + listener.getStartFieldASCII() + ((char)3) + "" + ((char)0));
                        #	return;
                        #}
                        #else
                        #{
                        #	notifyListener((char)1 + plainFn[pressedKey] + (char)(listener.getCursorX() + 0x20) + ""   + (char)(listener.getCursorY() + 0x20) + "" + ((char)13));
                        #	return;
                        sb += chr( 1 )
                        sb += self.plainFn[ self.__pressedKey ]
                        sb += chr( self.__listener.KeyGetPage() + 0x20 )
                        sb = self.__listener.KeyGetStartFieldASCII( sb )
                        sb += chr( 3 )
                        sb += chr( 0 )
                        self.NotifyListener( sb )
                        return
                    else:
                        sb += chr( 1 )
                        sb += self.plainFn[ self.__pressedKey ]
                        sb += chr( self.__listener.KeyGetCursorX() + 0x20 )
                        sb += chr( self.__listener.KeyGetCursorY() + 0x20 )
                        sb += chr( 13 )
                        self.NotifyListener( sb )
                        return
                    # end if
                # end if
            # end if
            if self.__pressedKey == 13 and self.__enterKeyOn and self.__protectMode:
                sb += chr( 1 )
                sb += 'V'
                sb += chr( self.__listener.KeyGetPage() + 0x20 )
                sb += chr( self.__listener.KeyGetCursorX() + 0x20 )
                sb += chr( self.__listener.KeyGetCursorY() + 0x20 )
                sb += chr( 3 )
                sb += chr( 0 )
                self.NotifyListener( sb )
            # end if
            if self.__localCmd[ self.__pressedKey ] != 0:
                self.NotifyListener( self.__localCmd[ self.__pressedKey ] )
                return
            # end if
            if not bFn:
                self.NotifyListener( self.__plain[ self.__pressedKey ] )
            # end if
         # end if
        return
    # end def


    def LockKeyboard( self ):
        self.__ignoreKeys = True
        return
    # end def

    def UnlockKeyboard( self ):
        self.__ignoreKeys = False
        return
    # end def

    def SetCrLfOn( self ):
        return
    # end def

    def SetCrLfOff( self ):
        return
    # end def

    def NotifyListener( self, b ):
        if not self.__ignoreKeys:
            if len( b ) == 1:
                self.__listener.KeyCommand( b )
            else:
                self.__listener.KeyMappedKey( str )
            # end if
        return
    # end def

    ansiChar        = [  ]
    ansiCharCtl     = [ TDM_ESC + "@",
                        TDM_ESC + "A",
                        TDM_ESC + "B",
                        TDM_ESC + "C",
                        TDM_ESC + "D",
					    TDM_ESC + "E",
                        TDM_ESC + "F",
                        TDM_ESC + "G", "\b", "\t", "\r",
                        TDM_ESC + "H",
                        TDM_ESC + "I", "\n",
                        TDM_ESC + "J",
			    		TDM_ESC + "[K", "0",
                        TDM_ESC + "[U",
                        TDM_ESC + "[H",
                        TDM_ESC + "[\24H",
		    			TDM_ESC + "[@",
                        TDM_ESC + "[P", "",
                        TDM_ESC + "[A",
                        TDM_ESC + "[B",
	    				TDM_ESC + "[D",
                        TDM_ESC + "[C",
                        TDM_ESC, "\0", "\0","\30", "\31", " ", "!", "\"",
				    	"#", "$", "%", "&", "\"", "(", ")", "*", "+", ",",
			    		"-", ".", "/", "0", "1", "2", "3", "4", "5", "6",
		    			"7", "8", "9", ":", ";", "<", "=", ">", "?", "@",
	    				"A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    					"K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
					    "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^",
				    	"_", "`", "a", "b", "c", "d", "e", "f", "g", "h",
			    		"i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
		    			"s", "t", "u", "v", "w", "x", "y", "z", "{", "|",
	    				"}", "~" ]

    ansiCharAlt     = [ "", "", "", "", "", "", "", "", "",
	                    "", "", "", "", "", "", "", "", "",
    					"", "", "", "", "", "", "", "","",
	    				"", "", "", "","", " ", "", "","", "", "",
		    			"", "", "", "", "", "", "", "", "", "", "",
			    		"", "", "", "", "", "", "", "", "", "", "",
				    	"", "", "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "", "",
    					"", "", "", "", "", "", "", "", "", "", "",
	    				"", "", "", "", "", "", "", "", "", "", "",
		    			"", "", "", "", "", "", "", "", "", "", "",
			    		"", "", "", "", "", "", "", "", "", "", "",
				    	"", ""  ]

    ansiCharShift   = [ TDM_ESC + "@",
                        TDM_ESC + "A",
                        TDM_ESC + "B",
                        TDM_ESC + "C",
                        TDM_ESC + "D",
					    TDM_ESC + "E",
                        TDM_ESC + "F",
                        TDM_ESC + "G", "\b", "\t", "\r",
                        TDM_ESC + "H",
                        TDM_ESC + "I", "\n",
                        TDM_ESC + "J",
				    	TDM_ESC + "[K", "0",
                        TDM_ESC + "[U",
                        TDM_ESC + "[H",
                        TDM_ESC + "[\24H",
			    		TDM_ESC + "[@",
                        TDM_ESC + "[P", "",
                        TDM_ESC + "[A",
                        TDM_ESC + "[B",
		    			TDM_ESC + "[D",
                        TDM_ESC + "[C",
                        TDM_ESC, "\0", "\0", "\30", "\31", " ", "!", "\"",
				    	"#", "$", "%", "&", "\"", "(", ")", "*", "+", ",",
			    		"-", ".", "/", "0", "1", "2", "3", "4", "5", "6",
		    			"7", "8", "9", ":", ";", "<", "=", ">", "?", "@",
	    				"A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    					"K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
					    "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^",
				    	"_", "`", "a", "b", "c", "d", "e", "f", "g", "h",
			    		"i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
		    			"s", "t", "u", "v", "w", "x", "y", "z", "{", "|",
	    				"}", "~" ]

    ansiLocal       = [ 0,0,0,0,0,0,0,0,0,0,
				    	0,0,0,0,0,0,0,0,0,0,
			    		0,0,0,0,0,0,0,0,0,0,
		    			0,0,0,0,0,0,0,0,0,0,
	    				0,0,0,0,0,0,0,0,0,0,
    					0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
				    	0,0,0,0,0,0,0,0,0,0,
			    		0,0,0,0,0,0,0,0,0,0,
		    			0,0,0,0,0,0,0,0,0,0,
	    				0,0,0,0,0,0,0,0,0,0,
    					0,0,0,0,0,0,0,0,0,0 ]

    ansiLocalCtl    = [ 0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
				    	0,0,0,0,0,0,0,0,0,0,
			    		0,0,0,0,0,0,0,0,0,0,
		    			0,0,0,0,0,0,0,0,0,0,
	    				0,0,0,0,0,0,0,0,0,0,
    					0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
				    	0,0,0,0,0,0,0,0,0,0,
			    		0,0,0,0,0,0,0,0,0,0,
		    			0,0,0,0,0,0,0,0,0,0,
	    				0,0,0,0,0,0,0,0,0,0 ]

    ansiLocalAlt    = [ 0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
				    	0,0,0,0,0,0,0,0,0,0,
			    		0,0,0,0,0,0,0,0,0,0,
		    			0,0,0,0,0,0,0,0,0,0,
	    				0,0,0,0,0,0,0,0,0,0,
    					0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
				    	0,0,0,0,0,0,0,0,0,0,
			    		0,0,0,0,0,0,0,0,0,0,
		    			0,0,0,0,0,0,0,0,0,0,
	    				0,0,0,0,0,0,0,0,0,0 ]

    convChar        = [ "@", "A", "B", "C", "D",
					    "E", "F", "G",  "\b", "\t",
					    "\r", "H", "I", "\n", "J",
					    "K", "\16", "\17", "\0", "\0",
					    "\20", TDM_NAK, "\22", "\23", "\11", "\r", "\b", TDM_ESC, "\t", "\0",
					    "\30", "\31", " ", "!", "\"", "#", "$", "%", "&", "\"",
					    "(", ")", "*", "+", ",", "-", ".", "/", "0", "1",
					    "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<",
					    "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G",
					    "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
					    "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]",
				    	"^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h",
			    		"i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
		    			"t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~",
	    				"\127"  ]

    convCharCtl     = [ "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "","",
				    	"", "", "", "","", " ", "", "","", "", "",
			    		"", "", "", "", "", "", "", "", "", "", "",
		    			"", "\0", "", "", "", "", "", "", "", "", "",
	    				"", "", "", "", "\0", "\1", "\2", "\3", "\4", "\5", "\6",
    					"\7", "", "\t", "\10", "\11", "\12", "\13", "\14", "\15", "\16", "\17",
					    "\18", "\19", "\20", "\21", "\22", "\23", "\24", "\25", "\26", "\27", "\28",
			    		"\29", "\30", "", "", "\1", "\2", "\3", "\4", "\5", "\6", "\7",
				    	"", "\t", "\10", "\11", "\12", "\13", "\14", "\15", "\16", "\17", "\18",
	    				"\19", "\20", "\21", "\22", "\23", "\24", "\25", "\26", "", "", "",
		    			"", ""  ]

    convCharAlt     = [ "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "","",
				    	"", "", "", "","", " ", "", "","", "", "",
			    		"", "", "", "", "", "", "", "", "", "", "",
		    			"", "", "", "", "", "", "", "", "", "", "",
	    				"", "", "", "", "", "", "", "", "", "", "",
    					"", "", "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "", "",
				    	"", "", "", "", "", "", "", "", "", "", "",
			    		"", "", "", "", "", "", "", "", "", "", "",
		    			"", "", "", "", "", "", "", "", "", "", "",
	    				"", ""  ]

    convCharShift   = [ "'", "a", "b", "c", "e",
		    			"e", "f", "g",  "", "",
	    				"\r", "h", "i", "\n", "j",
    					"k", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "",
				    	"", "", " ", "!", "\"", "#", "$", "%", "&", "\"",
			    		"(", ")", "*", "+", ",", "-", ".", "/", "0", "1",
		    			"2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<",
	    				"=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G",
    					"H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
					    "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]",
				    	"^", "_", "`", "A", "B", "C", "D", "E", "F", "G", "H",
			    		"I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
		    			"T", "U", "V", "W", "X", "Y", "Z", "{", "|", "}", "~",
	    				"\127" ]

    convLocal       = [   0,   0,   0,   0,   0,   0,   0,   7,   8,   9,
			    		 10,   0,   0,  13,   0,   0,  16,  17,  18,  19,
		    			 20,  21,  22,  23,  24,  25,  26,  27,  28,  29,
	    				 30,  31,  32,  33,  34,  35,  36,  37,  38,  39,
    					 40,  41,  42,  43,  44,  45,  46,  47,  48,  49,
					     50,  51,  52,  53,  54,  55,  56,  57,  58,  59,
				    	 60,  61,  62,  63,  64,  65,  66,  67,  68,  69,
			    		 70,  71,  72,  73,  74,  75,  76,  77,  78,  79,
		    			 80,  81,  82,  83,  84,  85,  86,  87,  88,  89,
	    				 90,  91,  92,  93,  94,  95,  96,  97,  98,  99,
    					100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
				    	110, 111, 112, 113, 114, 115, 116, 117, 118, 119,
			    		120, 121, 122, 123, 124, 125, 126, 127 ]

    convLocalCtl    = [ 0,0,0,0,0,0,0,0,8,0,
		    			0,0,0,13,0,0,16,17,18,19,
	    				0,0,0,0,0,0,0,0,0,0,
    					0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
				    	0,0,0,0,0,0,0,0,0,0,
			    		0,0,0,0,0,0,0,0,0,0,
		    			0,0,0,0,0,0,0,0,0,0,
	    				0,0,0,0,0,0,0,0,0,0,
    					0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0 ]

    convLocalAlt    = [ 0,0,0,0,0,0,0,0,8,0,
					    0,0,0,13,0,0,0,0,0,19,
					    0,0,0,23,24,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,49,
					    50,51,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
				    	0,0,0,0,0,0,0,0,0,0 ]

    blockChar       = [ "@", "A", "B", "C", "D",
			    		"E", "F", "G", TDM_BACKSPACE, "\t",
		    			"\r", "H", "I", "\n", "J",
	    				"K", "\16", "\17", "\0", "\0",
					    "\20", TDM_NAK, "\22", "\23", "\11", "\r", TDM_BACKSPACE, TDM_ESC, "\t", "\0",
    					"\30", "\31", " ", "!", "\"", "#", "$", "%", "&", "\"",
					    "(", ")", "*", "+", ",", "-", ".", "/", "0", "1",
					    "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<",
					    "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G",
					    "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
					    "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]",
					    "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h",
					    "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
					    "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~",
					    chr( 127 ) ]

    blockCharCtl    = [ "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "","",
				    	"", "", "", "","", " ", "", "","", "", "",
			    		"", "", "", "", "", "", "", "", "", "", "",
		    			"", "\0", "", "", "", "", "", "", "", "", "",
	    				"", "", "", "", "\0", "\1", "\2", "\3", "\4", "\5", "\6",
    					"\7", "", "\t", "\10", "\11", "\12", "\13", "\14", "\15", "\16", "\17",
					    "\18", "\19", "\20", "\21", "\22", "\23", "\24", "\25", "\26", "\27", "\28",
				    	"\29", "\30", "", "", "\1", "\2", "\3", "\4", "\5", "\6", "\7",
			    		"", "\t", "\10", "\11", "\12", "\13", "\14", "\15", "\16", "\17", "\18",
		    			"\19", "\20", "\21", "\22", "\23", "\24", "\25", "\26", "", "", "",
	    				"", ""  ]

    blockCharAlt    = [ "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "","",
					    "", "", "", "","", " ", "", "","", "", "",
					    "", "", "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "", "",
					    "", "" ]

    blockCharShift  = [ "'", "a", "b", "c", "e",
					    "e", "f", "g",  "", "",
					    "\r", "h", "i", "\n", "j",
					    "k", "", "", "", "",
					    "", "", "", "", "", "", "", "", "", "",
					    "", "", " ", "!", "\"", "#", "$", "%", "&", "\"",
					    "(", ")", "*", "+", ",", "-", ".", "/", "0", "1",
					    "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<",
					    "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G",
					    "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
					    "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]",
					    "^", "_", "`", "A", "B", "C", "D", "E", "F", "G", "H",
					    "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
					    "T", "U", "V", "W", "X", "Y", "Z", "{", "|", "}", "~",
					    chr(127) ]

    blockLocal      = [ 0,0,0,0,0,0,0,7,8,9,
					    10,0,0,13,0,0,16,17,18,19,
					    20,21,22,23,24,25,26,27,28,29,
					    30,31,32,33,34,35,36,37,38,39,
					    40,41,42,43,44,45,46,47,48,49,
					    50,51,52,53,54,55,56,57,58,59,
					    60,61,62,63,64,65,66,67,68,69,
					    70,71,72,73,74,75,76,77,78,79,
					    80,81,82,83,84,85,86,87,88,89,
					    90,91,92,93,94,95,96,97,98,99,
					    100,101,102,103,104,105,106,107,108,109,
					    110,111,112,113,114,115,116,117,118,119,
					    120,121,122,123,124,125,126,127 ]

    blockLocalCtl   = [ 0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0 ]

    blockLocalAlt   = [ 0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0,
					    0,0,0,0,0,0,0,0,0,0 ]

    shiftFn         = [ "'", "a", "b", "c", "d", "e", "f", "g", "", "", "", "h", "i", "", "j", "k" ]

    plainFn         = [ "@", "A", "B", "C", "D", "E", "F", "G", "", "", "", "H", "I", "", "J", "K" ]

# end class