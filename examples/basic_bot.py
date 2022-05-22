from EpikCord import Client, Intents

intents = Intents().all()

client: Client = Client("token", intents)


@client.event
async def ready():
    print("Ready!")

client.login()
