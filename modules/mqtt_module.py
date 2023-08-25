# mqtt_module.py
import json, pygame, curses, mqtt
from .user_module import *

def play_music(filename):
    try:
      pygame.mixer.init()
      pygame.mixer.music.load(filename)
      pygame.mixer.music.play()
      while pygame.mixer.music.get_busy():
          pygame.time.Clock().tick(10)
    except:
       pass

def on_connect(client, userdata, flags, rc, canal, connection_canal, rm_connected, user):
    client.subscribe(canal)
    client.subscribe(connection_canal)
    client.subscribe(rm_connected)
    client.publish(connection_canal, user["value"]["username"])

def on_message(client, userdata, msg, canal, connection_canal, rm_connected, user):
    
    global MAX_X
    global MAX_Y
    global CONNECTED
    global MESSAGES
    
    if msg.topic == connection_canal:
      curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
      connected_user = str(msg.payload.decode('utf-8'))
      try:
        CONNECTED.remove(connected_user) 
      except:
        pass
      CONNECTED.insert(0, connected_user) 
      play_music("sounds/connection_beep.mp3")
      
    elif msg.topic == rm_connected:
      curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
      data = json.loads(str(msg.payload.decode('utf-8')))
      disconnected_user = data["username"]
      try:
        CONNECTED.remove(disconnected_user)
      except:
        pass
      play_music("sounds/disconnection_beep.mp3")
      
    else:
      try:
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        
        data = json.loads(str(msg.payload.decode('utf-8')))
        connected_user = data["user"]
        
        if connected_user not in CONNECTED:
          play_music("sounds/connection_beep.mp3")
        try:
          CONNECTED.remove(connected_user) 
        except:
          pass
        CONNECTED.insert(0, connected_user) 
        
        newmessage=f"{data['user']}: {data['message']} [{data['time']}]"
        messagewin = curses.newwin(MAX_Y -8, MAX_X, 8, 1)
        x = 0 
        y = 0
        messagewin.addstr(y, x, "(last) ")
        x += 7
        messagewin.addstr(y, x, data['user']+": ", curses.color_pair(2))
        x += len(data['user']) + 2

        if "set_blue" in data['message']:
          messagewin.addstr(y, x, data['message'].replace("set_blue", ""), curses.color_pair(3))
          x += len(data['message']) + 1

        else:
          for word in data['message'].split():
            if "@" in word.lower():
              messagewin.addstr(y, x, word, curses.color_pair(1))    
            else:
              messagewin.addstr(y, x, word, curses.color_pair(2))
            x += len(word) + 1

        messagewin.addstr(y, x, "["+data['time']+"]", curses.color_pair(2))

        x = 0
        y = 2
        for words in MESSAGES.split("\n"):
          if "set_blue" in words:
            messagewin.addstr(y, x, words.replace("set_blue", ""), curses.color_pair(3))
          else:
            for word in words.split():
                if "@" in word.lower():
                  messagewin.addstr(y, x, word, curses.color_pair(1))
                else:
                  messagewin.addstr(y, x, word)
                x += len(word) + 1
          x = 0
          y += 1
        messagewin.refresh()
        MESSAGES =  newmessage + '\n' + MESSAGES 
      except:
        pass
    
    connectedwin = curses.newwin(1, 50, 1, 1)
    connectedwin.addstr(0, 0, "connected: ")
    connectedwin.addstr(0, 11, ' '.join(CONNECTED), curses.color_pair(4))
    connectedwin.refresh()