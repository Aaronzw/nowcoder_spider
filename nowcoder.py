#-*- coding:utf-8 -*-
import sys
import urllib2
from bs4 import BeautifulSoup  
from urllib import quote
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
	topic_content = soup.find('div', class_='post-topic-des')
	content = ''
	for x in topic_content:
		if x.string:
			content += x.string

	date = soup.find('span', class_='post-time').string

	return content.encode('utf-8'), date


def handler(signum, frame):
    raise AssertionError


class data():
	title = ''
	href = ''
	date = ''
	content = ''


if __name__ == '__main__':
	'''
	query: 搜索关键词
	whitelist: 只保存含有白名单关键词的帖子
	blacklist: 不保存含有黑名单关键词的帖子
	'''
	query = '机器学习 实习 面经'
	page_start = 1
	page_end = 200
	base_url = "https://www.nowcoder.com/search?type=post&order=time"
	whitelist = ['机器学习', '数据挖掘', 'svm', 'nlp', '深度学习', 'deep', 'cnn', '卷积', '大数据', '挖掘']
	blacklist = ['吗', '?', '？', '求', '有没有', '不知道', '如何', '怎么办']

	targets = searchhref(query, page_start, page_end)

	count_all = 0
	count_saved = 0
	valid = False

	results = []
	with open('机器学习实习面经.txt', 'w+') as f:
		for title in targets:
			try:
				#超时检测
				signal.signal(signal.SIGALRM, handler)
				signal.alarm(2)

				if not any(s in title for s in blacklist):
					href = targets[title]
					content, date = get_topic_detail(href)
					#一个utf-8中文字符的len是3, http://blog.csdn.net/handsomekang/article/details/9397025
					if len(content) > 150 and any(s in content for s in whitelist):
						d = data()
						d.title = title
						d.href = href.split('\n')[0]
						d.date = date[date.find('201'):]
						d.content = '' + content
						results.append(d)


						count_saved += 1
						valid = True
				count_all += 1
				if valid:
					print '已处理' + str(count_all) + '个帖子, 采集' + str(count_saved) + '个帖子, 有效率为' + str(round(count_saved / float(count_all), 4)*100) + '%, title:' + title
				valid = False
			except:
				pass
		# 按照最后更新日期进行排序
		results = sorted(results, key=lambda x: x.date, reverse=True)
		for x in results:
			f.write(x.title + '\n')
			f.write(x.href + '\n')
			f.write(x.date + '\n')
			f.write(x.content + '\n')
			f.write('=======================================================' + '\n')


