import re
import requests


def url_detector(string):
    """Find URLs in an string."""
    regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return regex.findall(string)


def detect_redirects(url):
    """Detect amount of redirects of the given url."""
    # TODO: handle http errors
    redirects = []
    try:
        response = requests.get(url, stream=True)  # using stream=True so it won't download the content.
        url = response.url
        if response.history:
            # redirected!
            for history in response.history:
                redirects.append(history.url)
    except requests.exceptions.ConnectionError:
        pass
    return redirects, url
