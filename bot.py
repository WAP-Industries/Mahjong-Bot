import nextcord
from nextcord.ext import commands
from openai import OpenAI, OpenAIError
import os

class Bot:
    Directory = os.path.dirname(os.path.abspath(__file__))
    Bot = commands.Bot(intents=nextcord.Intents.all(), command_prefix="!")
    GPT = None
    Context = None
    Notation={
        "Number": {
            "c": "Character",
            "d": "Dots",
            "b": "Bamboo",
        },
        "Honor": {
            "e": "East Wind",
            "s": "South Wind",
            "w": "West Wind",
            "n": "North Wind",
            "wh": "White Dragon",
            "g": "Green Dragon",
            "r": "Red Dragon",
            "a": "Animal",
            "f": "Flower"
        }
    }

    class Game:
        InSession = LastHand = None
        
        @staticmethod
        def Reset():
            Bot.Game.InSession = False
            Bot.Game.LastHand = None 
        

    @staticmethod
    def Run():
        Bot.GPT = OpenAI(api_key=os.environ.get("OPENAI_KEY"))
        Bot.Bot.run(os.environ.get("BOT_KEY"))

    @staticmethod
    async def Message(message):
        await Bot.Context.send(f"```{message}```")

    @staticmethod
    async def Error(message, tile=None):
        await Bot.Message(f"Error: {message}"+(f"\n\tat '{tile}'" if tile else ''))
        return False
    
    
    @staticmethod 
    def GetTiles(Hand):
        return [i.strip() for i in Hand.split(",") if len(i.strip())]
    
    @staticmethod
    def SortHand():
        Bot.Game.LastHand = ','.join(sorted(Bot.GetTiles(Bot.Game.LastHand)))
    
    @staticmethod 
    async def ValidateTile(Tile):
        [Number, Suit] = [Tile[0], Tile[1:]]
        try:
            Number = int(Number)
            return (await Bot.Error("Non-valid number tile", Tile) if Suit not in Bot.Notation["Number"] else True)
        except:
            return (await Bot.Error("Non-valid honor tile", Tile) if Tile not in Bot.Notation["Honor"] else True)

    @staticmethod
    async def ValidateHand(Hand):
        Tiles = Bot.GetTiles(Hand)
        if len(Tiles) not in [13, 14]: return await Bot.Error("Invalid number of tiles as starting hand")
        for i in Tiles:
            if not await Bot.ValidateTile(i):
                return False
        return True
    
    @staticmethod
    def GetResponse(user_input):
        try:
            Response = Bot.GPT.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                model="gpt-3.5-turbo",
            )
            return Response.choices[0].message.content.strip()
        except OpenAIError as e:
            return f"Error: {e}"
    
    @staticmethod
    async def GetMove(queries):
        def OrganiseHand():
            Hand = {} 
            for i in Bot.GetTiles(Bot.Game.LastHand):
                isNumber = i[0].isnumeric()
                Char = Bot.Notation["Number"][i[1:] if isNumber else i] if isNumber else "Honor"
                
                Hand[Char] = [] if Char not in Hand.keys() else Hand[Char]
                Hand[Char].append(i[0] if isNumber else Bot.Notation["Honor"][i])
            return {i:sorted(Hand[i]) for i in Hand}

        Tiles = OrganiseHand()

        return Bot.GetResponse('\n'.join([
            "I am playing Chinese Mahjong and this is my hand:",
            '\n'.join([f'{i} Tiles: {",".join(Tiles[i])}' for i in Tiles]),
            *queries
        ]))


@Bot.Bot.event
async def on_ready():
    Bot.Game.Reset()
    print("Mahjong bot is running")

@Bot.Bot.event
async def on_message(message):
    if message.author==Bot.Bot.user: return
    Bot.Context = message.channel
    await Bot.Bot.process_commands(message)