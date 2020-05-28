import chattrigger

import discord

class ProbeServer(chattrigger.ChatTrigger):
	
	async def run(self, message: discord.Message, trigger: str, client: discord.Client):

		targetserver: discord.Guild = client.get_guild(int(message.content[len(trigger):]))

		messagestr = ""

		messagestr += f"**{targetserver.name}**\n"

		if targetserver.owner == None:
			messagestr += f"**Server has no owner!**\n"
		else:
			messagestr += f"**{str(targetserver.owner)} is owner.**\n"

		members = [str(x) for x in targetserver.members]
		membersstr = ", ".join(members)

		messagestr += f"**Members ({len(members)}):** "

		messagestr += f"{membersstr}\n"

		channels = [str(x) for x in targetserver.channels]
		channelsstr = ", ".join(channels)

		messagestr += f"**Channels ({len(channels)}):** "

		messagestr += f"{channelsstr}\n"

		roles = [str(x) for x in targetserver.roles]
		rolesstr = ", ".join(roles)

		messagestr += f"**Roles ({len(roles)}):** "

		messagestr += f"{rolesstr}\n"

		#

		selfroles = [str(x) for x in targetserver.me.roles]
		selfrolesstr = ", ".join(selfroles)

		messagestr += f"**Dot2 Roles ({len(selfroles)}):** "

		messagestr += f"{selfrolesstr}\n"

		selfpermissions = targetserver.me.guild_permissions

		messagestr += f"**Dot2 Permission Values:**\n"

		messagestr += f'''Administrator: {selfpermissions.administrator}
Manage Channels: {selfpermissions.manage_channels}
Manage Roles: {selfpermissions.manage_roles}
Manage Guild: {selfpermissions.manage_guild}
Ban Members: {selfpermissions.ban_members}
Kick Members: {selfpermissions.kick_members}'''

		# 2020-05-28

		emojis = [str(x) for x in targetserver.emojis]
		emojisstr = ", ".join(emojis)

		messagestr += f"**Emojis ({len(emojis)}):**"

		messagestr += f"{emojisstr}\n"

		#

		messagestr = discord.utils.escape_mentions(messagestr)

		#

		chunksize = 2000 # discord 2000 character limit

		#nofchunks = -(-len(messagestr) // chunksize) # ceiling division

		#chunks = []
		
		a = ""
		c = 0
		for i in messagestr: # discord 2000 character limit
			if c == chunksize:
				print(len(a))
				await message.channel.send(a)
				
				a = ""
				c = 0
			a += str(i)
			c += 1
		await message.channel.send(a)