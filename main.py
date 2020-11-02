from discord.ext import commands
import helper_functions as hf


bot = commands.Bot(command_prefix='!!')
bot.games = {}


@bot.event
async def on_ready():
    print('Running complex rr as {0.user}'.format(bot))


@bot.command()
async def start(cxt, chamber: int = 6, bullets: int = 1):
    code = hf.get_code(cxt)

    if code in bot.games:
        await cxt.send("Slow down there bucko! There's a game already in progress."
                       "\ntype !!stop to stop the current game.")
        return
    elif bullets >= chamber:
        await cxt.send("Whoa there sheriff! You can't make a game that dangerous")
        return

    bot.games[code] = hf.Game(code, chamber, bullets)
    await cxt.send("Started a game with chamber size {} and {} bullets".format(chamber, bullets))


@bot.command()
async def shoot(cxt, shots: int = 1):
    code = hf.get_code(cxt)
    if code not in bot.games:
        await cxt.send("Don't shoot before you've even started, cowfolk!\n"
                       "Type !!start to make a game")
        return
    elif shots > bot.games[code].size:
        await cxt.send("Chill out there! That's a definite kill shot.")
        return
    elif cxt.author.id in bot.games[code].dead_players:
        await cxt.send("Ghosts can't shoot, buckaroo. You've already done shot yourself!")
        return

    is_dead, shots_made, bullets_remaining = bot.games[code].shoot(shots, cxt.author.id)

    if is_dead:
        await cxt.send("BLAM! {} was blown to smitherines after {} shots!!"
                       .format(cxt.message.author.mention, shots_made))
        if bullets_remaining != 0:
            await cxt.send("{} bullets left.".format(bullets_remaining))
        else:
            del bot.games[code]
            await cxt.send("No bullets remaining! Game ended.")
    else:
        await cxt.send("Nothing but blanks. You survive for now.")


@bot.command()
async def stop(cxt):
    code = hf.get_code(cxt)
    del bot.games[code]
    await cxt.send("All current games stopped, sheriff!")


@bot.command()
async def cheat(cxt):
    code = hf.get_code(cxt)
    await cxt.send(bot.games[code])


@bot.command()
async def h(cxt):
    await cxt.send("==WELCOME TO RUSSIAN ROULETTE==\n"
                   "!!start {clip} {ammo}: starts a game\n"
                   "!!shoot {shots}: shoots a bullet\n"
                   "!!stop: stops the game\n"
                   "!!h: ur already here buddy!!!!")

bot.run('put code here')
