import lightbulb
import hikari_lightbulb_bot.bot

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("CustomHelpPlugin")

#@plugin.command
#@lightbulb.command("help", description = "Get bot command info.")
#@lightbulb.implements(lightbulb.SlashCommand)
class CustomHelpCommand(lightbulb.BaseHelpCommand):

    # Sends an overall help message for the bot. This is called when no object is provided when the help command is invoked.
    async def send_bot_help(self, context):
        print("?")
        #await context.respond("Test")

    async def send_plugin_help(self, context, plugin):
        # Override this method to change the message sent when the help command
        # argument is the name of a plugin.
        print("?")
        #await context.respond("Test")

    async def send_command_help(self, context, command):
        # Override this method to change the message sent when the help command
        # argument is the name or alias of a command.
        print("?")
        #await context.respond("Test")

    async def send_group_help(self, context, group):
        # Override this method to change the message sent when the help command
        # argument is the name or alias of a command group.
        print("?")
        #await context.respond("Test")

    async def object_not_found(self, context, obj):
        # Override this method to change the message sent when help is
        # requested for an object that does not exist
        print("?")
        #await context.respond("Test")

#@plugin.command
#@lightbulb.command("help", description = "Get bot command info.")
#@lightbulb.implements(CustomHelpCommand)
#async def startTracking(ctx: lightbulb.Context) -> None:
#    await ctx.respond("hello?")

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.d.old_help_command = bot.help_command
    bot.help_command = CustomHelpCommand(bot)
    bot.add_plugin(plugin)

def unload(bot):
    bot.help_command = bot.d.old_help_command
    del bot.d.old_help_command
    bot.remove_plugin(plugin)