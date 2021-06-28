import discord


class Moddy(discord.Client):
    async def on_ready(self):
        print("It's me, Moddy")
    
    async def on_message(self, message: discord.message.Message):
        print(f'{message.author} on #{message.channel}: {message.content}')
