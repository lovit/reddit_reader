from glob import glob
import json
import os
import re

def parser(line):
    try:
        return json.loads(line.strip())
    except:
        return ''

file_pattern = re.compile('RS_[\d]{4}-[\d]{2}')

def acceptable(path):
    if os.path.isdir(path):
        return False
    name = path.split('/')[-1]
    if file_pattern.match(name):
        return True
    return False

class RedditSubmissionReader:
    def __init__(self, directory):
        self.directory = directory
        self.paths = sorted(glob(directory+'/*'))
        self.paths = [path for path in paths if acceptable(path)]

    def select(begin_date, end_date, subreddit=None, query_term=None):
        raise NotImplemented