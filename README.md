# Baritone Discord Bot
The bot for the Baritone discord, made in python because you can type fast.

Links: 
*   [Baritone discord invite](https://discord.gg/s6fRBAUpmr)
*   [Main Baritone repo](https://github.com/cabaletta/baritone)
## Things to-do
*   will update this when I merge into master
## How to run
Requires:
*   [Python 3.10.1](https://www.python.org/downloads/)
*   [Pip](https://pip.pypa.io/en/stable/installing/)
*   [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
*   [PostgreSQL database](https://www.postgresql.org/download/)

First, open terminal/cmd and do the following commands:
```bash
git clone https://github.com/Flurrrr/baritonebot.git
cd baritonebot
pip install -r requirements.txt
```
Then, make a `.env` file and add these variables:
```dotenv
DATABASE_URL =
GUILD_ID = 
DISCORD_TOKEN =
PASTE_TOKEN =
GITHUB_TOKEN = 
```
Finally, start the bot:
```bash
python main.py
```
