#-*- coding:utf-8 -*-
from jieba import analyse
import jieba
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--filepath', '-f', type=str, help='解析文件地址')
	args = parser.parse_args()

	try:
		if args.filepath:
			# 引入TF-IDF关键词抽取接口
			tfidf = analyse.extract_tags
			textrank = analyse.textrank
			with open(args.filepath) as f:
				t = f.read()
				# userdict = "./userdict/userdict.txt"
				# jieba.analyse.set_idf_path(userdict)
				kWords = jieba.analyse.extract_tags(t, topK=200,withWeight=True)
				for word,weight in kWords:
				   print word,":",weight
	except Exception as e:
		print '请输入正确的目标文件地址。'