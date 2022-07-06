import lightbulb
import hikari

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Help Command", description="Information on the how to use the bot.")

# Creates a command in the plugin
@plugin.command
@lightbulb.command("help", description="Gets help for bot commands")
@lightbulb.implements(lightbulb.SlashCommand)
async def custom_help(ctx: lightbulb.Context) -> None:
    embedHelp = (
        hikari.Embed(
            title="W&M Course Tracker", 
            description="""This bot allows you to track courses on the W&M Open Course List. You will recieve a DM notification whenever one of your tracked course has a status change. 

                        Commands for this bot can be executed in Discord servers containing the bot or directly in a DM with the bot.""",
            url="https://courselist.wm.edu/courselist/",
            color=hikari.Color(0x115740)
        )

        .add_field("Available Commands:", "- Information on the how to use the bot: /help\n- Track a new course: /track <CRN> <subject>\n- Untrack a course: /untrack <CRN>")
        .set_thumbnail("https://brand.wm.edu/wp-content/uploads/76-300x296.png")
    )

    print(ctx.channel_id)
    print(ctx.guild_id)

    #if ctx.guild_id is None:
    #    embedDM = (
    #        hikari.Embed(
    #            title=
    #        )
    #    )

    #await ctx.user.send(content=ctx.user.mention, embed=embedDM)
    await ctx.respond(embedHelp)

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)