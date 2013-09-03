#!/usr/bin/python

import urllib
import sys
from BeautifulSoup import BeautifulSoup

BASEURL= 'http://www.biltema.se'
SEARCHPAGE = BASEURL + '/sv/Sok/?query=%s&page=%u'


def getPage(url):
   return urllib.urlopen(url).read()


def priceToFloat(price):
   return float(price.replace(':','.').replace('-','0'))

def searchFor(query='pump'):

   results = []
   for pageNo in xrange(1,9000):
      page = getPage(SEARCHPAGE % (query,pageNo))
      if '500 - Internal server error' in page:
         break
      soup = BeautifulSoup(page)

      if pageNo == 1:
         i=soup.findAll('div',{'class':'mainBody'})[1].findAll('strong')[1].text
         i = int(i)
         print "Found %u items..." % i

      l = soup.find('ul',{"class" : "productList"}).findAll('li')
      for q in l:
         price = q.find('span', {'class': 'productPrice'}).contents[0]
         price = priceToFloat(price)
         a = q.find('h2').find('a')
         url = BASEURL + a['href']
         item = a.contents[0]
         results += [(price, item , url)]
      if i <= 20:
         break

   return results


def main():
   query = sys.argv[1:]
   if len(query) < 1:
      print "Searches biltema, sorted on price\nUsage: %s queries" % \
         sys.argv[0]
      return
   print 'Searching for: "' + ' '.join(query) + '"...'

   r = searchFor('+'.join(query))
   print "Found %u results:" % len(r)
   r.sort()
   ll = [0]*3
   for t in r:
      # no need for padding of the last element
      for i,e in enumerate(t[:-1]):
         e = str(e)
         if ll[i] < len(e):
            ll[i] = len(e)
   for t in r:
      for i,e in enumerate(t):
         e = str(e)
         print e + ' '*(ll[i] - len(e)),
      print

if __name__ == '__main__':
   main()
