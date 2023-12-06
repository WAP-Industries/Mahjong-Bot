import sys
sys.dont_write_bytecode = True

from dotenv import load_dotenv

from commands import *

def main():
    load_dotenv()
    Bot.Run()


if __name__=="__main__":
    main()
