import threading
import time

from urllib.request import Request, urlopen
from connection import DatabaseConnection
from torrent import Torrent

conn = DatabaseConnection()

categories = [100, 200, 300, 400, 500, 600]

# For Testing Purposes
categories = [100] 

def create_url(category, page):
    return 'https://thepiratebay.org/browse/' + str(category) + '/' + str(page) + '/7'


def save_torrent(url):
    req = Request(url)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')


    # Get Torrent ID
    start_string = 'torrent/'
    start = url.find(start_string)
    end = url.find('/', start + len(start_string))
    torrent_id = url[start + len(start_string) : end]
    print(torrent_id)
   
    print(url)
    try:     
        page = urlopen(req)
        content = page.read()

        torrent = Torrent(torrent_id)
        torrent.get_from_html(content)
    except:     
        torrent = Torrent(torrent_id)
    
    conn.insert_torrent(torrent)


def get_links_from_page(url):
    req = Request(url)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')

    page = urlopen(req)
    content = page.read()

    search_content = content
    links = []
    
    start_string = b'<div class="detName">'
    end_string = b'" class="detLink"' 

    while search_content.find(start_string) != -1:
        start = search_content.find(start_string)
        end = search_content.find(end_string, start)
        link = search_content[start + len(start_string) + 12:end]
        links.append(link)

        search_content = search_content[end:]

    for link in links:
        save_torrent('https://thepiratebay.org' + str(link.decode("utf-8") ))

class pirateThread(threading.Thread):

    def __init__(self, category):
        threading.Thread.__init__(self)
        self.category = category

    def run(self):
        print("Starting cat " + str(self.category))
        print(get_links_from_page(create_url(category, 0)))
        print('Exiting cat ' + str(self.category))        


# For category in categories start a thread
for category in categories: 
    thread = pirateThread(category)
    thread.start()


