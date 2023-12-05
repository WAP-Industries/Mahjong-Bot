from bot import *

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
    for i in Bot.Notation:
        for j in Bot.Notation[i]:
            Text+= f"{Bot.Notation[i][j]:<{sep}}{j}\n"
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
    await Bot.Message("Session successfully started")

@Bot.Bot.command()
async def draw(ctx, tile):
    if not Bot.Game.InSession:
        return await Bot.Error("Game not in session yet, use !start to start new session")
    
    if not await Bot.ValidateTile(tile):
        return
    if len(Bot.GetTiles(Bot.Game.LastHand))>=14:
        return await Bot.Error("14 tiles already in hand, unable to draw")
    Bot.Game.LastHand+=f",{tile}"
    await Bot.GetLastHand()

@Bot.Bot.command()
async def discard(ctx, tile):
    if not Bot.Game.InSession:
        return await Bot.Error("Game not in session yet, use !start to start new session")

    if not await Bot.ValidateTile(tile):
        return
    Tiles = Bot.GetTiles(Bot.Game.LastHand)
    if len(Tiles)<=13:
        return await Bot.Error(f"13 tiles already in hand, unable to discard")
    try:
        Tiles.remove(tile.strip())
        Bot.Game.LastHand = ','.join(Tiles)
        await Bot.GetLastHand()
    except:
        return await Bot.Error("Tile not in current hand", tile)
    

@Bot.Bot.command()
async def play(ctx):
    pass