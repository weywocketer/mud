#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 10:23:11 2019

@author: weywocketer
"""
import unidecode
import threading
import random
import time
import socket


def unpolish(word):
    """
    replace polish symbols with universal ones and go lowercase
    """

    word = word.lower()
    word = unidecode.unidecode(word)  # remove accents
    return word


class Character:
    cid_counter = 0

    def __init__(self, login, password, location, hp):
        self.login = login
        self.password = password
        self.location = location
        self.hp = hp
        self.cid = Character.cid_counter  # character id
        Character.cid_counter += 1


class Player(Character):

    def __init__(self, login, password, location, hp):
        super().__init__(login, password, location, hp)

    def do_command(self):
        pass

        '''print(self.location.description)  # (client)

        command = unpolish(input("Co robisz? ")).split()
        if command[0] == "idz":
            if command[1] in self.location.neighbours:
                self.location.characters.remove(self.cid)  # server
                self.location = get_location(command[1])
                self.location.characters.append(self.cid)
            else:
                print("To niemożliwe!")
        elif command[0] == "uzyj":
            print("użyto")
            pass
        elif command[0] == "patrz":
            pass
        elif command[0] == "rozmawiaj":
            pass
        elif command[0] == "zaatakuj":
            pass
        elif command[0] == "wez":
            pass
        elif command[0] == "":
            pass'''

    def move(self, command):
        location = command[0]
        for i in range(1, len(command)):
            location = location + " " + command[i]

        print("you moved from {}".format(self.location.name))
        if location in self.location.neighbours:
            self.location.characters.remove(self.cid)
            self.location = get_location(location)
            self.location.characters.append(self.cid)
            print("you moved to {}".format(self.location.name))
        else:
            print('{}, {}, {}'.format(self.login, self.location.name, self.location.neighbours))

    command_dict = {"move": move}


class Npc(Character):
    pass


class Location:
    def __init__(self, name, description, neighbours):
        self.name = name
        self.description = description
        self.neighbours = neighbours
        self.objects = []
        self.characters = []


class Thing:
    def __init__(self, name):
        self.name = name


class PlayerList(list):
    def __contains__(self, item):
        logins = [i.login for i in self]
        if item in logins:
            return True
        else:
            return False

    def get_player(self, login):
        for player in self:
            if player.login == login:
                return player


def get_location(name):
    for i in locationList:
        if i.name == name:
            return i



#--------------networking section here---------------------

class ClientThread(threading.Thread):
    '''
    Main client thread. Allows user to log in (or register). Sends to a client all data to be displayed.
    '''

    def __init__(self, ip, port, conn):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.player = Player("", "", None, 0)
        print("New client connected. IP = {} PORT = {}".format(self.ip, self.port))

    def bind_player(self, player):
        self.player = player

    def register(self):
        register_data = self.conn.recv(4096).decode().split()
        login = register_data[0]
        password = register_data[1]
        # TODO: verify whether login not used before
        new_player = Player(login, password, random.choice(locationList), 10)
        new_player.location.characters.append(new_player.cid)
        playerList.append(new_player)
        self.bind_player(new_player)
        self.conn.sendall(b"0")  # player successfully created

        for player in playerList:
            print(player.login)

    def login(self):
        login_data = self.conn.recv(4096).decode().split()
        login = login_data[0]
        password = login_data[1]
        if login in playerList:
            for player in playerList:
                if player.login == login:
                    if player.password == password:
                        for thread in threads:  # check if someone is using this account
                            if thread.player.login == login:
                                self.conn.sendall(b"2")  # login failed - someone is logged in
                                return
                        self.bind_player(player)
                        self.conn.sendall(b"0")  # login successful
                        return
        self.conn.sendall(b"1")  # login failed - wrong login or password

    def run(self):
        while self.player.login == "":  # repeat until player is bound to thread
            command = self.conn.recv(4096)
            if command == b"0":
                self.register()
            elif command == b"1":
                self.login()

        while True:
            sendData.wait()

            neighbours = ""
            for i in self.player.location.neighbours:
                neighbours = neighbours + " " + i

            message = "{}\t{}\t{}".format(self.player.location.name,
                                          neighbours,
                                          self.player.location.description)

            self.conn.sendall(message.encode())
            time.sleep(2)

            #self.conn.sendall(str("a").encode())


class ClientCommandsThread(threading.Thread):

    def __init__(self, ip, port, conn):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.player = Player("", "", None, 0)
        print("Second channel created. IP = {} PORT = {}".format(self.ip, self.port))

    def run(self):
        global commandList
        commandBuffer = []
        while True:
            print("{}: Waiting for commands...".format(self))
            commandBuffer.append(self.conn.recv(4096).decode())
            print("New command arrived.")
            # can I modify commandList?
            addCommands.wait()
            commandList += commandBuffer
            commandBuffer = []


class ListenForSecondConn(threading.Thread):
    def run(self):
        server_ip2 = '127.0.0.1'
        server_port2 = 2005

        server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server2.bind((server_ip2, server_port2))
        threads2 = []
        server2.listen(4)

        while True:
            print("Waiting for second connections...")
            (conn2, (ip2, port2)) = server2.accept()
            new_thread2 = ClientCommandsThread(ip2, port2, conn2)
            new_thread2.start()
            threads2.append(new_thread2)

class ApplyCommands(threading.Thread):

    def run(self):
        global commandList
        while True:

            addCommands.clear()
            print("Parsing commands...")
            for i in range(len(commandList)):  # new commands should not be added when this for is running!
                print("command {}. is being analysed... ".format(i))
                command = commandList[i].split()
                player = playerList.get_player(command[0])

                try:
                    a = getattr(player, command[1])  # find player's method corresponding to command
                    a(command[2:])  # remember - arguments are sent as list - even if only one is left!
                except:
                    print("invalid command!")
            commandList = []

            addCommands.set()
            sendData.set()
            time.sleep(1)
            sendData.clear()

            time.sleep(4)





#-----------------main code here--------------------------------------

playerList = PlayerList()

locations = open("locations.csv").readlines()  # load csv file with locations (tab used as separator!)
for i in range(len(locations)):
    locations[i] = locations[i].replace("\n", "")
    locations[i] = locations[i].split("\t")
    locations[i][2] = locations[i][2].split(",")

locationList = []

for location in locations:
    locationList.append(Location(location[0], location[1], location[2]))


jon = Player("potWilk", "1234", random.choice(locationList), 14)
playerList.append(jon)
jon.location.characters.append(jon.cid) # trza to ogarnąć lepiej
clare = Player("ccl23", "5678", random.choice(locationList), 10)
playerList.append(clare)
clare.location.characters.append(clare.cid)

commandList = []

#a = threading.Condition()
addCommands = threading.Event()  # used to ensure that new commands won't be added to list during commands' analysis
sendData = threading.Event() # used to synchronize sending of updates to clients

ListenForSecondConn().start()
ApplyCommands().start()

server_ip = '127.0.0.1'
server_port = 2004
BUFFER_SIZE = 20  # Usually 1024, but we need quick response

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((server_ip, server_port))
threads = []
tcpServer.listen(4)

while True:

    print("Waiting for connections from TCP clients...")
    (conn, (ip, port)) = tcpServer.accept()
    new_thread = ClientThread(ip, port, conn)
    new_thread.start()

    
    threads.append(new_thread)
    for player in playerList:
        print(player.login)
