import feedparser

async def rssquery(querymsg, message, rss_url):
    if len(querymsg) == 1:
        await message.channel.send("Du kan väl åtminstone använda två tecken i din sökning?")
        return
    if len(querymsg) == 0:
        await message.channel.send("$rss <mellanslag> sökterm")
        return
    matches = 0
    news_feed = feedparser.parse(rss_url)
    entry = news_feed.entries

    for f in reversed(entry):
        if querymsg in f.title.lower():
            await message.author.send("%s\n%s\n<%s>\n%s\n----" % (f.published, f.title, f.link, f.description))
            matches = matches + 1
    if matches == 0:
        await message.channel.send("Inga träffar på %s" % querymsg)
    else:
        await message.channel.send("%i träff\(ar\) på %s" % (matches, querymsg))
