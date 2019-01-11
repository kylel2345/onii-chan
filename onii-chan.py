import discord
from discord.ext import commands
import random
import romkan

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='onii-chan ', description=description)


async def botErrorMessage(botRef, msg="Sumimasen, but your Onii-chan doesn't quite understand what you're trying to say"):
    await botRef.say(msg)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="Kiss x Sis"), status=True, afk=False)


@bot.command(pass_context=True)
async def hiragana(ctx, *args):
    if len(args) is 0:
        channel = ctx.message.channel
        pdf = "./Resources/pdf/hiragana_chart.pdf"
        png = "./Resources/png/hiragana_chart.png"
        await bot.send_file(channel, png, content='Onii-chan has some trouble remembering these sometimes too, here have a chart!')
        await bot.send_file(channel, pdf, content='Onii-chan thought you might like a pdf too!')

    elif args[0].lower() == "nani":
        if len(args) < 2:
            await botErrorMessage(bot, "Sumimasen, onii-chan needs text to parse!")
            return

        #good to parse text, check if parsing mode is indicated, if not default to hiragana
        mode = "h"
        ret = ""
        if len(args) > 2:
            mode = args[2]
        try:
            text = args[1]
            if mode is "h":
                ret = romkan.to_hiragana(text)
            else:
                ret = romkan.to_katakana(text)

            await bot.say('{0} --> {1}'.format(args[1], ret))
        except Exception as e:
            await botErrorMessage(bot)

@bot.command(pass_context=True)
async def invite(ctx):
    channel = ctx.message.channel
    invite = await bot.create_invite(channel)
    await bot.say('Onii-chan created this invite just so you could hang out with your friends! %s' % str(invite))


@bot.command(pass_context=True)
async def move(ctx, userMovingID, channelSentToName):
    """takes a user, and moves them to another chanell"""
    try:
        sender = str(ctx.message.author.nick)
        userMovingMember = discord.Server.get_member(ctx.message.server, userMovingID[2:-1])
        if userMovingMember.nick is not None:
            userMoving = userMovingMember.nick
        else:
            userMoving = str(userMovingMember)[:-5]
        channelSentTo = ctx.message.server._channels[channelSentToName]

        await discord.Client.move_channel(userMovingMember, channelSentTo, 1)
        await bot.say(
            'Onii-chan moved {0} to {1} like you asked {2}!'.format(str(userMoving), str(channelSentTo), str(sender)))
    except Exception as e:
        await botErrorMessage(bot)
    print()


@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def roll(dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await botErrorMessage(bot, 'Sorry but onii-chan only knows the "NdN [+/-N]" format!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices: str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))


@bot.command()
async def repeat(times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)


@bot.command()
async def joined(member: discord.Member):
    """Says when a member joined."""
    await bot.say('My imouto or otouto {0.name} joined in the love at {0.joined_at}!'.format(member))


@bot.command()
async def channel(member: discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))


@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')


def readInToken():
    """only used on startup to read in bot token"""
    with open("token", "r") as f:
        return f.read()


token = str(readInToken()).strip()  # ensure that we recieve a strip str like expected
bot.run(token)