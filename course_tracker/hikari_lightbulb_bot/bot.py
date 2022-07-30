"""Controls core functionality of the Discord Bot."""

import os
import dotenv
import asyncio

import hikari
import lightbulb

from course_tracker import tracker

dotenv.load_dotenv()    # Load environment variables

# Creates a bot instance
bot = lightbulb.BotApp(
    os.environ["DISCORD_BOT_TOKEN"],
    intents=hikari.Intents.ALL,
    #default_enabled_guilds=(833429143672717315, 914263704978219109),     # commenting this out makes slash commands available in DMs, uncommenting this is useful for testing since it instantly loads slash commands to the listed servers
    help_class=None,
    logs="INFO"    #DEBUG
)

def setup() -> None:
    """Startup the bot."""

    bot.load_extensions("course_tracker.hikari_lightbulb_bot.commands.customhelp", "course_tracker.hikari_lightbulb_bot.commands.track", "course_tracker.hikari_lightbulb_bot.commands.untrack", "course_tracker.hikari_lightbulb_bot.commands.shutdown")
    bot.run(activity=hikari.Activity(name="the W&M Course List", type=hikari.ActivityType.WATCHING))

async def shutdown() -> None:
    """Shutdown the bot."""

    await bot.close()

@bot.listen()
async def start_tracker(event: hikari.StartedEvent) -> None:
    """Called once the bot has started.
    
    Starts the course tracker as a background task.
    """

    tracker.tracking = True
    asyncio.create_task(tracker.track())

@bot.listen()
async def botDisconnected(event: hikari.StoppedEvent) -> None:
    """Called once the bot has disconnected from Discord."""

    print("The bot has disconnected from Discord!")

async def send_DM(ids: list, msgString: str) -> None:
    """Send a direct message to user(s).
    
    Args:
        ids: A list of the user ids.
        msgString: The contents of the message.
    """

    for id in ids:
        try:
            user = await bot.rest.fetch_user(id) #Old: bot.cache.get_user(id) or await bot.rest.fetch_user(id)
            await user.send(content = msgString)

            print(f"Sent Outbound Message: User: {id}, MESSAGE: {msgString}")
        except Exception as e:
            print(f"ERROR: Failed to send outbound DM with exception: {e}")