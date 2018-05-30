(.../TCBS/README.md)
------------------------------------------------------------------------
TOTALLY CUSTOMIZABLE BATTLE SIMULATOR

By Grant Yang

Totally Customizable Battle Simulator is a multiplayer strategy video game.
You can design and program your own soldiers and make them fight against your
friend's soldiers.

HOW TO RUN (MacOS):

   1. Download and unzip TCBS.zip
   2. Double-click on TCBS-Launcher.app
   
HOW TO RUN (Linux):
   1. Download and unzip TCBS.zip __ON YOUR DESKTOP__
   2. Open terminal
   3. Run the following commands:
    
    cd ~/Desktop/TCBS
    venv/bin/python __main__.py

Wiki: https://github.com/ROTARTSI82/TCBS/wiki

TCBS is inspired by Totally Accurate Battle Simulator
by Landfall. It uses Pygame 1.9 and Python 2.7 but
still works in Python 3. TCBS uses PodSixNet
written by chr15m (Chris McCormick).

TCBS uses PodSixNet for python3.4 by tborisova (Tsvetelina Borisova)
so that some multiplayer features work in Python 3.
Trying to connect to a Python 3 server using Python 2
(And vice versa) will result in an exception.
