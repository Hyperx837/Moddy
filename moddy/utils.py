import discord
from rich.console import Console

console = Console()


def log(*args, **kwargs):
    console.log(*args, **kwargs)


async def check_perm(command: str = ""):
    pass


def user_mention(user: discord.User, text: str):
    log(f"[{user.color}]@{user.name}[/{user.color}] ", text)


numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
