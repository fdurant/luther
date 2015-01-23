import re

def myAssert(actual,expected,fieldname):
    assert (actual == expected), "Incorrect %s: expected '%s', got '%s'" % (fieldname, expected, actual)

def removeTags(string):
    result = re.sub("<\/?[^>]+>",'',string)
    return result

def reduceWhiteSpace(string):
    result = re.sub("\s+",' ',string)
    return result

if __name__ == "__main__":

    myAssert(removeTags('<a href="http://some.website.com/">Some Website</a>'),"Some Website",'tag removal')
    myAssert(removeTags('<b>Important!</b>'),"Important!",'tag removal')
    myAssert(removeTags('<br/>'),"",'tag removal')
