import requests
import re
from bs4 import BeautifulSoup
import jieba.posseg as pseg
import jieba
from wordcloud import WordCloud
from textrank4zh import TextRank4Keyword, TextRank4Sentence

# 去掉停用词
def remove_stop_words(f):
    stop_words = ['和','的','把','也','搞','以','并','将','是','要','了','不','习近',
                  '就','我们','平','为','上','让','新','在','可','怕','同','更加',
                  '一个','取消','共','公','体']
    for stop_word in stop_words:
        f = f.replace(stop_word, '')
    return f

# 词云可视化
def create_word_cloud(f):
    add_list = ['习近平']
    for w in add_list:
        jieba.add_word(w)
    f = remove_stop_words(f)
    seg_list = jieba.lcut(f)
    cut_text = ' '.join(seg_list)
    wc = WordCloud(
		max_words=50,
		width=2000,
		height=1200,
        font_path='./msyh.ttf'
    )
    wordcloud = wc.generate(cut_text)
    wordcloud.to_file("wordcloud/wordcloud.jpg")

# 请求url
url = 'https://mp.weixin.qq.com/s/grwFpyIPPNLJx4cg2J0PCQ'

html = requests.get(url, timeout=10)
content = html.content

# 通过content创建beatutifulsoup对象
soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
text = soup.get_text()
# 获取人物，地点
words = pseg.lcut(text)
news_person = {word for word, flag in words if flag=='nr'}
news_place = {word for word, flag in words if flag=='ns'}
print('新闻人物：', news_person)
print('新闻地点：', news_place)

# 提取中文以及相关标点
text = re.sub('[^[\u4e00-\u9fa5。，！：]{3,}','',text)
print(text)

# 显示词云
create_word_cloud(text)

# 输出关键词，设置文本小写，窗口为2
tr4w = TextRank4Keyword()
tr4w.analyze(text=text, lower=True, window=3)
print('关键词：')
for item in tr4w.get_keywords(10, word_min_len=2):
    print(item.word, item.weight)

# 输出重要的句子
tr4s = TextRank4Sentence()
tr4s.analyze(text=text, lower=True, source = 'all_filters')
print('摘要：')
# 重要性较高的三个句子
for item in tr4s.get_key_sentences(num=3):
	# index是语句在文本中位置，weight表示权重
#    print(item.index, item.weight, item.sentence)
	print(item.sentence)
