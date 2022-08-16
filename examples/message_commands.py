from EpikCord import Client, Intents

intents = Intents.all()

client = Client("token", intents)


@client.event()
async def ready():
    print("Ready!")


@client.message_command("test")
async def test(interaction):
    await interaction.reply(content="Seems like a message to me.")


client.login()
