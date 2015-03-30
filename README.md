# flickr-dl
The photo urls collector for [Flickr](https://www.flickr.com/ "Flickr") written by Python.

## How to use
    # Step 1: Enter your API key and victim ID (User name)
    vim flickr-dl.py
    
    # Step 2: Collect photo urls using flickr-dl
    python3.4 flickr-dl.py > urls.txt
    
    # Step 3: Download a lot of photo!
    cat urls.txt | xargs -L 1 -P 0 -I@ wget -o log @
