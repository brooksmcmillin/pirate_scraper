import threading
import time
import sys
import getopt

from urllib.error import HTTPError
from urllib.request import Request, urlopen
from connection import DatabaseConnection
from torrent import Torrent

num_added = 0
categories = [100, 200, 300, 400, 500, 600]

def create_url(category, page):
    return 'https://thepiratebay.org/browse/' + str(category) + '/' + str(page) + '/7'

def save_torrent(url, category):
    conn = DatabaseConnection()

    req = Request(url)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')


    # Get Torrent ID
    start_string = 'torrent/'
    start = url.find(start_string)
    end = url.find('/', start + len(start_string))
    torrent_id = url[start + len(start_string) : end]
    
    try:     
        page = urlopen(req)
        content = page.read()

        torrent = Torrent(torrent_id, category)
        torrent.get_from_html(content)
    except:     
        torrent = Torrent(torrent_id, category)
    
    conn.insert_torrent(torrent)
    num_added = num_added + 1


def get_links_from_page(url, category, retrys=5):
   
    try: 
        req = Request(url)
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        
        links = []
       
        page = urlopen(req)
        content = page.read()

        search_content = content
        
        start_string = b'<div class="detName">'
        end_string = b'" class="detLink"' 

        while search_content.find(start_string) != -1:
            start = search_content.find(start_string)
            end = search_content.find(end_string, start)
            link = search_content[start + len(start_string) + 12:end]
            links.append(link)

            search_content = search_content[end:]
       
        for link in links:
            save_torrent('https://thepiratebay.org' + str(link.decode("utf-8") ), category)

        return len(links)
    except HTTPError as e: 
        if retrys > 0:
            get_links_from_page(url, category, retrys-1)
        else:
            print('Error: ' + str(e))
            return 0

def scrape_category(category):
    done = False
    i = 0
    while not done:
        #try:
        print("Cat " + str(category) + " Page " + str(i))
        num_links = get_links_from_page(create_url(category, i), category)
        if num_links == 0 and i > 30:
            done = True
        i = i + 1

# Get Category from Command line argument
try: 
    opts, args = getopt.getopt(sys.argv[1:], 'hc', ['category='])
except getopt.GetoptError: 
    print('piratebay_scrape.py -c <category>')
    sys.exit(2)
for opt, arg in opts:
    print(opt + ' :: ' + arg)
    if opt == '-h':
        print('piratebay_scrape.py -c <category>')
        sys.exit()
    elif opt in ('-c', '--category'):
        print('Found Category: ' + arg)
        category = sys.argv[2] # TODO: Change this to just 'arg' (when it works)

print('Category: ' + category)
scrape_category(category)
print('Done: ' + num_added + ' torrents scrapped')

