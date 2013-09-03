#!/bin/sh

if ! file "$1" | grep "$1: PDF document" > /dev/null ; then
   echo "$1 is not a pdf file"
   exit
fi

echo Printing \"$1\" as a booklet

#Create temporary directory
AAA=/tmp/printFolder
mkdir $AAA

# Convert to ps
pdf2ps "$1" $AAA/1.ps || exit

# Auto-stapling works for max 15 sheets, limit to 15*4=60 pages
psselect -p1-60 $AAA/1.ps $AAA/1.5.ps

# Rearrange pages
psbook $AAA/1.5.ps $AAA/2.ps || exit

# Reverse pages to get stapling/folding from the correct side
psselect -r $AAA/2.ps $AAA/3.ps  || exit

# Convert back to pdf
ps2pdf $AAA/3.ps $AAA/toPrint.pdf || exit

# Print document with automatic folding and stapling
lp -o "Duplex=DuplexTumble InputSlot=Auto number-up=2 number-up-layout=rltb PageSize=A4 StapleLocation=CenterW" $AAA/toPrint.pdf
