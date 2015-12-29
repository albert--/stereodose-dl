# stereodose-dl
# v1.0
# albert--@github

import wget, json, requests, mutagen, sys, glob
from os import remove, mkdir, path
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from bs4 import BeautifulSoup
from collections import defaultdict

link = str(sys.argv[1])
client_id = '8febd4179e4b98ccc312f9bfe21a5c8f'
r = requests.get(link)

soup = BeautifulSoup(r.text, "html.parser")
album = soup.title.string.split('|')[0].strip()
script = soup.findAll('script')[1].string

data = script.split('var songarray = ', 1)[-1].rsplit(';')[0]
json = json.loads(data)

songs = defaultdict(dict)
i = 0

for song in json:
    api = requests.get('http://api.soundcloud.com/tracks/' + song['stream_id'] + '.json?client_id=' + client_id).json()
    if 'errors' in api:
        continue
    
    if ' - ' in song['songtitle']:
        songs[i]['artist'] = song['songtitle'].split(' - ', 1)[0]
        songs[i]['title'] = song['songtitle'].split(' - ', 1)[1]
    else:
        songs[i]['artist'] = song['artist']
        songs[i]['title'] = song['songtitle']
    
    if song['webpic'] is None:
        if api['artwork_url'] is None:
            if api['user']['avatar_url'] is None:
                songs[i]['pic'] = None
            elif 'https://a1.sndcdn.com/images/default_avatar_large.png' in api['user']['avatar_url']:
                songs[i]['pic'] = None
            else:
                songs[i]['pic'] = api['user']['avatar_url'].replace('large', 't500x500')
        else:
            songs[i]['pic'] = api['artwork_url'].replace('large', 't500x500')
    else:
        songs[i]['pic'] = song['webpic'].replace('t300x300', 't500x500').rsplit('?')[0]

    songs[i]['genre'] = song['like_category_title']
    
    if api['downloadable'] is True:
        songs[i]['download_url'] = api['download_url'] + '?client_id=' + client_id
    else:
        songs[i]['download_url'] = api['stream_url'] + '?client_id=' + client_id
    
    i += 1

# modified https://gist.github.com/seanh/93666
def format_filename(s):
    import string
    valid_chars = '-_.() %s%s' % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    return filename

if not path.exists(format_filename(album)):
    mkdir(format_filename(album))
print('\nAlbum: ' + album + ' | Songs: ' + str(len(songs)) + '\n')

if not path.isfile('status.txt'):
    status = open('status.txt', 'w+')
else:
    status = open('status.txt', 'r+')
    oldfiles = glob.glob('stream.*.tmp')
    for file in oldfiles:
        remove(file)
skip = status.read()

for song in songs:
    if not skip:
        pass
    elif song <= int(skip):
        continue
    print('Downloading ' + str(song + 1) + '/' + str(len(songs)) + ': ' + format_filename(songs[song]['artist'] + ' - ' + songs[song]['title']))
    filename = wget.download(songs[song]['download_url'], out=format_filename(album) + '/' + format_filename(songs[song]['artist'] + ' - ' + songs[song]['title'] + '.mp3'))
    
    file = mutagen.File(filename, easy=True)
    try:
        file.add_tags()
    except:
        pass
    file['artist'] = songs[song]['artist']
    file['title'] = songs[song]['title']
    file['album'] = album
    file['genre'] = songs[song]['genre']
    file.save()

    if songs[song]['pic'] is not None:
        try:
            pic = wget.download(songs[song]['pic'])
            tag = MP3(filename, ID3=ID3)
            imgfile = open(pic, 'rb').read()
            img = APIC(3, 'image/jpeg', 3, 'Cover', imgfile)
            tag.tags.add(img)
            tag.save(v2_version=3) # id3v2.3 because windows
            remove(pic)
        except:
            pass

    status.seek(0)
    status.write(str(song))
    print('\n')

status.close()
remove('status.txt')

print('\n\nDone')
