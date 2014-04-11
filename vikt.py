#!/usr/bin/env python
"""
Small script for plotting weight over time, including BMI axis

Weight data is stored in a flat file with LF-newline:

file := line file | ''
line := timestamp weight '\n'
timestamp := integer
weight := integer '.' digit

timestamp is in UNIX-epoch, seconds since 1970-01-01
weight data is in kilograms with one decimal
"""

import time, os, sys
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Used for BMI calculation, person length in meters
LEN=1.84

# Target data to scale plot view area
ttarget = mdates.epoch2num(1400000000)
vtarget = 80

def saveVikt(filename, v):
        v = float(v)
        s = "%u %.1f\n" % (time.time(), v)
        f = open(filename, "a")
        f.write(s)
        f.close()

def convert2pdf(filename, outname):
   l = open(filename).read().split('\n')[:-1]
   l = [map(eval, e.split()) for e in l]

   vlist = [v for t,v in l]
   tlist = [t for t,v in l]
   vlist = [min(vlist + [vtarget])] + vlist + [min(vlist + [vtarget])]
   tlist = [min(tlist)] + tlist + [max(tlist)]

   tlist = map(mdates.epoch2num, tlist)

   fig, axbmi = plt.subplots()
   fig.autofmt_xdate()
   axkg = axbmi.twinx()
   axbmi.xaxis_date()
   axbmi.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
   axkg.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

   def Tbmi(kg):
      return kg / (LEN*LEN)

   def update_axbmi(axkg):
      y1, y2 = axkg.get_ylim()
      axbmi.set_ylim(Tbmi(y1), Tbmi(y2))
      axkg.figure.canvas.draw()

   # automatically update ylim of ax2 when ylim of ax1 changes.
   axkg.callbacks.connect("ylim_changed", update_axbmi)
   axkg.fill(tlist,vlist,facecolor='0.8',edgecolor='0')
   axkg.plot(tlist,vlist,'k+')
   ylim = axkg.get_ylim()
   axkg.plot([tlist[1], ttarget], [vlist[1], vtarget], 'r--')
   axkg.plot([tlist[1], ttarget], [vlist[1]-1, vtarget-1], 'b--')
   axkg.plot([tlist[1], ttarget], [vlist[1]-2, vtarget-2], 'g--')
   axkg.set_ylim(ylim)

   axbmi.set_ylabel('BMI')
   axkg.set_ylabel('Vikt (kg)')

   mint = min(tlist)
   maxt = max(tlist + [ttarget])
   extrat = (maxt-mint)/20
   axbmi.set_xlim(mint-extrat, maxt+extrat)

   plt.savefig(outname)

if __name__ == '__main__':
   filename = 'vikt.txt'
   outname = 'vikt.pdf'

   if len(sys.argv) > 1:
      saveVikt(filename, sys.argv[1])

   convert2pdf(filename, outname)
