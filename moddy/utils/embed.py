
import discord
class ModdyEmbed(discord.Embed):
    def __init__(self, title, description, **kwargs):
        super().__init__(**kwargs)
        self.color = 0xFFFFFF
        self.title = title
        self.description = description
