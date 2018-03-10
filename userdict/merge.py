#!/bin/python
# -*- coding: utf-8 -*-
import glob

files = glob.glob('./搜狗词库/*.txt')

result = open('userdict.txt','w')

userdict = set()
aaa= list()
for file in files:  
    for line in open(file): 
    	word = line.split()[0] 
        userdict.add(word)
        aaa.append(word)

for userword in userdict:
    result.write(str(userword) + ' ' + "1.0" + '\n')

print(len(userdict),len(aaa))
#关闭文件  
result.close()  
