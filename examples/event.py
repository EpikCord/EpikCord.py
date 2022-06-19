# Registering Events

from EpikCord import Client, Intents, Messageable

intents = Intents.all()

client = Client("your_token", intents)

# this is one way of registering events
@client.event()
async def message_create(message):
    # message action here
    if message.author.id == client.user.id:
        return
    if message.content == "example test":
        message.channel = Messageable(client, message.channel_id)

        await message.channel.send(content="Did i hear Example test?")
#or
#if you want another way of making events

@client.event("guild_member_leave") #Any event name
async def sad_to_see_you_go(guild_id, user):
    channel = Messageable(client, 2333232)# a message channel id
    await channel.send(content="Saaaaaaaaad to see u go ;(")


client.login()
