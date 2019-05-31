import socket
import threading
import npyscreen
import time

# ----------------TUI section here------------------------------

class TuiThread(threading.Thread):
    def run(self):
        myApp.run()

class MyFormBaseNew(npyscreen.FormBaseNew):  # my subclass of FormBaseNew
    def while_editing(self, *args, **keywords):
        myApp.getForm('MAIN').mainPager.values.append(myApp.getForm('MAIN').user_input.value)
        myApp.getForm('MAIN').mainPager.display()
        client2.sendall( (login + " " + myApp.getForm('MAIN').user_input.value).encode())

class LoggingScreen(MyFormBaseNew):
    def create(self):
        self.mainPager = self.add(npyscreen.Pager, name='myPager', max_height=25, editable=True,
                               values=["Welcome to MUD Mud v0.1. It's great to see you! Have fun.",
                                       "Connecting to the server..."])
        self.myName = self.add(npyscreen.TitleText, name='Name', editable=False, value=login)
        self.user_input = self.add(npyscreen.Textfield, value="...")

    def afterEditing(self):
        self.parentApp.setNextForm(None)


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        #npyscreen.setTheme(npyscreen.Themes.DefaultTheme)
        self.addForm('MAIN', LoggingScreen, name='MUD Mud v0.1')



# ---------------networking----------------------------------------

class CommandsThread(threading.Thread):

    def run(self):
        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2.connect((ip, port + 1))

        while True:

            #myApp.getForm('MAIN').user_input.when_value
            '''
            command = (login + " " + input(">: ")).encode()
            client2.sendall(command)
            print("Command sent.")
            '''



myApp = MyApplication()


print("Welcome to MUD Mud v0.1. It's great to see you! Have fun.")
# ip = input("Enter your's server IP address: ")
# port = int(input("Enter your's server port: "))
ip = "127.0.0.1"
port = 2004
print("Connecting to the server...")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


clientSocket.connect((ip, port))

while True:
    print('3')
    decision = input("0 - register, 1 - login ")
    if decision == "0":
        clientSocket.sendall(b"0")
        login = input("Choose your login: ")
        password = input("Choose your password: ")
        # TODO: add login and passwd validation
        clientSocket.sendall((login + " " + password).encode())
        response = clientSocket.recv(4096)
        if response == b"0":
            print("Account created successfully. Great!")
            break
        elif response == b"1":
            print("Cannot create account. Try using a different login...")
    elif decision == "1":
        clientSocket.sendall(b"1")
        login = input("Enter your login: ")
        password = input("Enter your password: ")
        clientSocket.sendall((login + " " + password).encode())
        response = clientSocket.recv(4096)
        if response == b"0":
            print("Login successful. Great!")
            break
        elif response == b"1":
            print("Login failed - wrong login or password.")
        elif response == b"2":
            print("Login failed - someone is logged in.")
        else:
            print("weird thing...")


client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client2.connect((ip, port + 1))

TuiThread().start()
time.sleep(1)


while True:  # główny wątek nasłuchuje wiadomości odświeżających od serwera (i wyświetla co trzeba)

    data = clientSocket.recv(4096).decode()
    myApp.getForm('MAIN').mainPager.values.append(data)
    myApp.getForm('MAIN').mainPager.display()  # refresh display
    #print(data)


