import discord
import asyncio
import os
import feedparser

from rssbot import rssquery
from fritext import fritext

from dotenv import load_dotenv
load_dotenv()

discordtoken = os.getenv('DISCORD_TOKEN')
discordchannel = int(os.getenv('DISCORD_CHANNEL'))
rss_url = os.getenv('rss_url')

class MyClient(discord.Client):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		print(rss_url)
		self.bg_task = self.loop.create_task(self.rssticker())
	async def rssticker(self):
		await self.wait_until_ready()
		rsschannel = self.get_channel(discordchannel)
		rssfeed = feedparser.parse(rss_url).entries[0]
		startid = rssfeed
		print("Hej")
		while not self.is_closed():
			rssfeed = feedparser.parse(rss_url).entries
			print("\nStart of loop. Startid=%s\n%s\n%s" % (startid.id, startid.published, startid.title))
			print(len(rssfeed))
			if startid.id == rssfeed[0].id:
				print("No change. Startid=%s. Entry0=%s" % (startid.id, rssfeed[0].id))
				#await rsschannel.send("Inget nytt ännu.")
			else:
				print("Change detected! Startid=%s. Entry0 = %s" % (startid.id, rssfeed[0].id))
				sendid = rssfeed[0]
				print("%s\n%s\n<%s>\n%s\n----" % (sendid.published, sendid.title, sendid.link, sendid.description))
				startid = rssfeed[0]
				await rsschannel.send("%s\n%s\n<%s>\n%s\n----" % (sendid.published, sendid.title, sendid.link, sendid.description))
			print("End of loop. Startid=%s\n" % startid.id)
			del rssfeed
			await asyncio.sleep(300)
client = MyClient()

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content == ('$help'):
		await message.channel.send(
		'Nuvarande funktioner:\n'
		'$rss <sökterm> : Söker igenom FZ.SE\'s RSS-feed efter en matchande titel\n')
		return
	if message.content.startswith('$rss'):
		await rssquery(message.content.lower()[5:], message, rss_url)
		return
	await fritext(message)

client.run(discordtoken)
