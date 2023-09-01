# Aurora scanner

A small program to extract aurora predictions using web scraping technique with Python Selenium and report to the ntfy.sh service.

## Workflow of web scraping:

1. Open https://www.gi.alaska.edu/monitors/aurora-forecast
1. Click on "Next" to open current day, because by default it shows previous day at start.
1. Select Europe region by clicking on the map of Europe.
1. Read the KP INDEX from scale (KP INDEX: 0 1 2 3 4 5 6 7 8 9). The current value is in bold.
1. If the current value is greater then or equal to threshold value (By default 5), then notify, that Aurora is visible today.
1. If the value is less, then continue pressing "Next" button 7 times. In each iteration check the KP VALUE. If it's greater or equal to threshold, then notify about the predicted date and KP VALUE.

## Receiving forecasts

To receive reports, install [Ntfy](https://ntfy.sh/) on your mobile phone and subscribe topic, which is configured on your project instance.

## Prerequisites [Ubuntu 22.04]
1. Installed Google Chrome (tested on v.116.0.5845.96)
1. (optional) Chrome driver https://googlechromelabs.github.io/chrome-for-testing/

## Installation [Ubuntu 22.04]
1. Clone git project on your server `git clone git@github.com:ATimrots/aurora_scanner.git .` (ssh example)
1. Install required Python packages from requirements.txt `pip install -r requirements.txt`
1. Configure .env variables. For `APP_ENV` use value `production` when you are using cron to run program in backroung. If it's set as production, then virtual display will be used instead of real Google Chrome display. You can adjust `KP_INDEX_THRESHOLD` as you wish to get the best results in your region. Example, in Latvia good starting point is KP 5. If it combines with enought dark night and no clouds, then it is high possibility to catch some Aurora. `NTFY_TOPIC` is used to know where to send notifications (See "Receiving forecasts" section).
1. Run app manually `python3 main.py` to test if no errors
1. Set up schedule `crontab -e`. Example, daily at 7am:
```
0 7 * * * /usr/bin/python3 ~/path/to/script/main.py
```
Example of `.env` file:
```
APP_ENV=local
KP_INDEX_THRESHOLD=5
NTFY_TOPIC=
```

## Disclaimer
Take into account, if you run this project on different instances with same ntfy topic, notifications will overlay.
