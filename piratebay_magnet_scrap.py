from urllib.request import Request, urlopen


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

# Get Magnet Link
link_pos = content.find(b'class="download"')
magnet_start = content.find(b'href="', link_pos) + 6
magnet_end = content.find(b'"', magnet_start)
magnet = content[magnet_start:magnet_end]

# Get Title
link_pos = content.find(b'<div id="title">')
start = link_pos + 16
end = content.find(b'</div>', start)
title = content[start:end].strip()

# Get Description
start = content.find(b'<pre>') + 5
end = content.find(b'</pre>', start)
desc = content[start:end]

# Get Seeders
link_pos = content.find(b'<dt>Seeders:</dt>')
start = content.find(b'<dd>', link_pos) + 4
end = content.find(b'</dd>', start)
seeders = content[start:end]

# Get Leechers
link_pos = content.find(b'<dt>Leechers:</dt>')
start = content.find(b'<dd>', link_pos) + 4
end = content.find(b'</dd>', start)
leechers = content[start:end]

# Get Uploaded Date
link_pos = content.find(b'<dt>Uploaded:</dt>')
start = content.find(b'<dd>', link_pos) + 4
end = content.find(b'</dd>', start)
uploaded_date = content[start:end]

# Get User
link_pos = content.find(b'<dt>By:</dt>')
start = content.find(b'/user/', link_pos) + 6
end = content.find(b'/', start)
user = content[start:end]

# Get Comment Count
link_pos = content.find(b'<dt>Comments</dt>')
start = content.find(b"<span id='NumComments'>", link_pos) + 23
end = content.find(b'</span>', start)
num_comments = content[start:end]

# Get Info Hash
link_pos = content.find(b'<dt>Info Hash:</dt>')
start = content.find(b'<dd></dd>', link_pos) + 9
end = content.find(b'</dl>', start)
info_hash = content[start:end].strip()


print(title)
print(magnet)
print(desc)
print(seeders)
print(leechers)
print(uploaded_date)
print(user)
print(num_comments)
print(info_hash)


#print(content)


