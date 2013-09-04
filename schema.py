#!/it/sw/python/bin/python2.3
import urllib
url = 'http://schema.angstrom.uu.se/4DACTION/iCal_downloadReservations/timeedit.ics?branch=2&lang=1'
time = 'from=1134&to=1201'
l = [78779000, 73832000, 79440000, 78784000, 78861000]
time = 'from=1201&to=1234'
l = [29410000, 78865000, 73921000] #  musik, bildanalys, parallell 
l += [1789000] # algebra II
time = 'from=1235&to=1309'
l = [   78866000, # bildanalys2 uu-12023
        79447000, # tradlosa sensornaetverk uu-14453
        79445000, # signalbehandling, uu-14432
        78858000] # regtek 2
        #78863000] # fem
time = 'from=1301&to=1330'
l = [   78809000, #VHDL
        69180000, #Operativsystem I
        78792000, #kryptologi
        85916000] #dirigering

ids = ["id%u=%u" % t for t in enumerate(l)]
url = '&'.join([url, time] + ids)

replacements = [
        ('Andreas Sandberg', 'Sandberg'),
        ('Erik Hagersten', 'Hagersten'),
        ('Katharina Kormann', 'Kormann'),
        ('Avancerad datorarkitektur', 'AvDark'),
        ('Optimeringsmetoder', 'OptMet'),
        ('Laboration', 'Lab'),
        #('46c3b672656cc3a4736e696e67'.decode('hex'),
        #    '46c3b672656c'.decode('hex') + '.'),
        ('46c3b672656cc3a4736e696e67'.decode('hex'), ''),
        ('Programmering av parallelldatorer', 'ParProg'),
        ('Datoriserad bildanalys II', 'BA2'),
        ('Jarmo Rantakokko', ''),
        ('Anders Brun', ''),
        ('Signalbehandling','SigBeh'),
        ('Tomas Olofsson',''),
        ('Finita elementmetoder','FEm'),
        ('Stefan Engblom',''),
        ('Cris Luengo',''),
        ('Digital elektronikkonstruktion med VHDL', 'VHDL'),
        ('Leif Gustafsson', ''),
        ('Operativsystem I', 'OpSys1')
        ]

m = 2 ** 32
filehash = '-%8.8x' % ((hash(open(__file__).read())+m)%m)

s = urllib.urlopen(url).read()
s = s.replace('\r\n ', '')
output = ''
for line in s.split('\r\n'):

    # only change summary lines
    if line[:8] == 'SUMMARY:':
        # remove class field
        line = 'SUMMARY:' + ' '.join(line.split('\\n')[1:])
        # perform replacements
        for o,n in replacements:
            line = line.replace(o,n)
        # remove double spaces
        line = ' '.join(filter(lambda x:x!='', line.split()))
    elif line[:4] == 'UID:':
        line = line +  filehash

    output += line + '\r\n'

print "Content-Type: text/calendar;charset=UTF-8\r\n" + \
        "Cache-Control: no-cache\r\n" + \
        "\r\n" + output

import time
f = open('callog.txt','a')
f.write(time.ctime()+'\n')
f.close()
f = open('update.txt','w')
f.write(time.ctime()+'\n')
f.close()
