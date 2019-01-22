import argparse
import os
import json
from reddit_reader import SubmissionReader, parser

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_directory', type=str, default='./', help='Output directory')
    parser.add_argument('--output_directory', type=str, default='./output', help='Output directory')
    parser.add_argument('--subreddit', type=str, default='MachineLearning', help='Subreddit name')
    parser.add_argument('--keyword', type=str, default='', help='Subreddit name')
    parser.add_argument('--begin_date', type=str, default='2018-01-01', help='datetime YYYY-mm-dd')
    parser.add_argument('--end_date', type=str, default='2019-01-10', help='datetime YYYY-mm-dd')
    parser.add_argument('--verbose', dest='VERBOSE', action='store_true')
    parser.add_argument('--debug', dest='DEBUG', action='store_true')

    args = parser.parse_args()
    input_directory = args.input_directory
    output_directory = args.output_directory
    subreddit = args.subreddit
    keyword = args.keyword
    begin_date = args.begin_date
    end_date = args.end_date
    VERBOSE = args.VERBOSE
    DEBUG = args.DEBUG

    if not keyword:
        keyword = None

    # check output directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    reader = SubmissionReader(input_directory, VERBOSE, DEBUG)
    print('num of subreddit JSON files = {}'.format(len(reader.paths)))
    output_path = '{}/{}{}'.format(output_directory, subreddit.lower(), '' if keyword is None else '__'+keyword)
    with open(output_path, 'w', encoding='utf-8') as f:
        for submission in reader.select(begin_date, end_date, subreddit, keyword):
            strf = json.dumps(submission)
            f.write('{}\n'.format(strf))

if __name__ == '__main__':
    main()