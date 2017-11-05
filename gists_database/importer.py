import requests
import pprint
import sqlite3

BASE_URL = 'https://api.github.com/users/{}/gists'

# Dorota - Add the query before the methods
SQL_GIST_QUERY = """INSERT INTO gists (github_id, html_url, git_pull_url, git_push_url, commits_url, 
            forks_url, public, created_at, updated_at, comments, comments_url) 
            VALUES (:id, :html_url, :git_pull_url, :git_push_url, :commits_url, :forks_url, :public, 
            :created_at, :updated_at,:comments, :comments_url);"""


def import_gists_to_database(db, username, commit=True):
    gists = requests.get(BASE_URL.format(username))
    gists.raise_for_status()
    gists = gists.json()
    
    # Dorota - We have to loop through the gists and next save them in db. If I'm right ;)
    # Ben - i think we can shortcut this, see below
    # Laura - Perhaps we are missing the id :) checkout the model 
    
    for gist in gists:
    #     parameters = {
    #         "id" : gist["id"], 
    #         "html_url" : gist["html_url"], 
    #         "git_pull_url" : gist["git_pull_url"],
    #         "git_push_url" : gist["git_push_url"], 
    #         "commits_url" : gist["commits_url"], 
    #         "forks_url" : gist["forks_url"], 
    #         "public" : gist["public"], 
    #         "created_at" : gist["created_at"], 
    #         "updated_at" : gist["updated_at"], 
    #         "comments" : gist["comments"], 
    #         "comments_url" : gist["comments_url"]
    #     }
    # Ben - we can reference the gist directly as it is a dictionary, this seems to work
        db.execute(SQL_GIST_QUERY, gist) #changed from parameters
        
    if commit:
        db.commit()
        