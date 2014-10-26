"""
TimeEdit url (de)obfuscation

Rewritten obfuscation and corresponding deobfuscation routines from
https://se.timeedit.net/static/3_5_2_I_1338/min.js
Very annoying. Not hard, just annoying. Don't piss off hackers.
"""

tabledata = [ ['h=t&sid=', '6='], \
      ['objects=', '1='], \
      ['sid=', '2='], \
      ['&ox=0&types=0&fe=0', '3=3'], \
      ['&types=0&fe=0', '5=5'], \
      ['&h=t&p=', '4=']]

pairs= [['=', 'Q'], ['&', 'Z'], [',', 'X'], ['.', 'Y'], [' ', 'V'], ['-', 'W']]

pattern = [4, 22, 5, 37, 26, 17, 33, 15, 39, 11, 45, 20, 2, 40, 19, 36, 28, 38,\
      30, 41, 44, 42, 7, 24, 14, 27, 35, 25, 12, 1, 43, 23, 6, 16, 3, 9, 47,\
      46, 48, 50, 21, 10, 49, 32, 18, 31, 29, 34, 13, 8]


def tableshort(result):
   for key in tabledata:
      result = result.replace(key[0], key[1])
   return result

def tablelong(result):
   ''' inverse of tableshort'''
   for key in tabledata:
      result = result.replace(key[1], key[0])
   return result

def modKey(ch):
   if ch in range(ord('a'),1+ord('z')):
      return (ord('a') + (ch - ord('a') + 9) % 26)
   elif ch in range(ord('1'), 1+ord('9')):
      return (ord('1') + (ch - ord('1') + 4) % 9);
   else:
      return ch;


def invmodKey(ch):
   '''inverse of modKey'''
   if ch in range(ord('a'),1+ord('z')):
      return (ord('a') + (ch - ord('a') - 9 + 26) % 26)
   elif ch in range(ord('1'), 1+ord('9')):
      return (ord('1') + (ch - ord('1') - 4 + 9) % 9);
   else:
      return ch;

def scrambleChar(ch):
   for pair in pairs:
      if ch == pair[0]:
         return pair[1]
      elif ch == pair[1]:
         return pair[0]
   return chr(modKey(ord(ch)))

def unscrambleChar(ch):
   '''Inverse of scrambleChar'''
   for pair in pairs:
      if ch == pair[0]:
         return pair[1]
      elif ch == pair[1]:
         return pair[0]
   return chr(invmodKey(ord(ch)))


def swap(result,first, second):
   """Swaps two elements in a list, it is the inverse of itself"""
   if not first in range(len(result)):
      return
   if not second in range(len(result)):
      return
   tmp = result[first]
   result[first] = result[second]
   result[second] = tmp


def swapPattern(result):
   for step in range(len(result)):
      for index in range(1,len(pattern),2):
         i = pattern[index    ] + step * len(pattern)
         j = pattern[index - 1] + step * len(pattern)
         swap(result, i, j)

def invswapPattern(result):
   '''Inverse of swapPattern'''
   for step in range(len(result))[::-1]:
      for index in range(1,len(pattern),2)[::-1]:
         i = pattern[index    ] + step * len(pattern)
         j = pattern[index - 1] + step * len(pattern)
         swap(result, i, j)

def swapChar(result):
   split = [c for c in result]
   split = map(scrambleChar, split)
   swapPattern(split)
   return ''.join(split)


def invswapChar(result):
   '''Inverse of swapChar'''
   split = [c for c in result]
   invswapPattern(split)
   split = map(unscrambleChar, split)
   return ''.join(split)

def scramble(query):
   """Main obfuscation function"""
   if len(query) < 2:
      return query;

   if query[:2] == 'i=':
      return query

   result = query # decode url

   result = tableshort(result)
   result = swapChar(result)
   result = result # encode url
   return result


def unscramble(query):
   """Inverse of scramble"""
   if len(query) < 2:
      return query;

   if query[:2] == 'i=':
      return query

   result = query # decode url

   result = invswapChar(result)
   result = tablelong(result)

   result = result # encode url
   return result

if __name__ == '__main__':
   import sys
   print """Usage: %s [i-string]
   Runs tests, and descrambles i-string if supplied."""%sys.argv[0]
   if len(sys.argv) > 1:
      print unscramble(sys.argv[1])

   # Test case
   s = "h=t&sid=3&p=130902-140118&objects=2625=0&types=0&fe=0"
   assert invswapChar(swapChar(s)) == s

   # Test case
   for c in range(256):
      assert invmodKey(modKey(c)) == c

   tests = {}
   tests["h=t&sid=3&p=130902-140118&objects=262589.200&ox=0&types=0&fe=0"] = \
         "1W746Q565ZQ6Q04Q530Z50y17958Y703706"
   for t in tests:
      assert scramble(t) == tests[t]
      assert unscramble(tests[t]) == t
   print "All tests passed"
