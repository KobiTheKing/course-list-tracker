import os
import dotenv
import hikari

dotenv.load_dotenv()

bot = hikari.GatewayBot(
    os.environ["DISCORD_BOT_TOKEN"],
    intents = hikari.Intents.ALL,
)

@bot.listen()
async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    if event.content.strip() == "+ping":
        await event.message.respond(
            f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms"
        )

if __name__ == "__main__":
    bot.run()