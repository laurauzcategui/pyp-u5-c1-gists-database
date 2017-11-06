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

    def search(self, conditions, id=None, github_id=None, html_url=None, git_pull_url=None, git_push_url=None, commits_url=None, forks_url=None, public=None, created_at=None, updated_at=None, comments=None, comments_url=None):
        ''' it will lookup only for the terms we are querying. '''
        params = {'id'           : id,
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
        if not any(params.values()):
            raise ValueError
        return SearchGistIterator(self.db_connection, conditions,**params)

class GistsIterator(object):
    def __init__(self,db_connection, conditions=None, params = None):
        ''' it will initialize the gist iterator object '''
        query_all = "select * from gists"
        self.gists = []
        self.idx = 0
        self.db_connection = db_connection
        self.query = query_all if conditions is None else '{} where {}'.format(query_all, conditions)
        self.params = params

    def __iter__(self):
        ''' it will initialize the iterator and will query based on self.query '''
        self.gists = []
        self.idx = 0
        self.select_gists()
        return self

    def select_gists(self):
        cur = self.db_connection.cursor()
        if self.params:
            print('query:{}, conds:{}'.format(self.query,self.params))
            cur.execute(self.query,self.params)
        else:
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
    def __init__(self, db_connection,conditions, id=None, github_id=None, html_url=None, git_pull_url=None, git_push_url=None, commits_url=None, forks_url=None, public=None, created_at=None, updated_at=None, comments=None, comments_url=None):
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
        filters = {k:v for k,v in filters.items() if v is not None}
        super(SearchGistIterator, self).__init__(db_connection, conditions, filters)

    def search_by_terms(self,gist):
        for key, value in self.params.items():
            if value and getattr(gist, key) != value:
                return False
        return True

    #def __next__(self):
    #    gist = super(SearchGistIterator, self).__next__()
    #    if self.search_by_terms(gist):
    #        return gist
    #    return next(self)
    #
    #next = __next__


def search_gists(db_connection, **kwargs):
    search_explorer = SearchExplore(db_connection)
    if len(kwargs) > 0:
        condition, new_kargs = build_query(**kwargs)
        print('condition:{} & new_kargs:{}'.format(condition,new_kargs))
        return search_explorer.search(condition,**new_kargs)
    else:
        return search_explorer.all()

def build_query(**kwargs):
    conditions = []
    key_condition = []
    comparisons = { 'gt'  : '>',
                    'gte' : '>=',
                    'lt'  : '<',
                    'lte' : '<='}
    new_kargs = {}
    for condition,value in kwargs.items():
        key_condition = condition.split('__')
        if len(key_condition) > 1:
            conditions.append('datetime({}) {} datetime(:{})'.format(key_condition[0],comparisons[key_condition[1]],key_condition[0]))
            new_kargs[str(key_condition[0])] = value
        else:
            conditions.append('{} = :{}'.format(condition,condition))
            new_kargs[str(condition)] = value

    return ' and '.join(conditions), new_kargs

    d = datetime(2014, 5, 3, 20, 26, 8)
    gists_iterator = search_gists(db, created_at__lte=d)
