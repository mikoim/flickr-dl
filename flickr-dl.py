#!/usr/bin/env python3

import sys
import json
import urllib.request
import urllib.parse
import argparse
import configparser
from os.path import expanduser

__author__ = 'Eshin Kunishima'
__license__ = 'MIT'


class Flickr:
    __api_url = 'https://api.flickr.com/services/rest/?'
    __user_agent = 'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285'

    def __init__(self, api_key, user_agent=None):
        self.__api_key = api_key

        if user_agent:
            self.__user_agent = user_agent

    def __call_api(self, list_args):
        request = urllib.request.Request(self.__api_url + urllib.parse.urlencode(list_args))
        request.add_header('User-Agent', self.__user_agent)
        response = urllib.request.urlopen(request)
        return response.read().decode(encoding='utf-8')

    def get_biggest_url_by_photo_id(self, photo_id):
        root = json.loads(self.__call_api({
            'method': 'flickr.photos.getSizes', 'api_key': self.__api_key, 'photo_id': photo_id,
            'format': 'json', 'nojsoncallback': 1
        }))

        if not root['stat'] == 'ok':
            raise Exception(root['message'])

        normalized = map(lambda x: (int(x['width']) * int(x['height']), x['source']), root['sizes']['size'])

        return sorted(normalized, key=lambda x: -x[0])[0][1]

    @staticmethod
    def __get_biggest_url_by_extras(extras):
        if 'url_o' in extras:  # Original
            return extras['url_o']
        elif 'url_k' in extras:  # Large 2048
            return extras['url_k']
        elif 'url_h' in extras:  # Large 1600
            return extras['url_h']
        elif 'url_l' in extras:  # Large
            return extras['url_l']
        elif 'url_c' in extras:  # Medium 800
            return extras['url_c']
        elif 'url_z' in extras:  # Medium 640
            return extras['url_z']
        elif 'url_m' in extras:  # Medium
            return extras['url_m']
        elif 'url_n' in extras:  # Small 320
            return extras['url_n']
        elif 'url_s' in extras:  # Small
            return extras['url_s']
        elif 'url_t' in extras:  # Thumbnail
            return extras['url_t']
        elif 'url_q' in extras:  # Large Square
            return extras['url_q']
        elif 'url_sq' in extras:  # Square
            return extras['url_sq']
        else:
            raise Exception('unable to identify size')

    def print_photoset(self, user_id=None):
        page = 1
        page_max = 999

        while page <= page_max:
            print('{:d}/{:d}'.format(page, page_max), file=sys.stderr)

            root = json.loads(self.__call_api({
                'method': 'flickr.photosets.getList', 'api_key': self.__api_key, 'user_id': user_id, 'page': page,
                'per_page': 500, 'format': 'json', 'nojsoncallback': 1
            }))

            if not root['stat'] == 'ok':
                raise Exception(root['message'])

            page_max = root['photosets']['pages']

            for photoset in root['photosets']['photoset']:
                print(photoset['id'], photoset['title']['_content'])

            page += 1

    def print_url(self, user_id=None, photoset_id=None, limit_photo_id=None):
        page = 1
        page_max = 999

        base_parameters = {
            'api_key': self.__api_key, 'per_page': '500', 'format': 'json', 'nojsoncallback': 1,
            'extras': 'url_sq,url_q,url_t,url_s,url_n,url_m,url_z,url_c,url_l,url_h,url_k,url_o'
        }

        while page <= page_max:
            print('{:d}/{:d}'.format(page, page_max), file=sys.stderr)

            if user_id:
                parameters = {'method': 'flickr.people.getPhotos', 'user_id': user_id, 'page': page}
                method = 'photos'
            elif photoset_id:
                parameters = {'method': 'flickr.photosets.getPhotos', 'photoset_id': photoset_id, 'page': page}
                method = 'photoset'
            else:
                return

            parameters.update(base_parameters)

            root = json.loads(self.__call_api(parameters))

            if not root['stat'] == 'ok':
                raise Exception(root['message'])

            page_max = root[method]['pages']

            for photo in root[method]['photo']:
                if photo['id'] == limit_photo_id:
                    print('limit_photo_id: {:s} found.'.format(limit_photo_id), file=sys.stderr)
                    return
                try:
                    print(self.__get_biggest_url_by_extras(photo))
                except:
                    print(photo, file=sys.stderr)
                    page_max = 0

            page += 1


def config(api_key):
    config_file = expanduser('~/.flickr-dl')

    parser = configparser.ConfigParser()
    parser.read(config_file)

    if api_key:
        parser['Options'] = {}
        parser['Options']['APIKey'] = api_key

        parser.write(open(config_file, mode='w'))

    if 'Options' in parser and 'APIKey' in parser['Options']:
        return parser['Options']['APIKey']
    else:
        return None


def main():
    parser = argparse.ArgumentParser(description='The photo urls collector for Flickr written by Python.')
    parser.add_argument('--api', dest='api_key', type=str, help='Set new API key and save to ~/.flickr-dl')
    parser.add_argument('--user-agent', dest='user_agent', type=str, help='Set new User-Agent')
    parser.add_argument('--photo', dest='photo_id', type=str, help='Get url by photo ID')
    parser.add_argument('--user', dest='user_id', type=str, help='Get urls by user ID')
    parser.add_argument('--photo-set', dest='photo_set_id', type=str, help='Get urls by photo set ID')
    parser.add_argument('--list-photo-set', dest='list_photo_set', type=str, help='Get list of photo set ID by user ID')
    parser.add_argument('--stop-photo', dest='limit_photo_id', type=str, help='Stop collecting when its photo id found')

    arguments = parser.parse_args()

    api_key = config(arguments.api_key)
    user_agent = arguments.user_agent
    limit_photo_id = arguments.limit_photo_id

    photo_id = arguments.photo_id
    user_id = arguments.user_id
    photo_set_id = arguments.photo_set_id
    list_photo_set = arguments.list_photo_set

    count_option = len(list(filter(lambda x: x is not None, [photo_id, user_id, photo_set_id, list_photo_set])))

    if count_option != 1:
        print('You must use one of --user or --photo-set, --stop-photo.', file=sys.stderr)
        return 1

    if api_key is None:
        print('API key is undefined. You must use --api option. (It will be stored on ~/.flickr-dl)', file=sys.stderr)
        return 1

    if user_agent:
        f = Flickr(api_key, user_agent)
    else:
        f = Flickr(api_key)

    if photo_id:
        print(f.get_biggest_url_by_photo_id(photo_id))
    elif list_photo_set:
        f.print_photoset(list_photo_set)
    else:
        f.print_url(user_id, photo_set_id, limit_photo_id)


if __name__ == '__main__':
    sys.exit(main())
