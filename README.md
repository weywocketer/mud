# Multi-User Dungeon game prototype for the High-level Programming Languages class

Repository contains .pdf file with presentation (in Polish) describing the base concepts of the project.

Tested with Python 3.9<br />
Required libraries: npyscreen, windows-curses (on Windows)

Launch instructions:
1. Run the server (mudServer.py)
2. Run clients (mudClient.py) — make sure that the terminal window in which client is run is quite large (as the Text User Interface will open in this window), otherwise the app will crash.

In game, player can use the following commands:<br />
move [destination name] — move to adjacent location<br />
shout [message] — send message visible to all players present at your location<br />
say [target name] [message] — send message to specific player present at your location
