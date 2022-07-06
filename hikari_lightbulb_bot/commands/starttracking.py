import lightbulb

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("StartTrackingPlugin")

# Creates a command in the plugin
@plugin.command
@lightbulb.command("starttracking", description = "Recieve a DM from the bot to begin tracking courses.")
@lightbulb.implements(lightbulb.SlashCommand)
async def startTracking(ctx: lightbulb.Context) -> None:
    await ctx.user.send(content = "Test message!")
    await ctx.respond("temp")


# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)