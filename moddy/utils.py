import discord
from rich.console import Console

console = Console()

def log(*args, **kwargs):
    console.log(*args, **kwargs)


class ModdyEmbed(discord.Embed):
    def __init__(self, title, description, **kwargs):
        super().__init__(**kwargs)
        self.color = 0xFFFFFF
        self.title = title
        self.description = description


numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
