import os
import dotenv
import hikari
import lightbulb
from hikari_lightbulb_bot.commands.customhelp import CustomHelpCommand
import tracker
from scraper import checkValidity
from datamanager import trackCourse, untrackCourse
import asyncio

dotenv.load_dotenv()    # Load environment variables

# Creates a bot instance
bot = lightbulb.BotApp(
    os.environ["DISCORD_BOT_TOKEN"],
    intents = hikari.Intents.ALL,
    default_enabled_guilds = (833429143672717315, 914263704978219109),     # commenting this out makes slash commands available in DMs, uncommenting this is useful for testing since it instantly loads slash commands to the listed servers
    #help_class = lightbulb.DefaultHelpCommand,
    logs = "INFO"
)

# Starts the bot.
def setup() -> None:
    #bot.load_extensions_from("hikari_lightbulb_bot.commands")
    #bot.load_extensions("hikari_lightbulb_bot.commands.starttracking", "hikari_lightbulb_bot.commands.customhelp")
    bot.load_extensions("hikari_lightbulb_bot.commands.starttracking")
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

# Recieves a direct message from a user of the bot and parses to identify commands
@bot.listen()
async def recieveDM(event: hikari.DMMessageCreateEvent) -> None:
    # Ignore the bot's own messages
    if event.is_bot:
        return

    #Retrieve message info
    senderName = event.author
    senderID = event.author_id
    senderMessage = event.content

    print(f"Recieved Inbound Message: User: {senderName}, MESSAGE: {senderMessage}")

    # Verify the message recieved is a command
    if senderMessage[0] == "/":
        if senderMessage.split()[0].lower() == "/track" and len(senderMessage.split()) == 3:
            # Command: 'track <CRN> <subject>'
            CRN = senderMessage.split()[1]
            subject = senderMessage.split()[2]
            print("CRN: " + CRN)
            print("subject: " + subject)
            print("senderMessage: " + senderMessage)
            print("sendername" + str(senderName))

            try:
                if checkValidity(CRN, subject):
                    # Both CRN and subject are good
                    trackCourse(CRN, subject, str(senderID))
                    await senderName.send(content = f"Success: Course with CRN: {CRN}, subject: {subject} now being tracked.")
                    return
                else:
                    # The CRN is invalid but the subject is good
                    await senderName.send(content = f"Error: CRN: {CRN} is invalid!")
                    return
            except Exception as e:
                # The subject is invalid
                await senderName.send(content = f"Error: subject: {subject} is invalid!")
                return
        elif senderMessage.split()[0].lower() == "/untrack" and len(senderMessage.split()) == 2:
            # Command: 'untrack <CRN>'
            CRN = senderMessage.split()[1]

            if untrackCourse(CRN, str(senderID)):
                await senderName.send(content = f"Success: Course with CRN: {CRN} no longer being tracked.")
                return
            else:
                await senderName.send(content = f"Error: CRN: {CRN} is invalid")
                return

        await senderName.send(content = "Invalid command!")
        return
    else:
        await senderName.send(content = "Invalid command! Use '/' before commands.")
        return