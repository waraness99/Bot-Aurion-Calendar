# Bot to get Aurion Calendar

The bot automatically connects to Aurion to retrieve the calendar events of the current week. It then exports the events in a .ics file so that you can import them into your calendar.

<div style="position: relative; padding-bottom: 64.86486486486486%; height: 0;"><iframe src="https://www.loom.com/embed/5a057eb5c62e4a8d84b4770131f1fd81" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>



## Configuration

**Download the program**
Clone this project, move to the root, then run the following command to download all required libraries:

```
pip install -r requirements.txt
```

**Download the Chrome Driver**
This program uses Selenium to automate your web browser. You will need to have [Google Chrome](https://www.google.com/chrome/) installed.

You will also need to install a Chrome Driver. This program allows you to automate Google Chrome. Go to [this link](https://chromedriver.chromium.org/downloads), and select the Driver corresponding to your OS and version of Google Chrome. Save the file to the root of your computer (or a place you can easily find later).

**Setup environment variables**
To connect to your Aurion account, the program needs your login and password. These elements being private, you will have to store them in a secured place. To do this, create a file called `.env` at the root of the project and fill in the following values:

```
CHROME_DRIVER_PATH=path to your chrome driver

AURION_EMAIL=your aurion email}
AURION_PASSWORD=your aurion password
```

*Just add your information without any quotes*

## To run the bot

To start the bot, you just have to launch the Python program. Everything else is automatic.
