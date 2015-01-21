from MovieIndex import MovieIndex
from bs4 import BeautifulSoup
import urllib2

indexIdentifiers = ['a']

movieIndices = [MovieIndex(id) for id in indexIdentifiers]

for mi in movieIndices:
#    print mi.getSameLetterPageList()
    print mi.getMoviePageList()
