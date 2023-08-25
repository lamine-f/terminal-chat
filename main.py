# main.py
from modules.pretty_text_module import *
from modules.user_module import *
from modules.curses_module import *
from curses import wrapper

# Code principal
if __name__ == "__main__":

    try:
        printLine()
        print("Authentification")
        user = authentification()
        while not user["authentification"]:
            printLine()
            print("Authentification")
            printCenterText("veuillez réessayer")
            user = authentification()
        canal = getCanal(user)
        connection_canal = canal+"-connection"
        rm_connected = canal+"-connection-remove"
        # ...
        # Appel de la fonction principale du module curses_module
        wrapper(lambda stdscr: main_d(stdscr, user, canal, connection_canal, rm_connected))
        # ...
    except KeyboardInterrupt:
        print("")
        printLine()
        print(AUTHENTIFICATION_ERROR+": "+ERROR_MESSAGE)
        printLine()
