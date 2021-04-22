# Baritone Discord Bot
The bot for the Baritone discord, made in python cause that's all I know.

Please submit prs cause this is probably really poorly made. (see [help.py](cogs/help.py) for all commands)

Links to [Baritone discord invite](https://discord.gg/s6fRBAUpmr) and [Main Baritone repo](https://github.com/cabaletta/baritone)

## Things to-do:
### look more into
* read [this](https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96) and see if it's better than current help command

* find a way to use the GitHub api and stuff to get info about the baritone repo
### can probably do
* Add durations to mute command

* Have a xp/rank system where it either tracks total messages, or you get random amount of xp (like 10-20) per message

* For the flip and rps commands, add db stats and stuff to that
  
* Add more options to the embed command (field, footer, author, image, etc) will probably require a new function in [const.py](const.py) or just put it in [embed.py](cogs/embed.py), also be able to edit it

* Make the "Watching" in the status changeable with commands (don't know where to store this, don't really want to make a new thing in [values](cogs/values.py), might wait for database)

* Add a nitro boost event like join/leave instead of discords default

* Add days to clear messages/max or no days to ban command 

* Add gif support/improve the emote command

* Add a polls command

* Some sort of lockdown command where you can lock down specific channels or all of them or a specific category

## How to run

[requirements are here](requirements.txt)

Open terminal/cmd, and do the following commands:
```
git clone https://github.com/Flurrrr/baritonebot.git
cd baritonebot
python bot.py
```
