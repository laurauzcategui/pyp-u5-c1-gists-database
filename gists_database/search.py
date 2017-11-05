from .models import Gist
import sqlite3


class SearchExplore(object):
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def all(self):
        return GistsIterator(self.db_connection)

    def search(self, id=None, github_id=None, html_url=None, git_pull_url=None, git_push_url=None, commits_url=None, forks_url=None, public=None, created_at=None, updated_at=None, comments=None, comments_url=None):
        params = {'id'          : None,
                  'github_id'    : None,
                  'html_url'     : None,
                  'git_pull_url' : None,
                  'git_push_url' : None,
                  'commits_url'  : None,
                  'forks_url'    : None,
                  'public'       : None,
                  'created_at'   :None,
                  'updated_at'   : None,
                  'comments'     : None,
                  'comments_url' : None }
        if not any(params.values()):
            raise ValueError
        return SearchGistIterator(**params)

class GistsIterator(object):
    def __init__(self,db_connection):
        self.gists = []
        self.idx = 0
        self.db_connection = db_connection

    def __iter__(self):
        self.gists = []
        self.idx = 0
        self.select_gists()
        return self

    def select_gists(self):
        conn = sqlite3.connect(self.db_connection)
        cur = conn.cursor()
        cur.execute("select * from gists")
        for row in cur:
            new_gist = Gist(row)
            self.gists.append(new_gist)
        conn.close()
        
    def __next__(self):
        if self.idx + 1 > len(self.gists):
            raise StopIteration
        gist = self.gists[self.idx]
        self.idx += 1
        return gist

    next = __next__        

class SearchGistIterator(GistsIterator):
    def __init__(self, db_connection, id=None, github_id=None, html_url=None, git_pull_url=None, git_push_url=None, commits_url=None, forks_url=None, public=None, created_at=None, updated_at=None, comments=None, comments_url=None):
        filters = {  'id'           : id,
                     'github_id'    : github_id,
                     'html_url'     : html_url,
                     'git_pull_url' : git_pull_url,
                     'git_push_url' : git_push_url,
                     'commits_url'  : commits_url,
                     'forks_url'    : forks_url,
                     'public'       : public,
                     'created_at'   : created_at,
                     'updated_at'   : updated_at,
                     'comments'     : comments,
                     'comments_url' : comments_url }

        super(SearchGistIterator, self).__init__(db_connection)

    def search_by_terms(self,gist):
        for key, value in self.filters.items():
            if value and getattr(gist, key) != value:
                return False
        return True
    
    def __next__(self):
        gist = super(SearchIterator, self).__next__()
        if self.search_by_terms(gist):
            return gist
        return next(self)
    
        next = __next__


def search_gists(db_connection, **kwargs):
    pass

def build_query():
    pass