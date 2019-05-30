import socket
import threading
import npyscreen


# ----------------TUI section here------------------------------

class LoggingScreen(npyscreen.FormBaseNew):
    def create(self):
        self.myName = self.add(npyscreen.Pager, name='myPager', max_height=25,
                               values=["Welcome to MUD Mud v0.1. It's great to see you! Have fun.",
                                       "Connecting to the server..."])
        # self.myDepartment  = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3,
        #                             name='Department', values = ['Department 1', 'Department 2', 'Department 3'])
        # self.myDate        = self.add(npyscreen.TitleDateCombo, name='Date Employed')
        self.user_input = self.add(npyscreen.Textfield)
        # self.user_input2 = self.add(npyscreen.Autocomplete)

    def afterEditing(self):
        self.parentApp.setNextForm(None)


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.DefaultTheme)
        self.addForm('MAIN', LoggingScreen, name='MUD Mud v0.1')


# ---------------networking----------------------------------------

class CommandsThread(threading.Thread):

    def run(self):
        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2.connect((ip, port + 1))

        while True:
            command = input(">: ").encode()
            print("Command sent.")
            client2.sendall(command)


MyApplication().run()

print("Welcome to MUD Mud v0.1. It's great to see you! Have fun.")
# ip = input("Enter your's server IP address: ")
# port = int(input("Enter your's server port: "))
ip = "127.0.0.1"
port = 2004
print("Connecting to the server...")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# clientSocket.connect((ip, port))

# try:
clientSocket.connect((ip, port))

while True:
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

print(login)

CommandsThread().start()  # tu tworzy się drugi wątek (do wysyłania komend)

while True:  # główny wątek nasłuchuje wiadomości odświeżających od serwera (i wyświetla co trzeba)
    data = clientSocket.recv(4096).decode()
    print(data)

clientSocket.close()

# except:
#   print("lipa")
