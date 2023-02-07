DinoBot (Legacy)
================

Bot Prefix
----------

The default prefix when you run the bot is `!`. It can be changed to avoid conflicts with other bots.

To change the prefix, use the following command:

```
!pf set "!db"
```

Otherwise, commands like `!bonk` should be `!db bonk` with a custom prefix.

Creating Bot Tokens
-------------------

To run & test locally, you will need a bot token.

1. Go to https://discord.com/developers/applications/
2. Create a new application. Name it something like `DinobotTest`
3. Once created, navigate to the "Bot" option in the sidebar, and click "Add Bot"
4. Just under the Username, will be a link called "Click to Reveal Token". Click it
5. Copy the token and put it in the blank secrets.py file
6. Scroll down and enabled the Privileged Gateway Intents
7. Navigate to the OAuth2 URL Generator, and select Bot, then check off the required permissions.
8. Copy the link and go to it, and proceed to add the bot to a server you own for testing purposes

```python
SUPER_USERS = []
BOT_TOKEN_DEV = 'TOKEN_GOES_HERE'
BOT_TOKEN_PROD = 'TOKEN_GOES_HERE'
BOT_TOKEN_LITE = 'TOKEN_GOES_HERE'
```

**Permissions:**

![permission text](https://cdn.discordapp.com/attachments/912081109028839424/912380005475029063/unknown.png)

Testing With Docker
-------------------

Please note: The initial build may be slow, but subsequent builds should be faster.

The `-v` option will mount the working directory to the container so that any changes you to the Python code can be "deployed" into the container without rebuilding it. You will have to stop/re-run the docker run command to restart the script.

**Windows:**

```
docker build -t dinobot .
docker run -itv ${PWD}:/usr/src/app dinobot # for windows
```

**Cygwin:**

```
docker build -t dinobot .
docker run -itv `cygpath -d $PWD`:/usr/src/app dinobot
```

**Linux:**

```
docker build -t dinobot .
docker run -itd -v /usr/src/dinobot/data:/usr/src/app/data -v /usr/src/dinobot:/usr/src/app dinobot
```

You should see output like this:

```
[Configuration: PROD] Logging in...
Successfully logged in as: DinobotTest#1280
```

Uploading Docker Image
----------------------

Save the image:

```
docker save -o dinobot.tar docker.io/library/dinobot
scp dinobot.tar bot-host
ssh bot-host
docker load dinobot.tar
```
