# coding=utf-8
import nltk


def segmenter(sentence):
	r"""
	Stanford Word Segmenter for Chinese.

	Split Chinese sentence into a sequence of words.

	Args:
		sentence:A Chinese sentence

	Returns:
		A list decode in utf-8

	Example:
		sentence="广东外语外贸大学是一所具有鲜明国际化特色的广东省属重点大学，是华南地区国际化人才培养和外国语言文化、对外经济贸易、国际战略研究的重要基地。"
		[u'\u5e7f\u4e1c', u'\u5916\u8bed', u'\u5916\u8d38', u'\u5927\u5b66', u'\u662f', u'\u4e00', u'\u6240', u'\u5177\u6709', u'\u9c9c\u660e', u'\u56fd\u9645\u5316', u'\u7279\u8272', u'\u7684', u'\u5e7f\u4e1c', u'\u7701\u5c5e', u'\u91cd\u70b9', u'\u5927\u5b66', u'\uff0c', u'\u662f', u'\u534e\u5357', u'\u5730\u533a', u'\u56fd\u9645\u5316', u'\u4eba\u624d', u'\u57f9\u517b', u'\u548c', u'\u5916\u56fd', u'\u8bed\u8a00', u'\u6587\u5316', u'\u3001', u'\u5bf9\u5916', u'\u7ecf\u6d4e', u'\u8d38\u6613', u'\u3001', u'\u56fd\u9645', u'\u6218\u7565', u'\u7814\u7a76', u'\u7684', u'\u91cd\u8981', u'\u57fa\u5730', u'\u3002']

	"""

	from nltk.tokenize.stanford_segmenter import StanfordSegmenter #初始化斯坦福中文分词器
	segmenter = StanfordSegmenter(path_to_jar='D:/python/nltk-3.1/nltk/chin/stanford-segmenter-2014-08-27/stanford-segmenter-3.4.1.jar', path_to_sihan_corpora_dict='D:/python/nltk-3.1/nltk/chin/stanford-segmenter-2014-08-27/data', path_to_model='D:/python/nltk-3.1/nltk/chin./stanford-segmenter-2014-08-27/data/pku.gz', path_to_dict='D:/python/nltk-3.1/nltk/chin./stanford-segmenter-2014-08-27/data/dict-chris6.ser.gz') #加载中文分词模型

	sent = segmenter.segment(sentence)#分词
	return sent.split()