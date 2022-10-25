# Baritone Discord Bot
The bot for the Baritone discord, made in python because you can type fast.

Links: 
*   [Baritone discord invite](https://discord.gg/s6fRBAUpmr)
*   [Main Baritone repo](https://github.com/cabaletta/baritone)
## Things to-do
*   Add an `on_error` listener to all buttons
*   Create an extension command to allow me to control extensions to fix them
*   Find out how to catch the rare cursor db problem and deal with it
*   Add logging to everything, currently there is none
*   Make the response list command have pages so the embed limit isn't reached with lots of responses
*   For the ban command add the ability to set a time, so it can be a temporary ban
*   Be able to edit the rules with a rule edit command
*   Have the bot control the rules embed and match the rules
*   Ability to change the channel and role ids, currently just manually in the db
*   Make the main db hold objects not ids, might be limited with what I can do but try to do roles/channels
*   Make the db create tables and a default db if nothing is there, allows others besides me to test things
*   Add comment stuff to the GitHub commands
*   Try to make env variables semi-optional in the way that some things are disabled when a specific one isn't present
*   Edit-embed command to edit embeds the bot sent (besides the rules)
*   Change all of the `Literal` code to choices, so it's less this equals that
*   Banner and accent color could be added to the info command, just need to deal with people who don't have those
*   Make the help command much better, pages for the different levels of commands, and descriptions with what each does
## How to run
Requires:
*   [Python 3.10.1](https://www.python.org/downloads/)
*   [Pip](https://pip.pypa.io/en/stable/installing/)
*   [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
*   [PostgreSQL database](https://www.postgresql.org/download/)

First, open terminal/cmd and do the following commands:
```bash
git clone https://github.com/ehylo/baritonebot.git
cd baritonebot
pip install -r requirements.txt
```
Then, make a `.env` file and add these variables:
```dotenv
DATABASE_URL=
GUILD_ID=
DISCORD_TOKEN=
PASTE_TOKEN=
GITHUB_TOKEN=
```
Finally, start the bot:
```bash
python main.py
```
