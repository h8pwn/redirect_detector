# Redirect Detector
A Telegram bot that finds urls in user messages and detect their HTTP redirects. If any, will reply the result.

## Usage
First you need to obtain a token from BotFather and insert it in "tg_bot_token" in config.py.

Then run the following command to install Python package dependencies needed:
```bash
pip install -r requirements.txt
```

And to execute the bot:
```bash
python tg_bot.py
```

Note: In order for the bot to work in groups, it needs admin access.