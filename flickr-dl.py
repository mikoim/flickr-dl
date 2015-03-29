__license__ = 'MIT'

import sys
import json
import urllib.request
import urllib.parse

api_url = 'https://api.flickr.com/services/rest/?'
api_key = 'TYPE YOUR API KEY'

user_id = 'TYPE YOUR VICTIM'


def main():
    page = 1
    page_max = 999

    while page <= page_max:
        print('{:d}/{:d}'.format(page, page_max), file=sys.stderr)

        request = urllib.request.Request(api_url + urllib.parse.urlencode(
            {'api_key': api_key, 'method': 'flickr.people.getPhotos', 'user_id': user_id,
             'extras': 'url_m,url_z,url_c,url_l,url_h,url_k,url_o', 'per_page': '500', 'page': page,
             'format': 'json', 'nojsoncallback': 1}))
        request.add_header('User-Agent', 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
        response = urllib.request.urlopen(request)

        root = json.loads(response.read().decode(encoding='utf-8'))

        if not root['stat'] == 'ok':
            return False

        page_max = root['photos']['pages']

        for photo in root['photos']['photo']:
            if 'url_o' in photo:  # Original
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
            elif 'url_sq' in photo: # Square
                print(photo['url_sq'])

        page += 1


if __name__ == '__main__':
    main()
