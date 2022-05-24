import asyncio
import datetime
import time

import humanize

from EpikCord import Client, Intents, StringOption, NumberOption

intents = Intents().all()

client: Client = Client("token", intents)


@client.event
async def ready():
    print("Ready!")


@client.command(name="ping", description="A test command", guild_ids=["id"])
async def ping(interaction):
    start = time.perf_counter()
    await interaction.reply(content="Pong!")
    end = time.perf_counter()

    await asyncio.sleep(0.5)

    trip = end - start
    rt_ping = f"{(trip * 1000):.2f}ms ({humanize.precisedelta(datetime.timedelta(seconds=trip))})"

    await interaction.edit_original_response(content=f"Pong! {rt_ping}")


@client.command(
    name="say",
    description="Say what you say",
    guild_ids=["id"],
    options=[
        StringOption(name="content", description="The message content"),
        NumberOption(name="delete_after", description="Delete after"),
    ],
)
async def say(interaction, content, delete_after):
    await interaction.reply(content=f"{content}")
    await asyncio.sleep(int(delete_after))
    await interaction.delete_original_response()


# extra
# @client.event
# async def interaction_create(interaction):
#     if interaction.is_message_component():
#         await interaction.reply(content = "You clicked me. Why.")

client.login()
