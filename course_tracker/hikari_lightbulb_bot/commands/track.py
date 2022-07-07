import lightbulb
import hikari
from course_tracker import scraper
from course_tracker import datamanager

# Plugins are structures that allow the grouping of multiple commands and listeners together.
plugin = lightbulb.Plugin("Track Course", description="Track a new course.")

# Creates a command in the plugin
@plugin.command
@lightbulb.option("crn", description="The unique CRN for the course")
@lightbulb.option("subject", description="The subject the course")
@lightbulb.command("track", description="Track a new course", ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def track(ctx: lightbulb.Context) -> None:
    print("CRN: " + ctx.options.crn)
    print("subject: " + ctx.options.subject)
    print("sendername: " + str(ctx.author))

    try:
        if scraper.checkValidity(ctx.options.crn, ctx.options.subject):
            # Both CRN and subject are good
            datamanager.trackCourse(ctx.options.crn, ctx.options.subject, str(ctx.author.id))

            await ctx.respond(content=hikari.Embed(
                title="Success!",
                description=f"Course with\n\nCRN: {ctx.options.crn}\nSubject: {ctx.options.subject}\nis now being tracked.",
                color=hikari.Color(0x008000)))
        else:
            # The CRN is invalid but the subject is good
            await ctx.respond(content=hikari.Embed(
                title="Error!",
                description=f"CRN: {ctx.options.crn} is invalid!",
                color=hikari.Color(0xFF0000)))
    except Exception as e:
        # The subject is invalid
        await ctx.respond(content=hikari.Embed(
            title="Error!",
            description=f"Subject: {ctx.options.subject} is invalid!",
            color=hikari.Color(0xFF0000)))

# Extensions are hot-reloadable (can be loaded/unloaded while the bot is live)

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)