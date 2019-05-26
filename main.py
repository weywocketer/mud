#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 10:23:11 2019

@author: weywocketer
"""
import unidecode


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


if __name__ == "__main__":
    idC = 0
    las = Location("las", "Znajdujesz się w ciemnym, ponurym lesie.")
    glaz = Location("głaz", "Znajdujesz się w szarym, ponurym głazie.")
    jon = Player("potWilk", "1234", las, 14)
    las.characters.append(jon.cid)
    las.neighbours.append(unpolish(glaz.name))
    clare = Player("ccl23", "5678", glaz, 10)
    glaz.characters.append(clare.cid)
    a = "idz glaz"
    location_dict = {"las": las, "glaz": glaz}  # tymczasowo słownik
    
    
    
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
# from pc
