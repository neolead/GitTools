Git Extractor
==============================

This is a script which tries to recover incomplete git repositories:

- Iterate through all commit-objects of a repository
- Try to restore the contents of the commit 
- Commits are *not* sorted by date

# Usage

```
bash extractor.sh /tmp/mygitrepo /tmp/mygitrepodump

threaded!!
python3 extract_thread.py /tmp/mygitrepo /tmp/mygitrepodump 30
```
where
- ```/tmp/mygitrepo``` contains a ```.git``` directory
- ```/tmp/mygitrepodump``` is the destination directory
- 30 - threads to run

This can be used in combination with the ```Git Dumper``` in case the downloaded repository is incomplete.

