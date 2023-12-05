import nextcord
from nextcord.ext import commands
import os

class Bot:
    Directory = os.path.dirname(os.path.abspath(__file__))
    Bot = commands.Bot(intents=nextcord.Intents.all(), command_prefix="!")
    Context = None
    Notation={
        "Number": {
            "c": "Character",
            "d": "Dots",
            "b": "Bamboo",
        },
        "Honor": {
            "e": "East",
            "s": "South",
            "w": "West",
            "n": "North",
            "wh": "White",
            "g": "Green",
            "r": "Red"
        }
    }
    Tiles = {
        "Numbered": [""]
    }

    class Game:
        InSession = LastHand = None
        @staticmethod
        def Reset():
            Bot.Game.InSession = False
            Bot.Game.LastHand = None 

    @staticmethod
    def Run():
        Bot.Bot.run(os.environ.get("BOT_KEY"))

    @staticmethod
    async def Message(message):
        await Bot.Context.send(f"```{message}```")

    @staticmethod
    async def Error(message, tile=None):
        await Bot.Message(f"Error: {message}"+(f"\n\tat '{tile}'" if tile else ''))
        return False
    

    @staticmethod
    async def GetLastHand():
        await Bot.Message(f"Current hand: {Bot.Game.LastHand}")
    
    @staticmethod 
    def GetTiles(Hand):
        return [i.strip() for i in Hand.split(",") if len(i.strip())]
    
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
        if len(Tiles)!=13: return await Bot.Error("Invalid number of tiles as starting hand")
        for i in Tiles:
            if not await Bot.ValidateTile(i):
                return False
        return True
    
    @staticmethod
    async def GetPlay():
        pass


    @Bot.event
    async def on_ready():
        Bot.Game.Reset()
        print("Mahjong bot is running")

    @Bot.event
    async def on_message(message):
        if message.author==Bot.Bot.user: return
        Bot.Context = message.channel
        await Bot.Bot.process_commands(message)



# client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )
# print(chat_completion)