import requests

def ntfy(message, tag = 'star_struck'):
    """
    See https://docs.ntfy.sh/ for more details
    """
    h = {
        "Tags": tag,
        # "Actions": "view, Open portal, https://www.gi.alaska.edu/monitors/aurora-forecast"
    }

    requests.post("https://ntfy.sh/atimrots-aurora-alerts", data=message, headers=h)
