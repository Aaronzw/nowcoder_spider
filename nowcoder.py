#-*- coding:utf-8 -*-
import urllib
import urllib2
from bs4 import BeautifulSoup  
import re
from urllib import quote
import sys
import signal

reload(sys)
sys.setdefaultencoding('utf-8')

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent' : user_agent}

def searchhref(query, start, end):
	targets = {}
	for i in range(start, end):
		try:
			page = str(i)
			url = base_url + '&query=' + quote(query) + '&page=' + page
			request = urllib2.Request(url,headers = headers)
			response = urllib2.urlopen(request)
			
			soup = BeautifulSoup(response.read(),'lxml')

			discuss_detail = soup.find_all('div',class_='discuss-detail')

			for x in discuss_detail:
				try:
					y=x.find('a', target='_blank')
					href = 'https://www.nowcoder.com' + y['href']
					title = y.string.split()[0].encode('utf-8')
					targets[title] = href
				except:
					pass
		except:
			pass
	return targets


def get_topic_detail(url):
	request = urllib2.Request(url,headers = headers)
	response = urllib2.urlopen(request)
	soup = BeautifulSoup(response.read(),'lxml')
	topic_detail = soup.find('div', class_='post-topic-des')
	text = ''
	for x in topic_detail:
		if x.string:
			text += x.string
	return text.encode('utf-8')


def handler(signum, frame):
    raise AssertionError


if __name__ == '__main__':
	'''
	query: 搜索关键词
	whitelist: 只保存含有白名单关键词的帖子
	blacklist: 不保存含有黑名单关键词的帖子
	'''
	query = '数据挖掘 实习 面经'
	page_start = 1
	page_end = 200
	base_url = "https://www.nowcoder.com/search?type=post&order=time"
	whitelist = ['机器学习', '数据挖掘', 'svm', 'nlp', '深度学习', 'deep', 'cnn', '卷积', '大数据', '挖掘']
	blacklist = ['吗', '?', '？', '求']

	targets = searchhref(query, page_start, page_end)

	count_all = 0
	count_saved = 0
	valid = False

	with open('数据挖掘实习面经.txt', 'w+') as f:
		for title in targets:
			try:
				#超时检测
				signal.signal(signal.SIGALRM, handler)
				signal.alarm(2)

				if not any(s in title for s in blacklist):
					href = targets[title]
					topic_detail = get_topic_detail(href)
					#一个utf-8中文字符的len是3, http://blog.csdn.net/handsomekang/article/details/9397025
					if len(topic_detail) > 150 and any(s in topic_detail for s in whitelist):
						f.write(title)
						f.write('\n')
						f.write(href)
						f.write('\n')
						f.write(''+topic_detail)
						f.write('\n')
						f.write('=======================================================')
						f.write('\n')
						count_saved += 1
						valid = True
				count_all += 1
				if valid:
					print '已处理' + str(count_all) + '个帖子, 保存' + str(count_saved) + '个帖子, 有效率为' + str(round(count_saved / float(count_all), 4)*100) + '%, title:' + title
				valid = False
			except:
				pass
