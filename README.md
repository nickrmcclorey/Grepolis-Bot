# Grepolis Bot

This project uses python and selenium to automate some boring tasks for the online game [Grepolis](https://en.grepolis.com/). This bot logs into grepolis and farms resources from farming villages. It then logs out, waits for the cooldown to end, and repeats the process. There is a GUI to select various options. See a video demonstration [here](https://www.youtube.com/watch?v=_WK7M6m7Z2g).

## Getting started

Unfortunately, this takes a little work to get started. There are a lot of prerequisites.

- Have a Grepolis account. You need to set this up yourself and join world and get past the tutorials so when the bot logs in, it's ready to farm.
- Install selenium. `pip install selenium`
- Install the webdriver. This is a single binary file that allows python to interact with your browser. See [this page](https://pypi.org/project/selenium/) for a list of webdriver downloads. I suggest using chrome.

Once you have everything in place, start the app at main.py using python 3

`python main.py`