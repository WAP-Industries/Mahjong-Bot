from bot import *

async def CheckSession():
    return (await Bot.Error("Game not in session yet, use !start to start new session") if not Bot.Game.InSession else True)

def PrintLastHand():
    return f"Current hand: {Bot.Game.LastHand}\nTiles: {len(Bot.GetTiles(Bot.Game.LastHand))}"

def GetTileRepr(notation):
    isNumber = notation[0].isnumeric()
    Suit = Bot.Notation["Number" if isNumber else "Honor"][notation[1:] if isNumber else notation]
    return (f"{notation[0]} of {Suit}s" if isNumber else Suit)+" Tile"


@Bot.Bot.command()
async def exit(ctx):
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



def SessionCommand():
    async def decorator(ctx, *args, **kwargs):
        return (await Bot.Error("Game not in session yet, use !start to start new session") if not Bot.Game.InSession else True)
    return commands.check(decorator)

@Bot.Bot.command()
@SessionCommand()
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
    Bot.SortHand()
    Bot.Game.InSession = True
    await Bot.Message(f"Session successfully started\n\n{PrintLastHand()}")

@Bot.Bot.command()
@SessionCommand()
async def claim(ctx, tile):
    if not await Bot.ValidateTile(tile):
        return
    if len(Bot.GetTiles(Bot.Game.LastHand))>=14:
        return await Bot.Error("14 tiles already in hand, unable to draw")
    Bot.Game.LastHand+=f",{tile}"
    Bot.SortHand()
    await Bot.Message(PrintLastHand())

@Bot.Bot.command()
@SessionCommand()
async def drop(ctx, tile):
    if not await Bot.ValidateTile(tile):
        return
    Tiles = Bot.GetTiles(Bot.Game.LastHand)
    if len(Tiles)<=13:
        return await Bot.Error(f"13 tiles already in hand, unable to discard")
    try:
        Tiles.remove(tile.strip())
        Bot.Game.LastHand = ','.join(Tiles)
        Bot.SortHand()
        await Bot.Message(PrintLastHand())
    except:
        return await Bot.Error("Tile not in current hand", tile)   
    
@Bot.Bot.command()
@SessionCommand()
async def chi(ctx, tile):
    if not await Bot.ValidateTile(tile):
        return
    if len(Bot.GetTiles(Bot.Game.LastHand))!=13: 
        return await Bot.Error("trick ass bitch u cant claim shit (invalid number of tiles)")
    Response = await Bot.GetMove([
        f"The last discarded tile was {GetTileRepr(tile.strip())}",
        "The last discarded tile was Red tile.",
        "Is claiming the tile the best strategy? Without providing any explanation, present your answer in this format:",
        "Claim: [Yes/No]",
        "Discard: [Tile to discard if yes]"
    ])
    await ctx.send(f"```{PrintLastHand()}``````{Response}```")
    

@Bot.Bot.command()
@SessionCommand()
async def play(ctx):
    if len(Bot.GetTiles(Bot.Game.LastHand))<14:
        return await Bot.Error("Insufficient number of tiles to play")
    Response = await Bot.GetMove([
        "Without providing any explanation, suggest which tile I should discard, and what sets to aim for, presenting your answer in the format:",
        "Discard: [Tile with suit and number]",
        "Sets: [Sets listed in point form, tiles separated with commas]"
    ])
    await ctx.send(f"```{PrintLastHand()}``````{Response}```")