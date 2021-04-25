import requests, re

from packaging import version
from ch1p import State, telegram_notify
from bs4 import BeautifulSoup


class VersionNotFoundError(RuntimeError): pass


class VivaldiUpdateChecker:
    def __init__(self):
        pass

    def get(self):
        r = requests.get('https://vivaldi.com/blog/')
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.select('.download-vivaldi-sidebar a')
        for link in links:
            if link['href'] == 'https://vivaldi.com/download/':
                return re.search(r'\((.*?)\)', link.get_text().strip()).group(1)
        raise VersionNotFoundError("version not found")


if __name__ == '__main__':
    state = State(default={'prev_version': '0.0'})

    try:
        checker = VivaldiUpdateChecker()
        cur_version = checker.get()

        if version.parse(state['prev_version']) < version.parse(cur_version):
            message = 'New Vivaldi version: <b>%s</b>. Download here: https://vivaldi.com/download/' % (cur_version)
            state['prev_version'] = cur_version
            telegram_notify(text=message, parse_mode='HTML')

    except VersionNotFoundError:
        print('version not found')
        pass

