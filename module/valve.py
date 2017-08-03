#!/usr/bin/env python3.6
#Bot Gerbouille Discord/ARK
#France-Evolved https://discord.gg/gVsveNY
#2017 By YotaSky https://github.com/YotaSky

import valve.source.a2s

def request(message, port):
    server = valve.source.a2s.ServerQuerier(address=('127.0.0.1', port), timeout = 5.0)
    name = server.info()["server_name"].format(message)    
    return name

def map(message, port):
    server = valve.source.a2s.ServerQuerier(address=('127.0.0.1', port), timeout = 5.0)
    map = server.info()["map"].format(message)    
    return map

def ping(message):
    msg = str(server.ping()).format(message)
    return msg

def status(message):
    server = valve.source.a2s.ServerQuerier(address=('127.0.0.1', 27015), timeout = 5.0)
    name = server.info()["server_name"].format(message)
    map = server.info()["map"].format(message)
    game = server.info()["game"].format(message)
    pl_count = server.info()["player_count"]
    pl_max = server.info()["max_players"]
    return "%s / %s / %s / %i / %s"%(name,map,game,pl_count,pl_max)
