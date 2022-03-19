from EpikCord import Client, Intents, StringOption, NumberOption

intents = Intents().guilds.guild_members.guild_messages.direct_messages.message_content

client: Client = Client("token", intents)
  
@client.event
async def ready():
    print("Ready!")
    
    
@client.message_command("test")
async def test(interaction):
    await interaction.reply(content = "Seems like a message to me.")

client.login()
