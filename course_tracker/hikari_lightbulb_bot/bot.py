import os
import dotenv
import hikari
import lightbulb
from course_tracker import tracker
from course_tracker import scraper
from course_tracker import datamanager
import asyncio

dotenv.load_dotenv()    # Load environment variables

# Creates a bot instance
bot = lightbulb.BotApp(
    os.environ["DISCORD_BOT_TOKEN"],
    intents=hikari.Intents.ALL,
    #default_enabled_guilds=(833429143672717315, 914263704978219109),     # commenting this out makes slash commands available in DMs, uncommenting this is useful for testing since it instantly loads slash commands to the listed servers
    help_class=None,
    logs="INFO"    #DEBUG
)

# Starts the bot.
def setup() -> None:
    bot.load_extensions("course_tracker.hikari_lightbulb_bot.commands.customhelp", "course_tracker.hikari_lightbulb_bot.commands.track", "course_tracker.hikari_lightbulb_bot.commands.untrack")
    bot.run()

# Called once the bot has started.
# Starts the course tracker as a background task.
@bot.listen()
async def startTracker(event: hikari.StartedEvent) -> None:
    tracker.tracking = True
    asyncio.create_task(tracker.track())

# Called once the bot has disconnected from Discord.
@bot.listen()
async def botDisconnected(event: hikari.StoppedEvent) -> None:
    print("The bot has disconnected from Discord!")

# Register command to bot
@bot.command
# Convert function into command
@lightbulb.command("ping", description="The bot's ping")
# Define command's type
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")

# Sends a direct message to user(s).
# param ids: a list of user ids to send the message to
# param msgString: the contents of the message
async def sendDM(ids: list, msgString: str) -> None:
    for id in ids:
        try:
            user = await bot.rest.fetch_user(id) #Old: bot.cache.get_user(id) or await bot.rest.fetch_user(id)
            await user.send(content = msgString)

            print(f"Sent Outbound Message: User: {id}, MESSAGE: {msgString}")
        except Exception as e:
            print(f"ERROR: Failed to send outbound DM with exception: {e}")