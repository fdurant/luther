from MoviePage import MoviePage
import glob
import re
import csv

filelist = glob.glob("mydata/movies/*.html")

with open('parsedMovieData.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')

    dummy = MoviePage('dummy')
    header = dummy.getCsvHeader()
    csvwriter.writerow(header)

    for f in filelist[0:100]:
        m = re.match("(.+/)(.+).html", f)
        dirname = m.group(1)
        id = m.group(2)

        mp = MoviePage(id)
        mp.loadContentsFromFile(dirname=dirname)
    
        try:
            row = mp.getCsvRow()
            csvwriter.writerow(row)
        except:
            pass
