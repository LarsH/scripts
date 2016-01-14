#!/usr/bin/env python
import urllib
from timeEditObfuscation import scramble, unscramble


'''
MANUAL:
   Ny kurs:
   1: Kopiera schemalink:, ex: schema/s.ics?i=647QyQYZ9Z88Q5036600
   2: python timeEditObfuscation.py 647QyQYZ9Z88Q5036600
       -> 449508
   3: Laegg till kurs i courses-dicten
   4: Uppdatera tidsomfaang i time
   5: Laegg till nya foerkortning i kurs
   6: Laegg ev till nya typer och nytt campus i typ och campus
"'''

baseurl = 'https://se.timeedit.net/web/uu/db1/schema/s.ics'

'''
time = '140124-140701'
courses = {'PProg': 253725, 'Krypto': 253479, 'Dir': 254498, 'Berv2': 253721,\
      'PT1': 253724, 'HPC': 253716}

time = '140801-150201'
courses = {'Musikteori2': 389680, 'ModIS': 387448, 'KKKons':449508}

time = '150101-150831'
courses = {'a': 871362, 'b': 388019, 'c': 389664, 'sysoperanalys':871314,\
      'KAnalys':387815}
'''

time = '150801-160129'
courses = { 'a' : 978650 # EMFT
      ,'b' : 1046835 # introF ?
      ,'c' : 1004077 # Extrema miljoer
      ,'d' : 909616 # Algebra Geometri
      ,'e' : 1004215 # analog elektronik
      ,'f' : 1004079 # ECAD 1
      ,'g' : 1004197 # signalbehandling
      ,'h' : 1004086 # Termo, fraagor
      ,'i' : 1004085 # Termo, foerlasningar
      }

time = '160101-160808'
courses = { 'a': 981415 # mekanik baskurs
      ,'b': 978601 # internet of things
      ,'c': 1070810 # kexjobb F
      ,'d': 1070807 # digital kommunikation
      ,'e': 1070780 # EMC
      }

objects = 'objects=' + ','.join(['%u.201,-1'%courses[c] for c in courses])

query = objects + '&p=' + time
url = baseurl + '?i=' + scramble(query)

# Replacements
typ = {'Tentamen': 'Tenta', 'Omtentamen': 'Omtenta', 'Laboration':'Lab',
'F\xc3\xb6rel\xc3\xa4sning': 'F\xc3\xb6rel.', 'Presentation':'Pres.',
'Datalab': 'Lab', 'Workshop': 'Workshop', 'Workout':'Workout',
'Probleml\xc3\xb6sning': 'Prob', 'studiebes\xc3\xb6k':'Studiebes\xc3\xb6k',
'Seminarium':'Seminarium', 'Lektion': 'Lekt.',
'Handledning datorer': 'DataPropp', 'Dugga':'Dugga',
'\xc3\x96vning':'\xc3\x96vning', 'Introduktion':'Intro',
'Obligatorisk n\xc3\xa4rvaro': 'OBLIGATORISKT',
'Redovisning':'Redov.','Fr\xc3\xa5gestund':'QA'
}

campus = { 'ITC': 'Pol:', '\xc3\x85ngstr\xc3\xb6m':'\xc3\x85ng:'}



'''
Kursfoerkortningar. Foer att ignorera en kurs, saett den till tomma straengen
'''
kurs = {'Programmering av parallelldatorer': 'PProg',
      'Kryptologi': 'Krypto',
      'Programmeringsteknik I': 'PT1',
      'H\xc3\xb6gprestandaber\xc3\xa4kningar och programmering': 'HPC',
      'Ber\xc3\xa4kningsvetenskap II': 'Berv2',
      'Modellbaserad utveckling av inbyggd programvara': 'ModIS',
      'Kretskortkonstruktion med ECAD-verktyg': 'PCB-CAD',
      'Programmering av enkapseldatorer':'uCprog',
      'Elektromekaniskt projekt':'ElMekProj',
      'System- och operationsanalys':'SysOpAn',
      'Komplex analys':'KAnalys',
      'Introduktion till teknisk fysik':'IntroF',
      'Elektromagnetisk f\xc3\xa4ltteori': 'EMFT',
      'Elektronik i extrema milj\xc3\xb6er':'ExtrEl',
      'Algebra och geometri':"AlGeo",
      'Analog elektronik': "AnEl",
      'Projekt i digital elektronikkonstruktion':'',
      'Signalbehandling': 'SigBH',
      'Teknisk termodynamik':'Termo',
      'Mekanik baskurs':'Mek1',
      'Digital kommunikation':'DigKom',
      'Internet of Things':'IoT'
      }
rum = {'H\xc3\xa4ggsalen':'H\xc3\xa4gg', 'Datorsal': 'Datorsal',\
      'Polhemsalen':'Polhem',\
      '\xc3\x85ng/73121: Oseenska rummet (Internt rum f\xc3\xb6r FysAst)': '73121',
      'F\xc3\xb6r tid och plats se studentportalen': 'TBD',
'Siegbahnsalen': 'Siegbahn',
'Hus 6': 'Hus 6',
'Aula' : 'Aula',
'B8\\,BMC': 'BMC:B8',
'Datasal 4103':'4103',
'V\xc3\xa4rmel\xc3\xa4ralab':'V\xc3\xa4rmelab',
'Mekaniklab':'MekLab',
'Lablektion':'LabLekt',
'Hemtenta':'Hemtenta'
}

lecturers = ['Andris Vaivads', 'Cecilia Norgren','Irina Dolguntseva',
      'Lennart \xc3\x85hl\xc3\xa9n', 'Cecilia Holmgren', 'Martin Herschend',
      'Jian Qiu', 'Helena Jonsson', 'Niklas Fejes','Viktoria Veselic',
      'Oleg Shebanits', 'J\xc3\xb6rgen Olsson', 'Pawel Marciniewski',
      'Leif Gustafsson','Magnus Jobs','Subhrakanti Dey','Matthias Weiszflog',
      'Sebastian George','Ulf Danielsson','Mattias Klintenberg',
      'Jacob Winding','Paul Barklem','Mattias Ellert','Anders Bergman',
      'Andrzej Kupsc','Thiemo Voigt','Mikael Sternad'
      ]

stringclasses = ['typ', 'campus', 'kurs', 'rum', 'instution', 'lecturer',\
      'program', 'group']

def classify(s):
   c = None
   if s in typ:
      assert c == None
      c = stringclasses.index('typ')
   elif s in campus:
      assert c == None
      c = stringclasses.index('campus')
   elif s in kurs:
      assert c == None
      c = stringclasses.index('kurs')
   elif s.isdigit() or s in rum or s.replace('K','').isdigit() or\
         s.replace('b','').isdigit():
      assert c == None
      c = stringclasses.index('rum')
   elif s.startswith('Institutionen f\xc3\xb6r ') or\
         s.endswith(' institutionen'):
      assert c == None
      c = stringclasses.index('instution')
   elif s in lecturers:
      assert c == None
      c = stringclasses.index('lecturer')
   elif s.startswith('Masterprogram') or s.startswith('Kandidatprogram') or\
         s.startswith('Teknisk fysik ') or\
         s.startswith('Civilingenj\xc3\xb6rsprogrammet') or\
         s in [ 'Energisystem',
               'Milj\xc3\xb6- och vattenteknik',
               'Informationsteknologi' ]:

      assert c == None
      c = stringclasses.index('program')
   elif s.startswith('Grupp ') or s.startswith('\xc3\xa5k '):
      assert c == None
      c = stringclasses.index('group')

   if c == None:
      print "Could not determine class for:" + repr(s)
   return c


class Entry(object):
   def __init__(self):
      self.start, self.end, self.uid = '', '', ''
      self.summary, self.location, self.description = '', '', ''
      self.isBeautified = False

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
      if self.isBeautified:
         return
      self.isBeautified = True

      self.description += self.summary
      l = self.summary.split('\, ')
      l = list(set(l))

      # Ugly hack for '\xc3\x85ngstr\xc3\xb6m 8K1117'
      for i,s in enumerate(l):
         for c in campus:
            if c+' ' in s:
               l[i] = c
               l += [s.replace(c+' ','')]

      cl = map(classify, l)
      if None in cl:
         print self.summary
         assert False, "Beskrivning: %r" % self.description

      summarylist = []
      for s, c in zip(l, cl):
         if stringclasses.index('kurs') == c and kurs[s] != '':
            # Some events are shared between several courses,
            # Don't add irrellevant courses to the description
            summarylist += [kurs[s]]
      for s, c in zip(l, cl):
         if stringclasses.index('typ') == c:
            summarylist += [typ[s]]
      self.summary = ', '.join(summarylist)

      assert self.location == '', repr(self.location)

      for s, c in zip(l, cl):
         if stringclasses.index('campus') == c:
            self.location += campus[s]
      rooms = []
      for s, c in zip(l, cl):
         if stringclasses.index('rum') == c:
            if s in rum:
               s = rum[s]
            rooms += [s]
      self.location += '/'.join(rooms)

   def parseEntry(self, line):
      cmd, data = line.split(':',1)
      if cmd == 'DTSTART':
         self.start = data
      elif cmd == 'DTEND':
         self.end = data
      elif cmd == 'END':
         assert data == 'VEVENT', repr(data)
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
   s = s.replace('\r','\n') # The server seems to use both CRLF and LF
   s = s.replace('\n \n', '\n')
   lines = []
   for e in s.split('\n'):
      if len(e) > 0:
         if e[0] == ' ':
            assert len(lines) > 0, "First line should not be a continuation"
            lines[-1] += e[1:]
         else:
            lines += [e]
   return lines

def parseCalendar(lines):
   cal = Calendar()
   for line in lines:
      cal.parseLine(line)
   return cal


lines = getLines(url)
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
