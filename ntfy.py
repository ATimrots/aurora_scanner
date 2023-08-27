import requests
import os

def ntfy(message, tag = 'star_struck'):
    """
    See https://docs.ntfy.sh/ for more details
    """

    topic = os.getenv('NTFY_TOPIC')

    # Do not rise an error, but let it print out result without sending notification
    if topic == "" or topic == None:
        return

    h = {
        "Tags": tag,
        # "Actions": "view, Open portal, https://www.gi.alaska.edu/monitors/aurora-forecast"
    }

    requests.post("https://ntfy.sh/"+topic, data=message, headers=h)
