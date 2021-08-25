# Baritone Discord Bot
The bot for the Baritone discord, made in python cause that's all I know.

Please submit prs cause this is probably really poorly made. (see [help.py](cogs/help.py) for all commands)

Links to [Baritone discord invite](https://discord.gg/s6fRBAUpmr) and [Main Baritone repo](https://github.com/cabaletta/baritone)
## Things to-do
*   support gifs in emote command
*   Add more options to the embed command (field, footer, author, image, etc.) also be able to edit it
*   Add some commands to change the roles/channels, preped for this by storing the ids in a db instead of hard coded
*   Add subrules to the rule command (like b?rule 4a)
*   GitHub command using the GitHub api
*   Redo everything to have buttons/slash commands when dpy 2.0 comes out
## How to run
Requires:
*   [Python 3.9](https://www.python.org/downloads/)
*   [Pip](https://pip.pypa.io/en/stable/installing/)
*   [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
*   [PostgreSQL database](https://www.postgresql.org/download/)

First, open terminal/cmd and do the following commands:
```bash
git clone https://github.com/Flurrrr/baritonebot.git
cd baritonebot
pip install -r requirements.txt
```
Then, make a `.env` file and add the following:
```dotenv
DATABASE_URL =
paste_token =
token =
```
Finally, start the bot:
```bash
python main.py
```
