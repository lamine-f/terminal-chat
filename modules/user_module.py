# user_module.py
import mysql.connector
from .pretty_text_module import *

DB_CONNECTION_ERROR = "error #1" 
AUTHENTIFICATION_ERROR = "error #2" 
ERROR_MESSAGE = "contactez le développeur sur instagram @mouhamed.lamine.faye"
CONNECTED = []
MESSAGES = ""

try:
    db = mysql.connector.connect(
        host="homevps.sytes.net",
        user="terminal_chat_user",
        password="terminal_chat_user_password2003",
        database="terminal_chat"
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user")
    results = cursor.fetchall()
    users = []
    for row in results:
        users.append({
            "id": row[0],
            "username": row[1],
            "password": row[2],
        })
    cursor.close()
    db.close()
except:
    printLine()
    printCenterText(DB_CONNECTION_ERROR+": "+ERROR_MESSAGE)
    printLine()
    quit()

def validationAuthentification (user):
  global users
  resultat = {"authentification": False, "value": {} }

  for el in users:
      if el["username"] == user["username"]:
        if el["password"] == user["password"]:
            resultat["authentification"] = True,
            resultat["value"] = el
      else:
          pass
  
  return resultat

def authentification ():
    return validationAuthentification({
        "username": centerInputText("username: "),
        "password": centerInputText("password: ")
    })

    return validationAuthentification({
    "username": "lord",
    "password": "passer"
  })


def getCanal (f_user) :
    printLine()
    printCenterText("welcom " + f_user["value"]["username"] + " :)")
    canal = centerInputText("channel: ")
    printLine()    
    return canal

