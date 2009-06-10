from core.exceptions import LocationNonExistant
import os
import urllib

import core.api as api

def http_download(link, location):
    assert link
    loc = os.path.isdir(location)
    filename = link.split('/')[-1:][0]
    if loc:
        data = urllib.urlretrieve(link, location + filename)
        urllib.urlcleanup()
    else:
        raise LocationNonExistant
