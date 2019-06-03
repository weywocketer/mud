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
        client2.sendall( (login + " " + myApp.getForm('MAIN').user_input.value).encode())
        myApp.getForm('MAIN').user_input.value = ""

#npyscreen.Form.set_editing()

'''
class MyTextfield(npyscreen.Textfield):
    def o
        myApp.getForm('MAIN').mainPager.values.append(myApp.getForm('MAIN').user_input.value)
        myApp.getForm('MAIN').mainPager.h_scroll_line_down(None)
        myApp.getForm('MAIN').mainPager.display()
        client2.sendall( (login + " " + myApp.getForm('MAIN').user_input.value).encode())
'''

class LoggingScreen(MyFormBaseNew):
    def create(self):
        self.login = self.add(npyscreen.TitleText, name='Name:', editable=False, value=login)
        self.nextrely += 1
        self.mainPager = self.add(npyscreen.Pager, max_height=30,
                               values=["Welcome to MUD Mud v0.1. It's great to see you! Have fun.",
                                       "Connecting to the server..."], editable=False)
        self.nextrely += 1
        self.location = self.add(npyscreen.TitleText, name='Location:', editable=False)
        self.characters = self.add(npyscreen.TitleText, name='In:', editable=False)
        self.neighbours = self.add(npyscreen.TitleText, name='Adjacent:', editable=False)
        self.nextrely += 1
        self.description = self.add(npyscreen.Pager, max_height=3, editable=False)
        self.nextrely += 1
        self.user_input = self.add(npyscreen.Textfield)

        self.set_editing(self.user_input)

    def afterEditing(self):
        self.parentApp.setNextForm(None)


#npyscreen.NPSAppManaged.

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

# try:
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
#Thread2().start()

#myApp.switchForm()

#CommandsThread().start()  # tu tworzy się drugi wątek (do wysyłania komend)


while True:  # główny wątek nasłuchuje wiadomości odświeżających od serwera (i wyświetla co trzeba)

    message = clientSocket.recv(4096).decode()

    message = message.split("\t")

    myApp.getForm('MAIN').location.value = message[0]
    myApp.getForm('MAIN').neighbours.value = message[1]
    myApp.getForm('MAIN').characters.value = message[2]
    myApp.getForm('MAIN').description.values = [message[3]]

    for i in message[4:]:
        if i != "":
            myApp.getForm('MAIN').mainPager.values.append(i)
            myApp.getForm('MAIN').mainPager.h_scroll_line_down(None)  # scroll down one line

    myApp.getForm('MAIN').display()  # refresh display






clientSocket.close()
