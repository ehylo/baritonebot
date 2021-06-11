# Baritone Discord Bot
The bot for the Baritone discord, made in python cause that's all I know.

Please submit prs cause this is probably really poorly made. (see [help.py](cogs/help.py) for all commands)

Links to [Baritone discord invite](https://discord.gg/s6fRBAUpmr) and [Main Baritone repo](https://github.com/cabaletta/baritone)
## Things to-do
### look more into
*   read [this](https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96) and see if it's better than current help command
*   support gifs in emote command
### can probably do
*   Show a leaderboard of the stats (currently tracking them just no way to display)
*   Add more options to the embed command (field, footer, author, image, etc) also be able to edit it
*   Add time to ban, also add weeks, months, years, and seconds (maybe more like decades :p) to the time aswell
*   Add some commands to change the roles/channels, preped for this by storing the ids in a db instead of hard coded
*   Add subrules to the rule command (like b?rule 4a)
*   Commands to add: polls, more api stuff (GitHub, cats, dog, random facts, literally any cool api)
## How to run
[requirements are here](requirements.txt)

Open terminal/cmd, and do the following commands:
```bash
git clone https://github.com/Flurrrr/baritonebot.git
cd baritonebot
python main.py
```
