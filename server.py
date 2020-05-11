import socket
from _thread import *
import pickle
from game import Game

server = ""
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {} #will store all the games running based on game ids
idCount = 0 #the number of games running


def threaded_client(conn, p, gameId):
    global idCount #global so know how many games running throughout code
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId] #will get rid of game id in list of games running
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1 #connection accepted so new game is started, so add to games list
    p = 0 #first player
    gameId = (idCount - 1)//2 #create a new game id
    if idCount % 2 == 1: #ensures every two players start a new game, no single player can be in a game alone
        games[gameId] = Game(gameId) #adding an instance of game to the games list
        print("Creating a new game...")
    else:
        games[gameId].ready = True #game is ready to be played if game is already in the list
        p = 1 #game already started so this player must be the second one


    start_new_thread(threaded_client, (conn, p, gameId)) #sets up a new thread on server with this game data
