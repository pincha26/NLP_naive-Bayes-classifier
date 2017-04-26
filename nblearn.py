from __future__ import division
import string
import sys
mylist = {}
mylist['deceptive'] = {}
mylist['truthful'] = {}
mylist['positive'] = {}
mylist['negative'] = {}
mylist['prior'] = {} 

text_file = open("words.txt", "r")
repeatedwordlist = text_file.read().split()

identityMap = {}
labellist = [];
labels=open(sys.argv[2],"r")
labellist = labels.readlines()
for text in range(len(labellist)):
    tokensplit = labellist[text].split()
    key = tokensplit.pop(0)
    identityMap[key] = tokensplit

deceptive = 0
truthful = 0
positive = 0
negative = 0
wordfreq = {}
uniquewordlist = []
text = open(sys.argv[1],"r")
textlist = text.readlines()
for line in range(len(textlist)):
    wordlist = textlist[line].split()
    uniqueId = wordlist.pop(0)
    if identityMap.get(uniqueId)[0] == "deceptive" or identityMap.get(uniqueId)[1] == "deceptive":
        deceptive += 1
    else:
        truthful += 1
    if identityMap.get(uniqueId)[0] == "positive" or identityMap.get(uniqueId)[1] == "positive":
        positive += 1
    else:
        negative += 1
    for w in wordlist:
        w = w.lower()
        w = w.translate(None, string.punctuation)
        if not w:
            continue
        if w.isdigit():
            continue
        if w in repeatedwordlist:
            continue
        else:
            uniquewordlist.append(w)
            if(w in mylist[identityMap.get(uniqueId)[0]]):
                mylist[identityMap.get(uniqueId)[0]][w] += 1
            else:
                mylist[identityMap.get(uniqueId)[0]][w] = 1
            if(w in mylist[identityMap.get(uniqueId)[1]]):
                mylist[identityMap.get(uniqueId)[1]][w] += 1
            else:
                mylist[identityMap.get(uniqueId)[1]][w] = 1

set(uniquewordlist)
totalreviews = deceptive + truthful + negative + positive
mylist['prior']['deceptive'] = deceptive/(deceptive + truthful )
mylist['prior']['truthful'] = truthful/(deceptive + truthful )
mylist['prior']['negative'] = negative/(negative + positive)
mylist['prior']['positive'] = positive/(negative + positive)

for unique in uniquewordlist:
    if not(mylist['deceptive'].has_key(unique)):
        mylist['deceptive'][unique] = 0
    if not(mylist['truthful'].has_key(unique)):
        mylist['truthful'][unique] = 0
    if not(mylist['positive'].has_key(unique)):
        mylist['positive'][unique] = 0
    if not(mylist['negative'].has_key(unique)):
        mylist['negative'][unique] = 0

deceptiveFreqList =  mylist['deceptive'].values()
truthfulFreqList =  mylist['truthful'].values()
positiveFreqList =  mylist['positive'].values()
negativeFreqList =  mylist['negative'].values()

print mylist

totaldeceptivewords = 0
for feature in mylist['deceptive'].keys():
    mylist['deceptive'][feature] += 1
    totaldeceptivewords += mylist['deceptive'][feature]

for feature in mylist['deceptive'].keys():
    mylist['deceptive'][feature] = mylist['deceptive'][feature]/totaldeceptivewords

totaltruthfulwords = 0
for feature in mylist['truthful'].keys():
    mylist['truthful'][feature] += 1
    totaltruthfulwords += mylist['truthful'][feature]

for feature in mylist['truthful'].keys():
    mylist['truthful'][feature] = mylist['truthful'][feature]/totaltruthfulwords

totalpositivewords = 0
for feature in mylist['positive'].keys():
    mylist['positive'][feature] += 1
    totalpositivewords += mylist['positive'][feature]

for feature in mylist['positive'].keys():
    mylist['positive'][feature] = mylist['positive'][feature]/totalpositivewords

totalnegativewords = 0
for feature in mylist['negative'].keys():
    mylist['negative'][feature] += 1
    totalnegativewords += mylist['negative'][feature]

for feature in mylist['negative'].keys():
        mylist['negative'][feature] = mylist['negative'][feature]/totalnegativewords

import json
with open('nbmodel.txt', 'w') as outfile:
    json.dump(mylist, outfile)
outfile.close()