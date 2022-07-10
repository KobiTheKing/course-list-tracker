import lightbulb
import hikari

from course_tracker import tracker

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Shutdown", description="Safely shut down the bot.")

# Custom check to be used to prevent commands from being executed once the shutdown command has been execuated.
@lightbulb.Check
def check_not_shutting_down(context: lightbulb.Context) -> bool:
    return tracker.tracking

# Creates a command in the plugin
@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.add_checks(check_not_shutting_down)
@lightbulb.command("shutdown", description="Shutdown the bot.", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def shutdown(ctx: lightbulb.Context) -> None:
    await ctx.respond(content=hikari.Embed(
                title="Shutting down the bot...",
                #description="",
                color=hikari.Color(0xFF5733)))


    tracker.tracking = False

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)
