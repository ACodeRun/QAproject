#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi, cgitb ,codecs
from math import log 
form = cgi.FieldStorage()

#一条病症对应多条疾病；疾病字典
illtoname_name = codecs.open("relate1_name.data",'r')
name1_lines = illtoname_name.readlines()
illtoname_name.close()
#一个疾病对于多条病症；病症字典
nametoill_ill = codecs.open("relate2_ill.data",'r')
ill2_lines = nametoill_ill.readlines()
nametoill_ill.close()

print "Content-type:text/html"
print
print "<html>"
print "<head>"
print "<meta charset=\"utf-8\">"
print "<title>illa</title>"
print "</head>"
print "<body>"

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
        lablev.append(ill_counter[x][0])
    return lablev

def indata(lablev):
    ill_list = []
    for i in range(12):
        if form.getvalue(str(i)):
            ill_list.append(lablev[i])
    if form.getvalue('-1'):
        site_ill = form.getvalue('-1')
        ill_list = ill_list + site_ill.split()
    return ill_list

def illline(ill_list):
    linenum = []
    for ill in ill_list:
        flag = 0
        illtoname_ill = codecs.open("relate1_ill.data",'r')
        ill1_line = illtoname_ill.readline().strip()
        i = 0
        while ill1_line:
            if ill == ill1_line:
                linenum.append(i)
                illtoname_ill.close()
                flag = 1
                break
            ill1_line = illtoname_ill.readline().strip()
            i = i + 1
        if flag == 0:
            linenum = []
            break
    return linenum

def judge(name_list,ill_list):
    linenum = illline(ill_list)
    if  len(linenum) == 0:
        print "<h1>未匹配到合适病症</h1>"
        return 0
    if len(name_list) == 0 and len(linenum) > 0:
        name_list = name1_lines[linenum[0]].strip().split()
    for i in linenum:
        name_sum = name1_lines[i].strip().split()
        name_list = list(set(name_list).intersection(set(name_sum)))
    if len(name_list) == 0:
        print "<h1>未匹配到合适疾病</h1>"
    if len(name_list) == 1:
        print "<h1>匹配疾病为 %s</h1>" %(name_list[0])
    if len(name_list) > 1:
    	print "<h1>提供信息较少，无法判断，请继续输入病症</h1>"
        print '<a href="/cgi-bin/illqq.py">继续输入</a>'
    return 0

lablev = all_Forecast()
ill_list = indata(lablev)
user = codecs.open("user.txt",'w')
for ill in ill_list:
    #print "<h1>匹配疾病为 %s</h1>" %(ill)
    user.write(ill)
    user.write(" ")
user.close()
# name = codecs.open("user.txt",'r')
# try:
#      all_ill = name.readline().strip().split()
# finally:
#      name.close()
# for ill in all_ill:
#     print "<h1>匹配疾病为 %s</h1>" %(ill)
name_list = []
judge(name_list,ill_list)

print "</body>"
print "</html>"
