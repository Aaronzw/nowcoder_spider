#-*- coding:utf-8 -*-
from jieba import analyse
import jieba

# 引入TF-IDF关键词抽取接口
tfidf = analyse.extract_tags
textrank = analyse.textrank

with open('数据挖掘实习面经合集.txt') as f:
	t = f.read()
	# userdict = "./userdict/userdict.txt"
	# jieba.analyse.set_idf_path(userdict)
	kWords = jieba.analyse.extract_tags(t, topK=200,withWeight=True)
	for word,weight in kWords:
	   print word,":",weight
