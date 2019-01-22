# Reddit Reader

Reader for archived reddit files. All archived reddit [submissions][submissions] and [comments][comments] are in `pushshift.io`

[submissions]: http://files.pushshift.io/reddit/submissions/
[comments]:  http://files.pushshift.io/reddit/comments/

First download the files and unzip them.

## Submission Reader

```python
from reddit_reader import SubmissionReader

dirname = 'YOUR_DOWNLOAD_DIRECTORY'
reader = SubmissionReader(dirname)
```