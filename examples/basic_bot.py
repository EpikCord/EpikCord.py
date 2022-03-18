from EpikCord import Client

intents = Intents().guilds.guild_members.guild_messages.direct_messages.message_content # Intents().all if you want all

client: Client = Client("token", intents)

@client.event
async def ready():
    print("Ready!")

client.login()
