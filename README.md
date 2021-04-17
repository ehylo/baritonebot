# Baritone Discord Bot
The bot for the Baritone discord, made in python cause that's all I know.

Please submit prs cause this is probably really poorly made. (see [help.py](cogs/help.py) for all commands)

Links to [Baritone discord invite](https://discord.gg/s6fRBAUpmr) and [Main Baritone repo](https://github.com/cabaletta/baritone)

## Things to-do:

### look more into
* use a database (no clue where to even start)

* add durations to mute command (requires database I think, though might be possible with just json)

* have a xp/rank system where it either tracks total messages, or you get random amount of xp (like 10-20) per message (probably requires database but I think I know a way with json)

* read [this](https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96) and see if it's better than current help command

* find a way to use the GitHub api and stuff to get info about the baritone repo

### can probably do
* Add trash emote delete to regex responses

* add a coin flip command/rock paper scissors

* add aliases to as many commands as possible, then add those aliases to each command's help

* clear a specific member's messages only without banning

* add more options to the embed command (field, footer, author, image, etc) will probably require a new function in [const.py](cogs/const.py) or just put it in [embed.py](cogs/embed.py), also be able to edit it

* find a way to make the "Watching" in the status changeable with commands

* maybe add a nitro boost event like join/leave instead of discords default

* add days to clear messages or max/none to ban command 

* add gif support/improve the emote command

* Some sort of lockdown/sync command where you can lock down specific channels or just sync them with the category

## How to run

You need [python 3.9.0](https://www.python.org/downloads/) +, [discord.py 1.7.1](https://pypi.org/project/discord.py/), and [Pillow 8.2.0](https://pypi.org/project/Pillow/)

Open terminal/cmd, and do the following commands:
```
git clone https://github.com/Flurrrr/baritonebot.git
cd baritonebot
python bot.py
```
