
'''
  @ AUTHOR NAME HERE
  @ Starter Code By Harris Christiansen (Harris@purduecs.com)
  2016-01-28
  For: Purdue Hackers - Battleship
  Battleship Client
'''

import sys
import socket
import time
import random

API_KEY = "175860009" ########## PUT YOUR API KEY HERE ##########

GAME_SERVER = "battleshipgs.purduehackers.com"

##############################  PUT YOUR CODE HERE ##############################

letters = ['A','B','C','D','E','F','G','H']
grid = [[-1 for x in range(8)] for x in range(8)] # Fill Grid With -1s


class Targeter:
  def __init__(self):
    self.hit = ()
    self.miss = []
    self.success = []
    self.targeting = False
    self.following = False
    self.reset = False
    self.hitlist = []

target = Targeter()

def placeShips(opponentID):
  global grid
  start = time.time()
  # Fill Grid With -1s
  grid = [[-1 for x in range(8)] for x in range(8)] # Fill Grid With -1s

  random.seed()
  taken = []
  found = False

  def getStr(c, i):
      return c+str(i)

  #destroyer
  pos1c = random.choice(letters[:-1])
  pos1n = random.randint(0,6)
  pos2c = pos1c
  pos2n = pos1n
  if random.randint(0,1) == 1:
      pos2c = letters[letters.index(pos1c)+1]
  else:
      pos2n += 1
  placeDestroyer(getStr(pos1c,pos1n),getStr(pos2c,pos2n)) # Ship Length = 2
  taken.extend([getStr(pos1c,pos1n),getStr(pos2c,pos2n)])

  #submarine
  while not found:
      pos1c = random.choice(letters[:-2])
      pos1n = random.randint(0,5)
      pos2c = pos1c
      pos2n = pos1n
      if random.randint(0,1) == 1:
         pos2c = letters[letters.index(pos1c)+2]
         if getStr(pos1c,pos1n) in taken or getStr(pos2c,pos2n) in taken or getStr(letters[letters.index(pos1c)+1],pos1n) in taken:
             continue
         taken.append(getStr(letters[letters.index(pos1c)+1],pos1n))
      else:
         pos2n += 2
         if getStr(pos1c,pos1n) in taken or getStr(pos2c,pos2n) in taken or getStr(pos1c,pos1n+1) in taken:
             continue
         taken.append(getStr(pos1c,pos1n+1))
      found = True
  found = False
  placeSubmarine(getStr(pos1c,pos1n), getStr(pos2c,pos2n)) # Ship Length = 3
  taken.extend([getStr(pos1c,pos1n), getStr(pos2c,pos2n)])

  #cruiser
  while not found:
      pos1c = random.choice(letters[:-2])
      pos1n = random.randint(0,5)
      pos2c = pos1c
      pos2n = pos1n
      if random.randint(0,1) == 1:
          pos2c = letters[letters.index(pos1c)+2]
          if getStr(pos1c,pos1n) in taken or getStr(pos2c,pos2n) in taken or getStr(letters[letters.index(pos1c)+1],pos1n) in taken:
              continue
          taken.append(getStr(letters[letters.index(pos1c)+1],pos1n))
      else:
        pos2n += 2
        if getStr(pos1c,pos1n) in taken or getStr(pos2c,pos2n) in taken or getStr(pos1c,pos1n+1) in taken:
            continue
        taken.append(getStr(pos1c,pos1n+1))
      found = True
  found = False
  placeCruiser(getStr(pos1c,pos1n), getStr(pos2c,pos2n)) # Ship Length = 3
  taken.extend([getStr(pos1c,pos1n), getStr(pos2c,pos2n)])

  #battleship
  while not found:
      pos1c = random.choice(letters[:-3])
      pos1n = random.randint(0,4)
      pos2c = pos1c
      pos2n = pos1n
      if random.randint(0,1) == 1:
          pos2c = letters[letters.index(pos1c)+3]
          if getStr(pos1c,pos1n) in taken or getStr(pos2c,pos2n) in taken or getStr(letters[letters.index(pos1c)+1],pos1n) in taken or getStr(letters[letters.index(pos1c)+2],pos1n) in taken:
              continue
          taken.append(getStr(letters[letters.index(pos1c)+1],pos1n))
          taken.append(getStr(letters[letters.index(pos1c)+2],pos1n))
      else:
        pos2n += 3
        if getStr(pos1c,pos1n) in taken or getStr(pos2c,pos2n) in taken or getStr(pos1c,pos1n+1) in taken or getStr(pos1c,pos1n+2) in taken:
            continue
        taken.append(getStr(pos1c,pos1n+1))
        taken.append(getStr(pos1c,pos1n+2))
      found = True
  found = False
  placeBattleship(getStr(pos1c,pos1n), getStr(pos2c,pos2n)) # Ship Length = 4
  taken.extend([getStr(pos1c,pos1n), getStr(pos2c,pos2n)])

  #carrier
  while not found:
    pos1c = random.choice(letters[:-4])
    pos1n = random.randint(0,3)
    pos2c = pos1c
    pos2n = pos1n
    if random.randint(0,1) == 1:
        pos2c = letters[letters.index(pos1c)+4]
        if getStr(pos1c,pos1n) in taken or getStr(pos2c,pos2n) in taken or getStr(letters[letters.index(pos1c)+1],pos1n) in taken or getStr(letters[letters.index(pos1c)+2],pos1n) in taken or getStr(letters[letters.index(pos1c)+3],pos1n) in taken:
            continue
    else:
      pos2n += 4
      if getStr(pos1c,pos1n) in taken or getStr(pos2c,pos2n) in taken or getStr(pos1c,pos1n+1) in taken or getStr(pos1c,pos1n+2) in taken or getStr(pos1c,pos1n+3) in taken:
          continue
    found = True
  placeCarrier(getStr(pos1c,pos1n), getStr(pos2c,pos2n)) # Ship Length = 4

  print "Placed : ", time.time()-start,"\n"


def makeMove():
  global grid

  if target.targeting:
    print "Targeting ship"
    targetShip(target)
    return

  for x in range(0,8): # Loop Till Find Square that has not been hit
    for y in range(0,8):

      if grid[x][y] == -1:
        wasHitSunkOrMiss = placeMove(letters[x]+str(y)) # placeMove(LetterNumber) - Example: placeMove(D5)

        if wasHitSunkOrMiss == "Hit":
          print "Hit"
          grid[x][y] = 1
          target.targeting = True
          target.hit = (x,y)
          target.hitlist.append((x, y))
        elif wasHitSunkOrMiss == "Sunk":
          print "Sunk"
          target.targeting = False
        else:
          grid[x][y] = 0

        return


def targetShip(target):

  # If we have hit this target keep going
  if target.following:
    x = target.success[-1][0]
    y = target.success[-1][1]
  elif target.reset:
    # Go back to first square we hit
    x = target.success[0][0]
    y = target.success[0][1]
  else:
    x = target.hit[0]
    y = target.hit[1]

  # Square grid around target
  possibilities = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]

  for coord in possibilities:

    # Discard coords that where we already missed or that don't exist
    if coord in target.hitlist:
      print coord
      print "Already hit here"
      continue
    if coord in target.miss:
      print coord
      print "Already missed here"
      continue
    if coord[0] < 0 or coord[1] < 0 or coord[0] > 7 or coord[1] > 7:
      continue

    # Bombs away
    print letters[x]+str(y)
    result = placeMove(letters[x]+str(y))
    if result == "Hit":
      print "Targeted hit"
      target.success.append(coord)
      target.hitlist.append(coord)
      target.following = True
    elif result == "Sunk":
      print "Targeted sink"
      target.targeting = False
      target.hit = ()
    elif result == "Miss":
      if target.following:
        target.reset = True
        target.following = False
    else:
      print result

      target.miss.append(coord)

    # Ugly
    break

  return


############################## ^^^^^ PUT YOUR CODE ABOVE HERE ^^^^^ ##############################

def sendMsg(msg):
  global s
  try:
    s.send(msg)
  except:
    s = None

def connectToServer():
  global s
  invalidKey = False
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((GAME_SERVER, 23345))

    sendMsg(API_KEY)
    data = s.recv(1024)

    if("False" in data):
      s = None
      print "Invalid API_KEY"
      invalidKey = True
  except:
    s = None

  if invalidKey:
    sys.exit()


destroyer=submarine=cruiser=battleship=carrier=("A0","A0")
dataPassthrough = None

def gameMain():
  global s, dataPassthrough, moveMade
  while True:
    if(dataPassthrough == None):
      if s == None:
        return
      data = s.recv(1024)
    else:
      data = dataPassthrough
      dataPassthrough = None

    if not data:
      s.close()
      return

    if "Welcome" in data: # "Welcome To Battleship! You Are Playing:xxxx"
      print data
      welcomeMsg = data.split(":")
      placeShips(welcomeMsg[1])
      if "Destroyer" in data: # Only Place Can Receive Double Message, Pass Through
        dataPassthrough = "Destroyer(2):"
    elif "Destroyer" in data: # Destroyer(2)
      sendMsg(destroyer[0])
      sendMsg(destroyer[1])
    elif "Submarine" in data: # Submarine(3)
      sendMsg(submarine[0])
      sendMsg(submarine[1])
    elif "Cruiser" in data: # Cruiser(3)
      sendMsg(cruiser[0])
      sendMsg(cruiser[1])
    elif "Battleship" in data: # Battleship (4)
      sendMsg(battleship[0])
      sendMsg(battleship[1])
    elif "Carrier" in data: # Carrier(3)
      sendMsg(carrier[0])
      sendMsg(carrier[1])
    elif "Enter" in data: # Enter Coordinates
      moveMade = False
      makeMove()
    elif "Error" in data: # Error: xxx
      print("Received Error: "+data)
      sys.exit()
    elif "Hit" in data or "Miss" in data or "Sunk" in data:
      print("Error: Please Make Only 1 Move Per Turn.")
      sys.exit()
    elif "Die" in data:
      print("Error: Your client was disconnected using the Game Viewer.")
      sys.exit()
    else:
      print("Received Unknown Response: "+data)
      sys.exit()


def placeDestroyer(startPos, endPos):
  global destroyer
  destroyer = (startPos.upper(), endPos.upper())
def placeSubmarine(startPos, endPos):
  global submarine
  submarine = (startPos.upper(), endPos.upper())
def placeCruiser(startPos, endPos):
  global cruiser
  cruiser = (startPos.upper(), endPos.upper())
def placeBattleship(startPos, endPos):
  global battleship
  battleship = (startPos.upper(), endPos.upper())
def placeCarrier(startPos, endPos):
  global carrier
  carrier = (startPos.upper(), endPos.upper())

def placeMove(pos):
  global dataPassthrough, moveMade
  if moveMade: # Only Make 1 Move Per Turn
    print("Error: Your client was disconnected using the GameViewer")
    sys.exit()

  moveMade = True
  sendMsg(pos)
  data = s.recv(1024)
  if "Hit" in data:
    return "Hit"
  elif "Sunk" in data:
    return "Sunk"
  elif "Miss" in data:
    return "Miss"
  else:
    dataPassthrough = data
    return "Miss"

while True:
  connectToServer()
  if s != None:
    try:
      gameMain()
    except socket.error, msg:
      None
  time.sleep(1)
