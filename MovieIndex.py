import urllib2
import re
from bs4 import BeautifulSoup

from MoviePage import MoviePage

class MovieIndex():
    ''' Class representing a movie index at Box Office Mojo '''

    _allowedIndexLetters = ['NUM','A','B','C','D','E','F','G','H','I','J','K','L',
                     'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    def __init__(self, letter, P='', page='1'):
        self.letter = letter
        self.P = P
        self.page = page
        self.url = MovieIndex.__makeIndexUrl__(self)
        self.__makeSoup__()

    def __makeIndexUrl__(self):
        ''' Produces a URL into one specific index page
        letter is a string, with allowed values:
        - a through z
        - A through Z
        - NUM
        - 0 through 9'

        returns a URL string'''
        if (self.letter in ['0','1','2','3','4','5','6','7','8','9']):
            letterUC = 'NUM'
        else:
            letterUC = self.letter.upper()
        assert(letterUC in MovieIndex._allowedIndexLetters), "letterUC %s is not OK" % letterU

        return "http://www.boxofficemojo.com/movies/alphabetical.htm?letter=%s&page=%s&p=%s.htm" % (letterUC, self.page, self.P)

    def getUrl(self):
        return self.url

    def __makeSoup__(self):
        page = urllib2.urlopen(self.url)
        self.soup = BeautifulSoup(page)

    def getSoup(self):
        return self.soup
 
    def getSameLetterPageList(self):
        ''' returns the list of all *other* partial Movie Indices referenced by this Movie Index, 
        i.e. those that with the same starting letter.
        The list can be empty, e.g. when there aren't that many movies the titles of which start with this letter
        '''

        otherIndexUrls = self.soup.find(class_='alpha-nav-holder').find_all('a',{'href':True})
        pattern = re.compile('page=(\d+)')
        otherPageNumbers = [pattern.search(str(otherIndexUrl)).group(1) for otherIndexUrl in otherIndexUrls]
        return [MovieIndex(self.letter, otherP) for otherP in otherPageNumbers if otherP is not None]

    def getMoviePageList(self):
        ''' returns the list of all movie pages referenced in this index '''

        allUrls = self.soup.find_all('a', {'href':True})
        pattern = re.compile('href="\/movies\/\?id=([^"]+?)\.htm">\s*<b>')
        moviePageMatches = [pattern.search(str(anyUrl)) for anyUrl in allUrls]
        moviePageIds = [m.group(1) for m in moviePageMatches if m is not None]

        return [MoviePage(moviePageId) for moviePageId in moviePageIds]

if __name__ == "__main__":

    mi1 = MovieIndex('a');
    exampleIndexUrl1 = mi1.getUrl()
    assert (exampleIndexUrl1 == "http://www.boxofficemojo.com/movies/alphabetical.htm?letter=A&page=1&p=.htm"), "Unexpected value: %s" % exampleIndexUrl1

    mi2 = MovieIndex('1');
    exampleIndexUrl2 = mi2.getUrl()
    assert (exampleIndexUrl2 == "http://www.boxofficemojo.com/movies/alphabetical.htm?letter=NUM&page=1&p=.htm"), "Unexpected value: %s" % exampleIndexUrl2

    # Example with explicit index page number
    mi3 = MovieIndex('A',page='2');
    exampleIndexUrl3 = mi3.getUrl()
    assert (exampleIndexUrl3 == "http://www.boxofficemojo.com/movies/alphabetical.htm?letter=A&page=2&p=.htm"), "Unexpected value: %s" % exampleIndexUrl3
