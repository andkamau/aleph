from aleph.crawlers.crawler import Crawler
import requests

SOURCE_AFRICA_URL = "http://dc.sourceafrica.net/api/search.json"

class SourceAfricaCrawler(Crawler):
    '''
    '''

    def get_documents():
        '''
        retrieve docs from sourceAfrica API
        '''
        resp = requests.get(url, params=dict(q='', per_page=1000), timeout=4)
        try:
            resp.raise_for_status()
        except:
            err = "sourceAfrica search fail: %s - %s" % (resp.status_code,
                    resp.text)
            log.warning(err)
            return
        docs = resp.json()
        print "fetched %s documents" % len(docs['documents'])
        return docs['documents']


    def crawl(self):
        documents = get_documents()
        source = self.create_source(foreign_id='sourceafrica', label='sourceafrica.net documents')
        for idx in range(0, len(documents)):
            doc = documents[idx]
            print "document %s of %s: {id} | {title} | {file_hash}".format(**doc) % (idx, len(documents))
            meta = self.metadata()
            meta.foreign_id = "sourceafrica.%s" % doc['id']
            meta.title = "%s" % doc['title']
            meta.mime_type = "application/pdf"
            meta.hash = doc['file_hash']
            self.emit_url(source, meta, doc['resources']['pdf'])
