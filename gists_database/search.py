from .models import Gist
import sqlite3


class SearchExplore(object):
    ''' base class to start to be called from search and build_query '''
    def __init__(self, db_connection, query=None):
        self.db_connection = db_connection
        self.query = query

    def all(self):
    ''' it will return a search of all gists across the table '''
        return GistsIterator(self.db_connection,self.query)

    def search(self, id=None, github_id=None, html_url=None, git_pull_url=None, git_push_url=None, commits_url=None, forks_url=None, public=None, created_at=None, updated_at=None, comments=None, comments_url=None):
    ''' it will lookup only for the terms we are querying. '''
        params = {'id'           : None,
                  'github_id'    : None,
                  'html_url'     : None,
                  'git_pull_url' : None,
                  'git_push_url' : None,
                  'commits_url'  : None,
                  'forks_url'    : None,
                  'public'       : None,
                  'created_at'   : None,
                  'updated_at'   : None,
                  'comments'     : None,
                  'comments_url' : None }
        if not any(params.values()):
            raise ValueError
        return SearchGistIterator(self.db_connection, **params)

class GistsIterator(object):
    def __init__(self,db_connection, conditions=None):
        ''' it will initialize the gist iterator object '''
        query_all = "select * from gists"
        self.gists = []
        self.idx = 0
        self.db_connection = db_connection
        self.query = query_all if conditions is None else '{} where {}'.format(query_all, conditions)

    def __iter__(self):
        ''' it will initialize the iterator and will query based on self.query '''
        self.gists = []
        self.idx = 0
        self.select_gists()
        return self

    def select_gists(self):
        cur = self.db_connection.cursor()
        cur.execute(self.query)
        for row in cur:
            new_gist = Gist(row)
            self.gists.append(new_gist)

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
        gist = super(SearchGistIterator, self).__next__()
        if self.search_by_terms(gist):
            return gist
        return next(self)

        next = __next__


def search_gists(db_connection, **kwargs):
    search_explorer = SearchExplore(db_connection)
    if len(kwargs) > 0:
        build_query(**kwargs)
        return search_explorer.search(**kwargs)
    else:
        return search_explorer.all()

def build_query(**kwargs):
    conditions = []
    key_condition = []
    comparisons = { 'gt'  : '>',
                    'gte' : '>=',
                    'lt'  : '<',
                    'lte' : '=<'}
    for condition in kwargs:
        key_condition = condition.split('__')
        new_kargs = []
        if len(key_condition) > 0:
            conditions.append('{} {} :{}'.format(key_condition[0],condition[key_condition[1]],key_condition[0]))
        else:
            pass
    return ' and '.join(conditions)
