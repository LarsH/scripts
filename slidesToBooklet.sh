#!/bin/sh

#Create temporary directory
AAA=/tmp/printFolder
mkdir -p $AAA

if file "$1" | grep "$1: PDF document" > /dev/null ; then
   # Argument is a pdf-file, convert
   pdf2ps "$1" $AAA/1.ps || exit
else
      if file "$1" | grep "$1: PostScript document" > /dev/null ; then
         # Argument is a ps-file, copy
         cp "$1" $AAA/1.ps || exit
      else
         echo "$1 is not a pdf/ps file"
         exit
      fi
fi

psnup -pa4 -f -n2 $AAA/1.ps $AAA/2.ps || exit

$(dirname $0)/printBooklet.sh $AAA/2.ps
