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

url = 'https://se.timeedit.net/web/uu/db1/schema/s.ics?i=5XX6Y660W915QYW50X9YQ05Z409505W53XX5335566y655756701W580568'

replacements = {
   'Realtidssystem': "Realtid",
   'Kompilatorteknik I': "Kompilator",
   'Laboration': 'Lab',
   'F\xc3\xb6rel\xc3\xa4sning': 'F\xc3\xb6rel',
   'ITC': 'Pol',
   '\xc3\x85ngstr\xc3\xb6m': '\xc3\x85ng'
 }

ignores = ['Teknisk fysik 5', 'Masterprogram i datavetenskap',
   'Informationsteknologi', 'Kandidatprogram i Datavetenskap \xc3\x85k 3 dvk',
   '\xc3\xa5k 4', 'Grupp Sy', 'Realtidssystem I',
   'Masterprogrammet i inbyggda system \xc3\x85r 1', 'Omtentamen',
   'Martin Stigge', 'Institutionen f\xc3\xb6r informationsteknologi'
]

for i in ignores:
   replacements[i] = ''

m = 2 ** 32
filehash = '-%8.8x' % ((hash(open(__file__).read())+m)%m)

s = urllib.urlopen(url).read()
s = s.replace('\r\n ', '')

lines = []
for e in s.split('\r\n'):
   if len(e) > 0 and e[0] == ' ':
      assert len(lines) > 0, "First line should not be a continuation"
      lines[-1] += e[1:]
   else:
      lines += [e]

output = ''
unknown = set([])
for line in lines:

    # only change summary lines
    if line[:8] == 'SUMMARY:':
       fields = line[8:].split('\\, ')
       line = 'SUMMARY:'
       for f in fields:
          if not f in replacements:
             line += ' ' + f
             unknown |= set([f])
          elif replacements[f] != '':
             line += ' ' + replacements[f]
    elif line[:4] == 'UID:':
        line = line +  filehash

    output += line + '\r\n'

"""
for a in unknown:
   print repr(a)
"""

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
