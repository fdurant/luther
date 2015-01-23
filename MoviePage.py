from SomePage import SomePage
import urllib2
import os.path
from bs4 import BeautifulSoup
from myutils import myAssert

class MoviePage(SomePage):
    ''' Represents a movie page from Box Office Mojo
    url is the URL of the page
    '''

    def __init__(self, id):
        self.id = id
        self.url = MoviePage.__makePageUrl__(self)        
        self.contents = None

    def __makePageUrl__(self):
        ''' Produces a URL into one specific movie page
        id is a string without spaces

        returns a URL string'''
        return "http://www.boxofficemojo.com/movies/?id=%s.htm" % self.id

    def __makeSoup__(self):
        self.soup = BeautifulSoup(self.contents)

    def getSoup(self):
        return self.soup
 
    def __getMovieTitle__(self):
        return "whatever"

    def getCsvRow(self):
        ''' Returns a row of comma separated data '''
        self.__makeSoup__()
        result = []
        result.append(self.__getMovieTitle__())
        return result

if __name__ == "__main__":

    # From web
    mp1 = MoviePage('bluesbrothers')
    assert (mp1.getUrl() == "http://www.boxofficemojo.com/movies/?id=bluesbrothers.htm")
    mp1Contents = mp1.getContents()
    mp1.saveContentsAsFile(dirname='mydata/movies',onlyIfNotExists=False)
    assert (mp1Contents.find('<html') >= 0), "No opening html tag found"
    assert (mp1Contents.find('Belushi') >= 0), "No mention of Belushii found"
    assert (mp1Contents.find('Aykroyd') >= 0), "No mention of Aykroyd found"
    assert (mp1Contents.find('</html>') >= 0), "No closing html tag found"

    # From local file
    mp2 = MoviePage('bluesbrothers')
    mp2.loadContentsFromFile(dirname="mydata/movies")
    assert (mp2.getUrl() == "http://www.boxofficemojo.com/movies/?id=bluesbrothers.htm")
    mp2Contents = mp2.getContents()
    assert (mp2Contents.find('<html') >= 0), "No opening html tag found"
    assert (mp2Contents.find('Belushi') >= 0), "No mention of Belushii found"
    assert (mp2Contents.find('Aykroyd') >= 0), "No mention of Aykroyd found"
    assert (mp2Contents.find('</html>') >= 0), "No closing html tag found"

    # Beautiful soup
    csvRow = mp2.getCsvRow()
    myAssert(csvRow[0],'whatever','movie title')
