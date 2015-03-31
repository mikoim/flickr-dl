# flickr-dl
The photo urls collector for [Flickr](https://www.flickr.com/ "Flickr") written by Python.

## How to use
    $ python3.4 flickr-dl.py -h
    usage: flickr-dl.py [-h] [-l LIMIT_PHOTO_ID] api_key user_id
    
    The photo urls collector for Flickr written by Python.
    
    positional arguments:
      api_key            API key
      user_id            Target username
    
    optional arguments:
      -h, --help         show this help message and exit
      -l LIMIT_PHOTO_ID  Stop collecting when its photo id found
    
    # Step 1: Collect photo urls using flickr-dl
    $ python3.4 flickr-dl.py bd3e5ad7631619ffe6bb398982739e53 lolcat > urls.txt
    
    # Step 2: Download a lot of photo!
    $ cat urls.txt | xargs -L 1 -P 4 -I@ wget -o log @
    # other is...
    $ cat urls.txt | xargs -L 1 -P 4 -I@ curl -O -s @
