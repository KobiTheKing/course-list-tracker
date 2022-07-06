import lightbulb
import hikari

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Start Tracking", description="Recieve a DM from the bot to begin tracking courses.")

# Creates a command in the plugin
@plugin.command
@lightbulb.command("starttracking", description="Starts up a DM page between yourself and the bot.")
@lightbulb.implements(lightbulb.SlashCommand)
async def startTracking(ctx: lightbulb.Context) -> None:
    embed = (
        hikari.Embed(
            title="W&M Course Tracker", 
            description="""This bot allows you to track courses on the W&M Open Course List. You will recieve a discord notification whenever one of your tracked course has a status change. 

                        If you are viewing this message, it means that you now have a DM page with the bot. All further interactions with the bot take place here including sending commands to the bot and recieving notifications from the bot.""",
            url="https://courselist.wm.edu/courselist/",
            color=hikari.Color(0x115740)
        )

        .add_field("Available Commands:", "- Track a new course: /track <CRN> <subject>\n- Untrack a course: /untrack <CRN>")
        .set_thumbnail("https://brand.wm.edu/wp-content/uploads/76-300x296.png")
    )

    await ctx.user.send(content=ctx.user.mention, embed=embed)
    await ctx.respond("View DM from me to start tracking courses!")

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)