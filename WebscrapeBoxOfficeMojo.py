from MovieIndex import MovieIndex
from bs4 import BeautifulSoup
import urllib2
import sys

indexIdentifiers = ['NUM','A','B','C','D','E','F','G','H','I','J','K','L',
                    'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

movieIndices = [MovieIndex(id) for id in indexIdentifiers]

for mi in movieIndices:
    allIndicesThisLetter = [mi]
    allIndicesThisLetter.extend(mi.getSameLetterPageList())
    print >> sys.stderr, allIndicesThisLetter

    moviePageList = []
    for i in allIndicesThisLetter:
#        print >> sys.stderr, i.getUrl()
        moviePageList.extend(i.getMoviePageList()) 
    for mp in moviePageList:
        mp.saveContentsAsFile(dirname='mydata/movies',onlyIfNotExists=True)
