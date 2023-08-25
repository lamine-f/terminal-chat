import shutil

terminal_size = shutil.get_terminal_size()
MAX_Y, MAX_X = terminal_size.lines, terminal_size.columns
SEP = "*"

def printLine():
  global MAX_X
  global SEP
  print("\n"+SEP*MAX_X+"\n")

def printCenterText(txt):
  global MAX_X
  size = len(txt)
  position = (MAX_X - size) // 2
  print(" "*position + txt)

def centerInputText(txt):
  global MAX_X
  size = len(txt)
  position = (MAX_X - size) // 2
  return input( " "*position + txt)
