import argparse
from glob import glob
import os
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_directory', type=str, default='./', help='Output directory')
    parser.add_argument('--output_directory', type=str, default='./output', help='Output directory')
    parser.add_argument('--subreddit', type=str, default='MachineLearning', help='Subreddit name')
    parser.add_argument('--keyword', type=str, default='', help='Subreddit name')
    parser.add_argument('--force', dest='force', action='store_true')

    args = parser.parse_args()
    input_directory = args.input_directory
    output_directory = args.output_directory
    subreddit = args.subreddit.lower()
    keyword = args.keyword
    force = args.force

    if not keyword:
        keyword = None

    # check output directory
    output_directory = '{}/{}{}/'.format(output_directory, subreddit.lower(), '' if keyword is None else '__'+keyword)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    print(output_directory)

    paths = sorted(glob('{}/RS_*'.format(input_directory)))
    for inpath in paths:
        n_write = 0
        name = inpath.split('/')[-1]
        outpath = '{}/{}'.format(output_directory, name)
        if not force and os.path.exists(outpath):
            print('{} already exists'.format(outpath))
            continue
        #print(outpath)
        #"""
        with open(inpath, encoding='utf-8') as fi:
            with open(outpath, 'w', encoding='utf-8') as fo:
                for i, line in enumerate(fi):
                    try:
                        obj = json.loads(line.strip())
                    except:
                        continue
                    if obj.get('subreddit', '').lower() != subreddit:
                        continue
                    if keyword is not None:                        
                        if not (keyword in obj.get('selftext', '').lower()) and not (keyword in obj.get('title', '').lower()):
                            continue
                    n_write += 1
                    fo.write(line)
                if i % 100000 == 0:
                    print('\r{} {} / {} lines'.format(name, n_write, i), end='')
        print('\r{} {} / {} lines was done'.format(name, n_write, i))
        #"""

if __name__ == '__main__':
    main()