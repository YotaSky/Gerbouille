#!/usr/bin/env python3.6
#Bot Gerbouille Discord/ARK
#France-Evolved https://discord.gg/gVsveNY
#2017 By YotaSky https://github.com/YotaSky

import discord
import asyncio
import os
import csv
import datetime

from module.status import Status
from module import scraping


client = discord.Client()

@client.event
async def on_ready():
	"""Fonction de lancement de Bot sur Discord"""
	print('CONNECT::{} ({})'.format(client.user.name,client.user.id))

@client.event
async def on_message(message):
	"""Toutes les interactions avec Discord doivent se faire en global (Lib Discord.py sux)"""
	if message.content.startswith('!help'):
		"""Rendre la composition de l'aide dynamique"""
		return

	if message.content.startswith('!status'):
		"""Récupération des informations serveur"""
		msg = Status().players(message)
		em = discord.Embed(title='Liste des survivant(e)s', 
            description="Les serveurs affichés sont ceux en ligne, seul les noms steam sont consultables et non ceux InGame.",
            colour=0xDEADBF, 
            author='Yota')
		await client.send_message(message.channel, "", embed=em)
		await client.send_message(message.channel, msg)

	if message.content.startswith('!load'):
		"""Récupération du load average"""
		await client.send_message(message.channel,"Load Average: "+str(os.getloadavg()))

	if message.content.startswith('!insulte'):
		"""Scraping sur le site http://www.insultron.com"""
		await client.send_message(message.channel,scraping.insultron())

	if message.content.startswith('!auth'):
		"""Fonction de vérification des droits
		Fichier /etc/gerbouille/users
		- Attribution groupe droits
		- Stockage des IDs Steam
		- Stockage des IDs Discord
		Commande à faire devenir passive"""
		user = Tools().auth(message)
		if user is None:
			await client.send_message(message.channel,'Gerbouille te connait pas !')
		else:
			await client.send_message(message.channel,'Voici mes informations sur %s'%user[1])
			await client.send_message(message.channel,'ID Discord : %s'%user[0])
			await client.send_message(message.channel,'ID Steam : %s'%user[2])
			await client.send_message(message.channel,'Groupe : %s'%user[3])

class Tools:
	def __init__(self):
		self.pathconf = os.path.join(os.path.sep,'etc','gerbouille')

	def run(self):
		data = 'token'
		client.run(open(os.path.join(os.path.sep,self.pathconf,data)).read().replace('\n',''))

	def auth(self, message):
		data = 'users'
		acl = open(os.path.join(os.path.sep,self.pathconf,data))
		try:
			reader = csv.reader(acl)
			for row in reader:
				if row[0] == message.author.id:
					return row
		finally:
			acl.close()

	def logger(self, message, command, verbose=False):
		date = datetime.datetime.now()
		print('{}::{} used command {}'.format(str(date),message.author.name,command))

gerbouille = Tools()
gerbouille.run()
