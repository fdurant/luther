from MoviePage import MoviePage
import glob
import re
import csv
import sys

filelist = glob.glob("mydata/movies/*.html")

csvwriter = csv.writer(sys.stdout, delimiter=',')

dummy = MoviePage('dummy')
header = dummy.getCsvHeader()
csvwriter.writerow(header)

for i,f in enumerate(filelist):
    if i % 100 == 0:
        print >> sys.stderr, "Processing file %d/%d ..." % (i, len(filelist)),

    m = re.match("(.+)\/(.+).html", f)
    dirname = m.group(1)
    id = m.group(2)
    
    mp = MoviePage(id)
    mp.loadContentsFromFile(dirname=dirname, verbose=False)
    
    try:
        row = mp.getCsvRow()
        csvwriter.writerow(row)
    except:
        pass
    
    if i % 100 == 0:
        print >> sys.stderr, "done"
