from SomePage import SomePage
import urllib2
import os.path

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

    def getCsvRow(self):
        ''' Saves the contents in a filename '''
        pass

if __name__ == "__main__":

    mp1 = MoviePage('bluesbrothers');
    assert (mp1.getUrl() == "http://www.boxofficemojo.com/movies/?id=bluesbrothers.htm")
    mp1Contents = mp1.getContents()
    assert (mp1Contents.find('<html') >= 0), "No opening html tag found"
    assert (mp1Contents.find('Belushi') >= 0), "No mention of Belushii found"
    assert (mp1Contents.find('Aykroyd') >= 0), "No mention of Aykroyd found"
    assert (mp1Contents.find('</html>') >= 0), "No closing html tag found"
