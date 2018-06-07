#!venv/bin/env python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/resources/scripts/multiplayer.py)

"""
from weakref import WeakKeyDictionary
import time

if False:
    # Ignore this code. It makes PyCharm happy
    # Since I call this script via execfile, PyCharm thinks
    # all the variables are undefined and gives me endless warnings :(
    from load import *
    from mainloop import *
    from funcsAndClasses import *
    from CONFIG import *
    from __main__ import *


class TCBSClient(ConnectionListener):
    """
    ConnectionListener object from PodSixNet.Connection
    """

    def __init__(self, host, port):
        log("CLIENT", "New TCBSClient at %s:%s" % (host, port))
        self.Connect((host, port))
        self.ping = time.time()
        self.lastping = 0

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
            if str(e) != "Game already full":
                c.Send({"action": "leave"})
                try:
                    connection.Pump()
                    self.Pump()
                except:
                    pass
                if selfIsHost:
                    s.shutdown()
            state = "mult-start"
            set_music("resources/sounds/menuMusic.mp3")
            set_background("resources/images/sky.png")

    def Network_kick(self, data):
        """
        Raises Exception(data["reason"]) so that we exit after we're kicked

        :param data: {"action": "kick", "reason": "xxx"}
        :rtype: None
        """
        log("CLIENT", "Was kicked because: " + data["reason"])
        raise Exception(data["reason"])

    def Network_updatesets(self, data):
        """
        Make sure the client's settings are the same as the server's

        :param data: {"action": "updatesets", "coinRR": int, "startBdgt": int}
        :rtype: None
        """
        global vCoinRR, vStartBdgt, coinsLeft, multBDict, multRDict
        global multBUnits, multRUnits, nextRID, nextBID
        if not selfIsHost:
            log("CHANNEL", "vCoinRR = %s" % str(data['coinRR']))
            log("CHANNEL", "vStartBdgt = %s" % str(data['startBdgt']))
            vCoinRR = data['coinRR']
            vStartBdgt = data['startBdgt']
        coinsLeft = [vStartBdgt, vStartBdgt]
        multBDict = {}
        multRDict = {}
        nextRID = 0
        nextBID = 0
        multBUnits = pygame.sprite.Group()
        multRUnits = pygame.sprite.Group()
        if selfIsHost:
            c.Send({"action": "updatebullets", "sentbyhost": selfIsHost, "bullets": BBullets.sprites()})
            c.Send({"action": "updateunits", "sentbyhost": selfIsHost, "units": multBUnits.sprites()})
        elif not selfIsHost:
            c.Send({"action": "updatebullets", "sentbyhost": selfIsHost, "bullets": RBullets.sprites()})
            c.Send({"action": "updateunits", "sentbyhost": selfIsHost, "units": multRUnits.sprites()})
        updatecost()

    def Network_battlestart(self, data):
        """
        Start the battle!

        :param data: {"action": "battlestart"}
        :rtype: None
        """
        global state, readyBt
        state = "mult-battle"
        readyBt = TxtOrBt(["READY", False, [0, 0, 0], [0, 255, 0]], [None, 45])
        updaterects()
        log("CLIENT", "Battle started!")

    def Network_updatebullets(self, data):
        """
        sets BBullets to pygame.sprite.Group(*data["units"]) if data["sentbyhost"]
        sets RBullets to pygame.sprite.Group(*data["units"]) otherwise


        :param data: {"action": "updateunits", "sentbyhost": bool, "bullets": [pygame.sprite.Sprite, ...]}
        :rtype: None
        """
        global BBullets, RBullets
        if data["sentbyhost"] and not selfIsHost:
            BBullets = pygame.sprite.Group(*data["bullets"])
            c.Send({"action": "updatebullets", "sentbyhost": selfIsHost, "bullets": RBullets.sprites()})
        elif not data["sentbyhost"] and selfIsHost:
            RBullets = pygame.sprite.Group(*data["bullets"])
            c.Send({"action": "updatebullets", "sentbyhost": selfIsHost, "bullets": BBullets.sprites()})

    def Network_updateunits(self, data):
        """
        sets multBUnits to pygame.sprite.Group(*data["units"]) if data["sentbyhost"]
        sets multRUnits to pygame.sprite.Group(*data["units"]) otherwise


        :param data: {"action": "updateunits", "sentbyhost": bool, "units": [pygame.sprite.Sprite, ...]}
        :rtype: None
        """
        global multRUnits, multBUnits
        if data["sentbyhost"] and not selfIsHost:
            multBUnits = pygame.sprite.Group(*data["units"])
            self.lastping = time.time() - self.ping
            c.Send({"action": "updateunits", "sentbyhost": selfIsHost, "units": multRUnits.sprites()})
            self.ping = time.time()
        elif not data["sentbyhost"] and selfIsHost:
            multRUnits = pygame.sprite.Group(*data["units"])
            self.lastping = time.time()-self.ping
            c.Send({"action": "updateunits", "sentbyhost": selfIsHost, "units": multBUnits.sprites()})
            self.ping = time.time()
        #if selfIsHost:
        #    c.Send({"action": "updateunits", "sentbyhost": selfIsHost, "units": multBUnits.sprites()})
        #elif not selfIsHost:
        #    c.Send({"action": "updateunits", "sentbyhost": selfIsHost, "units": multRUnits.sprites()})

    def Network_players(self, data):
        """
        Sets state to 'mult-placeUnits' once two people are conected

        :param data: {"action": "players", "players": len(TCBSServer.players)}
        :rtype: None
        """
        global state, updateselectedunit
        global coinRR, startBdgt
        if data["players"] == 2:
            log("CLIENT", "Starting game...")
            state = "mult-placeUnits"
            if selfIsHost:
                c.Send({"action": "updatesets",
                        "coinRR": coinRR, "startBdgt": startBdgt})
            updatecost()
            updateselectedunit(0)

    def Network_test(self, data):  # EXPIREMENTAL
        log("CLIENT", "Got test message: "+str(data))

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
        raise data['error']

    def Network_disconnected(self, data):
        """
        Raises Exception("Server disconnected") so that we exit

        :param data: {"action": "disconnected"}
        :rtype: None
        """
        log("CLIENT", "Server disconnected")
        raise Exception("Server disconnected")


class TCBSChannel(Channel):
    """
    This is the server representation of a single connected client.
    """

    def __init__(self, *args, **kwargs):
        log("CHANNEL", "New TCBSChannel at " + str(args[1]))
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        """
        Calls self._server.delplayer(self)
        (Deletes self from self._server.players)

        :rtype: None
        """
        if self in self._server.players:
            log("CHANNEL", "Closing channel...")
            self._server.delplayer(self)
            self._server.Pump()
        else:
            log("CHANNEL", "Cannot close Channel: Channel already closed!")

    def Network_leave(self, data):
        """
        Calls self._server.shutdown()

        :param data: {"action": "leave"}
        :rtype: None
        """
        log("CHANNEL", "Shutting down server...")
        self._server.shutdown()

    def Network_kick(self, data):
        """
        Raises Exception(data["reason"]) so that we exit after we're kicked

        :param data: {"action": "kick", "reason": "xxx"}
        :rtype: None
        """
        log("CHANNEL", "Was kicked because: " + data["reason"])
        raise Exception(data["reason"])

    def Network_test(self, data):  # EXPIREMENTAL
        log("CHANNEL", "Forwarding test message to all clients: " + str(data))
        self._server.sendtoall(data)

    def Network_updatebullets(self, data):
        """
        Forwards message to client(s)

        :param data: {"action": "updatebullets", "sentbyhost": bool, "bullets": [pygame.sprite.Sprite, ...]}
        :rtype: None
        """
        self._server.sendtoall(data)

    def Network_updateunits(self, data):
        """
        Forwards message to client(s)

        :param data: {"action": "updateunits", "sentbyhost": bool, "units": [pygame.sprite.Sprite, ...]}
        :rtype: None
        """
        #log("CHANNEL", "TCBSChannel.Network_updateunits(%r, %r) has been called" % (self, data))
        self._server.sendtoall(data)

    def Network_updatesets(self, data):
        """
        Make sure the client's settings are the same as the server's

        :param data: {"action": "updatesets", "coinRR": int, "startBdgt": int}
        :rtype: None
        """
        global vCoinRR, vStartBdgt, coinsLeft, multBDict, multRDict
        global multBUnits, multRUnits, nextBID, nextRID
        if not selfIsHost:
            log("CHANNEL", "vCoinRR = %s" % str(data['coinRR']))
            log("CHANNEL", "vStartBdgt = %s" % str(data['startBdgt']))
            vCoinRR = data['coinRR']
            vStartBdgt = data['startBdgt']
        coinsLeft = [vStartBdgt, vStartBdgt]
        multBDict = {}
        multRDict = {}
        nextRID = 0
        nextBID = 0
        multBUnits = pygame.sprite.Group()
        multRUnits = pygame.sprite.Group()
        updatecost()
        #if selfIsHost:
        #    c.Send({"action": "updateunits", "sentbyhost": selfIsHost, "units": multBUnits.sprites()})
        #elif not selfIsHost:
        #    c.Send({"action": "updateunits", "sentbyhost": selfIsHost, "units": multRUnits.sprites()})
        self._server.sendtoall(data)

    def Network_ready(self, data):
        """
        Handle ready requests

        :param data: {"action": "ready"}
        :rtype: None
        """
        global state
        self._server.playersready += 1
        log("CHANNEL", "%s of 2 players ready" % str(self._server.playersready))
        if self._server.playersready > 1:
            state = "mult-battle"
            self._server.sendtoall({"action": "battlestart"})
            self._server.playersready = 0
            log("BATTLE", "Starting battle...")

    def Network_players(self, data):
        """
        Sets state to 'mult-placeUnits' once two people are conected

        :param data: {"action": "players", "players": len(self._server.players)}
        :rtype: None
        """
        global state, coinRR, startBdgt
        if data["players"] == 2:
            log("CHANNEL", "Starting game...")
            state = "mult-placeUnits"
            if selfIsHost:
                c.Send({"action": "updatesets",
                        "coinRR": coinRR, "startBdgt": startBdgt})
            updatecost()
            updateselectedunit(0)


class TCBSServer(Server):
    """
    Server object from PodSixNet.Server
    """
    channelClass = TCBSChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        log("SERVER", "New TCBSServer at "+str(self.addr))
        self.playersready = 0
        self.players = WeakKeyDictionary()
        log("SERVER", "Waiting for players...")

    def Connected(self, channel, addr):
        """
        Add channel to a WeakKeyDictionary once they're connected

        :type channel: instance
        :type addr: tuple
        :rtype: None
        """
        if len(self.players) < 2:
            self.addplayer(channel)
        else:
            log("SERVER", "Kicked Player%s because Game already full" % str(addr))
            channel.Send({"action": "kick", "reason": "Game already full"})

    def addplayer(self, player):
        """
        Add player to a WeakKeyDictionary
        Kicks new player if two other players are already connected

        :type player: instance
        :rtype: None
        """
        log("SERVER", "New Player" + str(player.addr))
        self.players[player] = True
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
            if str(e) != "Game already full":
                c.Send({"action": "leave"})
                try:
                    self.Pump()
                except:
                    pass
                if selfIsHost:
                    s.shutdown()
            state = "mult-start"
            set_music("resources/sounds/menuMusic.mp3")
            set_background("resources/images/sky.png")
