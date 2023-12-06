from bot import *

async def CheckSession():
    return (await Bot.Error("Game not in session yet, use !start to start new session") if not Bot.Game.InSession else True)

def PrintLastHand():
    return f"Current hand: {Bot.Game.LastHand}\nTiles: {len(Bot.GetTiles(Bot.Game.LastHand))}"

def GetTileRepr(notation):
    isNumber = notation[0].isnumeric()
    Suit = Bot.Notation["Number" if isNumber else "Honor"][notation[1:] if isNumber else notation]
    return (f"{notation[0]} of {Suit}s" if isNumber else Suit)+" Tile"



class CustomHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        Commands = sorted(Bot.Bot.commands, key=lambda c: c.name)
        Longest = len(sorted(Bot.Bot.commands, key=lambda c: len(c.name), reverse=True)[0].name)
        await Bot.Message("Commands:\n"+'\n'.join([f"\t{i.name:<{Longest+3}}{i.help}" for i in Commands]))
Bot.Bot.help_command = CustomHelp()

@Bot.Bot.command(help="limpeh")
async def exit(ctx):
    await ctx.send("Bye nigger")
    await Bot.Bot.close()



@Bot.Bot.command(help="Tile picture reference")
async def tiles(ctx):
    await ctx.send(file=nextcord.File(f"{Bot.Directory}\\assets\\tiles.png"))

@Bot.Bot.command(help="Tile notation reference")
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

@Bot.Bot.command(help="End current game simulation")
@SessionCommand()
async def end(ctx):
    Bot.Game.Reset()
    await Bot.Message("Session ended")

@Bot.Bot.command(help="Start new game simulation")
async def start(ctx, tiles):
    if Bot.Game.InSession: 
        return await Bot.Error("Game already in session. Use !end to start new game.")
    if not await Bot.ValidateHand(tiles): 
        return
    Bot.Game.LastHand = ','.join(Bot.GetTiles(tiles))
    Bot.SortHand()
    Bot.Game.InSession = True
    await Bot.Message(f"Session successfully started\n\n{PrintLastHand()}")

@Bot.Bot.command(help="Add tile to hand")
@SessionCommand()
async def add(ctx, tile):
    if not await Bot.ValidateTile(tile):
        return
    if len(Bot.GetTiles(Bot.Game.LastHand))>=14:
        return await Bot.Error("14 tiles already in hand, unable to add")
    Bot.Game.LastHand+=f",{tile}"
    Bot.SortHand()
    await Bot.Message(PrintLastHand())

@Bot.Bot.command(help="Discard tile from hand")
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
    
@Bot.Bot.command(help="inshallah you will claim the tile")
@SessionCommand()
async def claim(ctx, tile):
    if not await Bot.ValidateTile(tile):
        return
    if len(Bot.GetTiles(Bot.Game.LastHand))!=13: 
        return await Bot.Error("trick ass bitch u cant claim shit (invalid number of tiles)")
    Response = await Bot.GetMove([
        f"The last discarded tile was {GetTileRepr(tile.strip())}",
        "Is claiming the tile the best strategy? Without providing any explanation, present your answer in this format:",
        "Claim: [Yes/No]",
        "(if claiming is the best strategy) Discard: [Tile (with suit and number) to discard from my hand]"
    ])
    await ctx.send(f"```{PrintLastHand()}``````{Response}```")
    

@Bot.Bot.command(help="negromancy")
@SessionCommand()
async def move(ctx):
    if len(Bot.GetTiles(Bot.Game.LastHand))<14:
        return await Bot.Error("Insufficient number of tiles to play")
    Response = await Bot.GetMove([
        "Without providing any explanation, suggest which tile I should discard, and what sets to aim for, presenting your answer in the format:",
        "Discard: [Tile with suit and number]",
        "Sets: [Sets listed in point form, tiles separated with commas]"
    ])
    await ctx.send(f"```{PrintLastHand()}``````{Response}```")