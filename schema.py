#!/usr/bin/env python
import urllib
from timeEditObfuscation import scramble, unscramble

baseurl = 'https://se.timeedit.net/web/uu/db1/schema/s.ics'

'''
time = '140124-140701'
courses = {'PProg': 253725, 'Krypto': 253479, 'Dir': 254498, 'Berv2': 253721,\
      'PT1': 253724, 'HPC': 253716}
'''

time = '140801-150201'
courses = {'Musikteori2': 389680, 'ModIS': 387448}

objects = 'objects=' + ','.join(['%u.201,-1'%courses[c] for c in courses])

query = objects + '&p=' + time
url = baseurl + '?i=' + scramble(query)

# Replacements
typ = {'Tentamen': 'Tenta', 'Omtentamen': 'Omtenta', 'Laboration':'Lab',
'F\xc3\xb6rel\xc3\xa4sning': 'F\xc3\xb6rel.', 'Presentation':'Pres.',
'Datalab': 'Lab', 'Workshop': 'Workshop', 'Workout':'Workout',
'Probleml\xc3\xb6sning': 'Prob'}
campus = { 'ITC': 'Pol:', '\xc3\x85ngstr\xc3\xb6m':'\xc3\x85ng:'}
kurs = {'Programmering av parallelldatorer': 'PProg',
      'Kryptologi': 'Krypto',
      'Programmeringsteknik I': 'PT1',
      'H\xc3\xb6gprestandaber\xc3\xa4kningar och programmering': 'HPC',
      'Ber\xc3\xa4kningsvetenskap II': 'Berv2',
      'Modellbaserad utveckling av inbyggd programvara': 'ModIS'}

class Entry(object):
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

   def beautify(self):
      self.description += self.summary
      l = self.summary.split('\, ')

      if l[0] in kurs:
         self.summary = kurs[l[0]]
      else:
         self.summary = l[0]

      for prev,this in zip(l,l[1:]):
         if this in typ:
            self.summary += ", " + typ[this]
         elif this in campus:
            if self.location != '':
               self.location += ', '
            self.location += campus[this]+prev

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
      elif cmd == 'UID':
         self.uid = data
      elif cmd == 'DESCRIPTION':
         self.description = data
      elif cmd == 'DTSTAMP':
         # IGNORED
         pass
      elif cmd == 'LAST-MODIFIED':
         # IGNORED
         pass
      elif cmd == 'LOCATION':
         self.location = data
      elif cmd == 'SUMMARY':
         self.summary = data
      else:
         raise NameError(cmd)
      return self

   @staticmethod
   def parseNewEntry(line):
      if line == "BEGIN:VEVENT":
         return Entry()
      else:
         return None

class Calendar(object):
   def __init__(self):
      self.entries = [] # entries are Events or strings, ending with newline
      self.handle = None

   def __str__(self):
      return ''.join(map(str, self.entries))

   def __repr__(self):
      return "Calendar: " + repr(self.entries)

   def beautify(self):
      for e in self.entries:
         if type(e) == Entry:
            e.beautify()

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
   return cal

cal = parseCalendar(lines)
cal.beautify()
output = str(cal)
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
