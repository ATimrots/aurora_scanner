# Aurora scanner

A small program to extract aurora predictions using web scraping technique with Python Selenium and report to the ntfy.sh service.

## Workflow of web scraping:

1. Open https://www.gi.alaska.edu/monitors/aurora-forecast
1. Click on "Next" to open current day, because by default it shows previous day at start.
1. Select Europe region by clicking on the map of Europe.
1. Read the KP INDEX from scale (KP INDEX: 0 1 2 3 4 5 6 7 8 9). The current value is in bold.
1. If the current value is greater then or equal to threshold value (By default 5), then notify, that Aurora is visible today.
1. If the value is less, then continue press "Next" button 7 times. In each iteration check the KP VALUE. If it's greater or equal to threshold, then notify about the predicted date and KP VALUE.

## Receiving forecasts

Install [Ntfy](https://ntfy.sh/) on your mobile phone and subscribe topic `atimrots-aurora-alerts`.
