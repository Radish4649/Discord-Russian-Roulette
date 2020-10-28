import random
from discord.ext import commands
from helper_functions import get_code, reset

bot = commands.Bot(command_prefix='!!')
bot.games_object = {}


@bot.event
async def on_ready():
    print('Running complex rr as {0.user}'.format(bot))


@bot.command()
async def start(cxt, chamber: int = 6, bullets: int = 1):
    code = get_code(cxt)

    # creates a new game object for channels without one
    if code not in bot.games_object.keys():
        bot.games_object[code] = reset()

    # checks if the game is in progress
    if bot.games_object[code]["in_progress"]:
        await cxt.send("Slow down there bucko! There's a game already in progress."
                       "\ntype !!stop to stop the current game.")
    # checks to see if the numbers make sense
    elif bullets >= chamber:
        await cxt.send("Whoa there sheriff! You can't make a game that dangerous")
    # starts a game proper
    else:
        # if there isn't, it creates the environment for a new game
        bot.games_object[code]["in_progress"] = 1
        bot.games_object[code]["game"] = random.sample(range(1, chamber+1), k=bullets)
        await cxt.send("Started a game with chamber size {} and {} bullets".format(chamber, bullets))


@bot.command()
async def shoot(cxt, shots: int = 1):
    code = get_code(cxt)
    game_max = max(bot.games_object[code]["game"])
    game_len = len(bot.games_object[code]["game"])
    if not bot.games_object[code]["in_progress"]:
        await cxt.send("Don't shoot before you've even started, cowfolk!\nType !!start to make a game")
    elif shots > game_max:
        await cxt.send("Chill out there! That's a definite kill shot.")
        return

    for XxX in range(0, shots):
        bot.games_object[code]["game"] = list(map(lambda x: x - 1, bot.games_object[code]["game"]))

        if 0 in bot.games_object[code]["game"]:
            await cxt.send("BLAM! {} was blown to smitherines after {} shots!!".format(cxt.message.author.mention, XxX+1))
            bot.games_object[code]["game"].remove(0)
            break

    if len(bot.games_object[code]["game"]) == game_len:
        await cxt.send("Nothing but blanks. You survive for now.")
    elif len(bot.games_object[code]["game"]) > 0:
        await cxt.send("{} bullets left.".format(game_len - 1))
    else:
        bot.games_object[code] = reset()
        await cxt.send("No bullets remaining! Game ended.")


@bot.command()
async def stop(cxt):
    code = get_code(cxt)
    bot.games_object[code] = reset()
    await cxt.send("All current games stopped, sheriff!")


@bot.command()
async def cheat(cxt):
    code = get_code(cxt)
    await cxt.send(bot.games_object[code])


@bot.command()
async def commands(cxt):
    await cxt.send("==WELCOME TO RUSSIAN ROULETTE==\n"
                   "!!start {clip} {ammo}: starts a game\n"
                   "!!shoot {shots}: shoots a bullet\n"
                   "!!stop: stops the game\n"
                   "!!help: ur already here buddy!!!!")

bot.run("enter code here")
