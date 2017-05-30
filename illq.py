#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi, cgitb ,codecs
from math import log 
form = cgi.FieldStorage()

#一个疾病对于多条病症；病症字典
nametoill_ill = codecs.open("relate2_ill.data",'r')
ill2_lines = nametoill_ill.readlines()
nametoill_ill.close()
print "Content-type:text/html"
print
print "<html>"
print "<head>"
print "<meta charset=\"utf-8\">"
print "<title>illq</title>"
print "</head>"
print "<body>"
print '<form action="/cgi-bin/illa.py" method="POST">'

def all_Forecast():
    ill_counter = []
    for line in range(len(ill2_lines)):
        ill_sum = ill2_lines[line].strip().split()
        for j in ill_sum:
            flag = 0
            for i in range (len(ill_counter)):
                if j == ill_counter[i][0]:
                    ill_counter[i][1] = str(int(ill_counter[i][1]) + 1)
                    flag = 1
                    break
            if flag == 0:
                ill_counter.append([j,'1'])
    ill_counter.sort(key=lambda x:int(x[1]),reverse=True)
    lablev = []
    for x in range(12):
    	print '<input type="checkbox" name=%d value="on" /> %s' %(x,ill_counter[x][0])
        lablev.append(ill_counter[i][0])
        if (x+1)%6 == 0:
        	print '<br/>'
    #return lablev

print '<br/>'
all_Forecast()
print '<input type="text" name="-1">' 
print '<input type="submit" value="确定" />'
print '</form>'
print "</body>"
print "</html>"
