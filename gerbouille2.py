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

	if message.content.startswith('!who'):
		"""Récupération des informations serveur"""
		Tools().logger(message, "!who")
		msg = Status().players(message)
		em = discord.Embed(title='Liste des survivant(e)s', 
            description="Les serveurs affichés sont ceux en ligne, seul les noms steam sont consultables et non ceux InGame.",
            colour=0xDEADBF, 
            author='Yota')
		await client.send_message(message.channel, "", embed=em)
		await client.send_message(message.channel, msg)

	if message.content.startswith('!load'):
		"""Récupération du load average"""
		Tools().logger(message, "!load")
		await client.send_message(message.channel,"Load Average: "+str(os.getloadavg()))

	if message.content.startswith('!insulte'):
		"""Scraping sur le site http://www.insultron.com"""
		await client.send_message(message.channel,scraping.insultron())

	if message.content.startswith('!admin'):


	if message.content.startswith('!auth'):
		"""Fonction de vérification des droits
		Fichier /etc/gerbouille/users
		- Attribution groupe droits
		- Stockage des IDs Steam
		- Stockage des IDs Discord
		Commande à faire devenir passive"""
		Tools().logger(message, "!auth")
		user = Tools().auth(message)
		if user == None:
			await client.send_message(message.channel,"Toi pas parler à Gerbouille, moi pas te connaitre ! {}".format(scraping.insultron()))
			return
		msg = 	"{name}" \
				"{discord}" \
				"{steam}" \
				"{group}" \
			.format(name="Voici mes informations sur **{}**\n".format(user[1]),
				discord="ID Discord : **{}**\n".format(user[0]),
				steam="ID Steam : **{}**\n".format(user[2]),
				group="Groupe de droits : **{}**".format(user[3]),
				)
		em = discord.Embed(title='Droits en base', 
            description="Informations de debug pour les informations utilisateurs qui permettra de configurer les accès Gerbouille",
            colour=0xDEADBF, 
            author='Yota')
		await client.send_message(message.channel, "", embed=em)
		await client.send_message(message.channel,msg)

class Tools:
	def __init__(self):
		self.pathconf = os.path.join(os.path.sep,'etc','gerbouille')

	def run(self):
		data = 'token'
		client.run(open(os.path.join(os.path.sep,self.pathconf,data)).read().replace('\n',''))

	def auth(self, message):
		data = 'users'
		file = open(os.path.join(os.path.sep,self.pathconf,data))
		try:
			for user in csv.reader(file):
				if user[0] == message.author.id:
					return msg
		finally:
			file.close()

	def logger(self, message, command, verbose=False):
		date = datetime.datetime.now()
		print('{}::{} used command {}'.format(str(date),message.author.name,command))

gerbouille = Tools()
gerbouille.run()
