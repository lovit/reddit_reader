from datetime import datetime
from glob import glob
import json
import os
import re


date_pattern = re.compile('[\d]{4}-[\d]{2}-[\d]{2}')
file_pattern = re.compile('RS_[\d]{4}-[\d]{2}')

def parser(line):
    try:
        return json.loads(line.strip())
    except:
        return {}

def acceptable(path):
    if os.path.isdir(path):
        return False
    name = path.split('/')[-1]
    if file_pattern.match(name):
        return True
    return False

def is_date(s):
    """
    Arguments
    ---------
    s : str
        Date string

    Returns
    -------
    True if s is right format such as 2018-01-23
    """

    if date_pattern.match(s):
        return True
    return False

def match_date(paths, yymm_b, yymm_e):
    """
    Arguments
    ---------
    paths : list of str
        List of file paths.
    yymm_b : str
        Year-month of begin date
        e.g) 2017-01
    yymm_e : str
        Year-month of end date
        e.g) 2017-03

    Returns
    -------
    list of date-matched paths
    """

    return sorted([path for path in paths if yymm_b <= path.split('/')[-1][3:10] <= yymm_e])

class RedditFile:
    def __init__(self, path):
        self.path = path
    def __iter__(self):
        with open(self.path, encoding='utf-8') as f:
            for doc in f:
                yield doc

class SubmissionReader:
    """
    Reddit Submission Reader from downloaded JSON format files

    directory : str
        Directory path
    verbose : Boolean
        If True verbose mode on. Print current search status
        Default is True
    debug : Boolean
        If True, search within only 1000 lines in each file
        Default is False
    """

    def __init__(self, directory, verbose=True, debug=False):
        self.directory = directory
        self.verbose = verbose
        self.debug = debug
        paths = sorted(glob(directory+'/*'))
        self.paths = [path for path in paths if acceptable(path)]

    def select(self, begin_date, end_date, subreddit=None, query_term=None, author=None):
        """
        Arguments
        ---------
        begin_date : str
            `yyyy-mm-dd` format. For example 2017-01-01
        end_date : str
            `yyyy-mm-dd` format. For example 2017-01-01
        subreddit : str or None
            Subreddit name. Ignore whether character is capital or lower
            If `subreddit` is None, it retrieves all subreddits.
            Default is None.
        query_term : str or None
            A query term that the selftext have to include.
            If the `query_term` is None, it dosent matter selftext
            Default is None
        author : str
            Author id
            If the `author` is None, it dosent matter author

        Yield
        -----
        It yield if condition satisfying submissions are found.
        """

        if not is_date(begin_date) or not is_date(end_date):
            raise ValueError('Check your input date: begin_date={}, end_date={}'.format(begin_date, end_date))

        yymm_b = begin_date[:7]
        yymm_e = end_date[:7]
        paths = match_date(self.paths, yymm_b, yymm_e)

        utc_b = datetime(
            year = int(begin_date[:4]),
            month = int(begin_date[5:7]),
            day = int(begin_date[8:10])).timestamp()
        utc_e = datetime(
            year = int(end_date[:4]),
            month = int(end_date[5:7]),
            day = int(end_date[8:10])).timestamp()

        # use lower case
        if query_term is None:
            query_term_ = None
        else:
            query_term_ = query_term.lower()

        n_yield = 0
        n_paths = len(paths)
        for i_path, path in enumerate(paths):
            submissions = RedditFile(path)
            for i_subm, submission_strf in enumerate(submissions):
                if self.debug and i_subm >= 10001:
                    break
                if i_subm % 10000 == 0:
                    args = (i_path+1, n_paths, i_subm, n_yield, ' '*20)
                    print('\r{} / {} files, from {} candidiates, yield {} submissions{}'.format(*args), end='')
                submission = parser(submission_strf)
                satisfy_flag = satisfy(
                    submission, utc_b, utc_e,
                    subreddit, query_term_, author
                )
                if not satisfy_flag:
                    continue
                yield submission
                n_yield += 1
        print('\ndone')

def satisfy(submission, utc_b, utc_e,
    subreddit, query_term, author):

    utc = submission.get('created_utc', None)
    if not utc:
        return False
    if not (utc_b <= utc <= utc_e):
        return False

    if subreddit is not None:
        subrd = submission.get('subreddit', '')
        if not subrd:
            return False
        if not (subrd.lower() == subreddit.lower()):
            return False

    if isinstance(query_term, str):
        selftext = submission.get('selftext', '').lower()
        title = submission.get('title', '').lower()
        if not (query_term in selftext or query_term in title):
            return False

    if isinstance(author, str):
        auth = submission.get('author', '')
        if not (author == auth):
            return False

    return True
