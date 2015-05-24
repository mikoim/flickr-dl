# flickr-dl
The photo urls collector for [Flickr](https://www.flickr.com/ "Flickr") written in Python.

写真共有サイトであるFlickrから大きなサイズの写真のURLを収集するスクリプトです．  
ユーザー名やアルバムのIDを指定すると直接ダウンロード可能なURLを集めます．  
アップロードした写真のバックアップにでも．

## How to use
	$ python3.4 flickr-dl.py -h
	usage: flickr-dl.py [-h] [-p PHOTO_ID] [-u USER_ID] [-s PHOTOSET_ID]
	                    [-ls USER_ID_LS] [-l LIMIT_PHOTO_ID]
	                    api_key
	
	The photo urls collector for Flickr written by Python.
	
	positional arguments:
	  api_key            API key
	
	optional arguments:
	  -h, --help         show this help message and exit
	  -ua USER_AGENT     Set a new User-Agent
	  -p PHOTO_ID        Get a url by photo ID
	  -u USER_ID         Get urls by user ID
	  -s PHOTOSET_ID     Get urls by photoset ID
	  -ls USER_ID_LS     Get photoset ID by user ID
	  -l LIMIT_PHOTO_ID  Stop collecting when its photo id found

### ex) Download all photos from photo ID list
	$ for x in `cat ids.txt`; do python3.4 flickr-dl.py -p $x API_KEY >> urls.txt; done;
	$ cat urls.txt | xargs -L 1 -P 4 -I@ curl -O -s @

### ex) Download all photos from a particular user
	$ python3.4 flickr-dl.py -u USER_ID API_KEY > urls.txt
	$ cat urls.txt | xargs -L 1 -P 4 -I@ curl -O -s @

### ex) Download all photos from a particular photoset
	$ python3.4 flickr-dl.py -s PHOTOSET_ID API_KEY > urls.txt
	$ cat urls.txt | xargs -L 1 -P 4 -I@ curl -O -s @

### ex) Retrieve all photosets ID from a particular user
	$ python3.4 flickr-dl.py -ls USER_ID API_KEY | grep KEYWORD | cut -d ' ' -f 1 > photosets.txt
	$ for x in `cat photosets.txt`; do python3.4 flickr-dl.py -s $x API_KEY >> urls.txt; done;
	$ cat urls.txt | xargs -L 1 -P 4 -I@ curl -O -s @
