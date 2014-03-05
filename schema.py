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

class Entry:
   def __init__(self):
      self.start, self.end, self.uid = '', '', ''
      self.summary, self.location, self.description = '', '', ''

   def __str__(self):
      head = "BEGIN:VEVENT\r\nDTSTART:%s\r\nDTEND:%s\r\nUID:%s" \
            % (self.start, self.end, self.uid)
      tail = "SUMMARY:%s\r\nLOCATION:%s\r\nDESCRIPTION:%s\r\nEND:VEVENT\r\n" \
            % (self.summary, self.location, self.description)
      m = 2 ** 32
      eh = '-%8.8x' % ((hash(head + tail)+m)%m)
      head += eh + '\r\n'
      return head + tail

   def parseEntry(self, line):
      cmd, data = line.split(':',1)
      if cmd == 'DTSTART':
         self.start = data
      elif cmd == 'DTEND':
         self.end = data
      elif cmd == 'END':
         assert data == 'VEVENT'
         # Entry is finished
         return None
      else:
         #raise NameError(cmd)
         pass
      return self

   @staticmethod
   def parseNewEntry(line):
      if line == "BEGIN:VEVENT":
         return Entry()
      else:
         return None

class Calendar:
   def __init__(self):
      self.entries = [] # entries are Events or strings, ending with newline
      self.handle = None

   def __str__(self):
      return ''.join(map(str, self.entries))

   def __repr__(self):
      return "Calendar: " + repr(self.entries)


   def parseLine(self, line):
      if self.handle == None:
         self.handle = Entry.parseNewEntry(line)
         if self.handle != None:
            self.entries += [self.handle]
         else:
            self.entries += [line + '\r\n']
      else:
         self.handle = self.handle.parseEntry(line)

def getLines(url):
   s = urllib.urlopen(url).read()
   s = s.replace('\r\n ', '')

   lines = []
   for e in s.split('\r\n'):
      if len(e) > 0 and e[0] == ' ':
         assert len(lines) > 0, "First line should not be a continuation"
         lines[-1] += e[1:]
      else:
         lines += [e]
   return lines

lines = getLines(url)

def parseCalendar(lines):
   cal = Calendar()
   for line in lines:
      cal.parseLine(line)
   return str(cal)

output = parseCalendar(lines)
isFindingReplacements = False

if isFindingReplacements:
   raise NotImplementedError

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
