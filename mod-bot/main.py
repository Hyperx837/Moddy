import os

from discord import client

from .logger import Moddy

def main():
    print(os.getenv('TOKEN'))
    client = Moddy()
    client.run(os.environ[ 'TOKEN' ])
