#!/usr/bin/env python3
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
from module.CmdServer import CmdServer


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

	if message.content.startswith('!ark'):
		"""Récupération des informations serveur"""
		Tools().logger(message, "!ark")
		play,info = Status().instances(message)
		txt = '```diff\n- ARK: Survival Evolved - Cross-Travel - {} Survivant(s) en Jeu\n\n{}\n```'.format(play,''.join(info))
		em = discord.Embed(title='Liste des serveurs France-Evolved', 
			description="Visitez notre site http://ark.france-evolved.team",
			colour=0xDEADBF, 
			author='Yota')
		await client.send_message(message.channel, "", embed=em)
		await client.send_message(message.channel, txt)

	if message.content.startswith('!load'):
		"""Récupération du load average"""
		Tools().logger(message, "!load")
		await client.send_message(message.channel,"Load Average: "+str(os.getloadavg()))	

	if message.content.startswith('!insulte'):
		"""Scraping sur le site http://www.insultron.com"""
		await client.send_message(message.channel,scraping.insultron())

	if message.content.startswith('!admin'):
		user = Tools().auth(message)
		if user == None:
			await client.send_message(message.channel,"Toi pas parler à Gerbouille, moi pas te connaitre ! {}".format(scraping.insultron()))
			return
		servers = Status().instances(message, True)
		await client.send_message(message.channel,servers[0])
		await client.send_message(message.channel,"Quelle instance veux-tu administrer ?")
		input_srv = await client.wait_for_message(timeout=120.0, author=message.author)
		
		input_opt = "```markdown\n" \
					"# Liste des commandes\n\n" \
					"> {start}" \
					"> {stop}" \
					"> {restart}" \
					"> {saveworld}" \
					"> {wipedinos}" \
					"> {installmod}" \
					"> {removemod}" \
					"> {backup}\n" \
					"# Etat des commandes\n\n" \
					"* Commande utilisable\n" \
					"> Commande non utilisable\n" \
					"```" \
			.format(start="!start - Démarrer instance\n",
					stop="!stop - Arrêter instance\n",
					restart="!restart - Redémarrer instance\n",
					saveworld="!saveworld - Sauvegarde Map\n",
					wipedinos="!wipedinos - Détruire tous les dinos sauvages\n",
					installmod="!installmod - Installer un nouveau Mod\n",
					removemod="!removemod - Supprimer un Mod\n",
					backup="!backup - Sauvegarde données Map\n",
					)
		await client.send_message(message.channel,input_opt)
		input_opt = await client.wait_for_message(timeout=120.0, author=message.author)

		#launch = CmdServer().admin(msg.content)
		#await client.send_message(message.channel,launch)

	
	if message.content.startswith('tagle'):
		"""Fonction indispensable pour un échange constructif et courtois"""
		user = Tools().auth(message)
		if user[1] == 'Yota':
			await client.send_message(message.channel,'Ouais ta gueule !')

	if message.content.startswith('vogle'):
		"""Fonction indispensable pour un échange constructif et courtois"""
		user = Tools().auth(message)
		if user[1] == 'Yota':
			await client.send_message(message.channel,"Vous êtes du vomi, vous êtes le niveau zéro de la vie sur Terre, vous n'êtes même pas humain bande d'enfoirés ! Donc fermez votre gueule !")

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
			await client.send_message(message.channel,"Arrêtes de me parler tête d'oeuf, t'as pas les droits pour ça.")
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
					return user
		finally:
			file.close()

	def logger(self, message, command, verbose=False):
		date = datetime.datetime.now()
		print('{}::{} used command {}'.format(str(date),message.author.name,command))

gerbouille = Tools()
gerbouille.run()
