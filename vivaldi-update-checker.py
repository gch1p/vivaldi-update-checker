import requests, re

from argparse import ArgumentParser
from packaging import version
from ch1p import State, telegram_notify
from bs4 import BeautifulSoup


class VersionNotFoundError(RuntimeError): pass


class VivaldiUpdateChecker:
    def __init__(self):
        pass

    def get(self):
        r = requests.get('https://archlinux.org/packages/community/x86_64/vivaldi/')
        soup = BeautifulSoup(r.text, 'html.parser')
        meta = soup.select('meta[itemprop=version]')
        if meta:
            return meta[0]['content']
        raise VersionNotFoundError("version not found")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--print', action='store_true',
                        help='Print version and exit')
    args = parser.parse_args()

    state = State(default={'prev_version': '0.0'})

    try:
        checker = VivaldiUpdateChecker()
        cur_version = checker.get()

        if args.print:
            print(cur_version)
        else:
            if version.parse(state['prev_version']) < version.parse(cur_version):
                message = 'New Vivaldi version: <b>%s</b>. Download here: https://vivaldi.com/download/' % (cur_version)
                state['prev_version'] = cur_version
                telegram_notify(text=message, parse_mode='HTML')

    except VersionNotFoundError:
        print('version not found')
        pass

