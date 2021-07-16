import random

import discord


class ModdyEmbed(discord.Embed):
    def __init__(self, title: str, description: str = "", **kwargs):
        super().__init__(**kwargs)
        self.color = 0x00B3EC
        self.title = title
        self.description = description


class ModdyError(ModdyEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = 0x8F003C


class ModdySuccess(ModdyEmbed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = 0x7DEB34


def ping_embed(latency: int, elapsed: int):
    return ModdySuccess(
        "Pong 🏓 !!",
        f"latency: {round(latency * 1000, 3)}ms\nAPI: {elapsed}s",
    )


def command_not_allowed(command: str, permission: str) -> ModdyEmbed:
    title = "You are not allowed to perform this action"
    desc = (
        f"You are not allowed to use command `{command}` because"
        f" of the missing permission **{permission}**"
    )
    return ModdyError(title, desc)


def provide_value(command):
    pass


reload_embed = ModdyEmbed("Bot successfully reloaded 🦾")


def google_embed(query: str, answer: str, *, img=None) -> ModdyEmbed:
    phrases = [
        "Here you go sir 🎀🕴️...",
        "It's good that I had a magnifiying glass 🔎 🔍",
        "I search all over the world just for u 🗺️🌏",
        "I get exhauseted too mate 😮‍💨🤬",
        "Don't use this command that much. I'm very tired 😡",
        "Why did you call me, I was going to the washroom. ⚰️🧟‍♀️",
        "Oh man pls give me break ❤️‍🔥❤️‍🔥❤️‍🔥",
    ]
    title = random.choice(phrases)
    embed = ModdyEmbed(title, f'**Results for "{query}"**\n\n{answer}')
    if img:
        embed.set_thumbnail(url=img)
    # embed.set
    # embed.add_field(name=query, value="")
    return embed
