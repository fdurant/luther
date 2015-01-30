import re
from datetime import datetime, date, timedelta
import sys

def myAssert(actual,expected,fieldname):
    assert (actual == expected), "Incorrect %s: expected '%s', got '%s'" % (fieldname, expected, actual)

def removeTags(string):
    result = re.sub("<\/?[^>]+>",'',string)
    return result

def reduceWhiteSpace(string):
    result = re.sub("\s+",' ',string)
    return result

def getMovieSeasonFromDate(inputDate):
    ''' returns the Box Office Mojo definition of season in which a given date falls: 
    - Winter: first day after New Year's week or weekend through Thursday before first Friday in March
    - Spring: first Friday in March through Thursday before first Friday in May
    - Summer: first Friday in May through Labor Day weekend (ends on first Monday in September)
    - Fall: (Tues)day after Labor Day weekend through Thursday before first Friday in November
    - Holiday: first Friday in November through New Year's week or weekend
    '''
    seasons = ['winter', 'spring', 'summer', 'fall', 'holiday']
    result = ''
    focusYear = inputDate.year
    focusMonth = inputDate.month
    firstDayofFocusMonth = inputDate.replace(day=1)
    
    lastDayOfHolidaySeason = date(focusYear,1,1)
    while (lastDayOfHolidaySeason.weekday() != 6):
        lastDayOfHolidaySeason = lastDayOfHolidaySeason + timedelta(days=1)
#    print >> sys.stderr, "lastDayOfHolidaySeason = ", lastDayOfHolidaySeason
    
    firstDayOfSpringSeason = date(focusYear,3,1)
    while (firstDayOfSpringSeason.weekday() % 7 != 4):
        firstDayOfSpringSeason = firstDayOfSpringSeason + timedelta(days=1)
    lastDayOfWinterSeason = firstDayOfSpringSeason - timedelta(days=1)
#    print >> sys.stderr, "lastDayOfWinterSeason = ", lastDayOfWinterSeason
#    print >> sys.stderr, "firstDayOfSpringSeason = ", firstDayOfSpringSeason

    firstDayOfSummerSeason = date(focusYear,5,1)
    while (firstDayOfSummerSeason.weekday() % 7 != 4):
        firstDayOfSummerSeason = firstDayOfSummerSeason + timedelta(days=1)
    lastDayOfSpringSeason = firstDayOfSummerSeason - timedelta(days=1)
#    print >> sys.stderr, "lastDayOfSpringSeason = ", lastDayOfSpringSeason
#    print >> sys.stderr, "firstDayOfSummerSeason = ", firstDayOfSummerSeason

    lastDayOfSummerSeason = date(focusYear,9,1)
    while (lastDayOfSummerSeason.weekday() % 7 != 0):
        lastDayOfSummerSeason = lastDayOfSummerSeason + timedelta(days=1)
    firstDayOfFallSeason = lastDayOfSummerSeason + timedelta(days=1)
#    print >> sys.stderr, "lastDayOfSummerSeason = ", lastDayOfSummerSeason
#    print >> sys.stderr, "firstDayOfFallSeason = ", firstDayOfFallSeason

    firstDayOfHolidaySeason = date(focusYear,11,1)
    while (firstDayOfHolidaySeason.weekday() % 7 != 4):
        firstDayOfHolidaySeason = firstDayOfHolidaySeason + timedelta(days=1)
    lastDayOfFallSeason = firstDayOfHolidaySeason - timedelta(days=1)
#    print >> sys.stderr, "lastDayOfFallSeason = ", lastDayOfFallSeason
#    print >> sys.stderr, "firstDayOfHolidaySeason = ", firstDayOfHolidaySeason    

    # We know by definition that inputDate falls in the same calendar year
    # as all the calculated season boundaries
    if inputDate <= lastDayOfHolidaySeason:
        result = 'holiday'
    elif inputDate <= lastDayOfWinterSeason:
        result = 'winter'
    elif inputDate <= lastDayOfSpringSeason:
        result = 'spring'
    elif inputDate <= lastDayOfSummerSeason:
        result = 'summer'
    elif inputDate <= lastDayOfFallSeason:
        result = 'fall'
    else:
        result = 'holiday'

    if (result in seasons):
        return result
    else:
        raise("Illegal result: %s" % result)

if __name__ == "__main__":

    myAssert(removeTags('<a href="http://some.website.com/">Some Website</a>'),"Some Website",'tag removal')
    myAssert(removeTags('<b>Important!</b>'),"Important!",'tag removal')
    myAssert(removeTags('<br/>'),"",'tag removal')

    myAssert(getMovieSeasonFromDate(date(2015,1,6)),'winter','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,2,1)),'winter','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,2,15)),'winter','BoxOfficeMojo Season-from-date calculation')

    myAssert(getMovieSeasonFromDate(date(2015,2,24)),'winter','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,3,5)),'winter','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2014,3,6)),'winter','BoxOfficeMojo Season-from-date calculation')

    myAssert(getMovieSeasonFromDate(date(2014,3,7)),'spring','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,3,6)),'spring','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,4,1)),'spring','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,4,30)),'spring','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2014,5,1)),'spring','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,4,30)),'spring','BoxOfficeMojo Season-from-date calculation')

    myAssert(getMovieSeasonFromDate(date(2014,5,2)),'summer','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,5,1)),'summer','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,6,1)),'summer','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,6,30)),'summer','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,7,1)),'summer','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,7,30)),'summer','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,8,1)),'summer','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,8,30)),'summer','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2014,9,1)),'summer','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,9,7)),'summer','BoxOfficeMojo Season-from-date calculation')

    myAssert(getMovieSeasonFromDate(date(2014,9,2)),'fall','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,9,8)),'fall','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,10,1)),'fall','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,10,30)),'fall','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2014,11,6)),'fall','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,11,5)),'fall','BoxOfficeMojo Season-from-date calculation')

    myAssert(getMovieSeasonFromDate(date(2014,11,7)),'holiday','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,11,6)),'holiday','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,12,1)),'holiday','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,12,31)),'holiday','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2012,1,1)),'holiday','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2012,1,2)),'winter','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,1,4)),'holiday','BoxOfficeMojo Season-from-date calculation')
    myAssert(getMovieSeasonFromDate(date(2015,1,5)),'winter','BoxOfficeMojo Season-from-date calculation')
