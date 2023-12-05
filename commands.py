from bot import *

async def CheckSession():
    return (await Bot.Error("Game not in session yet, use !start to start new session") if not Bot.Game.InSession else True)

def PrintLastHand():
    return f"Current hand: {Bot.Game.LastHand}"


@Bot.Bot.command()
async def exit(ctx):
    if not await CheckSession(): 
        return
    await ctx.send("Bye nigger")
    await Bot.Bot.close()


@Bot.Bot.command()
async def tiles(ctx):
    await ctx.send(file=nextcord.File(f"{Bot.Directory}\\assets\\tiles.png"))

@Bot.Bot.command()
async def notation(ctx):
    sep = 15
    header = f"{'Suit':<{sep}}Notation"
    Text = f"{header}\n{''.join(['-' for _ in range(len(header))])}\n"
    
    Keys = [j for i in Bot.Notation.values() for j in i]
    Text+=''.join([f"{Bot.Notation['Number' if i in Bot.Notation['Number'] else 'Honor'][i]:<{sep}}{i}\n" for i in Keys])
    await Bot.Message(Text)



@Bot.Bot.command()
async def end(ctx):
    Bot.Game.Reset()
    await Bot.Message("Session ended")

@Bot.Bot.command()
async def start(ctx, tiles):
    if Bot.Game.InSession: 
        return await Bot.Error("Game already in session. Use !end to start new game.")
    if not await Bot.ValidateHand(tiles): 
        return
    Bot.Game.LastHand = ','.join(Bot.GetTiles(tiles))
    Bot.Game.InSession = True
    await Bot.Message(f"Session successfully started\n{PrintLastHand()}")

@Bot.Bot.command()
async def draw(ctx, tile):
    if not await CheckSession(): 
        return
    
    if not await Bot.ValidateTile(tile):
        return
    if len(Bot.GetTiles(Bot.Game.LastHand))>=14:
        return await Bot.Error("14 tiles already in hand, unable to draw")
    Bot.Game.LastHand+=f",{tile}"
    await Bot.Message(PrintLastHand())

@Bot.Bot.command()
async def discard(ctx, tile):
    if not await CheckSession():
        return

    if not await Bot.ValidateTile(tile):
        return
    Tiles = Bot.GetTiles(Bot.Game.LastHand)
    if len(Tiles)<=13:
        return await Bot.Error(f"13 tiles already in hand, unable to discard")
    try:
        Tiles.remove(tile.strip())
        Bot.Game.LastHand = ','.join(Tiles)
        await Bot.Message(PrintLastHand())
    except:
        return await Bot.Error("Tile not in current hand", tile)
    

@Bot.Bot.command()
async def play(ctx):
    if not await CheckSession():
        return
    await Bot.Message(f"{PrintLastHand()}\n\n\n{await Bot.GetPlay()}")