# flickr-dl
The photo urls collector for [Flickr](https://www.flickr.com/ "Flickr") written in Python.

写真共有サイトであるFlickrから大きなサイズの写真のURLを収集するスクリプトです．  
ユーザー名やアルバムのIDを指定すると直接ダウンロード可能なURLを集めます．  
アップロードした写真のバックアップにでも．

## How to use

```bash
python3.5 flickr-dl.py -h

usage: flickr-dl.py [-h] [--api API_KEY] [--user-agent USER_AGENT]
                    [--photo PHOTO_ID] [--user USER_ID]
                    [--photo-set PHOTO_SET_ID]
                    [--list-photo-set LIST_PHOTO_SET]
                    [--stop-photo LIMIT_PHOTO_ID]

The photo urls collector for Flickr written by Python.

optional arguments:
  -h, --help            show this help message and exit
  --api API_KEY         Set new API key and save to ~/.flickr-dl
  --user-agent USER_AGENT
                        Set new User-Agent
  --photo PHOTO_ID      Get url by photo ID
  --user USER_ID        Get urls by user ID
  --photo-set PHOTO_SET_ID
                        Get urls by photo set ID
  --list-photo-set LIST_PHOTO_SET
                        Get list of photo set ID by user ID
  --stop-photo LIMIT_PHOTO_ID
                        Stop collecting when its photo id found
```

### ex) Set API key and save

```bash
python3.5 flickr-dl.py --api TYPE_YOUR_API_KEY

# Or you can also use --api option with other operations.
python3.5 flickr-dl.py --api TYPE_YOUR_API_KEY --user nasahqphoto
```

### ex) Download all photos from photo ID list

```bash
for x in `cat ids.txt`; do python3.5 flickr-dl.py --photo $x >> urls.txt; done;
cat urls.txt | xargs -L 1 -P 4 -I@ curl -O -s @
```

### ex) Download all photos from a particular user

```bash
python3.5 flickr-dl.py --user USER_ID > urls.txt
cat urls.txt | xargs -L 1 -P 4 -I@ curl -O -s @
```

### ex) Download all photos from a particular photoset

```bash
python3.5 flickr-dl.py --photo-set PHOTOSET_ID > urls.txt
cat urls.txt | xargs -L 1 -P 4 -I@ curl -O -s @
```

### ex) Retrieve all photosets ID from a particular user

```bash
python3.5 flickr-dl.py --list-photo-set USER_ID | grep KEYWORD | cut -d ' ' -f 1 > photosets.txt
for x in `cat photosets.txt`; do python3.5 flickr-dl.py --photo-set $x >> urls.txt; done;
cat urls.txt | xargs -L 1 -P 4 -I@ curl -O -s @
```
