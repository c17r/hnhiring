import re
import time
from datetime import timedelta, datetime, timezone
from functools import wraps
from typing import List, Tuple, Iterator, Optional, Union

import requests
from bs4 import BeautifulSoup


_index_url = "https://news.ycombinator.com/submitted?id="
_data_url_fragment = "https://news.ycombinator.com/item?id={}&p={}"
_date_re = re.compile(r"(\w+ \d{4})")
_id_re = re.compile(r"=(\d+)")

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


def retry(times=-1, delay=0.5, errors=(Exception,)):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    count = count + 1
                    return f(*args, **kwargs)
                except errors as e:
                    if count == times:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator


def _unhumanize(human_time_interval: str) -> Union[timedelta, None]:
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


def _human_to_date(string: str) -> datetime:
    td = _unhumanize(string)
    return (datetime.now() + td) if td is not None else datetime.now()


def get_months(user: Optional[str] = None) -> List[Tuple[str, str]]:
    if user is None:
        user = "whoishiring"
    r = requests.get(_index_url + user)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select("td.title > span > a")
    hiring = [
        (_date_re.findall(i.text)[0], _id_re.findall(i["href"])[0])
        for i in links
        if "hiring" in i.text and _date_re.search(i.text) is not None
    ]
    return hiring


def get_data(hn_id: int) -> Iterator[Tuple[int, str, datetime]]:
    page = 1
    while True:
        print(f'\t\tProcessing Page {page}...')
        r = requests.get(_data_url_fragment.format(hn_id, page))
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for thing in soup.find_all('tr', {'class': 'athing'}):

            spacer = thing.find('img', {'src': 's.gif', 'width': 0})
            if spacer is None:
                continue

            thing_id = thing['id']

            if not thing.select("a#up_" + thing_id):
                continue

            item = thing.select('td.default')[0]
            links = item.find_all('a')

            if len(links) == 0:
                continue

            perma_link = links[1]
            date = _human_to_date(perma_link.text)
            perma_id = _id_re.findall(perma_link["href"])[0]

            div = item.find(class_='comment').find("span").find("div")
            if div:
                div.decompose()
            text = str(item.find(class_='comment').find('span'))

            yield int(perma_id), text, date

        if soup.find('a', {'class': 'morelink'}):
            page = page + 1
        else:
            return


@retry(times=5, errors=(requests.exceptions.RequestException, ))
def get_entry_datetime(hn_id: int) -> datetime:
    r = requests.get("https://hacker-news.firebaseio.com/v0/item/{}.json".format(hn_id))
    r.raise_for_status()
    data = r.json()
    return datetime.fromtimestamp(int(data['time']), tz=timezone.utc)


@retry(times=5, errors=(requests.exceptions.RequestException, ))
def process_job_feed() -> Iterator[dict]:
    r = requests.get('https://hacker-news.firebaseio.com/v0/jobstories.json')
    r.raise_for_status()
    data = r.json()
    for job_id in data:
        j = requests.get("https://hacker-news.firebaseio.com/v0/item/{}.json".format(job_id))
        j.raise_for_status()
        job_data = j.json()
        if _validate_job(job_data):
            job_data['time'] = datetime.fromtimestamp(int(job_data['time']), tz=timezone.utc)
            yield job_data


def _validate_job(job: dict|None) -> bool:
    if not job: return False
    title = job.get('title', '')
    url = job.get('url', '')
    text = job.get('text', '')
    return len(title) > 0 and (len(url) > 0 or len(text) > 0)
