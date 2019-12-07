async def fritext(message):
    if 'göteborg' in message.content.lower():
        await message.channel.send("HALLÅ ELLER!?")
        return
    if ' keps' in message.content.lower() or message.content.lower().startswith('keps'):
        await message.channel.send("Du kan vara en keps!")
        return 
