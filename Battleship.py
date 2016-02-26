
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


def placeShips(opponentID):
  global grid
  # Fill Grid With -1s
  grid = [[-1 for x in range(8)] for x in range(8)] # Fill Grid With -1s

  # Place Ships
  placeDestroyer("A2","B2") # Ship Length = 2
  placeSubmarine("C3","C5") # Ship Length = 3
  placeCruiser("D6","F6") # Ship Length = 3
  placeBattleship("G2","G5") # Ship Length = 4
  placeCarrier("D0","H0") # Ship Length = 5


def makeMove():
  global grid

  target = Targeter()

  for x in range(0,8): # Loop Till Find Square that has not been hit
    for y in range(0,8):

      # Instead of going square by square, try and target
      if target.targeting:
        print "Targeting ship"
        targetShip(target)

      if grid[x][y] == -1:
        wasHitSunkOrMiss = placeMove(letters[x]+str(y)) # placeMove(LetterNumber) - Example: placeMove(D5)

        if(wasHitSunkOrMiss == "Hit" or wasHitSunkOrMiss == "Sunk"):
          print "Hit"
          grid[x][y] = 1
          target.targeting = True
          target.hit = (x,y)
        else:
          grid[x][y] = 0

        return


def targetShip(target):
  x = target.hits[0]
  y = target.hits[1]

  possibilities = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]

  for coord in possibilities:
    print coord
    if coord in target.miss:
      continue

    result = placeMove(letters[x]+str(y))
    if result == "Hit":
      target.success.append(coord)
    else:
      target.miss.append(coord)

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
