(.../TCBS/README.txt)
------------------------------------------------------------------------
TOTALLY CUSTOMIZABLE BATTLE SIMULATOR i21.18.03.31
------------------------------------------------------------------------
By Grant Yang

This application is designed to run using Python 2.7 and 
Pygame 1.9. Trying to run this application using any other 
version of Python or Pygame will likely result in
an Exception or game-breaking bugs.

HOW TO USE:
    1. Install Python 2.7 at www.python.org
    2. Install Pygame 1.9 at www.pygame.org
        -OR run one of the commands:
            "pip install pygame"
            "pip install upgrade pygame"
    2. Run __main__.py
    3. Enjoy!

Totally Customizable Battle Simulator is a multiplayer 
strategy videogame. You can design and program your 
own soldiers and make them fight against your
friend's soldiers. It is inspired by Totally Accurate
Battle Simulator by Landfall and requires Pygame 1.9 and
Python 2.7. TCBS uses PodSixNet written by chr15m (Chris McCormick).

I attempted to make this app compatible with Python 3, but
there will be some unexpected behaviour. I used 
PodSixNet for python3.4 by tborisova (Tsvetelina Borisova)
so that some multiplayer features work in Python 3.
Trying to connect to a Python 3 server using Python 2
(And vice versa) will result in an exception.

If pygame is not installed, Totally Customizable Battle
Simulator will try to install and uprade pygame for you.

If the game crashes, it will try to mail a crash report
to me so that I could fix it.
