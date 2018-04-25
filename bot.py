#!/usr/bin/python3.5

import sys
import socket

class Bot:

    sys.path[0] += "/plugins"
    d_plugins = {}
    d_load = {}

    def __init__(self, server, port, channel, user, nick):

        self.channel = channel

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server, port))

        self.s.send(("USER %s 0 *: %s\r\n" % (user, user)).encode())
        self.s.send(("NICK %s\r\n" % nick).encode())
        self.s.send(("JOIN %s\r\n" % channel).encode())

        while True:

            self.data = self.s.recv(4096)

            if self.data.find(b'PING') != -1:
                self.pong()
            if self.data.find(b'!load') != -1:
                self.loadPlugin((self.data.split(b"!load ")[1])[:-2])
            if self.data.find(b'!unload ') != -1:
                self.unloadPlugin((self.data.split(b"!unload ")[1])[:-2])
            if self.data.find(b'@mariobot') != -1:
                self.searchPlugin(self.data, self.d_load)

            print(self.data)  ### debugging purpose - commenting/deleting this line won't affect functionality ###

    def pong(self):

        self.s.send(("PONG %s \r\n" % (self.data.split()[1])).encode())
        self.s.send(("JOIN %s\r\n" % self.channel).encode())

    def loadPlugin(self, plugin):

        if plugin in self.d_plugins.keys():
            self.s.send(("PRIVMSG %s :Plugin %s has been loaded already.\r\n" % (self.channel, plugin)).encode())
        else:
            try:
                plug = __import__(plugin.decode(), globals(), locals(), ['control', 'main'])
                self.d_load[plug.control()] = plug.main
                self.d_plugins[plugin] = plug.control()
                self.s.send(("PRIVMSG %s :Plugin successfully loaded.\r\n" % self.channel).encode())
            except:
                self.s.send(("PRIVMSG %s :Failed to load plugin.\r\n" % self.channel).encode())

    def unloadPlugin(self, plugin):

        if plugin in self.d_plugins.keys():
            del self.d_load[self.d_plugins[plugin]]
            del self.d_plugins[plugin]
            self.s.send(("PRIVMSG %s :Plugin successfully unloaded.\r\n" % self.channel).encode())
        else:
            self.s.send(("PRIVMSG %s :Failed to unload plugin: no plugin named %s is currently loaded.\r\n" % (self.channel, plugin)).encode())

    def searchPlugin(self, string, dic):

        argList = [self.s, self.channel, self.data]

        for i in dic.keys():
            if string.find(i.encode()) != -1:
                startPlugin = dic[i]
                startPlugin(argList)


if __name__ == '__main__':

    Bot("irc.freenode.net", 6667, "#personale", "SuperMarioBot", "SuperMarioBot")