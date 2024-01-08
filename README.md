# Multi-User Dungeon game prototype
## Overview
Prototype of a platform for the text-based multiplayer game, created using Python.
- Clients can interact with the world by sending player commands to the server.
- In fixed intervals, server sends updated world information to clients.
- Communication based on TCP protocol — due to relatively wide server fixed intervals, higher packet delays are not a big concern.
- Multithreading is used to handle multiple server connections.
- Clients use text-based user interface (TUI) created with npyscreen library.

Repository contains .pdf file with presentation (in Polish) describing the base concepts of the project.

## Usage
Tested with Python 3.9<br>
Required libraries: windows-curses (on Windows), npyscreen

Launch instructions:
1. Run the server (mudServer.py)
2. Run clients (mudClient.py) — make sure that the terminal window in which client is run is quite large (as the Text User Interface will open in this window), otherwise the app will crash.

In game, player can use the following commands:<br>
move [destination name] — move to adjacent location<br>
shout [message] — send message visible to all players present at your location<br>
say [target name] [message] — send message to specific player present at your location
