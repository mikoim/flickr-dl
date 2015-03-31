__author__ = 'Eshin Kunishima'
__license__ = 'MIT'

import sys
import json
import urllib.request
import urllib.parse
import argparse

api_url = 'https://api.flickr.com/services/rest/?'


def main():
    page = 1
    page_max = 999

    parser = argparse.ArgumentParser(description='The photo urls collector for Flickr written by Python.')
    parser.add_argument('api_key', type=str, help='API key')
    parser.add_argument('user_id', type=str, help='Target username')
    parser.add_argument('-l', type=str, default=None, dest='limit_photo_id', required=False,
                        help='Stop collecting when its photo id found')
    arguments = parser.parse_args()

    api_key = arguments.api_key
    user_id = arguments.user_id
    limit_photo_id = arguments.limit_photo_id

    while page <= page_max:
        print('{:d}/{:d}'.format(page, page_max), file=sys.stderr)

        request = urllib.request.Request(api_url + urllib.parse.urlencode(
            {'api_key': api_key, 'method': 'flickr.people.getPhotos', 'user_id': user_id,
             'extras': 'url_sq,url_q,url_t,url_s,url_n,url_m,url_z,url_c,url_l,url_h,url_k,url_o',
             'per_page': '500', 'page': page, 'format': 'json', 'nojsoncallback': 1}))
        request.add_header('User-Agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
        response = urllib.request.urlopen(request)

        root = json.loads(response.read().decode(encoding='utf-8'))

        if not root['stat'] == 'ok':
            print(root['message'])
            return False

        page_max = root['photos']['pages']

        for photo in root['photos']['photo']:
            if photo['id'] == limit_photo_id:
                print('limit_photo_id: {:s} found.'.format(limit_photo_id))
                page_max = 0
                break
            elif 'url_o' in photo:  # Original
                print(photo['url_o'])
            elif 'url_k' in photo:  # Large 2048
                print(photo['url_k'])
            elif 'url_h' in photo:  # Large 1600
                print(photo['url_h'])
            elif 'url_l' in photo:  # Large
                print(photo['url_l'])
            elif 'url_c' in photo:  # Medium 800
                print(photo['url_c'])
            elif 'url_z' in photo:  # Medium 640
                print(photo['url_z'])
            elif 'url_m' in photo:  # Medium
                print(photo['url_m'])
            elif 'url_n' in photo:  # Small 320
                print(photo['url_n'])
            elif 'url_s' in photo:  # Small
                print(photo['url_s'])
            elif 'url_t' in photo:  # Thumbnail
                print(photo['url_t'])
            elif 'url_q' in photo:  # Large Square
                print(photo['url_q'])
            elif 'url_sq' in photo:  # Square
                print(photo['url_sq'])
            else:
                print(photo)
                page_max = 0

        page += 1


if __name__ == '__main__':
    main()
