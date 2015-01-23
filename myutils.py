def myAssert(expected,actual,fieldname):
    assert (actual == expected), "Incorrect %s: expected '%s', got '%s'" % (fieldname, expected, actual)
