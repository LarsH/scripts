#!/usr/bin/env python
import urllib
from timeEditObfuscation import scramble, unscramble

origurl = 'https://se.timeedit.net/web/uu/db1/schema/s.ics?i=6036X6695055QQ4XZ40X090Y55059W555YY5X67656661WX5X5WW90659557YX66560W604550YX5XZyQ3'
time = '130826-140124'

baseurl = origurl.split('?')[0]
i = origurl.split('=')[-1]

origrequest = unscramble(i).split('&')
objects = [e for e in origrequest if 'objects' in e][0]

query = objects + '&p=' + time
url = baseurl + '?i=' + scramble(query)

replacements = {
   'Realtidssystem': "Realtid",
   'Kompilatorteknik I': "Kompilator",
   'Laboration': 'Lab',
   'F\xc3\xb6rel\xc3\xa4sning': 'F\xc3\xb6rel',
   'ITC': 'Pol',
   '\xc3\x85ngstr\xc3\xb6m': '\xc3\x85ng',
   'Omtentamen' : 'Omtenta',
   'Konstantinos Sagonas': 'Kostis',
   'Martin Blomgren': 'Martin',
   'Vera Koponen' : 'Vera',
   'Lektion': 'Lekt',
   'Grafteori': 'GT',
   'Diskret matematik': 'Diskret'
  }

ignores = ['Teknisk fysik 5', 'Masterprogram i datavetenskap',
   'Informationsteknologi', 'Kandidatprogram i Datavetenskap \xc3\x85k 3 dvk',
   '\xc3\xa5k 4', 'Grupp Sy', 'Realtidssystem I',
   'Masterprogrammet i inbyggda system \xc3\x85r 1',
   'Martin Stigge', 'Institutionen f\xc3\xb6r informationsteknologi',
   'Matematiska institutionen', 'Gymnasiel\xc3\xa4rare Matematik \xc3\x85k2',
   'Kandidatprogrammet i Matematik \xc3\x85k 2', 'antagna v\xc3\xa5rtermin',
   'Gymnasiel\xc3\xa4rare Matematik \xc3\x85k1', '\xc3\xa5k 3'
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

isFindingReplacements = False

if isFindingReplacements:
   for a in unknown:
      print repr(a)

else:
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
