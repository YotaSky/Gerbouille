#!/usr/bin/python3

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

    def players(self,message):
        """Liste des joueurs sur les instances ARK"""
        #Recuperation des fichiers de configuration d'instance
        allconf = []
        for i in os.listdir(self.folder):
            if i.endswith('.cfg'):
                allconf.append(i)

        info = []
        for conf in allconf:
            config = self.extract(os.path.join(os.path.sep,self.folder,conf))
            if self.checkrcon(config) != 0:
                continue
            name = valve.map(message, int(config['QueryPort']))
            rcon = srcds.SourceRcon(config['IPserver'], int(config['RCONPort']), config['ServerAdminPassword'], 5)
            listplayers = []
            players = rcon.rcon("listplayers").decode("utf-8")
            if players.find('No Players Connected') < 0:
                for i in players.split('\n'):
                    if len(i) > 1:
                        listplayers.append(i.split(',')[0].split('. ',1)[1])
                lst = ' ('+', '.join(listplayers)+')'
            else: 
                lst = ''
            print('**{}**: {} survivant(s) en ligne {}'.format(config['SessionName'], str(len(msg)), lst))
            allconf.append(listplayers)

        return 