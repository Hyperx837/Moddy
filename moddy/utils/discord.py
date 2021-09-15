from discord import Member, TextChannel, utils  # type: ignore


async def send_hook(name, channel: TextChannel, *args, user: Member = None, **kwargs):
    hook = utils.get(await channel.webhooks(), name=name)
    if not hook:
        hook = await channel.create_webhook(name=name)
    if user:
        await hook.send(
            *args, username=user.display_name, avatar_url=user.avatar_url, **kwargs
        )
    else:
        await hook.send(*args, **kwargs)


def get_mention(user: Member):
    return f"[{user.color}]@{user.display_name}[/{user.color}]"
