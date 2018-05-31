(.../TCBS/README.md)
------------------------------------------------------------------------
TOTALLY CUSTOMIZABLE BATTLE SIMULATOR

By Grant Yang

Totally Customizable Battle Simulator is a multiplayer strategy video game.
You can design and program your own soldiers and make them fight against your
friend's soldiers.

HOW TO RUN (MacOS):

   1. Download the latest release of TCBS and unzip it.
   2. Run __TCBS-Launcher__ by double-clicking on it.
       - NOTE: __TCBS-Launcher__ could be found in the TCBS folder
   
HOW TO RUN (Linux):
   1. Download the latest release of TCBS and unzip it.
   2. Open terminal
   3. Change the directory to the data folder inside the TCBS folder.

    cd ~/TCBS/data

   4. Run `__main__.py` using the virtual environment

    venv/bin/python __main__.py

TCBS is inspired by Totally Accurate Battle Simulator
by Landfall. It uses Pygame 1.9 and Python 2.7 but
still works in Python 3. TCBS uses PodSixNet
written by chr15m (Chris McCormick).

TCBS uses PodSixNet for python3.4 by tborisova (Tsvetelina Borisova)
so that some multiplayer features work in Python 3.
Trying to connect to a Python 3 server using Python 2
(And vice versa) will result in an exception.
