import os
import dotenv
import hikari
import lightbulb
import logging

dotenv.load_dotenv()

# Creates a bot instance
bot = lightbulb.BotApp(
    os.environ["DISCORD_BOT_TOKEN"],
    intents = hikari.Intents.ALL,
    default_enabled_guilds = (833429143672717315),
    logs = "INFO"
)

# Register command to bot
@bot.command
# Convert function into command
@lightbulb.command("ping", description = "The bot's ping")
# Define command's type
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")

# Command to clear all the messages in a channel
@bot.command
@lightbulb.command("clear", description = "Clears the message history in the current channel.")
@lightbulb.implements(lightbulb.SlashCommand)
async def clear(ctx: lightbulb.Context) -> None:
    channel = ctx.get_channel()

    #if channel.name == "bot-commands" and channel.type == hikari.ChannelType.GUILD_TEXT:
    #    hikari.GuildTextChannel(channel).delete_messages()

    await ctx.respond("Channel contents cleared.")

#
#   Events
#

@bot.listen()
async def directMessageCreate(event: hikari.DMMessageCreateEvent) -> None:
    print(event.author)
    print(event.channel_id)
    print(event.content)
    print(event.is_human)
    print(event.message)



if __name__ == "__main__":
    bot.load_extensions("commands.starttracking")
    bot.run()