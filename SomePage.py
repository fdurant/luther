import urllib2
import os.path
import sys
import time
import random

class SomePage():
    ''' Represents a page from Box Office Mojo
    id is the id of the page (a string)
    '''

    def __init__(self, id):
        self.id = id
        self.url = __class__.__makePageUrl__(self)        
        self.contents = None

    def __makePageUrl__(self):
        ''' Produces a URL into one specific movie page
        id is a string without spaces

        returns a URL string'''
        pass

    def getUrl(self):
        return self.url

    def retrieve(self, sleepSec=0):
        ''' Performs the HTTP query and retrieves the contents '''
        try:
            time.sleep(sleepSec)
            print >> sys.stderr, "Downloading %s after sleeping for %d sec ..." % (self.url, sleepSec),
            response = urllib2.urlopen(self.url)
            self.contents = response.read()
            print >> sys.stderr, "done"
        except:
            self.contents = ''
            print >> sys.stderr, "ERROR"
            raise('Failed HTTP attempt')

    def getContents(self):
        ''' Returns the contents '''
        if self.contents is None:
            try:
                self.retrieve(sleepSec=random.randint(1,5))
            except:
                print >> sys.stderr, "Unable to get the contents for %s; continuing anyway" % self.url
                pass
        return self.contents

    def saveContentsAsFile(self, dirname=None, filename=None, onlyIfNotExists=False):
        ''' Saves the contents in a filename '''
        if filename is None:
            filename = '%s.html' % self.id

        if dirname is None:
            dirname = '.'

        fullpathtofile = "%s/%s" % (dirname, filename)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if onlyIfNotExists and os.path.exists(fullpathtofile) and os.stat(fullpathtofile).st_size > 0:
            print >> sys.stderr, "%s already exists and is not empty, so no need to write" % fullpathtofile
            return

        if self.contents is None:
            try:
                self.retrieve(sleepSec=random.randint(1,5))
            except:
                print >> sys.stderr, "Unable to save the contents for %s; continuing anyway" % self.url
                pass

        with open(fullpathtofile, 'w') as f:
            f.write(self.contents)
        f.close()

    def getCsvRow(self):
        ''' Saves the contents in a filename '''
        pass

