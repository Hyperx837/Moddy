import discord


class ModdyEmbed(discord.Embed):
    def __init__(self, title: str, description: str, **kwargs):
        super().__init__(**kwargs)
        self.color = 0x00B3EC
        self.title = title
        self.description = description


def command_not_allowed(command: str, permission: str):
    title = "You are not allowed to perform this action"
    desc = (
        f"You are not allowed to use command `{command}` because"
        f" of the missing permission **{permission}**"
    )
    return ModdyEmbed(title, desc)
