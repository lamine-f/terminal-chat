# curses_module.py
import curses, datetime
from curses.textpad import Textbox, rectangle
from .mqtt_module import *

def main_d(stdscr, user, canal, connection_canal, rm_connected):

    global CONNECTED 
    global MAX_X
    global MAX_Y
    
    client = mqtt.Client()
    client.on_connect = lambda client, userdata, flags, rc : on_connect(client, userdata, flags, rc, canal, connection_canal, rm_connected, user) 
    client.on_message = lambda client, userdata, msg : on_message (client, userdata, msg, canal, connection_canal, rm_connected, user)
    try:
      client.connect("homevps.sytes.net", 1883, 60)  
    except:
        print("connection error")
        pass
    client.loop_start()

    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)


    stdscr.addstr(0, 1, f"channel: {canal}")
    stdscr.addstr(1, 1, f"connected: ")
    stdscr.addstr(2, 1, f"username: {user['value']['username']}")

    bottom_text = "@mouhamed.lamine.faye"
    text_y = MAX_Y - 1
    text_x = (MAX_X - len(bottom_text)) // 2 
    stdscr.addstr(text_y, text_x, bottom_text, curses.color_pair(2))
    
    rectangle(stdscr, 4, 1, 6, (MAX_X // 2)-2)
    stdscr.refresh()

    try:
      while True:
          inputwin = curses.newwin(1, (MAX_X // 2)-4, 5, 2)
          box = Textbox(inputwin)
          box.edit()
          text = box.gather().strip().replace("\n", "")
          if text != "":
            if text == "!quit":
              client.publish(rm_connected, json.dumps({"username": user['value']['username']}))
              
            else:
              now = datetime.datetime.now()
              h, m, s = now.hour, now.minute, now.second
              message = {"user": user['value']['username'], "message": text, "time": f'{h}:{m}:{s}'}
              client.publish(canal, json.dumps(message))
            
            inputwin.clear()
            stdscr.refresh()

    except KeyboardInterrupt:
      client.publish(rm_connected, json.dumps({"username": user['value']['username']}))
      return 0