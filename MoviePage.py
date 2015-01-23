from SomePage import SomePage
import urllib2
import os.path
from bs4 import BeautifulSoup
from myutils import myAssert, removeTags, reduceWhiteSpace
import re
import sys
import dateutil.parser

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
        try:
            result = self.soup.find('font', {'face':'Verdana', 'size':'6'}).find('b').text
        except:
            result = ''
        return result

    def __getGenre__(self):
        result=''
        try:
            pattern = re.compile("Genre:\s+<b>(.+?)<\/b>")
            result = pattern.search(str(self.soup)).group(1)
        except AttributeError:
            pass
        return result.lower()

    def __getCompositeTableItem__(self, qualifier):
        result = ''
        try:
            pattern = re.compile("%s:.*?<td>(.+?)<\/td>" % qualifier)
            tmp = pattern.search(str(self.soup)).group(1)
            tmpList = tmp.split('<br>')
            result = [reduceWhiteSpace(removeTags(a)).replace('*','') for a in tmpList]
            return "|".join(result)
        except AttributeError:
            pass
        return result

    def __getActors__(self):
        result = ''
        try:
            pattern = re.compile("Actors:.*?<td>(.+?)<\/td>")
            tmp = pattern.search(str(self.soup)).group(1)
            tmpList = tmp.split('<br>')
            result = [reduceWhiteSpace(removeTags(a)).replace('*','') for a in tmpList]
            return "|".join(result)
        except AttributeError:
            pass
        return result

    def __getSingleTableItem__(self, qualifier, lowerCase=False):
        result=''
        try:
            pattern = re.compile("%s:.*?<td>(.+?)<\/td>" % qualifier)
            tmp = pattern.search(str(self.soup)).group(1)
            result = reduceWhiteSpace(removeTags(tmp)).replace('*','')
        except AttributeError:
            pass
        if (lowerCase):
            return result.lower()
        else:
            return result

    def __getDomesticTotalGross__(self):
        result=''
        try:
            pattern = re.compile("Domestic Total Gross:\s+<b>\$([\d,]+?)<\/b>")
            result = pattern.search(str(self.soup)).group(1)
        except AttributeError:
            pass
        return result.replace(',','')

    def __getProductionBudget__(self):
        result=''
        try:
            pattern = re.compile("Production Budget:\s+<b>\$?([\d,N\/A]+?)<\/b>")
            result = pattern.search(str(self.soup)).group(1)
        except AttributeError:
            pass
        return result.replace(',','')

    def __getRuntimeInMinutes__(self):
        result=''
        try:
            pattern = re.compile("Runtime:\s+<b>([^<]*?)<\/b>")
            tmp = pattern.search(str(self.soup)).group(1)
            hours = re.search('(\d+)\s*ho?u?rs\.?',tmp)
            if hours is None:
                hh = 0
            else:
                hh=hours.group(1)
            mins = re.search('(\d+)\s*min\.',tmp)
            if mins is None:
                mm = 0
            else:
                mm=mins.group(1)
#            print >> sys.stderr, "found %s hrs and %s mins" % (hh, mm)
            totalMins = int(mm) + (int(hh) * 60)
            result = str(totalMins)
        except AttributeError:
            pass
        return result

    def __getReleaseDate__(self):
        result=''
        try:
            pattern = re.compile("Release Date:\s+<b><nobr>(.+?)</nobr><\/b>")
            result = pattern.search(str(self.soup)).group(1)
        except AttributeError:
            pass
        return str(dateutil.parser.parse(result))

    def getCsvRow(self):
        ''' Returns a row of comma separated data '''
        self.__makeSoup__()
        result = []
        result.append(self.__getMovieTitle__())
        result.append(self.__getGenre__())
        result.append(self.__getActors__())
        result.append(self.__getCompositeTableItem__('Directors?'))
        result.append(self.__getCompositeTableItem__('Writers?'))  
        result.append(self.__getCompositeTableItem__('Producers?'))  
        result.append(self.__getCompositeTableItem__('Composers?'))  
        result.append(self.__getDomesticTotalGross__())
        result.append(self.__getProductionBudget__())
        result.append(self.__getRuntimeInMinutes__())
        result.append(self.__getReleaseDate__())
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
    myAssert(csvRow[0],'The Blues Brothers','Title')
    myAssert(csvRow[1],'comedy','Genre')
    myAssert(csvRow[2],'John Belushi|Dan Aykroyd|Carrie Fisher','Actors')
    myAssert(csvRow[3],'John Landis','Directors')
    myAssert(csvRow[4],'John Landis','Writers')
    myAssert(csvRow[5],'Robert K. Weiss','Producers')
    myAssert(csvRow[6],'Elmer Bernstein','Composers')
    myAssert(csvRow[7],'57229890','DomesticTotalGross')
    myAssert(csvRow[8],'N/A','ProductionBudget')
    myAssert(csvRow[9],'150','RuntimeInMinutes')
    myAssert(csvRow[10],'1980-06-20 00:00:00','Release Date')
#    print >> sys.stderr, "cvsRow is ", csvRow
