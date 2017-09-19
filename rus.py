#!/usr/bin/env python

"""rus.py: scraps data from the Rus(Professor at the University of Memphis)."""

__author__      = "Saurab Dulal"
__copyright__   = "..Bam.."

import urllib
import re as regx
from collections import Counter

def word_count_in_list(revised_list): #count the words(not refined much) in a list and returns a dictonary
    words = revised_list
    counts = Counter(words)
    return counts


def parserRus():

    url = "http://www.cs.memphis.edu/~vrus/teaching/ir-websearch/"

    fp = urllib.request.urlopen(url) #getting html dome
    mybytes = fp.read() #reading content

    mystr = mybytes.decode("utf8") #decoding to readable ascii
    fp.close()
    mystr = str(mystr)
    mystr_split = mystr.split("<!--BEGIN PAGE CONTENT") #this will get the body containt

    m = (regx.sub(r'<([^>]*)>','Nepali',mystr_split[1])).strip() #replace any content "<*any*>" with Nepali(free to choose yours)
    text_list = m.split('Nepali')
    revised_list = []
    for item in text_list:
        text_list = item.strip()
        if text_list !='':
            temp = regx.split(' |\n|/',text_list) #spliting text on the basis of space and newline, we can add other spliting ws her
            for temp_item in temp:
                revised_list.append(temp_item)

    print(word_count_in_list(revised_list)) #getting word count and printing the list


def main():
    parserRus()

if __name__ == '__main__':
    main()
