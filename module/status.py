#!/usr/bin/env python3.6
#Bot Gerbouille Discord/ARK
#France-Evolved https://discord.gg/gVsveNY
#2017 By YotaSky https://github.com/YotaSky

import os
import socket
import discord

from module import srcds
from module import valve

class Status: # Définition des méthodes de fonction de Gerbouille
    """Classe regroupant les fonction d'information de notre Gerbouille, à savoir:
    - Liste des serveurs
    - Liste des joueurs
    - Informations diverses"""

    def __init__(self): # Construction des variables
        """Encore quelques attributs statique à rendre dynamique ou en fichier de conf """
        self.folder = os.path.join(os.path.sep,'etc','gerbouille')
        self.message = []
        self.client = discord.Client()
        
        #Recuperation des fichiers de configuration d'instance
        self.etcconf = []
        for i in os.listdir(self.folder):
            if i.endswith('.cfg'):
                self.etcconf.append(i)

    def extract(self, path):
        """Recuperation des attributs du fichier de configuration des instances"""
        extract={}
        with open(path, 'r') as data:
            for line in data.readlines():
                li = line.lstrip()
                if not li.startswith("#") and '=' in li:
                    extract[line.split('=')[0]] = line.split('=')[1].strip()
        return extract

    def checkrcon(self, config):
        """Fonction de vérification si instance en ligne via port TCP RCON"""
        x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return x.connect_ex((config['IPserver'],int(config['RCONPort'])))

    def servers(self, listview=True):
        listmap = []
        namemap = []
        for conf in self.etcconf:
            config = self.extract(os.path.join(os.path.sep,self.folder,conf))
            if config['Enable'] == "True":
                enable = 'by Gerbouille'
            else:
                enable = 'by ArkTools'
            if config['Protect'] == "True":
                protect = ' and Lock'
            else:
                protect = ''
            if self.checkrcon(config) != 0:
                up = 'Offline'
            else:
                up = 'Online'
            name = config['SessionName']
            listmap.append('**!{}** {} - {} - **{}** {}\n'.format(conf.split('.')[0],enable,name,up,protect))
            namemap.append(conf.split('.')[0])
        print(listmap)
        if listview: 
            txt = '```markdown\n{}\n{}```'"#Liste des instances ARK (http://www.france-evolved.fr)".format(''.join(listmap))
            return txt

    def players(self,message):
        """Liste des joueurs sur les instances ARK
        Recuperation de la liste des joueurs par map
        - Verification de l'etat online/hors line
        - Composition de la liste joueurs"""
        info = []
        for conf in self.etcconf:
            config = self.extract(os.path.join(os.path.sep,self.folder,conf))
            if self.checkrcon(config) != 0:
                continue
            name = valve.map(message, int(config['QueryPort']))
            rcon = srcds.SourceRcon(config['IPserver'], int(config['RCONPort']), config['ServerAdminPassword'], 5)
            version = valve.version(message, int(config['QueryPort']))
            listplayers = []
            players = rcon.rcon("listplayers").decode("utf-8")
            if players.find('No Players Connected') < 0:
                for i in players.split('\n'):
                    if len(i) > 1:
                        listplayers.append(i.split(',')[0].split('. ',1)[1])
                lst = ' ('+', '.join(listplayers)+')'
            else: 
                lst = ''
            info.append('**{}**: {} survivant(s) en ligne {}\n'.format(config['SessionName'], str(len(listplayers)), lst))
            #info.append('**{} - ({})**: {} survivant(s) en ligne {}\n'.format(config['SessionName'], version, str(len(listplayers)), lst))
        return ''.join(info)