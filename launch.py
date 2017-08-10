#!/usr/bin/env python3.6
#Bot Gerbouille Discord/ARK
#France-Evolved https://discord.gg/gVsveNY
#2017 By YotaSky https://github.com/YotaSky

import discord
import csv
import asyncio
import socket
import datetime
import os
from daemon import runner
import daemon

from module import valve
from module import srcds
from module import scraping
from module.CmdServer import CmdServer

folder = '/etc/gerbouille/'
token = open(folder+'token')
host = '127.0.0.1'
client = discord.Client()

class Test:
    def run(self):
        client.run(open('/etc/gerbouille/token').read().replace('\n',''))

def auth(message):
    file = open("/etc/gerbouille/users")
    try:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == message.author.id:
                return row
    finally:
        file.close()
    
@client.event
async def on_ready():
    print('Connexion')
    print(client.user.name)
    print(client.user.id)
    print ('------')

def logger(message, command):
    date = datetime.datetime.now()
    print (str(date)+": " +message.author.name+" used command: "+command)

def config(cfg):
    extract = {}
    with open(cfg, 'r') as f:
        for line in f.readlines():
            li=line.lstrip()
            if not li.startswith("#") and '=' in li:
                extract[line.split('=')[0]] = line.split('=')[1].strip()
    return extract
    
@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        help_msg =  "{admin}" \
                    "{listplayers}" \
                    "{infos}"\
                    "{roulette}"\
                    "{insulte}"\
            .format(admin="**!admin** - Gestion des instances ARK\n",
                    listplayers="**!listplayers** - Liste des survivants actuellement en jeu \n",
                    infos="**!infos** - Informations sur nos serveurs\n",
                    roulette="**!roulette** - Projet de jeu a la con\n",
                    insulte="**!insulte** - A vos risques et périls ..."
                    )
                    
        em = discord.Embed(title='Liste des commandes', 
            description="Gerbouille est un bot développé pour la communauté France-Evolved mais souffrant du syndrôme de Gilles de la Tourette."\
                        "Ses fonctions vont évoluer progressivement (ou parfois même regresser !)."\
                        "En cas de soucis, contacter Yota.",
            colour=0xDEADBF, 
            author='Yota')
        
        await client.send_message(message.channel, "", embed=em)
        await client.send_message(message.channel, help_msg)

    if message.content.startswith('!auth'):
        logger(message, "!auth")
        user = auth(message)
        if user is not None:
            await client.send_message(message.channel,'Voici mes informations sur %s'%user[1])
            await client.send_message(message.channel,'ID Discord : %s'%user[0])
            await client.send_message(message.channel,'ID Steam : %s'%user[2])
            await client.send_message(message.channel,'Groupe : %s'%user[3])

    if message.content.startswith('!saveworld'):
        if message.author.id in temp:
            rcon = srcds.SourceRcon(settings.Address, settings.ark_main_rconport, settings.ark_main_password, 5)
            list = rcon.rcon("saveworld").decode("utf-8")
            await client.send_message(message.channel, list)
        else:
            pass

    if message.content.startswith('!listplayers'):
        logger(message, "!listplayers")
        arkmap = []
        
        for x in os.listdir(folder):
            if x.endswith('.cfg'):
                arkmap.append(x)
        
        em = discord.Embed(title='Liste des survivant(e)s', 
            description="Les serveurs affichés sont ceux en ligne, seul les noms steam sont consultables et non ceux InGame.",
            colour=0xDEADBF, 
            author='Yota')
        await client.send_message(message.channel, "", embed=em)
        
        for cfg in arkmap:
            var = config(folder+cfg)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if sock.connect_ex((host,int(var['RCONPort']))) != 0:
                say = '**'+var['SessionName']+'** : Serveur Hors Ligne'
                #await client.send_message(message.channel, say)
                continue
            name = valve.map(message, int(var['QueryPort']))
            if not name:
                continue
            rcon = srcds.SourceRcon(host, int(var['RCONPort']), var['ServerAdminPassword'], 5)
            extract = []
            players = rcon.rcon("listplayers").decode("utf-8")
            if players.find('No Players Connected') < 0:
                for i in players.split('\n'):
                    if len(i) > 1:
                        extract.append(i.split(',')[0].split('. ',1)[1])
                lst = ' ('+', '.join(extract)+')'
            else: 
                lst = ''
            
            say = '**'+var['SessionName']+'** : '+str(len(extract))+' survivant(s) en ligne'+lst
            await client.send_message(message.channel, say)

    if message.content.startswith('!admin'):
        '''
        Commandes sur les serveurs ARK
        Creation de la syntaxe de lancement
        '''
        logger(message, "!admin")
        user = auth(message)
        if user is None:
            await client.send_message(message.channel, 'Cette commande nécessite un peu plus de droits !')
            await client.send_message(message.channel,scraping.insultron())
            return
        
        listmap = []
        namemap = []
        for x in os.listdir(folder):
            if x.endswith('.cfg'):
                if config(folder+x)['Enable'] != "True":
                    continue
                name = config(folder+x)['SessionName']
                listmap.append('**!%s** - %s'%(x.split('.')[0],name))
                namemap.append(x.split('.')[0])
        
        em = discord.Embed(title='Liste des instances configurées',
            description="La liste des instances est issue de la liste des fichiers de configuration en .cfg",
            colour=0xDEADBF,
            author='Yota'
            )
        
        await client.send_message(message.channel, "", embed=em)
        
        await client.send_message(message.channel, '\n'.join(listmap))
        msg = await client.wait_for_message(timeout=120.0, author=message.author)
             
        choice_map = msg.content.replace('!','')
        
        if choice_map is None:
            return
        
        if choice_map not in namemap:
            await client.send_message(message.channel, "C'est quoi que t'as pas compris dans choisir une instance ???")
            await client.send_message(message.channel,scraping.insultron())
            return

        admin_msg = "{start}" \
                    "{stop}" \
                    "{restart}" \
                    "{saveworld}" \
                    "{wipedinos}" \
                    "{installmod}" \
                    "{removemod}" \
                    "{backup}" \
            .format(start="**!start** - Démarrer instance\n",
                    stop="**!stop** - Arrêter instance\n",
                    restart="**!restart** - Redémarrer instance [OFF]\n",
                    saveworld="**!saveworld** - Sauvegarde Map [OFF]\n",
                    wipedinos="**!wipedinos** - Détruire tous les dinos sauvages [OFF]\n",
                    installmod="**!installmod** - Installer un nouveau Mod [OFF]\n",
                    removemod="**!removemod** - Supprimer un Mod [OFF]\n",
                    backup="**!backup** - Sauvegarde données Map [OFF]\n",
                    )

        em = discord.Embed(title='Action sur instance **%s**'%(choice_map),
            description="Attention, ces commandes agissent directement sur les serveurs ARK de France-Evolved."\
                        " Certaines demanderont une confirmation en plus des accès Administrateur."\
                        " Saisir l'option souhaitée !",
            colour=0xDEADBF,
            author='Yota'
            )
        
        await client.send_message(message.channel, "", embed=em)
        await client.send_message(message.channel, admin_msg)

        msg = await client.wait_for_message(timeout=120.0, author=message.author)
        
        choice_cmd = msg.content

        instance = folder+msg.content.replace('!','')+'.cfg'
        
        if choice_cmd == "!start":
            logger(message, "!start")
            server = CmdServer(config(folder+choice_map+'.cfg')).start()
            await client.send_message(message.channel, server['message'])

        elif choice_cmd == "!stop":
            logger(message, "!stop")
            server = CmdServer(config(folder+choice_map+'.cfg')).stop()
            await client.send_message(message.channel, server['message'])
    
        else:
            return
        
    if message.content.startswith('!load'):
        await client.send_message(message.channel,"Load Average: "+str(os.getloadavg()))

    if message.content.startswith('!insulte'):
        await client.send_message(message.channel,scraping.insultron())

n = Test()
n.run()
