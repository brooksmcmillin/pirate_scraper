from urllib.request import Request, urlopen
from connection import DatabaseConnection
from torrent import Torrent


conn = DatabaseConnection()

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

# 100: Audio
# 200: Video
# 300: Applications
# 400: Games
# 500: Porn
# 600: Other
categories = [100, 200, 300, 400, 500, 600];

# Order: 7-Seeders DESC, 9-Leechers DESC
def create_url(category, page, order):
    return 'https://thepiratebay.org/browse/' + str(category) + '/' + str(page) + '/' + str(order)

url = create_url(categories[0], 0, 9)
url = 'https://thepiratebay.org/torrent/19892614'

req = Request(url)
req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')

print(url)

page = urlopen(req)
content = page.read()

torrent = Torrent(19892614)
torrent.get_from_html(content)
conn.insert_torrent(torrent)
