# STATICBOT
Floraverse Companion bot
Hello! I am SlashScreen, and I enjoy the webcomic [Floraverse](https://floraverse.com/).


I noticed that there was an RSS feed that I could access on the website. So, I set about making a python script that could read the RSS feed and thell me if there were updates. And then I made a discord bot that can push a message to a server if there was an update.


USE:

Step 1: Open `private.json`.

Step 2: Fill in the json strings. `update-channels` and `update-servers` are what channels to ping with the rss updates on which servers, in the form of a list of snowflake ids. `test-channel` and `test-server` is for admin stuff, `self-id` is the id of the bot, `admin-id` is the id of the admin, and `token` is bot token.

Step 3: Run like a normal discord bot!

All availible public commands are shown [here](http://www.slashscreen.com/code/bots/static/statichelp.html).
