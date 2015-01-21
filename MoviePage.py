import urllib2

class MoviePage():
    ''' Represents a movie page from Box Office Mojo
    url is the URL of the page
    '''

    def __init__(self, id):
        self.id = id
        self.url = MoviePage.__makePageUrl__(self)        

    def __makePageUrl__(self):
        ''' Produces a URL into one specific movie page
        id is a string without spaces

        returns a URL string'''
        return "http://www.boxofficemojo.com/movies/?id=%s.htm" % self.id

    def getUrl(self):
        return self.url

    def retrieve(self):
        ''' Performs the HTTP query and retrieves the contents '''
        page = urllib2.urlopen(url)
        return page

if __name__ == "__main__":

    mp1 = MoviePage('bluesbrothers');
    assert (mp1.getUrl() == "http://www.boxofficemojo.com/movies/?id=bluesbrothers.htm")
