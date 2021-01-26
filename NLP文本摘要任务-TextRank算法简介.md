# NLP文本摘要-TextRank算法简介

在NLP中有一类任务是根据文章内容来生成摘要。这类任务到目前为止主要分为两类：

- **抽取型摘要**：这种方法依赖于从文本中提取几个部分，例如短语、句子，把它们堆叠起来创建摘要。因此，这种抽取型的方法最重要的是识别出适合总结文本的句子。
- **抽样型摘要**：这种方法应用先进的NLP技术生成一篇全新的总结。可能总结中的文本甚至没有在原文中出现。

而TextRank是一种从PageRank发展而来的抽取型摘要算法。PageRank是一种图算法，主要用于对在线搜索结果中的网页进行排序，他根据是否有链接从其他网页指向当前网页来计算PageRank分数，并遵循以下两点核心思想：

- 如果一个网页被很多其他网页链接到的话说明这个网页比较重要，也就是PageRank值会相对较高
- 如果一个PageRank值很高的网页链接到一个其他的网页，那么被链接到的网页的PageRank值会相应地因此而提高

## 1. PageRank原理

在下面的公式中$v_j$表示链接到$v_i$这个页面的链接，$In(v_i)$表示网页$v_i$所有入链的集合，$Out(v_j)$表示到页面$v_j$指向其他网页的集合，$d$表示阻尼系数，用来克服后面公式的固有缺陷用，一般取0.85。所以$S(v_i)$来表示当前页面的PR(PageRank)值为：
$$
S(v_i)=(1-d)+d\ast \sum_{j\in In(v_i))}^{}\frac{1}{\left | Out(v_j) \right |}S(v_j)
$$
在所有的网页都得到PR值之后进行排序就可以呈现在网页内容的推荐上了。

## 2. TextRank原理

而根据PageRank而得来的TextRank值表示为：
$$
WS(v_i)=(1-d)+d\ast \sum_{v_j\in In(v_i))}^{}\frac{w_ji}{\sum_{v_k\in Out(v_j)}^{}w_{jk}}WS(v_j)
$$
如果用TextRank来进行关键词提取的算法为：

1. 首先也是文本拆分和分词和词性标注处理。
2. 构建候选关键词图$G=(V,E)$，其中$V$为节点集，由候选管检测组成，然后用共现关系构造任两点之间的边，两个节点之间存在边仅当它们对应的词汇在长度为$K$的窗口中共现，$K$表示窗口短小，即最多共现$K$个单词。
3. 根据上面公式，迭代传播各节点的权重，只至收敛。
4. 对节点权重进行倒序排序，从而得到最重要的$T$个单词，作为候选关键词。
5. 由上一步得到的最重要的$T$个单词，在原始文本中进行标记，若形成相邻词组，则组合冲多词关键词。



而TextRank的生成摘要算法在PageRank的基础上，用句子代替网页，把每个句子分别看做一个节点，如果两个句子有相似性，那么认为这两个句子对应的节点之间存在一条无向有权边，而句子的相似性方法是根据如下公式：
$$
Similarity(S_i,S_j)=\frac{\left | {w_k |w_k\in S_i \cap w_k\in S_j} \right |}{\log(\left | S_i \right |)+\log(\left | S_j \right |)}
$$
其中$S_{i}S_{j}$分别表示两个句子，$w_k$表示句子中的词，那么分子部分的意思是同时出现在两个句子中的同一个词的个数，分母是对句子中词的个输球对数和。坟墓这样的设计可以抑制较长的句子在相似度计算上的优势。不过通常在构造完句子词向量之后用余弦相似度就可以计算。



其主要的流程如下图。

![textrank](https://gitee.com/zhanghang23/picture_bed/raw/master/TextRank/tr.png)

1. 首先把文章合成文本数据。
2. 把文本分割成单个句子。
3. 为每个句子找到词向量表示。
4. 计算句子向量间的相似性。
5. 将相似性矩阵转换为以句子为节点，相似性得分为边的图结构，用于句子TextRank计算。
6. 最后一定数量的排名最高的句子构成最后的摘要。

## 3. TextRank的调用

python中有jieba以及textrank4zh这两个库可以来调用TextRank算法，其中textrank4zh库用法如下：

- 寻找关键词：

  ```python
  from textrank4zh import TextRank4Keyword
  
  tr4w = TextRank4Keyword()
  tr4w.analyze(text=text, lower=True, window=3)
  print('关键词：')
  for item in tr4w.get_keywords(20, word_min_len=2):
      # weight表示权重
      print(item.word, item.weight)
  ```

  其中analyze()中的text接受需要分析的文章，window表示单词的最长界数，然后用.get_keywords()来计算排序后的关键词，第一个参数表示最终输出的关键词个数，word_min_len表示关键词的最短长度。

- 寻找关键句（用于生成抽取型摘要）：

  ```python
  from textrank4zh import TextRank4Sentence
  
  tr4s = TextRank4Sentence()
  tr4s.analyze(text=text, lower=True, source='all_filters')
  print('摘要：')
  for item in tr4s.get_key_sentences(num=3):
  	# index是语句在文本中位置，weight表示权重
      print(item.index, item.weight, item.sentence)
  ```

  其中analyze()中的text接受需要分析的文章，source生成句子之间相似度得方法，然后用.get_key_sentences()来计算排序后的句子，nums表示最终输出的关键句子个数。



**参考资料**：

- https://zhuanlan.zhihu.com/p/55270310
- https://www.cnblogs.com/xueyinzhe/p/7101295.html
- https://blog.csdn.net/wotui1842/article/details/80351386



