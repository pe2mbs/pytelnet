#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses

def color_pair_number( fg, bg ):
    return ( fg * ( curses.COLOR_WHITE ) + bg ) + 1
# end if

def color_attr( fg, bg ):
    return ( ( fg * ( curses.COLOR_WHITE ) + bg ) + 1 ) << 8
# end if


def main1( stdscr ):
    counter = 1
    stdscr.addstr( "BLA" )
    stdscr.refresh()
    for fg in range( curses.COLOR_BLACK, curses.COLOR_WHITE ):
        for bg in range( curses.COLOR_BLACK, curses.COLOR_WHITE ):
            # curses.init_pair( counter, fg, bg )
            stdscr.addstr( "counter: %X fg %i bg %i \n" % ( counter, fg, bg ) )
            stdscr.refresh()
            counter += 1
        # next
    # next
# end def

def main( screen ):
    screen.addstr("This is a Sample Curses Script\n\n")
    cnt = 1
    for fg in range( curses.COLOR_BLACK, curses.COLOR_WHITE ):
        for bg in range( curses.COLOR_BLACK, curses.COLOR_WHITE ):
            curses.init_pair( cnt, fg, bg )
            stdscr.addstr( "counter: %X fg %i bg %i \n" % ( cnt, fg, bg ), color_attr( fg, bg ) )
            cnt += 1
        # next
    # next
    while True:
        event = screen.getch()
        if event == ord("q"):
            break

    return
# end def

def colortest():
    # init
    window = curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    print( curses.COLORS )
    # assign 'default' pairs, pairs are assigned +1 MORE than the color value!
    cnt = 1
    for fg in range( curses.COLORS ):
        #curses.init_pair( each + 1, each, -1 )
        for bg in range( curses.COLORS ):
            curses.init_pair( fg << 3 | bg, fg, bg )
            cnt += 1
         # next
    # next
    # custom/non-default pair
    #curses.init_pair( 1 + 2 * curses.COLORS, 0x0F, 0x15 )  # white on cobalt according to colors above ???
    #curses.init_pair( 4321, 0xd5, 0x81 )  # hot pink on violet according to colors above ???

    # setup
    curses.meta(1)
    curses.noecho()
    curses.cbreak()
    window.leaveok(1)
    window.scrollok(0)
    window.keypad(1)
    window.refresh()

    # print all pairs in their colors
    for fg in range( curses.COLORS ):
        for bg in range( curses.COLORS ):
            window.addstr( " %02X " % ( fg << 3 | bg ), curses.color_pair( fg << 3 | bg ) )  # these are all perfect
        # next
        window.addstr("\n")
    # next
    #window.addstr(hex(1 + 2*curses.COLORS).join('  '), curses.color_pair(1 + 2*curses.COLORS))  # nope: this prints 0,-1: black on default ???
    #window.addstr(hex(4321).join('  '), curses.color_pair(4321))  # nope: this prints 0xe1,-1: pinkish on default ???

    # update
    window.noutrefresh()
    curses.doupdate()

    # pause
    window.getch()

    # teardown
    window.leaveok(0)
    window.scrollok(1)
    window.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()


if __name__ == "__main__":
    colortest()
    """
    try:
        stdscr = curses.initscr()
        curses.cbreak()
        curses.echo()
        curses.start_color()
        curses.use_default_colors()
        stdscr.nodelay( True )
        stdscr.scrollok( True )
        print( "main\r\n" )
        stdscr.keypad(1)
        main( stdscr )
        print( "finish\r\n" )
    except Exception, exc:
        print( "Error", exc )
    # end try
    curses.echo()
    stdscr.keypad(0)
    curses.endwin()
    """
# end if