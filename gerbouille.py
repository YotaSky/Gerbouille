#!/usr/bin/python3

from module import scraping
from disco.bot import Bot, Plugin

class Gerbouille(Plugin):
    @Plugin.command('insulte')
    def on_insulte_command(self, event):
        event.msg.reply(scraping.insultron())

    #@Plugin.command('info')
    #def on_info_command(self, event):
    #    event.msg.reply(status.players())

    # Which includes command argument parsing
    #@Plugin.command('echo', '<content:str...>')
    #def on_echo_command(self, event, content):
    #    event.msg.reply(content)
