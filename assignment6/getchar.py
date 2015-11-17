import tty, sys
# windows implementation
try:

    import msvcrt

    def getchar():
        return msvcrt.getch()

# unix/mac implementation
except:

    import termios

    def getchar():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

