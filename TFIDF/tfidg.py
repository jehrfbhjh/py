from textrank4zh import TextRank4Keyword, TextRank4Sentence
import codecs


#text = "xxxxxx"
text = codecs.open('/Users/wangshuaishuai/Desktop/重采样test.txt', "r", "utf-8").read()

tr4w = TextRank4Keyword()
tr4w.analyze(text=text, window=5, lower=True)

print ("关键词：")
for item in tr4w.get_keywords(num=20, word_min_len=1):
    print (item.word, item.weight)

print ("关键短语：\n", ", ".join(tr4w.get_keyphrases(keywords_num=20, min_occur_num=2)))

tr4s = TextRank4Sentence()
tr4s.analyze(text=text, lower=True, source="all_filters")

print ("摘要：")
for item in tr4s.get_key_sentences(num=3):
    print (item.index, item.weight, item.sentence)   # index是语句在文本中位置，weight是权重