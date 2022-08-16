from EpikCord import Client, Intents

intents: Intents = Intents.all()

client: Client = Client("token", intents)


@client.event()
async def ready() -> None:
    print("Ready!")


@client.user_command("mention")
async def mention(interaction):
    await interaction.reply(content="Lol I'm not pinging them.")


client.login()
