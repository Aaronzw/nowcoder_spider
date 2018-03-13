# 牛客网爬虫

需要搜集一下面经，所以写了这个爬虫。

如需修改关键词、爬取数目、关键词白名单、关键词黑名单等，只需要更改nowcoder.py中main函数参数即可。

另有初步尝试用结巴分词结合搜狗词库，对面经进行关键考点分析。但帖子内容较复杂（比如一个关键考点后跟几十句以其它术语名词进行的解释），直接提取效果不佳。不过在对黑名单、白名单词汇扩充之后，发现有一点点work，有一定参考意义。keywords.py使用如下：


```
usage: keywords.py [-h] [--filepath FILEPATH]

optional arguments:
  -h, --help            show this help message and exit
  --filepath FILEPATH, -f FILEPATH
                        解析文件地址
```