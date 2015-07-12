import re
from datetime import timedelta, datetime
import requests
from bs4 import BeautifulSoup


_index_url = "https://news.ycombinator.com/submitted?id="
_data_url_fragment = "https://news.ycombinator.com/item?id="
_date_re = re.compile("(\w+ \d{4})")
_id_re = re.compile("=(\d+)")

_DELTAS = {
    'now': timedelta(seconds=0),
    'moment': timedelta(seconds=1),
    'second': timedelta(seconds=1),
    'minute': timedelta(minutes=1),
    'hour': timedelta(hours=1),
    'day': timedelta(days=1),
    'week': timedelta(weeks=1),
    # months and years are approximate.
    'month': timedelta(days=30),
    'year': timedelta(days=365)
}
_SINGULARS = ['a ', 'an ', 'just ']


def _unhumanize(human_time_interval):
    """Converts human_time_interval (e.g. 'an hour ago') into a
    datetime.timedelta.
    """
    munged = human_time_interval.strip()
    for needle in _SINGULARS:
        munged = munged.replace(needle, '1 ')

    interval_re = '|'.join(_DELTAS.keys())
    sre = re.match(r'[. ]*([0-9]*)[ ]*(' + interval_re + r')s?( ago)?', munged)

    if sre:
        ago = sre.groups(1)[2] == ' ago'
        mul = int(sre.groups(1)[0])
        if ago:
            mul = mul * -1
        delta = _DELTAS[sre.groups(1)[1]]
        return delta * mul
    else:
        return None


def _human_to_date(string):
    td = _unhumanize(string)
    return (datetime.now() + td).strftime("%Y-%m-%d %H:%M:%S")


def get_months(user=None):
    if user is None:
        user = "whoishiring"
    r = requests.get(_index_url + user)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select("td.title > a")
    hiring = [
        (_date_re.findall(i.text)[0], _id_re.findall(i["href"])[0])
        for i in links
        if "hiring" in i.text and _date_re.search(i.text) is not None
    ]
    return hiring


def get_data(hn_id):
    r = requests.get(_data_url_fragment + hn_id)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for entry in soup.find_all("img", {"src": "s.gif", "width": 0}):
        if len(entry.contents) > 0:
            continue
        item = entry.parent.find_next_sibling("td", {"class": "default"})
        if '[deleted]' in str(item):
            continue
        perma_link = item.find_all("a")[1]
        date = _human_to_date(perma_link.text)
        perma_id = _id_re.findall(perma_link["href"])[0]
        text = str(item.find("span", {"class": "comment"}).find("font"))
        yield perma_id, text, date
