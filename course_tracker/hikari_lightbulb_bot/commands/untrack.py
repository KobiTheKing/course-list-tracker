import lightbulb
from course_tracker import datamanager

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Untrack Course", description="Untrack a course.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("crn", description="The unique CRN for the course")
@lightbulb.command("untrack", description="Untrack a course", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def untrack(ctx: lightbulb.Context) -> None:
    print("CRN: " + ctx.options.crn)
    print("sendername: " + str(ctx.author))

    if datamanager.untrackCourse(ctx.options.crn, str(ctx.author.id)):
        await ctx.respond(content=f"Success: Course with CRN: {ctx.options.crn} no longer being tracked.")
    else:
        await ctx.respond(content=f"Error: CRN: {ctx.options.crn} is invalid")
    

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)