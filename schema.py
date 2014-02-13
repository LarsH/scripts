#!/usr/bin/env python
import urllib
from timeEditObfuscation import scramble, unscramble

origurl = 'https://se.timeedit.net/web/uu/db1/schema/s.ics?i=6036X6695055QQ4XZ40X090Y55059W555YY5X67656661WX5X5WW90659557YX66560W604550YX5XZyQ3'
time = '130826-140124'
origurl = 'https://se.timeedit.net/web/uu/db1/schema/s.ics?i=yQX65X8W6Z05Q06Y5X656Z670049W6630875YQ95622X96Y8596XW5'
time = '140124-140701'

baseurl = origurl.split('?')[0]
i = origurl.split('=')[-1]

origrequest = unscramble(i).split('&')
objects = [e for e in origrequest if 'objects' in e][0]

query = objects + '&p=' + time
url = baseurl + '?i=' + scramble(query)

replacements = {
   'Realtidssystem': "Realtid",
   'Kompilatorteknik I': "KT",
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
   'Diskret matematik': 'DM'
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

# Entry contains either one or three elements
# The second element is the UID line, wich is not \r\n terminated until
# the entry hash has been computed.
entry = ['']

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


    if line[:4] == 'UID:':
        # Save away uid line, without \r\n for later
        entry += [line, '']

    elif line[:4] == 'END:':

        # Don't forget the current  line
        entry[-1] += line + '\r\n'

        # Calculate entry hash if needed
        if len(entry) == 3:
            m = 2 ** 32
            tohash=''.join(entry)
            eh = '-%8.8x' % ((hash(tohash)+m)%m)
            # Add hash and newlines to UID line
            entry[1] += eh + '\r\n'
            entry = [''.join(entry)]

        assert len(entry) == 1

        # Flush to output buffer
        output += entry[0]
        entry = ['']
    elif not line.startswith("DTSTAMP:") and \
          not line.startswith("LAST-MODIFIED:"):
      # Save lines until whole entry is parsed
      # Timestamp entries change on every retrieval, so don't include them in
      # the hashing.
      entry[-1] += line + '\r\n'

assert len(entry) == 1
# The last newline needs to be added as well
output += entry[0]

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
