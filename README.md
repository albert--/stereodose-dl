# stereodose-dl
Stereodose.com user playlist downloader written in Python 3

###Usage
`python stereodose-dl.py <user playlist link>`

example:

`python stereodose-dl.py https://www.stereodose.com/user_playlist/8436/road-trip`

###Installation
- tl;dr `pip install requests wget mutagen beautifulsoup4`

or
- wget `pip install wget`
- Requests `pip install requests`
- Mutagen `pip install mutagen`
- BeautifulSoup 4 `pip install beautifulsoup4`

###Features
- Downloads Stereodose.com user playlists
- Automatic mp3 tagging (ID3v2.3, Windows doesn't support ID3v2.4 in Windows Explorer)
  - Artist
  - Title
  - Album (Playlist title)
  - Genre (Campfire, Chill, etc.)
  - Cover (If there is no cover the avatar of the SoundCloud user is used)
- Resume downloads
