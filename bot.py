import discord
import random
import time
import asyncio


class Bot(discord.Client):

	def __init__(self):
		super().__init__()


	def random_color(self):
		hexa = "0123456789abcdef"
		random_hex = "0x"
		for i in range(6):
			random_hex += random.choice(hexa)
		return discord.Colour(int(random_hex, 16))

	def create_embed(self, title, description, color, img=""):
		embed = discord.Embed()
		embed.title = title
		embed.description = description
		embed.colour = color
		if(img != ""):
			embed.set_image(url=img)
		return embed

	async def check_bot_channel(self, message):
		if(message.channel.id != 722417752375033886 and message.content != ""):
			await message.delete()
			bot_channel = discord.utils.get(message.guild.channels, id=722417752375033886)
			await bot_channel.send("<@" + str(message.author.id) + "> c'est ici qu'on doit envoyer les commandes du bot")
			return True

	def check_admin_rights(self, message):
		admin_role = discord.utils.get(message.guild.roles, name="Administrateur")
		modo_role = discord.utils.get(message.guild.roles, name="Modérateur")

		return (message.author.top_role != admin_role and message.author.top_role != modo_role)

	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')

	async def on_message(self, message):

		if(message.author == self.user):
			return

		if(message.content.startswith("!ping")):
			if(self.check_admin_rights(message)):
				await message.channel.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande")
				return

			if(await self.check_bot_channel(message)):
				return
			await message.channel.send("pong")

		if(message.content.startswith("!dm")):
			if(await self.check_bot_channel(message)):
				return

			name = message.content.split(" ")[1]

			if(name == "all"):
				for member in message.guild.members:
					if not member == self.user:
						try:
							await member.send("Hello!")
						except discord.Forbidden:
							await message.channel.send("Erreur l'utilisateur " + str(member) + " n'a pas ouvert ses DMs")
			else:
				member = discord.utils.get(message.guild.members, name=name)

				try:
					await member.send("Hello!")
				except discord.Forbidden:
					await message.channel.send("Erreur l'utilisateur " + name + " n'a pas ouvert ses DMs")
				except AttributeError:
					await message.channel.send("Erreur l'utilisateur " + name + " n'existe pas")


		if(message.content.startswith("!embed")):
			if(await self.check_bot_channel(message)):
				return
			color = self.random_color()
			description = "Salut je suis un d4rk H4x0r"
			embed = self.create_embed("HACKER", description, color, message.author.avatar_url)

			await message.channel.send(embed=embed)
		

		if(message.content.startswith("!invite")):
			if(await self.check_bot_channel(message)):
				return
			#Invitation unique, n'expire jamais
			#invite = await message.channel.create_invite(unique = False)

			#Invitation expire dans 1 heure
			#invite = await message.channel.create_invite(max_age = 3600, unique = False)

			#Invitation expire dans une invitation
			invite = await message.channel.create_invite(max_uses = 1, unique = False)

			await message.channel.send(invite.url)

		if(message.content.startswith("!del_invites")):
			if(await self.check_bot_channel(message)):
				return

			invites = await message.guild.invites()
			for i in invites:
				await i.delete()


		if(message.content.startswith("!create_role")):
			if(await self.check_bot_channel(message)):
				return

			role_name = " ".join(message.content.split(" ")[1:])
			permissions = discord.Permissions(268435504)
			color = self.random_color()

			await message.guild.create_role(name=role_name, permissions=permissions, colour=color)


		if(message.content.startswith("!kick")):
			msg = message.content.split(" ")
			if(len(msg) < 2):
				print("erreur nombre d'arguments")
				return
			user = msg[1]
			reason = " ".join(msg[2:])

			member_to_kick = discord.utils.get(message.guild.members, id=int(user[3:-1]))

			await message.guild.kick(member_to_kick, reason=reason)


		if(message.content.startswith("!ban")):
			msg = message.content.split(" ")
			if(len(msg) < 2):
				print("erreur nombre d'arguments")
				return
			user = msg[1]
			reason = " ".join(msg[2:])

			member_to_ban = discord.utils.get(message.guild.members, id=int(user[3:-1]))

			await message.guild.ban(member_to_ban, reason=reason)

		if(message.content.startswith("!prison")):
			msg = message.content.split(" ")
			if(len(msg) != 2):
				print("erreur nombre d'arguments")
				return

			user = msg[1]
			member_to_prison = discord.utils.get(message.guild.members, id=int(user[3:-1]))

			prison_channel = discord.utils.get(message.guild.channels, name="prison")
			prisonnier_role = discord.utils.get(message.guild.roles, name="prisonnier")
			admin_role = discord.utils.get(message.guild.roles, name="Administrateur")

			member_roles = list()
			all_roles = message.guild.roles

			for role in all_roles:
				for member_role in member_to_prison.roles:
					if(member_role.name != "@everyone"):
						member_roles.append(member_role)
						await member_to_prison.remove_roles(member_role)

			await member_to_prison.add_roles(prisonnier_role)

			await asyncio.sleep(900)

			await member_to_prison.remove_roles(prisonnier_role)

			for role in member_roles:
				await member_to_prison.add_roles(role)


	async def on_raw_reaction_add(self, payload):

		if(payload.message_id == 725662437923356672 and payload.emoji.name == "🍉"):
			#member = self.get_user(payload.user_id)
			guild = self.get_guild(payload.guild_id)

			watermelon_role = discord.utils.get(guild.roles, name='watermelon')
			member = discord.utils.get(guild.members, id=payload.user_id)

			await member.add_roles(watermelon_role)


	async def on_member_join(self, member):
		role_en_attente = discord.utils.get(member.guild.roles, name='En attente')
		await member.add_roles(role_en_attente)


		color = self.random_color()
		description = "User " + str(member) + "(" + str(member.id) + ") \nAccount created at " + member.created_at.strftime("%d %B %Y")
		embed = self.create_embed("New member joined the server", description, color, member.avatar_url)

		log_channel = discord.utils.get(member.guild.channels, name="log")

		await log_channel.send(embed=embed)


	async def on_message_delete(self, message):
		color = self.random_color()
		description = "Message from " + str(message.author) + "(" + str(message.author.id) + ") deleted \nContent : " + message.content
		embed = self.create_embed("Message deleted", description, color)

		log_channel = discord.utils.get(message.guild.channels, name="log")

		await log_channel.send(embed=embed)


if(__name__ == "__main__"):

	bot = Bot()
	bot.run("NjY5NjI4MTMyNTg3NzMyOTky.XvRoFw.z7wlJLI7rtl5l42m_zwgo-UWgfo")	#Remplacer ici par votre token
