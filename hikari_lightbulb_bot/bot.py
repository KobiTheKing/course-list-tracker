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
@lightbulb.command("ping", description="The bot's ping")
# Define command's type
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    test(ctx)
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")

def test(ctx: lightbulb.Context):
    print(ctx.app)
    print(ctx.author)
    print(ctx.bot)
    print(ctx.channel_id)
    print(ctx.command)
    print(ctx.event)
    print(ctx.member)
    print(ctx.user)


if __name__ == "__main__":
    bot.run()