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

    def move(self):
        print(self.location.description)  # (client)

        command = unpolish(input("Co robisz? ")).split()
        if command[0] == "idz":
            if command[1] in self.location.neighbours:
                self.location.characters.pop(self.cid)  # server
                self.location = location_dict[command[1]]
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
            pass


class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.neighbours = []
        self.objects = []
        self.characters = []


class Object:  # zły pomysł - Object
    def __init__(self):
        self.name = name


class Word:
    def __init__(self, mian, dop, cel, bier, narz, miej, wol):
        pass

class PlayerList(list):
    def __contains__(self, item):
        logins = [i.login for i in self]
        if item in logins:
            return True
        else:
            return False


#--------------networking section here---------------------

class ClientThread(threading.Thread):

    def __init__(self, ip, port, conn):
        threading.Thread.__init__(self)
        self.i = random.random()
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
        new_player = Player(login, password, las, 10)
        players.append(new_player)
        self.bind_player(new_player)
        self.conn.sendall(b"0")  # player successfully created


        for player in players:
            print(player.login)

    def login(self):
        login_data = self.conn.recv(4096).decode().split()
        login = login_data[0]
        password = login_data[1]
        if login in players:
            for player in players:
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
            pass

            #time.sleep(2)
            #self.conn.sendall(str("a").encode())





players = PlayerList()
idC = 0
las = Location("las", "Znajdujesz się w ciemnym, ponurym lesie.")
glaz = Location("głaz", "Znajdujesz się w szarym, ponurym głazie.")
jon = Player("potWilk", "1234", las, 14)
players.append(jon)
las.characters.append(jon.cid)
las.neighbours.append(unpolish(glaz.name))
clare = Player("ccl23", "5678", glaz, 10)
players.append(clare)
glaz.characters.append(clare.cid)
a = "idz glaz"
location_dict = {"las": las, "glaz": glaz}  # tymczasowo słownik


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
    for player in players:
        print(player.login)



'''    
import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'
x2 = '[34, 17, "bill"]'
# parse x:
y = json.loads(x)
y2 = json.loads(x2)

# the result is a Python dictionary:
print(y["age"])
'''
