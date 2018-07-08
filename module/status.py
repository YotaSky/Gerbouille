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
        x.settimeout(10)
        return x.connect_ex((config['IPserver'],int(config['RCONPort'])))

    def servers(self, message, listview=True):
        listmap = []
        namemap = []
        num = 0
        for conf in self.etcconf:
            num += 1
            config = self.extract(os.path.join(os.path.sep,self.folder,conf))
            if self.checkrcon(config) != 0:
                up = '**Offline**'
            else:
                up = '<Online>'
            name = valve.request(message, config['IPserver'], int(config['QueryPort']))
            listmap.append('{}. {} {}\n'.format(num,name,up))
            namemap.append(conf.split('.')[0])
        if listview: 
            txt = '```markdown\n#Liste des instances ARK (http://www.france-evolved.fr)\n{}\n```'.format(''.join(listmap))
            return txt

    def instances(self, message, admin=False):
        """Liste des joueurs sur les instances ARK
        Recuperation de la liste des joueurs par map
        - Verification de l'etat online/hors line
        - Composition de la liste joueurs"""
        num = 0
        info = []
        for conf in self.etcconf:
            num += 1
            config = self.extract(os.path.join(os.path.sep,self.folder,conf))
            if self.checkrcon(config) != 0:
                up = b'**Offline**'
            else:
                up = b'<Online>'
            #request = valve.request(message, int(config['QueryPort']))
            request = valve.request(message, config['IPserver'], int(config['QueryPort']))
            rcon = srcds.SourceRcon(config['IPserver'], int(config['RCONPort']), config['ServerAdminPassword'], 5)
            ipaddress = socket.gethostbyname(socket.gethostname())
            connect = 'steam://connect/194.177.58.120:{}'.format(config['QueryPort'])
            listplayers = []
            players = rcon.rcon("listplayers").decode("utf-8")
            if players.find('No Players Connected') < 0:
                for i in players.split('\n'):
                    if len(i) > 1:
                        listplayers.append(i.split(',')[0].split('. ',1)[1])
                lst = ' ('+', '.join(listplayers)+')'
            else: 
                lst = ''
            #info.append('**{}** ({} ms - {}): {} survivant(s) en ligne {}\n'.format(config['SessionName'], round(float(ping)), version, str(len(listplayers)), lst))
            if admin is True:
                info.append('{}. **{}** {} survivant(s) en ligne\n```'.format(num,request, str(len(listplayers))))
            else:
                info.append('**{}** ({}): {} survivant(s) en ligne {}\n'.format(request, connect, str(len(listplayers)), lst))
            txt = '```markdown\n#Liste des instances ARK\n{}\n```'.format(''.join(info))
        return txt