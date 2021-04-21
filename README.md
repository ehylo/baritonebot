# Baritone Discord Bot
The bot for the Baritone discord, made in python cause that's all I know.

Please submit prs cause this is probably really poorly made. (see [help.py](cogs/help.py) for all commands)

Links to [Baritone discord invite](https://discord.gg/s6fRBAUpmr) and [Main Baritone repo](https://github.com/cabaletta/baritone)

## Things to-do:

### look more into
* add durations to mute command

* have a xp/rank system where it either tracks total messages, or you get random amount of xp (like 10-20) per message

* For the flip and rps commands, add db stats and stuff to that

* read [this](https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96) and see if it's better than current help command

* find a way to use the GitHub api and stuff to get info about the baritone repo

### can probably do
* Add more options to the embed command (field, footer, author, image, etc) will probably require a new function in [const.py](const.py) or just put it in [embed.py](cogs/embed.py), also be able to edit it

* Find a way to make the "Watching" in the status changeable with commands (don't know where to store this, don't really want to make a new thing in [values](cogs/values.py), might wait for database)

* Maybe add a nitro boost event like join/leave instead of discords default

* Add days to clear messages or max/none to ban command 

* Add gif support/improve the emote command

* Add a polls command

* Some sort of lockdown command where you can lock down specific channels or all of them or a specific category

## How to run

You need [python 3.9.0](https://www.python.org/downloads/) +, [discord.py 1.7.1](https://pypi.org/project/discord.py/), [python-dotenv](https://pypi.org/project/python-dotenv/), and [Pillow 8.2.0](https://pypi.org/project/Pillow/)

Open terminal/cmd, and do the following commands:
```
git clone https://github.com/Flurrrr/baritonebot.git
cd baritonebot
python bot.py
```
