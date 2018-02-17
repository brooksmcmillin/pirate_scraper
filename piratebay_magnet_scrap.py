from urllib.request import Request, urlopen
from connection import DatabaseConnection
from torrent import Torrent


conn = DatabaseConnection()

def save_torrent(torrent_id):
    url = 'https://thepiratebay.org/torrent/' + str(torrent_id)
    req = Request(url)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
   
    print(url)
    try:     
        page = urlopen(req)
        content = page.read()

        torrent = Torrent(torrent_id)
        torrent.get_from_html(content)
    except:     
        torrent = Torrent(torrent_id)
    
    conn.insert_torrent(torrent)



for i in range(20125996):
    print(i) 
    save_torrent(i)

