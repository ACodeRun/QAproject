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
print "<title>illqq</title>"
print "</head>"
print "<body>"
print '<form action="/cgi-bin/illaa.py" method="POST">'

def illdata():
    name = codecs.open("user.txt",'r')
    try:
         ill_list = name.readline().strip().split()
    finally:
         name.close()
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

def namedata(ill_list):
    linenum = illline(ill_list)
    name_list = name1_lines[linenum[0]].strip().split()
    for i in linenum:
        name_sum = name1_lines[i].strip().split()
        name_list = list(set(name_list).intersection(set(name_sum)))
    return name_list


def nameline(name_list):
    linenum = []
    for name in name_list:
        nametoill_name = codecs.open("relate2_name.data",'r')
        name2_line = nametoill_name.readline().strip()
        i = 0
        while name2_line:
            if name == name2_line:
                linenum.append(i)
                nametoill_name.close()
                break
            name2_line = nametoill_name.readline().strip()
            i = i + 1
    return linenum

def createDataSet(linenum,name_list):
    #dataSet = [[1,0,0,'fight'],[0,1,1,'fight2'],[0,1,0,'fight3']]
    #lables = ['weapon','bullet','blood']
    lables = []
    for i in linenum:
        ills = ill2_lines[i].strip().split()
        lables = list(set(lables).union(set(ills)))
    dataSet =  [[] * len(lables) for row in range(len(linenum))]
    for i in range(len(linenum)):
        ills = ill2_lines[linenum[i]].strip().split()
        for lable in lables:
            flag = 0
            for ill in ills:
                if lable == ill:
                    flag = 1
                    break
            dataSet[i].append(flag)
        dataSet[i].append(name_list[i])
    return dataSet,lables

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    lableCounts = {}
    for featVec in dataSet:
        currentLable = featVec[-1]
        if currentLable not in lableCounts.keys():
            lableCounts[currentLable] = 0
        lableCounts[currentLable] += 1
    shannonEnt = 0
    for key in lableCounts:
        prob = float(lableCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def FeatureSplit(dataSet):
    numlist = []
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        numlist.append([infoGain,i])
        numlist.sort(key=lambda x:int(x[0]),reverse=True)
    return numlist

def Forecast(datalist,lable):
    lablev = []
    for i in range(min(6,len(datalist))):
        lablev.append(lable[datalist[i][1]])
    return lablev

print '<br/>'
ill_list = illdata()
name_list = namedata(ill_list)
linenum = nameline(name_list)
myDat,lable = createDataSet(linenum,name_list)
datalist = FeatureSplit(myDat)
lablev = Forecast(datalist,lable)
for x in range(len(lablev)):
    print '<input type="checkbox" name=%d value="on" /> %s' %(x,lablev[x])
print '<br/>'
print '<input type="text" name="-1">' 
print '<input type="submit" value="确定" />'
print '</form>'
print "</body>"
print "</html>"
