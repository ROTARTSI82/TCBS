#!venv/bin/env python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/resources/scripts/multiplayer.py)
------------------------------------------------------------------------
TOTALLY CUSTOMIZABLE BATTLE SIMULATOR a21.18.04.14
------------------------------------------------------------------------
By Grant Yang

Totally Customizable Battle Simulator is a multiplayer
strategy videogame. You can design and program your
own soldiers and make them fight against your
friend's soldiers. It is inspired by Totally Accurate
Battle Simulator by Landfall and uses Pygame 1.9 and
Python 2.7. TCBS uses PodSixNet written by chr15m (Chris McCormick).

SEE README.md FOR MORE DETAILS
"""
from weakref import WeakKeyDictionary

if False:
    # Ignore this code. It makes PyCharm happy
    # Since I call this script via execfile, PyCharm thinks
    # all the variables are undefined and gives me endless warnings :(
    from load import *
__appName__ = "Totally Customizable Battle Simulator"
__version__ = "a21.18.04.15"
__author__ = "Grant Yang"


class TCBSClient(ConnectionListener):
    """
    ConnectionListener object from PodSixNet.Connection
    """

    def __init__(self, host, port):
        self.Connect((host, port))

    def loop(self):
        """
        Is called every tick to update connection

        :rtype: None
        """
        global selfIsHost, c, s, state, serverMsg
        global log, TxtOrBt, set_music
        global screen, connection
        try:
            connection.Pump()
            self.Pump()
        except Exception as e:
            log("EXCEPTION", "Cannot Pump: " + str(e))
            serverMsg = TxtOrBt([str(e), False, [255, 0, 0]], [None, 45])
            serverMsg.rect.center = [screen.get_width() / 2,
                                     screen.get_height() / 2 - 45]
            c.Send({"action": "leave"})
            try:
                connection.Pump()
                self.Pump()
            except:
                pass
            if selfIsHost:
                s.shutdown()
            state = "mult-start"
            set_music("resources/sounds/menuMusic.wav")

    def Network_kick(self, data):
        """
        Raises Exception(data["reason"]) so that we exit after we're kicked

        :param data: {"action": "kick", "reason": "xxx"}
        :rtype: None
        """
        log("CHANNEL", "Was kicked because: " + data["reason"])
        del self
        raise Exception(data["reason"])

    def Network_players(self, data):
        """
        Sets state to 'mult-placeUnits' once two people are conected

        :param data: {"action": "players", "players": len(TCBSServer.players)}
        :rtype: None
        """
        global state
        if data["players"] == 2:
            log("CLIENT", "Starting game...")
            state = "mult-placeUnits"
            updateselectedunit(0)

    def Network_test(self, data):  # EXPIREMENTAL
        print(data['test'])

    def Network_connected(self, data):
        """
        Log that we connected!

        :param data: {"action": "connected"}
        :rtype: None
        """
        log("CLIENT", "Client connected to the server successfully")

    def Network_error(self, data):
        """
        Raises the exception in data["error"] so that we exit

        :param data: {"action": "error", "error": Exception("xxx")}
        :rtype: None
        """
        log("EXCEPTION", "Error: " + str(data['error']))
        del self
        raise data['error']

    def Network_disconnected(self, data):
        """
        Rases Exception("Server disconnected") so that we exit

        :param data: {"action": "disconnected"}
        :rtype: None
        """
        log("CLIENT", "Server disconnected")
        del self
        raise Exception("Server disconnected")


class TCBSChannel(Channel):
    """
    This is the server representation of a single connected client.
    """

    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        """
        Calls self._server.delplayer(self)
        (Delets self from self._server.players)

        :rtype: None
        """
        self._server.delplayer(self)
        self.loop()

    def loop(self):
        """
        Is called every tick to update connection

        :rtype: None
        """
        global state, c, s, selfIsHost, serverMsg
        global log, TxtOrBt, set_music
        global screen
        try:
            self.Pump()
        except Exception as e:
            log("EXCEPTION", "Cannot Pump: " + str(e))
            serverMsg = TxtOrBt([str(e), False, [255, 0, 0]], [None, 45])
            serverMsg.rect.center = [screen.get_width() / 2,
                                     screen.get_height() / 2 - 45]
            c.Send({"action": "leave"})
            try:
                c.loop()
            except:
                self._server.shutdown()
            if selfIsHost:
                s.shutdown()
            state = "mult-start"
            set_music("resources/sounds/menuMusic.wav")

    def Network_leave(self, data):
        """
        Calls self._server.shutdown()

        :param data: {"action": "leave"}
        :rtype: None
        """
        self._server.shutdown()

    def Network_kick(self, data):
        """
        Raises Exception(data["reason"]) so that we exit after we're kicked

        :param data: {"action": "kick", "reason": "xxx"}
        :rtype: None
        """
        log("CHANNEL", "Was kicked because: " + data["reason"])
        self.Close()
        del self
        raise Exception(data["reason"])

    def Network_test(self, data):  # EXPIREMENTAL
        print(data['test'])
        self._server.sendtoall(data)

    def Network_players(self, data):
        """
        Sets state to 'mult-placeUnits' once two people are conected

        :param data: {"action": "players", "players": len(self._server.players)}
        :rtype: None
        """
        global state
        if data["players"] == 2:
            log("CHANNEL", "Starting game...")
            state = "mult-placeUnits"
            updateselectedunit(0)


class TCBSServer(Server):
    """
    Server object from PodSixNet.Server
    """
    channelClass = TCBSChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        log("SERVER", "Server launched. Waiting for players...")

    def Connected(self, channel, addr):
        """
        Add channel to a WeakKeyDictionary once they're connected

        :type channel: instance
        :type addr: tuple
        :rtype: None
        """
        self.addplayer(channel)

    def addplayer(self, player):
        """
        Add player to a WeakKeyDictionary
        Kicks new player if two other players are already connected

        :type player: instance
        :rtype: None
        """
        log("SERVER", "New Player" + str(player.addr))
        self.players[player] = True
        if len(self.players) > 2:
            player.Send({"action": "kick", "reason": "Game already full"})
            log("SERVER", "Kicked Player" + str(player.addr))
            self.delplayer(player)
        self.sendplayers()

    def delplayer(self, player):
        """
        Delete player from WeakKeyDictionary
        Checks if player exists

        :type player: instance
        :rtype: None
        """
        if player in self.players:
            log("SERVER", "Deleting Player" + str(player.addr))
            del self.players[player]
        else:
            log("SERVER", "Cannot delete player: Player doesn't exist!")
        self.sendplayers()

    def sendplayers(self):
        """
        Send some info about self.players to connected clients

        :rtype: None
        """
        log("SERVER", str(len(self.players)) + " player(s) connected")
        self.sendtoall({"action": "players", "players": len(self.players)})

    def sendtoall(self, data):
        """
        Send data to all connected clients

        :param data: {"action": "xxx", ...}
        :rtype: None
        """
        [p.Send(data) for p in self.players]

    def shutdown(self):
        """
        Kicks all clients because "Opponent Disconnected"

        :rtype: None
        """
        log("SERVER", "Shutting down...")
        self.sendtoall({"action": "kick", "reason": "Opponent Disconnected"})
        self.loop()

    def loop(self):
        """
        Is called every tick to update connection

        :rtype: None
        """
        global selfIsHost, c, s, state, serverMsg
        global log, TxtOrBt, set_music
        global screen
        try:
            self.Pump()
        except Exception as e:
            log("EXCEPTION", "Cannot Pump: " + str(e))
            serverMsg = TxtOrBt([str(e), False, [255, 0, 0]], [None, 45])
            serverMsg.rect.center = [screen.get_width() / 2,
                                     screen.get_height() / 2 - 45]
            c.Send({"action": "leave"})
            try:
                self.loop()
            except:
                pass
            if selfIsHost:
                s.shutdown()
            state = "mult-start"
            set_music("resources/sounds/menuMusic.wav")
