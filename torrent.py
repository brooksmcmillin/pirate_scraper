class Torrent:
    id = -1
    title = None
    magnet = None
    desc = None
    seeders = 0
    leachers = 0
    upload_date = None
    user = None
    num_comments = 0
    info_hash = None

    def __init__(self, id):
        self.id = id

    def get_from_html(self, content):
        # Get Magnet Link
        link_pos = content.find(b'class="download"')
        magnet_start = content.find(b'href="', link_pos) + 6
        magnet_end = content.find(b'"', magnet_start)
        self.magnet = content[magnet_start:magnet_end]

        # Get Title
        link_pos = content.find(b'<div id="title">')
        start = link_pos + 16
        end = content.find(b'</div>', start)
        self.title = content[start:end].strip()

        # Get Description
        start = content.find(b'<pre>') + 5
        end = content.find(b'</pre>', start)
        self.desc = content[start:end]

        # Get Seeders
        link_pos = content.find(b'<dt>Seeders:</dt>')
        start = content.find(b'<dd>', link_pos) + 4
        end = content.find(b'</dd>', start)
        self.seeders = content[start:end]

        # Get Leechers
        link_pos = content.find(b'<dt>Leechers:</dt>')
        start = content.find(b'<dd>', link_pos) + 4
        end = content.find(b'</dd>', start)
        self.leachers = content[start:end]

        # Get Uploaded Date
        link_pos = content.find(b'<dt>Uploaded:</dt>')
        start = content.find(b'<dd>', link_pos) + 4
        end = content.find(b'</dd>', start)
        self.upload_date = content[start:end]

        # Get User
        link_pos = content.find(b'<dt>By:</dt>')
        start = content.find(b'/user/', link_pos) + 6
        end = content.find(b'/', start)
        self.user = content[start:end]

        # Get Comment Count
        link_pos = content.find(b'<dt>Comments</dt>')
        start = content.find(b"<span id='NumComments'>", link_pos) + 23
        end = content.find(b'</span>', start)
        self.num_comments = content[start:end]

        # Get Info Hash
        link_pos = content.find(b'<dt>Info Hash:</dt>')
        start = content.find(b'<dd></dd>', link_pos) + 9
        end = content.find(b'</dl>', start)
        self.info_hash = content[start:end].strip()
